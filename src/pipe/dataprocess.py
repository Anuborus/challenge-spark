from src.pipe import pipeline,keydef,normalize,filtercolumn
from dataclasses import dataclass,field
from typing import List
import json
from glob import glob
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,when

def find_offset() -> dict:
    with open(keydef.SETTINGS.value,'r') as settingsfile:
        settings = json.load(settingsfile)
        return settings
def set_offset(settings:dict) -> None:
    with open(keydef.SETTINGS.value, 'w') as f:
        json.dump(settings, f)

@dataclass
class Pandaspipe(pipeline):
    files:List[str] = field(default_factory=list)
    dataframes:dict = field(default_factory=dict)
    def find_files(self) -> None:
        self.files = glob(keydef.PATH_INPUT.value) # Identifica los archios .csv en la carpeta
    def load_base(self) -> None:
        # Se utiliza dict comprehension para la carga de los dataframes con el nombre del archio como clave
        self.dataframes = {file.split('\\')[-1]:pd.read_csv(file,engine='pyarrow') for file in self.files}
    def manage_offset(self) -> None:
        self.offset = find_offset() # Se obtiene offset del archivo settings.json
        # Se realiza iteración sobre los dataframes y se filtra según el offset para aquellos que contengan columna de fecha
        for file,data in self.dataframes.items():
            if filtercolumn.Date.name in data.columns:
                data = data[data[filtercolumn.Date.name]>=pd.to_datetime(self.offset[file],format="%d-%m-%Y")]
                self.dataframes[file] = data
                if not data.empty:
                    self.offset[file]=data[filtercolumn.Date.name].max().strftime("%d-%m-%Y")
        set_offset(self.offset) # Se sobreescribe offset del archivo settings.json
    def normalize_data(self) -> None:
        # Se realiza normalización (limpieza) de datos y tipos
        self.dataframes[normalize.COUNTRY_WISE_SP.value['name']].replace({normalize.COUNTRY_WISE_SP.value['column']:normalize.COUNTRY_WISE_SP.value['data']},inplace=True)
        self.dataframes[normalize.COUNTRY_WISE_SP.value['name']][normalize.COUNTRY_WISE_SP.value['column']] = pd.to_numeric(self.dataframes[normalize.COUNTRY_WISE_SP.value['name']][normalize.COUNTRY_WISE_SP.value['column']])
        # Se realiza iteración sobre los dataframes y se cambia el tipo de la columna Date a fecha
        for file,data in self.dataframes.items():
            if filtercolumn.Date.name in data.columns:
                data[filtercolumn.Date.name] = pd.to_datetime(data[filtercolumn.Date.name])
            self.dataframes[file] = data
    def write_data(self) ->None:
        # Se realiza iteración sobre los dataframes y se escriben en formato parquet en la carpeta src/data/out
        for file,data in self.dataframes.items():
            namefile = file.split('.')[0]
            data.to_parquet(keydef.PATH_OUTPUT.value+namefile+".parquet",index=False)
    @property
    def check_data(self) -> dict:
        return self.dataframes

@dataclass
class Sparkpipe(pipeline):
    files:List[str] = field(default_factory=list)
    dataframes:dict = field(default_factory=dict)
    def get_cluster(self) -> None:
        # Se realiza configuración de la sesión de Spark a utilizar
        self.spark = SparkSession.builder \
                    .appName("Carga Coronavirus") \
                    .master("local[4]") \
                    .config("spark.executor.memory", "8g") \
                    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
                    .getOrCreate()
        self.spark.sparkContext.setLogLevel("OFF")
    def find_files(self) -> None:
        self.files = glob(keydef.PATH_INPUT.value) # Identifica los archios .csv en la carpeta
    def load_base(self) -> None:
        self.get_cluster() # Se carga la sesión de spark
        # Se utiliza dict comprehension para la carga de los dataframes con el nombre del archio como clave
        self.dataframes = {file.split('\\')[-1]:self.spark.read.options(header=True, inferSchema=True).csv(file) for file in self.files}
    def manage_offset(self) -> None:
        self.offset = find_offset() # Se obtiene offset del archivo settings.json
        # Se realiza iteración sobre los dataframes y se filtra según el offset para aquellos que contengan columna de fecha
        for file,data in self.dataframes.items():
            if filtercolumn.Date.name in data.columns:
                data = data[col(filtercolumn.Date.name)>=pd.to_datetime(self.offset[file],format="%d-%m-%Y")]
                self.dataframes[file] = data
                if not data.rdd.isEmpty:
                    self.offset[file]=data[filtercolumn.Date.name].max().strftime("%d-%m-%Y")
        set_offset(self.offset) # Se sobreescribe offset del archivo settings.json
    def normalize_data(self) -> None:
        # Se realiza normalización (limpieza) de datos y tipos
        self.dataframes[normalize.COUNTRY_WISE_SP.value['name']].withColumn(normalize.COUNTRY_WISE_SP.value['column'], \
                                                                                    when(col(normalize.COUNTRY_WISE_SP.value['column'])=="inf" ,'0.0') \
                                                                                        .otherwise(col(normalize.COUNTRY_WISE_SP.value['column'])))
        self.dataframes[normalize.COUNTRY_WISE_SP.value['name']].withColumn(normalize.COUNTRY_WISE_SP.value['column'],col(normalize.COUNTRY_WISE_SP.value['column']).cast("double"))
        # Se realiza iteración sobre los dataframes y se cambia el tipo de la columna Date a fecha
        for file,data in self.dataframes.items():
            if filtercolumn.Date.name in data.columns:
                data.withColumn(filtercolumn.Date.name,col(filtercolumn.Date.name).cast("timestamp"))
            self.dataframes[file] = data
    def write_data(self) ->None:
        # Se realiza iteración sobre los dataframes y se escriben en formato parquet en la carpeta src/data/out
        for file,data in self.dataframes.items():
            namefile = file.split('.')[0]
            data.write.mode('overwrite').parquet(keydef.PATH_OUTPUT.value+namefile+".parquet")
    @property
    def check_data(self) -> dict:
        return self.dataframes




from enum import Enum,auto
from pathlib import Path
class keydef(Enum):
    """ Path definition
    """
    PATH_INPUT = str(Path(__file__).parent.parent)+'\data\input\*.csv'
    PATH_OUTPUT = str(Path(__file__).parent.parent)+'\data\output\\'
    SETTINGS = str(Path(__file__).parent.parent)+'\settings.json'
class filtercolumn(Enum):
    Date = auto()
class normalize(Enum):
    COUNTRY_WISE_SP = {'name':'country_wise_latest.csv',
                    'column':'Deaths / 100 Recovered',
                    'data':{'inf':'0.0'}}
    USA_WISE = {'name':'usa_county_wise.csv',
                    'column':'Date'}
class sparkset(Enum):
    NAME = 'Carga Coronavirus'
    SERVER = 'local[4]'
    MEMORY = {'param':'spark.executor.memory','value':'8g'}
    READER = {'param':'spark.sql.execution.arrow.pyspark.enabled','value':'true'}
    LOG = 'OFF'
    
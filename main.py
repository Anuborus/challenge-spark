from src.service import DataService
from src.pipe.dataprocess import Pandaspipe,Sparkpipe
from src.model import colors

def main():
    """Ejecución de lo dos tipos de procesos bajo la misma clase abstracta.
       Se pueden ejecutar individual, pero para la visualización del objetivo
       del challenge se dejan los dos.
    """
    print(f'{colors.NEGATIVE}UTILIZANDO PANDAS{colors.END}',end="\n\n")
    dataservice = DataService(Pandaspipe)
    dataservice.get_data()
    dataservice.review_data()
    dataservice.set_data()
    for file,data in dataservice.datapreview.items():
        print(f"{colors.GREEN}Archivo: {file}{colors.LIGHT_WHITE}")
        print(data.info(),end="\n\n")

    #-----------------------------------------------------------------#

    print(f'{colors.NEGATIVE}UTLIZANDO SPARK{colors.END}',end="\n\n")
    dataservice = DataService(Sparkpipe)
    dataservice.get_data()
    dataservice.review_data()
    dataservice.set_data()
    for file,data in dataservice.datapreview.items():
        print(f"{colors.BLUE}Archivo: {file}{colors.LIGHT_WHITE}")
        print(data.printSchema(),end="\n\n")

if __name__=='__main__':
    main()
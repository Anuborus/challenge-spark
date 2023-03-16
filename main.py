from src.service import DataService
from src.pipe.dataprocess import Pandaspipe,Sparkpipe
from src.model import icons,colors
import random

def main():
    dataservice = DataService(Pandaspipe)
    dataservice.get_data()
    dataservice.review_data()
    dataservice.set_data()
    for file,data in dataservice.datapreview.items():
        print(f"{colors.GREEN}Archivo: {file}{colors.LIGHT_WHITE}")
        print(data.info(),end="\n\n")

if __name__=='__main__':
    main()
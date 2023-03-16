from enum import Enum,auto
from pathlib import Path
print(Path(__file__).parent.parent)
class keydef(Enum):
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
    
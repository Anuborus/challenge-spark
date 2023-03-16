from src.core.process import pipeline
from src.model import icons,colors
class DataService:
    def __init__(self,manager:pipeline) -> None:
        manager = manager()
        self.manager = manager
        print(colors.LIGHT_WHITE+'Manager Started'+ icons.check)
    def get_data(self) -> None:
        self.manager.find_files()
        self.manager.load_base()
        print(colors.LIGHT_WHITE+'Data Loaded'+ icons.check)
    def review_data(self) -> None:
        self.manager.normalize_data()
        self.manager.manage_offset()
        print(colors.LIGHT_WHITE+'Data Transformed'+ icons.check)
    def set_data(self) -> None:
        self.manager.write_data()
    @property
    def datapreview(self) -> dict:
        return self.manager.check_data



# pandasdata = Pandaspipe()
# pandasdata.find_files()
# pandasdata.load_base()
# pandasdata.normalize_data()
# pandasdata.manage_offset()
# for file,data in pandasdata.dataframes.items():
#     print(file)
#     print(data.info())
from dataclasses import dataclass
from abc import ABC,abstractmethod

@dataclass
class pipeline(ABC):
    """Abstract class to define process executon with Spark and Pandas
    """
    @abstractmethod
    def find_files(self) -> None:
        """
        Find Files to load
        """
    @abstractmethod
    def load_base(self) -> None:
        """
        Load data from files
        """
    @abstractmethod
    def normalize_data(self) -> None:
        """
        Typing column with correct datatype
        """
    @abstractmethod
    def manage_offset(self) -> None:
        """
        Filter data with offset to save parquet
        """
    @abstractmethod
    def write_data(self) -> None:
        """
        Write data processed in parquet files
        """
    @property
    @abstractmethod
    def check_data(self) -> dict:
        """
        Preview data output
        """
    
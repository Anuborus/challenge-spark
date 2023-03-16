from dataclasses import dataclass,field
from abc import ABC,abstractmethod
from enum import Enum,auto
from typing import Any,Dict,List

@dataclass
class pipeline(ABC):
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
    
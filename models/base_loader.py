"""
base_loader.py

Abstract base class used for loading CSV datasets.

Author: Mohamed Amro
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseLoader(ABC):
    """
    Abstract class representing a generic CSV loader.

    Every data loader in the project inherits from this class.
    """

    def __init__(self, filepath: str):
        """
        Initialize the loader.

        Parameters
        ----------
        filepath : str
            Path to CSV file.
        """
        self.filepath = filepath

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """
        Load CSV data.

        Returns
        -------
        pandas.DataFrame
            Loaded dataset.
        """
        pass
import os
import pandas as pd

from models.base_loader import BaseLoader 
from models.exceptions import DataLoadingError

class DataLoader(BaseLoader):
    """
    Loads train, ideal, and test datasets.
    Supports both:
    - single file mode (for unit tests)
    - pipeline mode (for main program)
    """

    def __init__(self, filepath=None, train_path=None, ideal_path=None, test_path=None):
        self.filepath = filepath
        self.train_path = train_path
        self.ideal_path = ideal_path
        self.test_path = test_path

    # -------------------------
    # Single file mode (TESTS)
    # -------------------------
    def load_data(self) -> pd.DataFrame:
        if self.filepath:
            return self.load_csv(self.filepath)

        # fallback for safety
        return self.load_all()

    # -------------------------
    # CSV loader
    # -------------------------
    def load_csv(self, path: str) -> pd.DataFrame:
        if not path:
            try:
                df = pd.read_csv(path)
            except FileNotFoundError as e:
                raise DataLoadingError("File not found") from e

        if not os.path.exists(path):
            raise DataLoadingError(f"File '{path}' does not exist.")

        df = pd.read_csv(path)

        if df.empty:
            raise DataLoadingError(f"File '{path}' is empty.")

        return df

    # -------------------------
    # Full pipeline loader
    # -------------------------
    def load_all(self):
        if not (self.train_path and self.ideal_path and self.test_path):
            raise DataLoadingError("Missing train/ideal/test paths")

        return (
            self.load_csv(self.train_path),
            self.load_csv(self.ideal_path),
            self.load_csv(self.test_path),
        )
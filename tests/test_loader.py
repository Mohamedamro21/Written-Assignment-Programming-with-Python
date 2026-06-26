"""
Unit tests for data loading module.
"""

import pandas as pd
from models.data_loader import DataLoader
import pytest
from models.exceptions import DataLoadingError


def test_load_all_returns_dataframes():
    loader = DataLoader(
        train_path="data/train.csv",
        ideal_path="data/ideal.csv",
        test_path="data/test.csv"
    )

    train_df, ideal_df, test_df = loader.load_all()

    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(ideal_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)

    assert not train_df.empty
    assert not ideal_df.empty
    assert not test_df.empty

def test_load_missing_file_raises():
    loader = DataLoader("fake.csv")

    with pytest.raises(DataLoadingError):
        loader.load_data()
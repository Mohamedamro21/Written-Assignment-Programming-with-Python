"""
Unit tests for FunctionSelector (Least Squares logic).
"""

import pandas as pd
from models.function_selector import FunctionSelector
import numpy as np



def test_selector_returns_four_mappings():
    # minimal synthetic dataset
    train_df = pd.DataFrame({
        "x": [1, 2, 3],
        "y1": [1.0, 2.0, 3.0],
        "y2": [2.0, 4.0, 6.0],
        "y3": [1.5, 2.5, 3.5],
        "y4": [0.5, 1.5, 2.5]
    })

    ideal_df = pd.DataFrame({
        "x": [1, 2, 3],
        "y1": [1.0, 2.0, 3.0],
        "y2": [2.0, 4.0, 6.0],
        "y3": [3.0, 6.0, 9.0],
        "y4": [4.0, 8.0, 12.0]
    })

    selector = FunctionSelector(train_df, ideal_df)
    results = selector.select_best_functions()

    assert len(results) == 4

    for r in results:
        assert r.sse >= 0
        assert r.max_deviation >= 0

def test_sse_is_zero_for_identical_data():
    df = pd.DataFrame({
        "x": [1, 2, 3],
        "y1": [1, 2, 3]
    })

    selector = FunctionSelector(df, df)

    sse = selector._sse(
        df["y1"].values,
        df["y1"].values
    )

    assert sse == 0
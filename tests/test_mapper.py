"""
Unit tests for FunctionMapper.
"""

import pandas as pd
from models.mapper import FunctionMapper


def test_mapper_applies_threshold_rule():
    test_df = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [1.0, 2.0, 3.0]
    })

    ideal_df = pd.DataFrame({
        "x": [1, 2, 3],
        "y1": [1.0, 2.0, 3.0]
    })

    mappings = {
        "y1": {
            "ideal_function": "y1",
            "max_deviation": 0.1
        }
    }

    mapper = FunctionMapper(test_df, ideal_df, mappings)
    result = mapper.map_points()

    assert isinstance(result, pd.DataFrame)
    assert "x" in result.columns
    assert "y" in result.columns
    assert "delta_y" in result.columns
    assert "ideal_function" in result.columns

def test_mapper_returns_empty_when_no_match():
    test_df = pd.DataFrame({
        "x": [1],
        "y": [999]
    })

    ideal_df = pd.DataFrame({
        "x": [1],
        "y1": [1]
    })

    mappings = {
        "y1": {
            "ideal_function": "y1",
            "max_deviation": 0.01
        }
    }

    mapper = FunctionMapper(test_df, ideal_df, mappings)
    result = mapper.map_points()

    assert result.empty
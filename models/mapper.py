"""
mapper.py

This module maps test data points to the selected ideal functions
based on the deviation constraint:

|y_test - y_ideal| ≤ sqrt(2) * max_deviation

Only points satisfying this condition are assigned to an ideal function.
"""

import numpy as np
import pandas as pd
from math import sqrt

from models.exceptions import MappingError


class FunctionMapper:
    """
    Maps test data points to selected ideal functions.
    """

    def __init__(self, test_df: pd.DataFrame, ideal_df: pd.DataFrame, mappings: dict):
        """
        Parameters:
        ----------
        test_df : pd.DataFrame
            Test dataset (X, Y)
        ideal_df : pd.DataFrame
            Ideal functions dataset
        mappings : dict
            Output from FunctionSelector.get_mapping_dict()
        """
        self.test_df = test_df
        self.ideal_df = ideal_df
        self.mappings = mappings

        self.results = []

    def map_points(self) -> pd.DataFrame:
        """
        Maps each test point to an ideal function if condition is satisfied.

        Returns:
        --------
        pd.DataFrame with columns:
            x, y, delta_y, ideal_function
        """
        try:
            x_test = self.test_df.iloc[:, 0].values
            y_test = self.test_df.iloc[:, 1].values

            ideal_columns = self.ideal_df.columns[1:]

            for i in range(len(self.test_df)):
                x = x_test[i]
                y = y_test[i]

                best_fit = None
                best_delta = float("inf")
                best_func = None

                # Check against each selected training->ideal mapping
                for train_func, info in self.mappings.items():
                    ideal_func = info["ideal_function"]
                    threshold = sqrt(2) * info["max_deviation"]

                    y_ideal_series = self.ideal_df[ideal_func].values

                    # find closest x in ideal dataset
                    idx = np.argmin(np.abs(self.ideal_df.iloc[:, 0].values - x))
                    y_ideal = y_ideal_series[idx]

                    delta = abs(y - y_ideal)

                    if delta <= threshold and delta < best_delta:
                        best_delta = delta
                        best_fit = train_func
                        best_func = ideal_func

                if best_fit is not None:
                    self.results.append({
                        "x": x,
                        "y": y,
                        "delta_y": best_delta,
                        "ideal_function": best_func
                    })

            return pd.DataFrame(self.results)

        except Exception as e:
            raise MappingError(f"Mapping failed: {str(e)}")
    
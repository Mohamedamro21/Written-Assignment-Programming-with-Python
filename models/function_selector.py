"""
function_selector.py

This module is responsible for selecting the best matching ideal functions
for each training function using the Least Squares method (Sum of Squared Errors).

It also computes maximum deviations required for later mapping of test data.
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd

from models.exceptions import FunctionSelectionError


@dataclass
class FunctionMatch:
    """Stores mapping between a training function and its best ideal function."""
    train_col: str
    ideal_col: str
    sse: float
    max_deviation: float


class FunctionSelector:
    """
    Selects the best 4 ideal functions for the 4 training functions.
    """

    def __init__(self, train_df: pd.DataFrame, ideal_df: pd.DataFrame):
        """
        Parameters:
        ----------
        train_df : pd.DataFrame
            Training dataset containing X and Y1..Y4
        ideal_df : pd.DataFrame
            Ideal functions dataset containing X and Y1..Y50
        """
        self.train_df = train_df
        self.ideal_df = ideal_df

        self.mappings: list[FunctionMatch] = []

    def _sse(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute Sum of Squared Errors (Least Squares criterion).
        """
        return np.sum((y_true - y_pred) ** 2)

    def select_best_functions(self) -> list[FunctionMatch]:
        """
        Selects best matching ideal function for each training function.

        Returns:
        --------
        list[FunctionMatch]
        """
        try:
            x = self.train_df.iloc[:, 0].values

            train_columns = self.train_df.columns[1:]
            ideal_columns = self.ideal_df.columns[1:]

            results = []

            for t_col in train_columns:
                y_train = self.train_df[t_col].values

                best_match = None
                best_sse = float("inf")
                best_ideal_col = None

                for i_col in ideal_columns:
                    y_ideal = self.ideal_df[i_col].values

                    # align safety check
                    if len(y_train) != len(y_ideal):
                        raise FunctionSelectionError(
                            f"Length mismatch between {t_col} and {i_col}"
                        )

                    sse = self._sse(y_train, y_ideal)

                    if sse < best_sse:
                        best_sse = sse
                        best_ideal_col = i_col
                        best_match = y_ideal

                max_dev = np.max(np.abs(y_train - best_match))

                match = FunctionMatch(
                    train_col=t_col,
                    ideal_col=best_ideal_col,
                    sse=best_sse,
                    max_deviation=max_dev
                )

                results.append(match)

            self.mappings = results
            return results

        except Exception as e:
            raise FunctionSelectionError(f"Failed to select functions: {str(e)}")

    def get_mapping_dict(self) -> dict:
        """
        Returns mapping in dictionary form for mapper module.
        """
        return {
            m.train_col: {
                "ideal_function": m.ideal_col,
                "max_deviation": m.max_deviation
            }
            for m in self.mappings
        }
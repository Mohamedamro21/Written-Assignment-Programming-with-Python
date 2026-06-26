"""
visualizer.py

This module creates interactive visualizations using Bokeh.

It visualizes:
- Training functions
- Selected ideal functions
- Test data mappings

The goal is to clearly show deviations and function fitting.
"""

from bokeh.plotting import figure, show
from bokeh.models import Legend
from bokeh.io import output_notebook, output_file, show, export_png
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import pandas as pd

from models.exceptions import VisualizationError


class Visualizer:
    """
    Handles all plotting operations using Bokeh.
    """

    def __init__(self):
        # Optional notebook output (safe for scripts too)
        output_notebook()
        self.plots = []

    # -----------------------------
    # TRAINING + IDEAL COMPARISON
    # -----------------------------
    def plot_training_vs_ideal(self, train_df: pd.DataFrame, ideal_df: pd.DataFrame, mapping: dict):
        """
        Plots training functions vs selected ideal functions.
        """
        try:
            p = figure(
                title="Training vs Selected Ideal Functions",
                x_axis_label="X",
                y_axis_label="Y",
                width=1000,
                height=600
            )

            legend_items = []

            # Plot training functions
            for col in train_df.columns[1:]:
                r = p.line(
                    train_df.iloc[:, 0],
                    train_df[col],
                    line_width=2
                )
                legend_items.append((f"Train {col}", [r]))

            # Plot selected ideal functions
            for train_func, info in mapping.items():
                ideal_col = info["ideal_function"]

                r = p.line(
                    ideal_df.iloc[:, 0],
                    ideal_df[ideal_col],
                    line_dash="dashed",
                    line_width=2
                )
                legend_items.append((f"Ideal {ideal_col}", [r]))

            legend = Legend(items=legend_items)
            p.add_layout(legend, "right")

            output_file("results.html")
            show(p)
            self.plots.append(p)
            return p

        except Exception as e:
            raise VisualizationError(f"Training/Ideal plot failed: {str(e)}")

    # -----------------------------
    # TEST MAPPINGS VISUALIZATION
    # -----------------------------
    def plot_test_mappings(self, test_mapped_df: pd.DataFrame):
        """
        Plots test points and their assigned ideal functions.
        """
        try:
            p = figure(
                title="Test Data Mappings",
                x_axis_label="X",
                y_axis_label="Y",
                width=1000,
                height=600
            )

            # Plot all test points
            for func in test_mapped_df["ideal_function"].unique():
                subset = test_mapped_df[test_mapped_df["ideal_function"] == func]

                p.circle(
                    subset["x"],
                    subset["y"],
                    size=6,
                    alpha=0.6,
                    legend_label=f"{func}"
                )

            p.legend.click_policy = "hide"

            show(p)
            self.plots.append(p)
            return p

        except Exception as e:
            raise VisualizationError(f"Test mapping plot failed: {str(e)}")

    # -----------------------------
    # FULL OVERVIEW PLOT
    # -----------------------------
    def plot_full_overview(self, train_df, ideal_df, test_mapped_df, mapping):
        """
        Combined visualization of everything.
        """
        try:
            p = figure(
                title="Full Function Overview",
                x_axis_label="X",
                y_axis_label="Y",
                width=1200,
                height=700
            )

            # Training lines
            for col in train_df.columns[1:]:
                p.line(train_df.iloc[:, 0], train_df[col], line_width=2)

            # Ideal dashed lines
            for _, info in mapping.items():
                p.line(
                    ideal_df.iloc[:, 0],
                    ideal_df[info["ideal_function"]],
                    line_dash="dashed",
                    line_width=2
                )

            # Test points
            p.circle(
                test_mapped_df["x"],
                test_mapped_df["y"],
                size=5,
                color="red",
                alpha=0.5
            )

            show(p)
            self.plots.append(p)
            return p

        except Exception as e:
            raise VisualizationError(f"Full overview plot failed: {str(e)}")
        
    def save_png(self, plot, filename: str):
        try:
            options = Options()
            options.add_argument("--headless")  # run without opening browser
            options.add_argument("--disable-gpu")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            export_png(plot, filename=filename, webdriver=driver)
            driver.quit()

            print(f"[OK] Saved PNG: {filename}")

        except Exception as e:
            print(f"[ERROR] PNG export failed: {e}")


    def save_all(self):
        try:
            for i, plot in enumerate(self.plots, start=1):
                self.save_png(plot, f"plot{i}.png")
                print(f"[OK] plot{i}.png saved")
        except Exception as e:
            print(f"[ERROR] save_all failed: {e}")
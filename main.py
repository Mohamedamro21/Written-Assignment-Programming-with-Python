"""
Entry point for Ideal Function Project
"""

import os

from models.data_loader import DataLoader
from models.database import DatabaseManager
from models.function_selector import FunctionSelector
from models.mapper import FunctionMapper
from models.visualizer import Visualizer



def main():
    print("Current working directory:", os.getcwd())
    # -----------------------------
    # 1. LOAD DATA
    # -----------------------------
    loader = DataLoader(
        train_path="data/train.csv",
        ideal_path="data/ideal.csv",
        test_path="data/test.csv"
    )

    train_df, ideal_df, test_df = loader.load_all()

    # -----------------------------
    # 2. DATABASE INIT
    # -----------------------------
    db = DatabaseManager(db_name="database/ideal_functions.db")

    # IMPORTANT: create tables first
    db.create_tables(ideal_df)

    # insert training + ideal data
    db.insert_dataframe(train_df, db.training_table)
    db.insert_dataframe(ideal_df, db.ideal_table)

    # -----------------------------
    # 3. SELECT IDEAL FUNCTIONS
    # -----------------------------
    selector = FunctionSelector(train_df, ideal_df)
    selector.select_best_functions()

    mapping_dict = selector.get_mapping_dict()

    # -----------------------------
    # 4. MAP TEST DATA
    # -----------------------------
    mapper = FunctionMapper(test_df, ideal_df, mapping_dict)
    mapped_df = mapper.map_points()

    # -----------------------------
    # 5. SAVE TEST RESULTS
    # -----------------------------
    db.insert_dataframe(mapped_df, db.mapping_table)

    # -----------------------------
    # 6. VISUALIZATION
    # -----------------------------
    viz = Visualizer()

    viz.plot_training_vs_ideal(train_df, ideal_df, mapping_dict)
    viz.plot_test_mappings(mapped_df)
    viz.plot_full_overview(train_df, ideal_df, mapped_df, mapping_dict)

    viz.save_all()

    print("Pipeline executed successfully!")


if __name__ == "__main__":
    main()
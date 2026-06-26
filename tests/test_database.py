"""
Unit tests for DatabaseManager.
"""

import pandas as pd
from models.database import DatabaseManager


def test_database_insert_and_read():
    db = DatabaseManager(":memory:")

    df = pd.DataFrame({
        "x": [1],
        "y1": [2],
        "y2": [3],
        "y3": [4],
        "y4": [5]
    })

    db.metadata.create_all(db.engine)
    db.insert_dataframe(df, db.training_table)

    result = db.read_table("training_data")

    assert len(result) == 1
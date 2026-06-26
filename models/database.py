"""
database.py

Creates and manages the SQLite database using SQLAlchemy.

Author: Mohamed Amro
"""

import pandas as pd

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float
)
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import text

from models.exceptions import DatabaseError


class DatabaseManager:
    """
    Handles all SQLite database operations.
    """

    def __init__(self, db_name: str = "database/ideal_functions.db"):
        """
        Initialize the SQLite database.

        Parameters
        ----------
        db_name : str
            Database file path.
        """
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.metadata = MetaData()

        # ----------------------------
        # Training Table
        # ----------------------------
        self.training_table = Table(
            "training_data",
            self.metadata,
            Column("x", Float, primary_key=True),
            Column("y1", Float),
            Column("y2", Float),
            Column("y3", Float),
            Column("y4", Float)
        )

        # ----------------------------
        # Test Mapping Table
        # ----------------------------
        self.mapping_table = Table(
            "mapped_test_data",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("x", Float),
            Column("y", Float),
            Column("delta_y", Float),
            Column("ideal_function", Integer)
        )

    def create_tables(self, ideal_dataframe: pd.DataFrame):
        """
        Create all required database tables.

        Parameters
        ----------
        ideal_dataframe : pandas.DataFrame
            Ideal function dataset used to dynamically create
            the ideal_functions table.
        """
        try:

            columns = [
                Column("x", Float, primary_key=True)
            ]

            for column in ideal_dataframe.columns[1:]:
                columns.append(Column(column, Float))

            self.ideal_table = Table(
                "ideal_functions",
                self.metadata,
                *columns
            )

            self.metadata.create_all(self.engine)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                f"Failed creating tables: {exc}"
            ) from exc

    def insert_dataframe(
        self,
        dataframe: pd.DataFrame,
        table: Table
    ):
        """
        Insert a pandas DataFrame into a SQL table.

        Parameters
        ----------
        dataframe : pandas.DataFrame

        table : sqlalchemy.Table
        """
        try:
            dataframe.to_sql(
                table.name,
                self.engine,
                if_exists="replace",
                index=False
            )

        except SQLAlchemyError as exc:
            raise DatabaseError(
                f"Failed inserting into '{table.name}': {exc}"
            ) from exc

    def save_mapping(
        self,
        x: float,
        y: float,
        delta_y: float,
        ideal_function: int
    ):
        """
        Save one mapped test point.

        Parameters
        ----------
        x : float
        y : float
        delta_y : float
        ideal_function : int
        """
        try:

            row = pd.DataFrame(
                [{
                    "x": x,
                    "y": y,
                    "delta_y": delta_y,
                    "ideal_function": ideal_function
                }]
            )

            row.to_sql(
                self.mapping_table.name,
                self.engine,
                if_exists="append",
                index=False
            )

        except SQLAlchemyError as exc:
            raise DatabaseError(
                f"Failed saving mapped point: {exc}"
            ) from exc

    def read_table(
        self,
        table_name: str
    ) -> pd.DataFrame:
        """
        Read an entire database table.

        Parameters
        ----------
        table_name : str

        Returns
        -------
        pandas.DataFrame
        """
        try:

            query = f"SELECT * FROM {table_name}"

            return pd.read_sql(query, self.engine)

        except SQLAlchemyError as exc:
            raise DatabaseError(
                f"Unable to read table '{table_name}': {exc}"
            ) from exc

    def clear_table(
        self,
        table_name: str
    ):
        """
        Delete all rows from a table.

        Parameters
        ----------
        table_name : str
        """
        try:

            with self.engine.begin() as connection:
                connection.execute(
                    f"DELETE FROM {table_name}"
                )

        except SQLAlchemyError as exc:
            raise DatabaseError(
                f"Unable to clear table '{table_name}': {exc}"
            ) from exc
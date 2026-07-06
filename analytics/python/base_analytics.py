"""
base_analytics.py
-----------------
Base class for all Python analytics modules.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    load_query,
    save_csv,
    save_excel,
    save_plot
)


class BaseAnalytics:
    """
    Base class for analytics modules.
    """

    def __init__(self, module_name: str):
        self.module_name = module_name

    # =====================================================
    # Database
    # =====================================================

    def load_data(self, query: str, params: dict | None = None) -> pd.DataFrame:
        """
        Execute a SQL query and return a DataFrame.
        """
        return load_query(query, params=params)

    # =====================================================
    # Export
    # =====================================================

    def export_csv(self, df: pd.DataFrame, filename: str):
        """
        Export DataFrame as CSV.
        """
        save_csv(df, filename)

    def export_excel(self, df: pd.DataFrame, filename: str):
        """
        Export DataFrame as Excel.
        """
        save_excel(df, filename)

    # =====================================================
    # Charts
    # =====================================================

    def save_chart(self, filename: str):
        """
        Save the current matplotlib figure.
        """
        save_plot(filename)

    # =====================================================
    # Display
    # =====================================================

    @staticmethod
    def print_dataframe(df: pd.DataFrame, rows: int = 10):
        """
        Print the first N rows of a DataFrame.
        """
        if df.empty:
            print("No data found.")
            return

        print(df.head(rows))

    @staticmethod
    def print_summary(df: pd.DataFrame):
        """
        Print DataFrame summary.
        """
        print(df.info())

    # =====================================================
    # Utilities
    # =====================================================

    @staticmethod
    def check_empty(df: pd.DataFrame):
        """
        Raise an exception if DataFrame is empty.
        """
        if df.empty:
            raise ValueError("Query returned no data.")

    @staticmethod
    def add_title(title: str):
        """
        Add a title to the current matplotlib figure.
        """
        plt.title(title)

    @staticmethod
    def add_grid():
        """
        Add a grid to the current matplotlib figure.
        """
        plt.grid(True, linestyle="--", alpha=0.4)

    @staticmethod
    def format_axis(xlabel: str = "", ylabel: str = ""):
        """
        Set axis labels.
        """
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
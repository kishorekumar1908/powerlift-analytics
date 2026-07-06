"""
utils.py
---------
Common helper functions used across analytics modules.
"""

import pandas as pd
import matplotlib.pyplot as plt

from config import (
    get_engine,
    CHART_DIR,
    EXPORT_DIR
)


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load an entire table from the warehouse.
    """
    engine = get_engine()

    query = f"SELECT * FROM {table_name}"

    return pd.read_sql(query, engine)


def load_query(query: str, params=None) -> pd.DataFrame:
    """
    Execute a SQL query with optional parameters.
    """
    engine = get_engine()
    return pd.read_sql(query, engine, params=params)


def save_csv(df: pd.DataFrame, filename: str):

    path = EXPORT_DIR / filename

    df.to_csv(path, index=False)

    print(f"Saved: {path}")


def save_excel(df: pd.DataFrame, filename: str):

    path = EXPORT_DIR / filename

    df.to_excel(path, index=False)

    print(f"Saved: {path}")


def save_plot(filename: str):

    path = CHART_DIR / filename

    plt.tight_layout()

    plt.savefig(path, dpi=300)

    plt.close()

    print(f"Saved: {path}")
"""
==========================================================
PowerLift Analytics
Extract Module
==========================================================
"""

from pathlib import Path

import pandas as pd

# Path to processed dataset
DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "career_analysis.csv"
)


REQUIRED_COLUMNS = [
    "AthleteID",
    "Name",
    "Sex",
    "BirthYearClass",
    "Age",
    "AgeClass",
    "BodyweightKg",
    "WeightClassKg",
    "Equipment",
    "Event",
    "Best3SquatKg",
    "Best3BenchKg",
    "Best3DeadliftKg",
    "TotalKg",
    "Dots",
    "Federation",
    "MeetName",
    "Date",
    "Tested"
]


def extract_data():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df["Date"] = pd.to_datetime(df["Date"])

    return df
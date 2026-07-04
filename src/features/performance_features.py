import numpy as np
import pandas as pd


def add_performance_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["StrengthRatio"] = (
        df["TotalKg"] / df["BodyweightKg"]
    ).round(2)

    df["BestLift"] = df[
        [
            "Best3SquatKg",
            "Best3BenchKg",
            "Best3DeadliftKg"
        ]
    ].max(axis=1)

    df["StrongestLift"] = df[
        [
            "Best3SquatKg",
            "Best3BenchKg",
            "Best3DeadliftKg"
        ]
    ].idxmax(axis=1)

    mapping = {
        "Best3SquatKg": "Squat",
        "Best3BenchKg": "Bench",
        "Best3DeadliftKg": "Deadlift"
    }

    df["StrongestLift"] = df["StrongestLift"].map(mapping)

    df["SquatContribution"] = (
        df["Best3SquatKg"] / df["TotalKg"]
    ).round(3)

    df["BenchContribution"] = (
        df["Best3BenchKg"] / df["TotalKg"]
    ).round(3)

    df["DeadliftContribution"] = (
        df["Best3DeadliftKg"] / df["TotalKg"]
    ).round(3)

    return df
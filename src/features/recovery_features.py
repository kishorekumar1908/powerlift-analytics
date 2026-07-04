import pandas as pd


def add_recovery_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create recovery and competition frequency features.
    """

    df = df.copy()

    grouped = df.groupby("AthleteID")

    # ============================================
    # Average Days Between Competitions
    # ============================================
    df["AverageRecoveryDays"] = (
        grouped["DaysSinceLastCompetition"]
        .transform("mean")
        .round(0)
    )

    # ============================================
    # Competitions Per Year
    # ============================================
    career_days = (
        df["LastCompetitionDate"]
        - df["FirstCompetitionDate"]
    ).dt.days

    career_years = career_days / 365.25

    career_years = career_years.replace(0, 1)

    df["CompetitionsPerYear"] = (
        df["TotalCompetitions"]
        / career_years
    ).round(2)

    # ============================================
    # Running Average Total
    # ============================================
    df["RunningAverageTotal"] = (
        grouped["TotalKg"]
        .expanding()
        .mean()
        .reset_index(level=0, drop=True)
        .round(2)
    )

    # ============================================
    # Running Average Dots
    # ============================================
    df["RunningAverageDots"] = (
        grouped["Dots"]
        .expanding()
        .mean()
        .reset_index(level=0, drop=True)
        .round(2)
    )

    return df
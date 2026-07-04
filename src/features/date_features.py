import pandas as pd


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create date-based features.
    """

    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"])

    df["CompetitionYear"] = df["Date"].dt.year

    df["CompetitionMonth"] = df["Date"].dt.month

    df["CompetitionMonthName"] = df["Date"].dt.month_name()

    df["CompetitionQuarter"] = "Q" + df["Date"].dt.quarter.astype(str)

    df["CompetitionDay"] = df["Date"].dt.day_name()

    return df
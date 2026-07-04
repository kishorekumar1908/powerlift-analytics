import pandas as pd


def add_career_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create athlete career progression features.

    Features Created:
    -----------------
    CompetitionNumber
    PreviousTotal
    PreviousDots
    TotalImprovement
    DotsImprovement
    ImprovementPercentage

    CareerBestSquat
    CareerBestBench
    CareerBestDeadlift
    CareerBestTotal
    CareerBestDots

    PreviousCareerBestSquat
    PreviousCareerBestBench
    PreviousCareerBestDeadlift
    PreviousCareerBestTotal
    PreviousCareerBestDots

    FirstCompetitionDate
    LastCompetitionDate
    CareerLengthDays
    DaysSinceLastCompetition
    """

    df = df.copy()

    # =====================================================
    # Sort Athlete Career Chronologically
    # =====================================================
    df = df.sort_values(
        by=["AthleteID", "Date"]
    ).reset_index(drop=True)

    grouped = df.groupby("AthleteID")

    # =====================================================
    # Competition Number
    # =====================================================
    df["CompetitionNumber"] = (
        grouped.cumcount() + 1
    )

    # =====================================================
    # Previous Competition Metrics
    # =====================================================
    df["PreviousTotal"] = (
        grouped["TotalKg"].shift(1)
    )

    df["PreviousDots"] = (
        grouped["Dots"].shift(1)
    )

    # =====================================================
    # Improvement
    # =====================================================
    df["TotalImprovement"] = (
        df["TotalKg"] - df["PreviousTotal"]
    )

    df["DotsImprovement"] = (
        df["Dots"] - df["PreviousDots"]
    )

    # =====================================================
    # Improvement Percentage
    # =====================================================
    df["ImprovementPercentage"] = (
        (
            df["TotalImprovement"]
            / df["PreviousTotal"].replace(0, pd.NA)
        ) * 100
    ).round(2)

    # =====================================================
    # Running Career Bests
    # (Includes Current Competition)
    # =====================================================
    df["CareerBestSquat"] = (
        grouped["Best3SquatKg"].cummax()
    )

    df["CareerBestBench"] = (
        grouped["Best3BenchKg"].cummax()
    )

    df["CareerBestDeadlift"] = (
        grouped["Best3DeadliftKg"].cummax()
    )

    df["CareerBestTotal"] = (
        grouped["TotalKg"].cummax()
    )

    df["CareerBestDots"] = (
        grouped["Dots"].cummax()
    )

    # =====================================================
    # Previous Career Bests
    # (Useful for Machine Learning)
    # =====================================================
    df["PreviousCareerBestSquat"] = (
        grouped["CareerBestSquat"].shift(1)
    )

    df["PreviousCareerBestBench"] = (
        grouped["CareerBestBench"].shift(1)
    )

    df["PreviousCareerBestDeadlift"] = (
        grouped["CareerBestDeadlift"].shift(1)
    )

    df["PreviousCareerBestTotal"] = (
        grouped["CareerBestTotal"].shift(1)
    )

    df["PreviousCareerBestDots"] = (
        grouped["CareerBestDots"].shift(1)
    )

    # =====================================================
    # First & Last Competition Dates
    # =====================================================
    df["FirstCompetitionDate"] = (
        grouped["Date"].transform("min")
    )

    df["LastCompetitionDate"] = (
        grouped["Date"].transform("max")
    )

    # =====================================================
    # Career Length
    # =====================================================
    df["CareerLengthDays"] = (
        df["LastCompetitionDate"]
        - df["FirstCompetitionDate"]
    ).dt.days

    # =====================================================
    # Days Since Previous Competition
    # =====================================================
    previous_date = grouped["Date"].shift(1)

    df["DaysSinceLastCompetition"] = (
        df["Date"] - previous_date
    ).dt.days

    return df
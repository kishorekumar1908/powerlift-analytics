import pandas as pd


def add_analytics_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create career statistics for each athlete.
    """

    df = df.copy()

    grouped = df.groupby("AthleteID")

    # ============================================
    # Total Competitions
    # ============================================
    df["TotalCompetitions"] = grouped["AthleteID"].transform("count")

    # ============================================
    # Average Career Performance
    # ============================================
    df["AverageTotal"] = grouped["TotalKg"].transform("mean").round(2)

    df["AverageDots"] = grouped["Dots"].transform("mean").round(2)

    # ============================================
    # Average Lift Performance
    # ============================================
    df["AverageSquat"] = grouped["Best3SquatKg"].transform("mean").round(2)

    df["AverageBench"] = grouped["Best3BenchKg"].transform("mean").round(2)

    df["AverageDeadlift"] = grouped["Best3DeadliftKg"].transform("mean").round(2)

    # ============================================
    # Best Competition Number
    # ============================================
    best_total = grouped["TotalKg"].transform("max")

    df["BestCompetition"] = (
        df["TotalKg"] == best_total
    ).astype(int)

    # ============================================
    # Career Improvement
    # ============================================
    first_total = grouped["TotalKg"].transform("first")

    last_total = grouped["TotalKg"].transform("last")

    df["CareerImprovement"] = (
        last_total - first_total
    )

    df["CareerImprovementPercentage"] = (
        (
            (last_total - first_total)
            / first_total
        ) * 100
    ).round(2)

    return df
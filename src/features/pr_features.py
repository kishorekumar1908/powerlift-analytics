import pandas as pd


def add_pr_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create NewPersonalRecord feature.

    Definition:
        1 -> Current TotalKg is greater than every previous TotalKg
        0 -> Otherwise

    Note:
        The first competition is always considered a Personal Record.
    """

    df = df.copy()

    grouped = df.groupby("AthleteID", sort=False)

    # Previous career best total
    previous_best_total = grouped["CareerBestTotal"].shift(1)

    # First competition
    first_competition = previous_best_total.isna()

    # New PR only if TotalKg exceeds previous career best
    total_pr = df["TotalKg"] > previous_best_total

    # Final PR flag
    df["NewPersonalRecord"] = (
        first_competition | total_pr
    ).astype(int)

    return df
import pandas as pd

from date_features import add_date_features
from performance_features import add_performance_features
from career_features import add_career_features
from pr_features import add_pr_features
from analytics_features import add_analytics_features
from recovery_features import add_recovery_features


# ======================================================
# Load Datasets
# ======================================================

india_df = pd.read_csv(
    "data/processed/india_clean.csv"
)

career_df = pd.read_csv(
    "data/processed/career_analysis.csv"
)


# ======================================================
# Convert Date
# ======================================================

india_df["Date"] = pd.to_datetime(india_df["Date"])

career_df["Date"] = pd.to_datetime(career_df["Date"])


# ======================================================
# INDIA DATASET
# ======================================================

india_df = add_date_features(india_df)

india_df = add_performance_features(india_df)


# ======================================================
# CAREER DATASET
# ======================================================

career_df = add_date_features(career_df)

career_df = add_performance_features(career_df)

career_df = add_career_features(career_df)

career_df = add_pr_features(career_df)

career_df = add_analytics_features(career_df)

career_df = add_recovery_features(career_df)


# ======================================================
# Save Datasets
# ======================================================

india_df.to_csv(
    "data/processed/india_features.csv",
    index=False
)

career_df.to_csv(
    "data/processed/career_features.csv",
    index=False
)


print("=" * 60)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 60)

print(f"India Features  : {india_df.shape}")

print(f"Career Features : {career_df.shape}")

print("\nFiles Created")

print("india_features.csv")

print("career_features.csv")
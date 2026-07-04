import pandas as pd

# Load the dataset
df = pd.read_csv(
    "data/raw/openipf-2026-06-27/openipf-2026-06-27-7197dc8d.csv",
    low_memory=False
)

# Filter only Indian athletes
india_df = df[df["Country"] == "India"].copy()

# Convert Date column to datetime
india_df["Date"] = pd.to_datetime(india_df["Date"])

# ===========================
# Basic Dataset Information
# ===========================
print("=" * 50)
print("INDIAN POWERLIFTING DATASET SUMMARY")
print("=" * 50)

print(f"Rows                : {india_df.shape[0]}")
print(f"Columns             : {india_df.shape[1]}")
print(f"Unique Athletes     : {india_df['Name'].nunique()}")
print(f"Competitions        : {india_df['MeetName'].nunique()}")
print(f"Date Range          : {india_df['Date'].min().date()} to {india_df['Date'].max().date()}")

# ===========================
# Records by Year
# ===========================
print("\n" + "=" * 50)
print("RECORDS BY YEAR")
print("=" * 50)

print(india_df["Date"].dt.year.value_counts().sort_index())

# ===========================
# Sex Distribution
# ===========================
print("\n" + "=" * 50)
print("SEX DISTRIBUTION")
print("=" * 50)

print(india_df["Sex"].value_counts())

# ===========================
# Equipment Distribution
# ===========================
print("\n" + "=" * 50)
print("EQUIPMENT DISTRIBUTION")
print("=" * 50)

print(india_df["Equipment"].value_counts())

# ===========================
# Event Distribution
# ===========================
print("\n" + "=" * 50)
print("EVENT DISTRIBUTION")
print("=" * 50)

print(india_df["Event"].value_counts())

# ===========================
# Top Federations
# ===========================
print("\n" + "=" * 50)
print("TOP 15 FEDERATIONS")
print("=" * 50)

print(india_df["Federation"].value_counts().head(15))

# ===========================
# Top States
# ===========================
print("\n" + "=" * 50)
print("TOP 20 STATES")
print("=" * 50)

print(india_df["State"].value_counts().head(20))

# ===========================
# Missing Values
# ===========================
print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print(india_df.isnull().sum())

# ===========================
# Save Filtered Dataset
# ===========================
india_df.to_csv(
    "data/processed/india_powerlifting.csv",
    index=False
)

print("\n" + "=" * 50)
print("Filtered dataset saved successfully!")
print("Location: data/processed/india_powerlifting.csv")
print("=" * 50)
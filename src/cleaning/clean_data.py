import pandas as pd

# ==========================================================
# Load Dataset
# ==========================================================
df = pd.read_csv(
    "data/processed/india_selected_columns.csv",
    low_memory=False
)

print("=" * 60)
print("INITIAL DATASET")
print("=" * 60)
print(df.shape)

# ==========================================================
# Missing Values
# ==========================================================
print("\nMissing Values")
print("-" * 40)
print(df.isnull().sum())

# ==========================================================
# Remove Duplicate Rows
# ==========================================================
duplicates = df.duplicated().sum()

print(f"\nDuplicate Rows: {duplicates}")

df.drop_duplicates(inplace=True)

print("Shape After Removing Duplicates:", df.shape)

# ==========================================================
# Keep Only Full Power Competitions
# ==========================================================
print("\nKeeping only Full Power (SBD) competitions...")

df = df[df["Event"] == "SBD"].copy()

print("Shape After Event Filter:", df.shape)

# ==========================================================
# Remove MeetState
# ==========================================================
df.drop(columns=["MeetState"], inplace=True)

# ==========================================================
# Clean Athlete Names
# ==========================================================
df["Name"] = df["Name"].str.strip()

# ==========================================================
# Convert Date
# ==========================================================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# ==========================================================
# Convert Numeric Columns
# ==========================================================
numeric_columns = [
    "Age",
    "BodyweightKg",
    "Best3SquatKg",
    "Best3BenchKg",
    "Best3DeadliftKg",
    "TotalKg",
    "Dots"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================================
# Remove Invalid Records
# ==========================================================
df = df[df["BodyweightKg"] > 0]
df = df[df["TotalKg"] > 0]

# ==========================================================
# Fill Missing Values
# ==========================================================
df["Tested"] = df["Tested"].fillna("Unknown")
df["MeetTown"] = df["MeetTown"].fillna("Unknown")

# ==========================================================
# Sort Dataset
# ==========================================================
df.sort_values(
    by=["Name", "Date"],
    inplace=True
)

df.reset_index(drop=True, inplace=True)

# ==========================================================
# Create AthleteID
# ==========================================================

# Get unique athlete names in alphabetical order
unique_names = sorted(df["Name"].unique())

# Create mapping: Athlete Name -> AthleteID
athlete_mapping = {
    name: f"ATH{idx + 1:05d}"
    for idx, name in enumerate(unique_names)
}

# Assign AthleteID
df["AthleteID"] = df["Name"].map(athlete_mapping)

# Move AthleteID to the first column
cols = ["AthleteID"] + [col for col in df.columns if col != "AthleteID"]
df = df[cols]


# ==========================================================
# Format Date
# ==========================================================
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

# ==========================================================
# Save Master Dataset
# ==========================================================
df.to_csv(
    "data/processed/india_clean.csv",
    index=False
)

print("\nindia_clean.csv saved.")

# ==========================================================
# Create Career Dataset
# Athletes with >=2 Competitions
# ==========================================================
competition_counts = df["Name"].value_counts()

career_df = df[
    df["Name"].isin(
        competition_counts[competition_counts >= 2].index
    )
].copy()

career_df.reset_index(drop=True, inplace=True)

career_df.to_csv(
    "data/processed/career_analysis.csv",
    index=False
)

print("career_analysis.csv saved.")

# ==========================================================
# Final Summary
# ==========================================================
print("\n")
print("=" * 60)
print("INDIA CLEAN DATASET")
print("=" * 60)

print(f"Rows               : {df.shape[0]}")
print(f"Columns            : {df.shape[1]}")
print(f"Unique Athletes    : {df['Name'].nunique()}")
print(f"Competitions       : {df['MeetName'].nunique()}")

print("\nRemaining Missing Values")
print("-" * 40)
print(df.isnull().sum())

print("\n")
print("=" * 60)
print("CAREER ANALYSIS DATASET")
print("=" * 60)

print(f"Rows               : {career_df.shape[0]}")
print(f"Columns            : {career_df.shape[1]}")
print(f"Unique Athletes    : {career_df['Name'].nunique()}")
print(f"Competitions       : {career_df['MeetName'].nunique()}")

print("\nAthletes Removed (Single Competition)")
print("-" * 40)
print(df["Name"].nunique() - career_df["Name"].nunique())

print("\n")
print("=" * 60)
print("FILES CREATED")
print("=" * 60)
print("✓ data/processed/india_clean.csv")
print("✓ data/processed/career_analysis.csv")
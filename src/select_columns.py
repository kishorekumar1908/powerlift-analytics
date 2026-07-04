import pandas as pd

# Load filtered Indian dataset
df = pd.read_csv(
    "data/processed/india_powerlifting.csv",
    low_memory=False
)

print("Original Shape:", df.shape)

# Keep only useful columns
columns_to_keep = [
    "Name",
    "Sex",
    "Age",
    "AgeClass",
    "BirthYearClass",
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
    "MeetState",
    "MeetTown",
    "Date",
    "Tested"
]

df = df[columns_to_keep]

print("\nSelected Columns:")
print(df.columns)

print("\nNew Shape:")
print(df.shape)

df.to_csv(
    "data/processed/india_selected_columns.csv",
    index=False
)

print("\nDataset saved successfully!")
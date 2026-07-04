import pandas as pd

india = pd.read_csv("data/processed/india_features.csv")
career = pd.read_csv("data/processed/career_features.csv")

print("="*60)
print("INDIA DATASET")
print("="*60)

print(india.shape)
print(india.columns)

print("\n")

print("="*60)
print("CAREER DATASET")
print("="*60)

print(career.shape)
print(career.columns)

print(career.isnull().sum())

athlete = career["AthleteID"].sample(
    1,
    random_state=42
).iloc[0]

sample = career[
    career["AthleteID"] == athlete
]

sample = sample[
[
    "Date",
    "CompetitionNumber",
    "TotalKg",
    "PreviousTotal",
    "TotalImprovement",
    "CareerBestTotal",
    "PreviousCareerBestTotal",
    "NewPersonalRecord",
    "DaysSinceLastCompetition"
]]

print(sample)

print(career["StrengthRatio"].describe())
print(career["TotalImprovement"].describe())
career.groupby(
    "AthleteID"
)["CompetitionNumber"].max().describe()
print(career["NewPersonalRecord"].value_counts())

sample_ids = career["AthleteID"].sample(
    10,
    random_state=42
)

for athlete in sample_ids:

    print("="*60)

    print(athlete)

    print("="*60)

    print(
        career[
            career["AthleteID"] == athlete
        ][[
            "Date",
            "CompetitionNumber",
            "TotalKg",
            "CareerBestTotal",
            "NewPersonalRecord"
        ]]
    )

print("\n")
print("=" * 60)
print("FEATURE ENGINEERING REPORT")
print("=" * 60)

print(f"Rows                    : {career.shape[0]}")
print(f"Columns                 : {career.shape[1]}")
print(f"Athletes                : {career['AthleteID'].nunique()}")
print(f"Competitions            : {career.shape[0]}")
print(f"Career PRs              : {career['NewPersonalRecord'].sum()}")

print(
    f"Average Strength Ratio  : {career['StrengthRatio'].mean():.2f}"
)

career_improvement = (
    career.groupby("AthleteID")
          .first()["CareerImprovement"]
)

print(
    f"Average Career Improvement : {career_improvement.mean():.2f} kg"
)

print(
    f"Average Competitions/Athlete : {career['TotalCompetitions'].mean():.2f}"
)

print(
    f"First Competition Year : {career['CompetitionYear'].min()}"
)

print(
    f"Latest Competition Year : {career['CompetitionYear'].max()}"
)

print(
    f"Maximum Career Length : {career['CareerLengthDays'].max()} days"
)

print(
    f"Longest Career Athlete : "
    f"{career.loc[career['CareerLengthDays'].idxmax(), 'AthleteID']}"
)
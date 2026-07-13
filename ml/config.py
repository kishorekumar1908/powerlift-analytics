"""
Configuration file for the Machine Learning pipeline.

This module centralizes all configurable parameters used across
the ML workflow to ensure consistency and simplify maintenance.
"""

from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "career_features.csv"
)

MODEL_DIR = PROJECT_ROOT / "ml" / "saved_models"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Feature Configuration
# ==========================================================

NUMERIC_FEATURES = [
    "Age",
    "BodyweightKg",
    "CompetitionNumber",
    "PreviousTotal",
    "CareerBestTotal",
    "DaysSinceLastCompetition",
    "StrengthRatio",
    "TotalImprovement",
]

CATEGORICAL_FEATURES = [
    "Sex",
    "Equipment",
    "Tested",
]

FEATURE_COLUMNS = (
    NUMERIC_FEATURES +
    CATEGORICAL_FEATURES
)

TARGET_COLUMN = "NextCompetitionTotal"

# ==========================================================
# Train/Test Split
# ==========================================================

TEST_SIZE = 0.20
RANDOM_STATE = 42

# ==========================================================
# Model File Names
# ==========================================================

PREPROCESSOR_FILE = MODEL_DIR / "preprocessor.pkl"
FEATURE_FILE = MODEL_DIR / "feature_columns.pkl"
BEST_MODEL_FILE = MODEL_DIR / "best_model.pkl"

# ==========================================================
# Evaluation Metrics
# ==========================================================

METRICS = [
    "MAE",
    "MSE",
    "RMSE",
    "R2"
]

# ==========================================================
# Prediction Files
# ==========================================================

INPUT_DIR = PROJECT_ROOT / "ml" / "inputs"
INPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_INPUT_FILE = INPUT_DIR / "sample_input.json"
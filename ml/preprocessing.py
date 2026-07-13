"""
Preprocesses the dataset for Machine Learning.

Responsibilities:
- Load prepared dataset
- Split features and target
- Train/Test split
- Impute missing values
- Encode categorical variables
- Scale numerical features
- Save fitted preprocessor
"""

import joblib

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import (
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    PREPROCESSOR_FILE,
    TEST_SIZE,
    RANDOM_STATE,
)

from data_loader import DataLoader


class DataPreprocessor:

    def __init__(self):

        self.numeric_features = NUMERIC_FEATURES
        self.categorical_features = CATEGORICAL_FEATURES
        self.feature_columns = FEATURE_COLUMNS
        self.target = TARGET_COLUMN

    def preprocess(self):

        # --------------------------------------------------
        # Load prepared dataset
        # --------------------------------------------------

        loader = DataLoader()
        df = loader.prepare_dataset()

        # --------------------------------------------------
        # Validate required columns
        # --------------------------------------------------

        required_columns = self.feature_columns + [self.target]

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns:\n{missing_columns}"
            )

        # --------------------------------------------------
        # Select Features
        # --------------------------------------------------

        df = df[required_columns].copy()

        X = df[self.feature_columns]
        y = df[self.target]

        # --------------------------------------------------
        # Train/Test Split
        # --------------------------------------------------

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            shuffle=True,
        )

        # --------------------------------------------------
        # Numerical Pipeline
        # --------------------------------------------------

        numeric_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="median"),
                ),
                (
                    "scaler",
                    StandardScaler(),
                ),
            ]
        )

        # --------------------------------------------------
        # Categorical Pipeline
        # --------------------------------------------------

        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="most_frequent"),
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    ),
                ),
            ]
        )

        # --------------------------------------------------
        # Column Transformer
        # --------------------------------------------------

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    numeric_pipeline,
                    self.numeric_features,
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    self.categorical_features,
                ),
            ]
        )

        # --------------------------------------------------
        # Fit & Transform
        # --------------------------------------------------

        X_train_processed = preprocessor.fit_transform(
            X_train
        )

        X_test_processed = preprocessor.transform(
            X_test
        )

        # --------------------------------------------------
        # Save Preprocessor
        # --------------------------------------------------

        joblib.dump(
            preprocessor,
            PREPROCESSOR_FILE,
        )

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        print("=" * 60)
        print("PREPROCESSING COMPLETED")
        print("=" * 60)
        print(f"Training Samples : {len(y_train):,}")
        print(f"Testing Samples  : {len(y_test):,}")
        print(f"Features         : {len(self.feature_columns)}")
        print("=" * 60)

        return (
            X_train_processed,
            X_test_processed,
            y_train,
            y_test,
        )


def main():

    processor = DataPreprocessor()

    processor.preprocess()


if __name__ == "__main__":
    main()
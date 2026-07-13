"""
Selects and validates the features used for Machine Learning.
"""

import joblib

from config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    FEATURE_FILE,
)

from data_loader import DataLoader


class FeatureSelector:
    """
    Validates and selects the final features
    used for model training.
    """

    def __init__(self):

        self.features = FEATURE_COLUMNS
        self.target = TARGET_COLUMN

    def select_features(self):
        """
        Load prepared dataset and select features.
        """

        # -----------------------------------------
        # Load prepared dataset
        # -----------------------------------------

        loader = DataLoader()
        df = loader.prepare_dataset()

        # -----------------------------------------
        # Validate Required Columns
        # -----------------------------------------

        required_columns = self.features + [self.target]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns:\n{missing_columns}"
            )

        # -----------------------------------------
        # Select Final Dataset
        # -----------------------------------------

        selected_df = df[required_columns].copy()

        # -----------------------------------------
        # Save Feature List
        # -----------------------------------------

        joblib.dump(
            self.features,
            FEATURE_FILE
        )

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        print("=" * 60)
        print("FEATURE SELECTION COMPLETED")
        print("=" * 60)

        print(f"Features Selected : {len(self.features)}")
        print(f"Target            : {self.target}")

        print("=" * 60)

        print("\nSelected Features\n")

        for feature in self.features:
            print(f" {feature}")

        print("\nTarget\n")

        print(f" {self.target}")

        print("\nSelected Dataset Shape")

        print(selected_df.shape)

        return selected_df


def main():

    selector = FeatureSelector()

    selector.select_features()


if __name__ == "__main__":
    main()
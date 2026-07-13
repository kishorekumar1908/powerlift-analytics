"""
Predicts an athlete's next competition total.
"""

import json

import joblib
import pandas as pd

from config import (
    BEST_MODEL_FILE,
    PREPROCESSOR_FILE,
    FEATURE_FILE,
    SAMPLE_INPUT_FILE,
)


class PerformancePredictor:

    def __init__(self):

        self.model = joblib.load(BEST_MODEL_FILE)

        self.preprocessor = joblib.load(
            PREPROCESSOR_FILE
        )

        self.feature_columns = joblib.load(
            FEATURE_FILE
        )

    def load_input(self):
        """
        Load athlete information from JSON.
        """

        with open(
            SAMPLE_INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def validate_input(self, athlete):

        missing = [
            feature
            for feature in self.feature_columns
            if feature not in athlete
        ]

        if missing:

            raise ValueError(
                f"Missing input features:\n{missing}"
            )

    def predict(self):

        athlete = self.load_input()

        self.validate_input(athlete)

        input_df = pd.DataFrame([athlete])

        input_df = input_df[self.feature_columns]

        processed = self.preprocessor.transform(
            input_df
        )

        prediction = self.model.predict(
            processed
        )[0]

        return athlete, prediction


def main():

    predictor = PerformancePredictor()

    athlete, prediction = predictor.predict()

    print("=" * 60)
    print("POWERLIFT PERFORMANCE PREDICTION")
    print("=" * 60)

    print("\nInput Athlete\n")

    for key, value in athlete.items():
        print(f"{key:<30}: {value}")

    print("\n" + "=" * 60)

    print(
        f"Predicted Next Competition Total : "
        f"{prediction:.2f} kg"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
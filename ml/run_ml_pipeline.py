"""
PowerLift Analytics
Machine Learning Pipeline Runner

Runs the complete machine learning workflow:
1. Feature Selection
2. Data Preprocessing
3. Model Training
4. Model Evaluation
5. Sample Prediction
"""

from feature_selection import FeatureSelector
from preprocessing import DataPreprocessor
from train import ModelTrainer
from evaluate import ModelEvaluator
from predict import PerformancePredictor


class MLPipeline:

    @staticmethod
    def run():

        print("\n" + "=" * 70)
        print("POWERLIFT ANALYTICS")
        print("MACHINE LEARNING PIPELINE")
        print("=" * 70)

        # --------------------------------------------------
        # Step 1
        # --------------------------------------------------

        print("\n[1/5] Feature Selection\n")

        FeatureSelector().select_features()

        # --------------------------------------------------
        # Step 2
        # --------------------------------------------------

        print("\n[2/5] Data Preprocessing\n")

        DataPreprocessor().preprocess()

        # --------------------------------------------------
        # Step 3
        # --------------------------------------------------

        print("\n[3/5] Model Training\n")

        ModelTrainer().train_models()

        # --------------------------------------------------
        # Step 4
        # --------------------------------------------------

        print("\n[4/5] Model Evaluation\n")

        ModelEvaluator().evaluate_models()

        # --------------------------------------------------
        # Step 5
        # --------------------------------------------------

        print("\n[5/5] Sample Prediction\n")

        predictor = PerformancePredictor()

        athlete, prediction = predictor.predict()

        print("=" * 70)
        print("SAMPLE PREDICTION")
        print("=" * 70)

        for key, value in athlete.items():
            print(f"{key:<30}: {value}")

        print("-" * 70)

        print(
            f"Predicted Next Competition Total : "
            f"{prediction:.2f} kg"
        )

        print("\n" + "=" * 70)
        print("MACHINE LEARNING PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)


def main():

    pipeline = MLPipeline()

    pipeline.run()


if __name__ == "__main__":
    main()
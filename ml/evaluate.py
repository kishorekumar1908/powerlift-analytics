"""
Evaluates all trained Machine Learning models.
Generates:

1. model_metrics.csv
2. predictions.csv
3. feature_importance.csv
4. best_model.pkl
"""

import joblib
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from config import (
    BEST_MODEL_FILE,
    PREPROCESSOR_FILE,
    OUTPUT_DIR,
)

from train import ModelTrainer


class ModelEvaluator:
    """
    Evaluates trained regression models.
    """

    def __init__(self):

        self.metrics_file = (
            OUTPUT_DIR /
            "model_metrics.csv"
        )

        self.predictions_file = (
            OUTPUT_DIR /
            "predictions.csv"
        )

        self.feature_importance_file = (
            OUTPUT_DIR /
            "feature_importance.csv"
        )

    def evaluate_models(self):

        (
            trained_models,
            X_test,
            y_test,
        ) = ModelTrainer().train_models()

        results = []

        best_model = None
        best_name = None
        best_predictions = None

        best_r2 = float("-inf")

        print("=" * 70)
        print("MODEL EVALUATION")
        print("=" * 70)

        # --------------------------------------------------
        # Evaluate Every Model
        # --------------------------------------------------

        for model_name, model in trained_models.items():

            predictions = model.predict(X_test)

            mae = mean_absolute_error(
                y_test,
                predictions,
            )

            mse = mean_squared_error(
                y_test,
                predictions,
            )

            rmse = mse ** 0.5

            r2 = r2_score(
                y_test,
                predictions,
            )

            results.append(
                {
                    "Model": model_name,
                    "MAE": round(mae, 3),
                    "MSE": round(mse, 3),
                    "RMSE": round(rmse, 3),
                    "R2 Score": round(r2, 4),
                }
            )

            print(f"\n{model_name}")

            print(f"MAE  : {mae:.3f}")
            print(f"MSE  : {mse:.3f}")
            print(f"RMSE : {rmse:.3f}")
            print(f"R²   : {r2:.4f}")

            if r2 > best_r2:

                best_r2 = r2
                best_model = model
                best_name = model_name
                best_predictions = predictions

        # --------------------------------------------------
        # Save Metrics
        # --------------------------------------------------

        results_df = pd.DataFrame(results)

        results_df = (
            results_df
            .sort_values(
                by="R2 Score",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        results_df.to_csv(
            self.metrics_file,
            index=False,
        )

        # --------------------------------------------------
        # Save Best Model
        # --------------------------------------------------

        joblib.dump(
            best_model,
            BEST_MODEL_FILE,
        )

                # --------------------------------------------------
        # Save Prediction Results
        # --------------------------------------------------

        predictions_df = pd.DataFrame({
            "Actual": y_test.values,
            "Predicted": best_predictions,
        })

        predictions_df["Error"] = (
            predictions_df["Actual"] -
            predictions_df["Predicted"]
        )

        predictions_df["AbsoluteError"] = (
            predictions_df["Error"].abs()
        )

        predictions_df.to_csv(
            self.predictions_file,
            index=False,
        )

        # --------------------------------------------------
        # Feature Importance
        # --------------------------------------------------

        if hasattr(best_model, "feature_importances_"):

            preprocessor = joblib.load(
                PREPROCESSOR_FILE
            )

            feature_names = (
                preprocessor.get_feature_names_out()
            )

            importance_df = pd.DataFrame({

                "Feature": feature_names,

                "Importance":
                    best_model.feature_importances_

            })

            importance_df = (
                importance_df
                .sort_values(
                    by="Importance",
                    ascending=False,
                )
                .reset_index(drop=True)
            )

            importance_df.to_csv(
                self.feature_importance_file,
                index=False,
            )

        # --------------------------------------------------
        # Console Summary
        # --------------------------------------------------

        print("\n" + "=" * 70)
        print("MODEL RANKING")
        print("=" * 70)

        print(results_df)

        print("\n" + "=" * 70)
        print("BEST MODEL")
        print("=" * 70)

        print(best_name)

        print(f"R² Score : {best_r2:.4f}")

        print("\nGenerated Files")

        print("-" * 70)

        print(f"Metrics             : {self.metrics_file}")

        print(f"Predictions         : {self.predictions_file}")

        if hasattr(best_model, "feature_importances_"):

            print(
                f"Feature Importance  : "
                f"{self.feature_importance_file}"
            )

        print(f"Best Model          : {BEST_MODEL_FILE}")

        print("=" * 70)

        return results_df


def main():

    evaluator = ModelEvaluator()

    evaluator.evaluate_models()


if __name__ == "__main__":
    main()
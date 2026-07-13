"""
Trains all Machine Learning models.
"""

import joblib

from config import MODEL_DIR
from models import ModelFactory
from preprocessing import DataPreprocessor


class ModelTrainer:
    """
    Trains all regression models and saves them.
    """

    def __init__(self):

        self.models = ModelFactory.get_models()

    def train_models(self):

        # --------------------------------------------------
        # Load Preprocessed Data
        # --------------------------------------------------

        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = DataPreprocessor().preprocess()

        trained_models = {}

        print("=" * 60)
        print("MODEL TRAINING")
        print("=" * 60)

        # --------------------------------------------------
        # Train Each Model
        # --------------------------------------------------

        for model_name, model in self.models.items():

            print(f"\nTraining {model_name}...")

            model.fit(X_train, y_train)

            trained_models[model_name] = model

            filename = (
                model_name.lower()
                .replace(" ", "_")
                + ".pkl"
            )

            model_path = MODEL_DIR / filename

            joblib.dump(model, model_path)

            print("Completed")

        print("\n" + "=" * 60)
        print("ALL MODELS TRAINED SUCCESSFULLY")
        print("=" * 60)

        print(f"Total Models : {len(trained_models)}")

        return (
            trained_models,
            X_test,
            y_test,
        )


def main():

    trainer = ModelTrainer()

    trainer.train_models()


if __name__ == "__main__":
    main()
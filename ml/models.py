"""
Defines all Machine Learning models used in the project.
"""

from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from config import RANDOM_STATE


class ModelFactory:
    """
    Creates and returns all regression models.
    """

    @staticmethod
    def get_models():
        """
        Returns
        -------
        dict
            Dictionary of model name -> model object.
        """

        models = {

            "Linear Regression": LinearRegression(),

            "Decision Tree": DecisionTreeRegressor(
                random_state=RANDOM_STATE,
                max_depth=10,
                min_samples_split=10,
                min_samples_leaf=5,
            ),

            "Random Forest": RandomForestRegressor(
                n_estimators=200,
                random_state=RANDOM_STATE,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=3,
                n_jobs=-1,
            ),

            "Gradient Boosting": GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=4,
                random_state=RANDOM_STATE,
            ),
        }

        return models


def main():

    print("=" * 60)
    print("AVAILABLE MACHINE LEARNING MODELS")
    print("=" * 60)

    models = ModelFactory.get_models()

    for index, model_name in enumerate(models, start=1):
        print(f"{index}. {model_name}")

    print("=" * 60)
    print(f"Total Models : {len(models)}")


if __name__ == "__main__":
    main()
"""
comparative_analysis.py
-----------------------
Comparative analysis across athlete groups.
"""

import matplotlib.pyplot as plt
import pandas as pd

from base_analytics import BaseAnalytics
from queries import COMPARATIVE_DATA


class ComparativeAnalysis(BaseAnalytics):

    def __init__(self):
        super().__init__("Comparative Analysis")

    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------

    def load_dataset(self) -> pd.DataFrame:

        return self.load_data(COMPARATIVE_DATA)

    # --------------------------------------------------
    # Generic Comparison
    # --------------------------------------------------

    def compare(
        self,
        df: pd.DataFrame,
        group_column: str
    ) -> pd.DataFrame:
        """
        Compare groups based on summary statistics.
        """

        comparison = (

            df

            .groupby(group_column)

            .agg(

                AthleteCount=("TotalKg", "count"),

                AverageBodyweight=("BodyweightKg", "mean"),

                AverageSquat=("Best3SquatKg", "mean"),

                AverageBench=("Best3BenchKg", "mean"),

                AverageDeadlift=("Best3DeadliftKg", "mean"),

                AverageTotal=("TotalKg", "mean"),

                AverageDOTS=("Dots", "mean"),

                AverageStrengthRatio=("StrengthRatio", "mean"),

                AverageImprovement=("TotalImprovement", "mean")

            )

            .round(2)

        )

        return comparison.reset_index()

    # --------------------------------------------------
    # Print
    # --------------------------------------------------

    def print_results(self, comparison: pd.DataFrame):

        print("\n")
        print("=" * 90)
        print(comparison)
        print("=" * 90)

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def export_results(
        self,
        comparison: pd.DataFrame,
        filename: str
    ):

        self.export_csv(
            comparison,
            f"{filename}.csv"
        )

        self.export_excel(
            comparison,
            f"{filename}.xlsx"
        )

    # --------------------------------------------------
    # Visualization
    # --------------------------------------------------

    def plot_average_total(
        self,
        comparison: pd.DataFrame,
        group_column: str,
        filename: str
    ):

        plt.figure(figsize=(8, 5))

        plt.bar(

            comparison[group_column],

            comparison["AverageTotal"]

        )

        self.add_title(
            f"Average Total by {group_column}"
        )

        self.format_axis(
            group_column,
            "Average Total (kg)"
        )

        self.add_grid()

        self.save_chart(filename)

    # --------------------------------------------------
    # Run
    # --------------------------------------------------

    def run(self):

        df = self.load_dataset()

        self.check_empty(df)

        analyses = {

            "sex": "Sex",

            "equipment": "EquipmentName",

            "tested": "Tested"

        }

        for name, column in analyses.items():

            print(f"\n{name.upper()} ANALYSIS")

            result = self.compare(df, column)

            self.print_results(result)

            self.plot_average_total(
                result,
                column,
                f"{name}_average_total.png"
            )

            self.export_results(
                result,
                f"{name}_comparison"
            )


def main():

    analyzer = ComparativeAnalysis()

    analyzer.run()


if __name__ == "__main__":
    main()

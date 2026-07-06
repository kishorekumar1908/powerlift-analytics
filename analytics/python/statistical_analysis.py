"""
statistical_analysis.py
-----------------------
Descriptive statistical analysis of the PowerLift dataset.
"""

import pandas as pd

from base_analytics import BaseAnalytics
from queries import STATISTICAL_DATA


class StatisticalAnalysis(BaseAnalytics):

    def __init__(self):
        super().__init__("Statistical Analysis")

    def load_dataset(self) -> pd.DataFrame:

        return self.load_data(STATISTICAL_DATA)

    def calculate_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate descriptive statistics for all numeric columns.
        """

        numeric_df = df.select_dtypes(include="number")

        stats = pd.DataFrame(index=numeric_df.columns)

        stats["Mean"] = numeric_df.mean()
        stats["Median"] = numeric_df.median()
        stats["Mode"] = numeric_df.mode().iloc[0]
        stats["Std Dev"] = numeric_df.std()
        stats["Variance"] = numeric_df.var()
        stats["Minimum"] = numeric_df.min()
        stats["25%"] = numeric_df.quantile(0.25)
        stats["50%"] = numeric_df.quantile(0.50)
        stats["75%"] = numeric_df.quantile(0.75)
        stats["Maximum"] = numeric_df.max()
        stats["Missing Values"] = numeric_df.isna().sum()

        return stats.round(2)

    def print_statistics(self, stats: pd.DataFrame):

        print("\n")
        print("=" * 90)
        print("DESCRIPTIVE STATISTICS")
        print("=" * 90)
        print(stats)
        print("=" * 90)

    def export_statistics(self, stats: pd.DataFrame):

        self.export_csv(stats, "descriptive_statistics.csv")
        self.export_excel(stats, "descriptive_statistics.xlsx")

    def run(self):

        df = self.load_dataset()

        self.check_empty(df)

        stats = self.calculate_statistics(df)

        self.print_statistics(stats)

        return stats


def main():

    analyzer = StatisticalAnalysis()

    stats = analyzer.run()

    choice = input("\nExport statistics? (y/n): ").lower()

    if choice == "y":

        analyzer.export_statistics(stats)

        print("\nStatistics exported successfully.")


if __name__ == "__main__":
    main()
"""
correlation_analysis.py
-----------------------
Correlation analysis of numerical features.
"""

import matplotlib.pyplot as plt

from base_analytics import BaseAnalytics
from queries import CORRELATION_DATA


class CorrelationAnalysis(BaseAnalytics):

    def __init__(self):
        super().__init__("Correlation Analysis")

    def load_dataset(self):

        return self.load_data(CORRELATION_DATA)

    def calculate_correlation(self, df):

        numeric_df = df.select_dtypes(include="number")

        return numeric_df.corr().round(3)

    def print_correlation(self, corr):

        print("\n")
        print("=" * 90)
        print("CORRELATION MATRIX")
        print("=" * 90)
        print(corr)
        print("=" * 90)

    def export_correlation(self, corr):

        self.export_csv(
            corr,
            "correlation_matrix.csv"
        )

        self.export_excel(
            corr,
            "correlation_matrix.xlsx"
        )

    def plot_heatmap(self, corr):

        plt.figure(figsize=(10, 8))

        image = plt.imshow(
            corr,
            interpolation="nearest",
            aspect="auto"
        )

        plt.colorbar(image)

        plt.xticks(
            range(len(corr.columns)),
            corr.columns,
            rotation=90
        )

        plt.yticks(
            range(len(corr.columns)),
            corr.columns
        )

        self.add_title("Correlation Matrix")

        plt.tight_layout()

        self.save_chart("correlation_heatmap.png")

    def run(self):

        df = self.load_dataset()

        self.check_empty(df)

        corr = self.calculate_correlation(df)

        self.print_correlation(corr)

        self.plot_heatmap(corr)

        return corr


def main():

    analyzer = CorrelationAnalysis()

    corr = analyzer.run()

    choice = input("\nExport correlation matrix? (y/n): ").lower()

    if choice == "y":

        analyzer.export_correlation(corr)

        print("\nCorrelation matrix exported successfully.")


if __name__ == "__main__":
    main()
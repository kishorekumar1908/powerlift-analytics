"""
outlier_detection.py
--------------------
Outlier detection using the IQR method.
"""

import pandas as pd

from base_analytics import BaseAnalytics
from queries import OUTLIER_DATA


class OutlierDetection(BaseAnalytics):

    def __init__(self):
        super().__init__("Outlier Detection")

    def load_dataset(self):

        return self.load_data(OUTLIER_DATA)

    def detect_outliers(self, df, column):

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = df[
            (df[column] < lower)
            |
            (df[column] > upper)
        ].copy()

        outliers["Metric"] = column

        return outliers.sort_values(
            column,
            ascending=False
        )

    def print_outliers(self, df, column):

        print("\n")
        print("=" * 90)
        print(f"OUTLIERS : {column}")
        print("=" * 90)

        if df.empty:
            print("No outliers found.")
        else:
            print(df)

        print("=" * 90)

    def export_outliers(self, df, filename):

        self.export_csv(
            df,
            f"{filename}.csv"
        )

        self.export_excel(
            df,
            f"{filename}.xlsx"
        )

    def run(self):

        dataset = self.load_dataset()

        self.check_empty(dataset)

        columns = [

            "TotalKg",

            "Dots",

            "TotalImprovement"

        ]

        results = {}

        for column in columns:

            outliers = self.detect_outliers(
                dataset,
                column
            )

            self.print_outliers(
                outliers,
                column
            )

            self.export_outliers(
                outliers,
                f"{column.lower()}_outliers"
            )

            results[column] = outliers

        return results


def main():

    analyzer = OutlierDetection()

    analyzer.run()


if __name__ == "__main__":
    main()
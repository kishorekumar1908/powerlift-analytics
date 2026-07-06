"""
athlete_report.py
-----------------
Generate a career report for a single athlete.
"""

import pandas as pd

from base_analytics import BaseAnalytics
from queries import ATHLETE_REPORT


class AthleteReport(BaseAnalytics):
    """
    Generate a career summary for a single athlete.
    """

    def __init__(self):
        super().__init__("Athlete Report")

    def load_report(self, athlete_id: str) -> pd.DataFrame:
        """
        Load the complete competition history of an athlete.
        """

        return self.load_data(
            ATHLETE_REPORT,
            params={"athlete_id": athlete_id}
        )

    def generate_report(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a one-row athlete summary.
        """

        if df.empty:
            return pd.DataFrame()

        career_length = (
            df["CompetitionDate"].max()
            - df["CompetitionDate"].min()
        ).days / 365.25

        report = pd.DataFrame({

            "Athlete ID": [
                df["AthleteID"].iloc[0]
            ],

            "Athlete Name": [
                df["AthleteName"].iloc[0]
            ],

            "Competitions": [
                len(df)
            ],

            "Career Length (Years)": [
                round(career_length, 2)
            ],

            "Best Squat (kg)": [
                df["Best3SquatKg"].max()
            ],

            "Best Bench (kg)": [
                df["Best3BenchKg"].max()
            ],

            "Best Deadlift (kg)": [
                df["Best3DeadliftKg"].max()
            ],

            "Best Total (kg)": [
                df["TotalKg"].max()
            ],

            "Average Total (kg)": [
                round(df["TotalKg"].mean(), 2)
            ],

            "Best DOTS": [
                round(df["Dots"].max(), 2)
            ],

            "Career Improvement (kg)": [
                round(
                    df["CareerBestTotal"].max()
                    - df["TotalKg"].iloc[0],
                    2
                )
            ],

            "PR Count": [
                int(df["IsPR"].sum())
            ]
        })

        return report

    def print_report(self, report: pd.DataFrame):
        """
        Display the athlete report.
        """

        if report.empty:
            print("No athlete found.")
            return

        print("\n" + "=" * 65)
        print("ATHLETE CAREER REPORT")
        print("=" * 65)

        row = report.iloc[0]

        for column in report.columns:
            print(f"{column:<30}: {row[column]}")

        print("=" * 65)

    def export_report(
        self,
        report: pd.DataFrame,
        filename: str = "athlete_report"
    ):
        """
        Export the report to CSV and Excel.
        """

        self.export_csv(
            report,
            f"{filename}.csv"
        )

        self.export_excel(
            report,
            f"{filename}.xlsx"
        )

    def run(self, athlete_id: str):
        """
        Complete workflow.
        """

        history = self.load_report(athlete_id)

        report = self.generate_report(history)

        self.print_report(report)

        return report


def main():

    athlete_id = input(
        "Enter Athlete ID: "
    ).strip().upper()

    analyzer = AthleteReport()

    report = analyzer.run(athlete_id)

    choice = input(
        "\nExport report? (y/n): "
    ).lower()

    if choice == "y":

        analyzer.export_report(
            report,
            athlete_id
        )

        print("\nReport exported successfully.")


if __name__ == "__main__":
    main()
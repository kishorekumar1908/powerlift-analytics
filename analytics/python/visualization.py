"""
visualization.py
----------------
Generate athlete progression charts.
"""

import matplotlib.pyplot as plt
import pandas as pd

from base_analytics import BaseAnalytics
from queries import ATHLETE_REPORT


class Visualization(BaseAnalytics):

    def __init__(self):
        super().__init__("Visualization")

    def load_history(self, athlete_id: str) -> pd.DataFrame:
        """
        Load competition history for an athlete.
        """

        return self.load_data(
            ATHLETE_REPORT,
            params={"athlete_id": athlete_id}
        )

    def _plot(
        self,
        df: pd.DataFrame,
        y_column: str,
        title: str,
        ylabel: str,
        filename: str
    ):
        """
        Generic line chart.
        """

        if df.empty:
            print("No data found.")
            return

        plt.figure(figsize=(10, 5))

        plt.plot(
            df["CompetitionDate"],
            df[y_column],
            marker="o",
            linewidth=2
        )

        self.add_title(title)
        self.format_axis("Competition Date", ylabel)
        self.add_grid()

        plt.xticks(rotation=45)

        self.save_chart(filename)

    # --------------------------------------------------
    # Individual Charts
    # --------------------------------------------------

    def total_progression(self, df: pd.DataFrame):

        self._plot(
            df,
            "TotalKg",
            "Total Progression",
            "Total (kg)",
            "total_progression.png"
        )

    def squat_progression(self, df: pd.DataFrame):

        self._plot(
            df,
            "Best3SquatKg",
            "Squat Progression",
            "Squat (kg)",
            "squat_progression.png"
        )

    def bench_progression(self, df: pd.DataFrame):

        self._plot(
            df,
            "Best3BenchKg",
            "Bench Progression",
            "Bench (kg)",
            "bench_progression.png"
        )

    def deadlift_progression(self, df: pd.DataFrame):

        self._plot(
            df,
            "Best3DeadliftKg",
            "Deadlift Progression",
            "Deadlift (kg)",
            "deadlift_progression.png"
        )

    def dots_progression(self, df: pd.DataFrame):

        self._plot(
            df,
            "Dots",
            "DOTS Progression",
            "DOTS",
            "dots_progression.png"
        )

    def bodyweight_progression(self, df: pd.DataFrame):

        self._plot(
            df,
            "BodyweightKg",
            "Bodyweight Progression",
            "Bodyweight (kg)",
            "bodyweight_progression.png"
        )

    # --------------------------------------------------
    # Run All
    # --------------------------------------------------

    def run(self, athlete_id: str):

        df = self.load_history(athlete_id)

        self.check_empty(df)

        self.total_progression(df)
        self.squat_progression(df)
        self.bench_progression(df)
        self.deadlift_progression(df)
        self.dots_progression(df)
        self.bodyweight_progression(df)

        print("\nAll charts generated successfully.")

def main():

    athlete_id = input("Enter Athlete ID: ").strip().upper()

    visualizer = Visualization()

    visualizer.run(athlete_id)


if __name__ == "__main__":
    main()
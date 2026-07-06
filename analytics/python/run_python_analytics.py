"""
run_python_analytics.py
-----------------------
Main entry point for PowerLift Analytics.
"""

from athlete_report import AthleteReport
from visualization import Visualization
from statistical_analysis import StatisticalAnalysis
from comparative_analysis import ComparativeAnalysis
from correlation_analysis import CorrelationAnalysis
from outlier_detection import OutlierDetection


class PowerLiftAnalytics:

    def __init__(self):

        self.athlete_report = AthleteReport()
        self.visualization = Visualization()
        self.statistics = StatisticalAnalysis()
        self.comparative = ComparativeAnalysis()
        self.correlation = CorrelationAnalysis()
        self.outliers = OutlierDetection()

    # --------------------------------------------------

    def athlete_report_menu(self):

        athlete_id = input(
            "\nEnter Athlete ID: "
        ).strip().upper()

        report = self.athlete_report.run(
            athlete_id
        )

        if report.empty:
            return

        choice = input(
            "\nExport report? (y/n): "
        ).lower()

        if choice == "y":

            self.athlete_report.export_report(
                report,
                athlete_id
            )

    # --------------------------------------------------

    def visualization_menu(self):

        athlete_id = input(
            "\nEnter Athlete ID: "
        ).strip().upper()

        self.visualization.run(
            athlete_id
        )

    # --------------------------------------------------

    def statistics_menu(self):

        stats = self.statistics.run()

        choice = input(
            "\nExport statistics? (y/n): "
        ).lower()

        if choice == "y":

            self.statistics.export_statistics(
                stats
            )

    # --------------------------------------------------

    def comparative_menu(self):

        self.comparative.run()

    # --------------------------------------------------

    def correlation_menu(self):

        corr = self.correlation.run()

        choice = input(
            "\nExport correlation matrix? (y/n): "
        ).lower()

        if choice == "y":

            self.correlation.export_correlation(
                corr
            )

    # --------------------------------------------------

    def outlier_menu(self):

        self.outliers.run()

    # --------------------------------------------------

    def run_all(self):

        print("\nRunning all analyses...\n")

        self.statistics.run()

        self.comparative.run()

        self.correlation.run()

        self.outliers.run()

        print("\nCompleted.")

    # --------------------------------------------------

    @staticmethod
    def menu():

        print("\n")
        print("=" * 55)
        print("        POWERLIFT ANALYTICS")
        print("=" * 55)
        print("1. Athlete Report")
        print("2. Visualization")
        print("3. Statistical Analysis")
        print("4. Comparative Analysis")
        print("5. Correlation Analysis")
        print("6. Outlier Detection")
        print("7. Run All")
        print("0. Exit")
        print("=" * 55)

    # --------------------------------------------------

    def start(self):

        while True:

            self.menu()

            choice = input(
                "\nEnter your choice: "
            ).strip()

            if choice == "1":

                self.athlete_report_menu()

            elif choice == "2":

                self.visualization_menu()

            elif choice == "3":

                self.statistics_menu()

            elif choice == "4":

                self.comparative_menu()

            elif choice == "5":

                self.correlation_menu()

            elif choice == "6":

                self.outlier_menu()

            elif choice == "7":

                self.run_all()

            elif choice == "0":

                print("\nThank you for using PowerLift Analytics.")

                break

            else:

                print("\nInvalid choice. Try again.")


def main():

    app = PowerLiftAnalytics()

    app.start()


if __name__ == "__main__":
    main()
"""
Loads and prepares the engineered dataset for Machine Learning.
"""

import pandas as pd

from config import DATA_PATH, TARGET_COLUMN


class DataLoader:

    def __init__(self):
        self.data_path = DATA_PATH

    def load_data(self):
        """
        Load the engineered dataset.
        """

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Dataset not found:\n{self.data_path}"
            )

        df = pd.read_csv(self.data_path)

        print("=" * 60)
        print("POWERLIFT ANALYTICS - MACHINE LEARNING")
        print("=" * 60)
        print(f"Dataset : {self.data_path.name}")
        print(f"Rows    : {len(df):,}")
        print(f"Columns : {len(df.columns)}")
        print("=" * 60)

        return df

    def prepare_dataset(self):
        """
        Create the ML target by shifting TotalKg to the next competition.
        """

        df = self.load_data()

        df = (
            df
            .sort_values(["AthleteID", "CompetitionNumber"])
            .reset_index(drop=True)
        )

        df[TARGET_COLUMN] = (
            df.groupby("AthleteID")["TotalKg"]
              .shift(-1)
        )

        df = df.dropna(subset=[TARGET_COLUMN]).reset_index(drop=True)

        return df


def main():

    loader = DataLoader()

    df = loader.prepare_dataset()

    print("\nPrepared Dataset")
    print(df.head())

    print(f"\nRows Available : {len(df):,}")


if __name__ == "__main__":
    main()
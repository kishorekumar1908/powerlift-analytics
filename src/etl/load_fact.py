import logging
from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db_connection import get_engine
from extract import extract_data
from lookup import get_all_lookups

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

FACT_COLUMNS = [

    "AthleteKey",
    "DateKey",
    "MeetKey",
    "FederationKey",
    "WeightClassKey",
    "EquipmentKey",
    "EventKey",
    "AgeClassKey",

    "Age",
    "BodyweightKg",

    "Best3SquatKg",
    "Best3BenchKg",
    "Best3DeadliftKg",

    "TotalKg",

    "Dots",

    "Tested"

]

FACT_TABLE = "fact_results"

def prepare_fact_dataframe(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Prepare the source dataframe for fact loading.
    """

    logger.info("Preparing fact dataframe...")

    fact_df = dataframe.copy()

    # Convert Tested to Boolean
    fact_df["Tested"] = (
        fact_df["Tested"]
        .fillna("No")
        .str.strip()
        .str.upper()
        .map({
            "YES": True,
            "NO": False
        })
    )

    logger.info(
        "Fact dataframe prepared (%d rows).",
        len(fact_df)
    )

    return fact_df

def map_surrogate_keys(
    dataframe: pd.DataFrame,
    lookups: dict
) -> pd.DataFrame:
    """
    Replace business keys with surrogate keys.
    """

    logger.info("Mapping surrogate keys...")

    fact_df = dataframe.copy()

    # Athlete
    fact_df["AthleteKey"] = (
        fact_df["AthleteID"]
        .map(lookups["athlete"])
    )

    # Date
    fact_df["DateKey"] = (
        pd.to_datetime(fact_df["Date"])
        .map(lookups["date"])
    )

    # Meet
    fact_df["MeetKey"] = list(
        map(
            lookups["meet"].get,
            zip(
                fact_df["MeetName"],
                pd.to_datetime(fact_df["Date"])
            )
        )
    )

    # Federation
    fact_df["FederationKey"] = (
        fact_df["Federation"]
        .fillna("Unknown")
        .map(lookups["federation"])
    )

    # Weight Class
    fact_df["WeightClassKey"] = (
        fact_df["WeightClassKg"]
        .fillna("Unknown")
        .map(lookups["weight_class"])
    )

    # Equipment
    fact_df["EquipmentKey"] = (
        fact_df["Equipment"]
        .fillna("Unknown")
        .map(lookups["equipment"])
    )

    # Event
    fact_df["EventKey"] = (
        fact_df["Event"]
        .fillna("Unknown")
        .map(lookups["event"])
    )

    # Age Class
    fact_df["AgeClassKey"] = (
        fact_df["AgeClass"]
        .fillna("Unknown")
        .map(lookups["age_class"])
    )

    logger.info("Surrogate key mapping completed.")

    return fact_df

def validate_fact_dataframe(
    dataframe: pd.DataFrame
) -> None:
    """
    Validate the fact dataframe before loading into the warehouse.

    Raises
    ------
    ValueError
        If any surrogate key contains missing values.
    """

    logger.info("Validating fact dataframe...")

    # -------------------------------------------------------
    # Check for duplicate rows
    # -------------------------------------------------------

    duplicate_count = dataframe.duplicated().sum()

    if duplicate_count > 0:

        logger.warning(
            "%d duplicate fact row(s) detected.",
            duplicate_count
        )

    # -------------------------------------------------------
    # Validate foreign keys
    # -------------------------------------------------------

    foreign_keys = [
        "AthleteKey",
        "DateKey",
        "MeetKey",
        "FederationKey",
        "WeightClassKey",
        "EquipmentKey",
        "EventKey",
        "AgeClassKey"
    ]

    validation_errors = []

    for column in foreign_keys:

        missing_count = dataframe[column].isna().sum()

        if missing_count > 0:

            validation_errors.append(
                f"{column}: {missing_count} missing value(s)"
            )

    if validation_errors:

        logger.error("Fact dataframe validation failed.")

        for error in validation_errors:
            logger.error(error)

        raise ValueError("\n".join(validation_errors))

    logger.info("Fact dataframe validation passed.")

def prepare_fact_records(
    dataframe: pd.DataFrame
) -> list[dict[str, Any]]:
    """
    Prepare fact records for database insertion.
    """

    logger.info("Preparing fact records for insertion...")

    fact_df = dataframe[FACT_COLUMNS].copy()

    records = fact_df.to_dict(
        orient="records"
    )

    # Clean NaN/NaT values to None for MySQL compatibility
    for record in records:
        for key, val in record.items():
            if pd.isna(val):
                record[key] = None

    logger.info(
        "%d fact records prepared.",
        len(records)
    )

    return records
    
def insert_fact_records(
    engine: Engine,
    records: list[dict[str, Any]]
) -> None:
    """
    Insert records into the fact table.
    """

    logger.info("Loading fact table...")

    if not records:

        logger.warning(
            "No fact records found."
        )

        return

    columns = ", ".join(FACT_COLUMNS)

    placeholders = ", ".join(
        f":{column}"
        for column in FACT_COLUMNS
    )

    query = text(
        f"""
        INSERT INTO fact_results
        ({columns})
        VALUES
        ({placeholders})
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            records
        )

    logger.info(
        "%d rows inserted into fact_results.",
        len(records)
    )

def load_fact() -> None:
    """
    Load the fact table into the data warehouse.
    """

    logger.info("=" * 60)
    logger.info("Starting Fact Table Load Process")
    logger.info("=" * 60)

    # Create database engine
    engine = get_engine()

    # Extract source data
    dataframe = extract_data()

    # Prepare source dataframe
    fact_dataframe = prepare_fact_dataframe(dataframe)

    # Load lookup dictionaries
    lookups = get_all_lookups()

    # Map business keys to surrogate keys
    fact_dataframe = map_surrogate_keys(
        dataframe=fact_dataframe,
        lookups=lookups
    )

    # Validate mapped dataframe
    validate_fact_dataframe(fact_dataframe)

    # Prepare records for insertion
    records = prepare_fact_records(fact_dataframe)

    # Clear existing fact table
    with engine.begin() as connection:
        connection.execute(
            text(f"TRUNCATE TABLE {FACT_TABLE}")
        )

    logger.info("%s truncated.", FACT_TABLE)

    # Insert records
    insert_fact_records(
        engine=engine,
        records=records
    )

    logger.info("=" * 60)
    logger.info("Fact Table loaded successfully.")
    logger.info("=" * 60)


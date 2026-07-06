import logging
from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db_connection import get_engine
from extract import extract_data

DIM_ATHLETE = "dim_athlete"
DIM_DATE = "dim_date"
DIM_MEET = "dim_meet"
DIM_FEDERATION = "dim_federation"
DIM_WEIGHT_CLASS = "dim_weight_class"
DIM_EQUIPMENT = "dim_equipment"
DIM_EVENT = "dim_event"
DIM_AGE_CLASS = "dim_age_class"

SIMPLE_DIMENSIONS = {
    DIM_FEDERATION: ("Federation", "FederationName"),
    DIM_EQUIPMENT: ("Equipment", "EquipmentName"),
    DIM_EVENT: ("Event", "EventName"),
    DIM_WEIGHT_CLASS: ("WeightClassKg", "WeightClassKg"),
    DIM_AGE_CLASS: ("AgeClass", "AgeClassName"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def clear_table(
    engine: Engine,
    table_name: str
) -> None:
    """
    Remove all rows from a dimension table.
    """

    with engine.begin() as connection:
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        connection.execute(
            text(f"TRUNCATE TABLE {table_name}")
        )
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    logger.info("%s truncated.", table_name)

def prepare_records(
    dataframe: pd.DataFrame
) -> list[dict[str, Any]]:
    """
    Convert a DataFrame into a list of dictionaries.
    """

    records = dataframe.to_dict(orient="records")
    for record in records:
        for key, val in record.items():
            if pd.isna(val):
                record[key] = None
    return records

def insert_records(
    engine: Engine,
    table_name: str,
    columns: list[str],
    records: list[dict[str, Any]]
) -> None:
    """
    Insert records into a dimension table.
    """

    if not records:
        logger.warning(
            "%s has no records to insert.",
            table_name
        )
        return

    column_names = ", ".join(columns)

    placeholders = ", ".join(
        f":{column}"
        for column in columns
    )

    query = text(
        f"""
        INSERT INTO {table_name}
        ({column_names})
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
        "%d rows inserted into %s.",
        len(records),
        table_name
    )

def load_simple_dimension(
    engine: Engine,
    dataframe: pd.DataFrame,
    source_column: str,
    table_name: str,
    target_column: str
) -> None:
    """
    Load a simple one-column dimension table.

    Parameters
    ----------
    engine : Engine
        SQLAlchemy database engine.
    dataframe : pd.DataFrame
        Source dataframe.
    source_column : str
        Column name in the source dataframe.
    table_name : str
        Destination dimension table.
    target_column : str
        Column name in the destination table.
    """

    logger.info("Loading %s...", table_name)

    # Extract unique values
    dimension_df = (
        dataframe[[source_column]]
        .dropna()
        .drop_duplicates()
        .sort_values(by=source_column)
        .rename(columns={source_column: target_column})
        .reset_index(drop=True)
    )

    # Ensure "Unknown" is present in the simple dimension
    unknown_df = pd.DataFrame({target_column: ["Unknown"]})
    dimension_df = pd.concat(
        [dimension_df, unknown_df],
        ignore_index=True
    ).drop_duplicates()

    # Convert DataFrame into list of dictionaries
    records = prepare_records(dimension_df)

    # Clear existing data
    clear_table(engine, table_name)

    # Insert new records
    insert_records(
        engine=engine,
        table_name=table_name,
        columns=[target_column],
        records=records
    )

    logger.info(
        "%s loaded successfully (%d rows).",
        table_name,
        len(records)
    )

def load_dim_athlete(
    engine: Engine,
    dataframe: pd.DataFrame
) -> None:
    """
    Load the Athlete dimension table.
    """

    logger.info("Loading %s...", DIM_ATHLETE)

    athlete_df = (
        dataframe[
            [
                "AthleteID",
                "Name",
                "Sex",
                "BirthYearClass"
            ]
        ]
        .sort_values(by="AthleteID")
        .drop_duplicates(subset=["AthleteID"], keep="first")
        .rename(
            columns={
                "Name": "AthleteName"
            }
        )
        .reset_index(drop=True)
    )

    records = prepare_records(athlete_df)

    clear_table(engine, DIM_ATHLETE)

    insert_records(
        engine=engine,
        table_name=DIM_ATHLETE,
        columns=[
            "AthleteID",
            "AthleteName",
            "Sex",
            "BirthYearClass"
        ],
        records=records
    )

    logger.info(
        "%s loaded successfully (%d rows).",
        DIM_ATHLETE,
        len(records)
    )

def load_dim_date(
    engine: Engine,
    dataframe: pd.DataFrame
) -> None:
    """
    Load the Date dimension table.
    """

    logger.info("Loading %s...", DIM_DATE)

    # Get unique dates
    dates = (
        pd.to_datetime(dataframe["Date"])
        .drop_duplicates()
        .sort_values()
    )

    # Build date dimension
    date_df = pd.DataFrame({
        "DateKey": dates.dt.strftime("%Y%m%d").astype(int),
        "FullDate": dates,
        "Year": dates.dt.year,
        "Quarter": dates.dt.quarter,
        "Month": dates.dt.month,
        "MonthName": dates.dt.month_name(),
        "WeekOfYear": dates.dt.isocalendar().week.astype(int),
        "DayOfMonth": dates.dt.day,
        "DayOfWeek": dates.dt.day_name()
    })

    records = prepare_records(date_df)

    clear_table(engine, DIM_DATE)

    insert_records(
        engine=engine,
        table_name=DIM_DATE,
        columns=[
            "DateKey",
            "FullDate",
            "Year",
            "Quarter",
            "Month",
            "MonthName",
            "WeekOfYear",
            "DayOfMonth",
            "DayOfWeek"
        ],
        records=records
    )

    logger.info(
        "%s loaded successfully (%d rows).",
        DIM_DATE,
        len(records)
    )

def load_dim_meet(
    engine: Engine,
    dataframe: pd.DataFrame
) -> None:
    """
    Load the Meet dimension table.
    """

    logger.info("Loading %s...", DIM_MEET)

    # Extract required columns
    meet_df = (
        dataframe[
            [
                "MeetName",
                "MeetTown",
                "Date"
            ]
        ]
        .rename(
            columns={
                "Date": "MeetDate"
            }
        )
    )

    # Clean MeetTown values
    meet_df["MeetTown"] = (
        meet_df["MeetTown"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .str.strip()
    )

    # Deduplicate based on unique key constraint (MeetName, MeetDate)
    meet_df = (
        meet_df.drop_duplicates(subset=["MeetName", "MeetDate"])
        .reset_index(drop=True)
    )

    records = prepare_records(meet_df)

    clear_table(engine, DIM_MEET)

    insert_records(
        engine=engine,
        table_name=DIM_MEET,
        columns=[
            "MeetName",
            "MeetTown",
            "MeetDate"
        ],
        records=records
    )

    logger.info(
        "%s loaded successfully (%d rows).",
        DIM_MEET,
        len(records)
    )

def load_dimensions() -> None:
    """
    Load all dimension tables into the data warehouse.
    """

    logger.info("=" * 60)
    logger.info("Starting Dimension Load Process")
    logger.info("=" * 60)

    engine = get_engine()

    dataframe = extract_data()

    # Load custom dimensions
    load_dim_athlete(
        engine=engine,
        dataframe=dataframe
    )

    load_dim_date(
        engine=engine,
        dataframe=dataframe
    )

    load_dim_meet(
        engine=engine,
        dataframe=dataframe
    )

    # Load simple dimensions
    for table_name, (
        source_column,
        target_column
    ) in SIMPLE_DIMENSIONS.items():

        load_simple_dimension(
            engine=engine,
            dataframe=dataframe,
            source_column=source_column,
            table_name=table_name,
            target_column=target_column
        )

    logger.info("=" * 60)
    logger.info("All dimension tables loaded successfully.")
    logger.info("=" * 60)



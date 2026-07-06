"""
==========================================================
PowerLift Analytics
Data Warehouse Validation Module
==========================================================
"""

import logging

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db_connection import get_engine
from extract import extract_data

# -------------------------------------------------------
# Logger Configuration
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

FACT_TABLE = "fact_results"

def validate_row_count(
    engine: Engine,
    dataframe: pd.DataFrame
) -> None:
    """
    Validate source and fact table row counts.
    """

    logger.info("Validating row count...")

    source_rows = len(dataframe)

    query = text(
        f"""
        SELECT COUNT(*) AS RowCount
        FROM {FACT_TABLE}
        """
    )

    with engine.connect() as connection:

        warehouse_rows = connection.execute(
            query
        ).scalar()

    if source_rows != warehouse_rows:

        raise ValueError(
            f"""
Row count validation failed.

Source Rows    : {source_rows}

Warehouse Rows : {warehouse_rows}
"""
        )

    logger.info(
        "Row count validation passed (%d rows).",
        source_rows
    )

def validate_foreign_keys(
    engine: Engine
) -> None:
    """
    Validate foreign key integrity.
    """

    logger.info("Validating foreign keys...")

    query = text(
        """
        SELECT COUNT(*) AS InvalidRows
        FROM fact_results f

        LEFT JOIN dim_athlete a
        ON f.AthleteKey = a.AthleteKey

        LEFT JOIN dim_date d
        ON f.DateKey = d.DateKey

        LEFT JOIN dim_meet m
        ON f.MeetKey = m.MeetKey

        LEFT JOIN dim_federation fd
        ON f.FederationKey = fd.FederationKey

        LEFT JOIN dim_weight_class wc
        ON f.WeightClassKey = wc.WeightClassKey

        LEFT JOIN dim_equipment eq
        ON f.EquipmentKey = eq.EquipmentKey

        LEFT JOIN dim_event ev
        ON f.EventKey = ev.EventKey

        LEFT JOIN dim_age_class ac
        ON f.AgeClassKey = ac.AgeClassKey

        WHERE

            a.AthleteKey IS NULL

            OR d.DateKey IS NULL

            OR m.MeetKey IS NULL

            OR fd.FederationKey IS NULL

            OR wc.WeightClassKey IS NULL

            OR eq.EquipmentKey IS NULL

            OR ev.EventKey IS NULL

            OR ac.AgeClassKey IS NULL
        """
    )

    with engine.connect() as connection:

        invalid_rows = connection.execute(
            query
        ).scalar()

    if invalid_rows > 0:

        raise ValueError(
            f"{invalid_rows} invalid foreign key records found."
        )

    logger.info("Foreign key validation passed.")

def validate_null_keys(
    engine: Engine
) -> None:
    """
    Validate that no foreign key is NULL.
    """

    logger.info("Validating NULL foreign keys...")

    query = text(
        """
        SELECT COUNT(*) AS NullKeys
        FROM fact_results

        WHERE

        AthleteKey IS NULL

        OR DateKey IS NULL

        OR MeetKey IS NULL

        OR FederationKey IS NULL

        OR WeightClassKey IS NULL

        OR EquipmentKey IS NULL

        OR EventKey IS NULL

        OR AgeClassKey IS NULL
        """
    )

    with engine.connect() as connection:

        null_rows = connection.execute(
            query
        ).scalar()

    if null_rows > 0:

        raise ValueError(
            f"{null_rows} NULL foreign keys found."
        )

    logger.info("NULL key validation passed.")

def validate() -> None:
    """
    Execute all warehouse validation checks.
    """

    logger.info("=" * 60)
    logger.info("Starting Warehouse Validation")
    logger.info("=" * 60)

    engine = get_engine()

    dataframe = extract_data()

    validate_row_count(
        engine,
        dataframe
    )

    validate_null_keys(
        engine
    )

    validate_foreign_keys(
        engine
    )

    logger.info("=" * 60)
    logger.info("Warehouse Validation Successful")
    logger.info("=" * 60)


"""
==========================================================
PowerLift Analytics
Lookup Dictionary Module

Reads dimension tables and creates lookup dictionaries
for the fact table loading process.
==========================================================
"""

import logging

import pandas as pd

from db_connection import get_engine

# -------------------------------------------------------
# Logger Configuration
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# Table Names
# -------------------------------------------------------

DIM_ATHLETE = "dim_athlete"
DIM_DATE = "dim_date"
DIM_MEET = "dim_meet"
DIM_FEDERATION = "dim_federation"
DIM_WEIGHT_CLASS = "dim_weight_class"
DIM_EQUIPMENT = "dim_equipment"
DIM_EVENT = "dim_event"
DIM_AGE_CLASS = "dim_age_class"

def get_lookup_dictionary(
    table_name: str,
    business_key: str,
    surrogate_key: str
) -> dict:
    """
    Read a dimension table and create a lookup dictionary.

    Parameters
    ----------
    table_name : str
        Dimension table name.

    business_key : str
        Business key column.

    surrogate_key : str
        Surrogate key column.

    Returns
    -------
    dict
        Dictionary mapping business key to surrogate key.
    """

    engine = get_engine()

    query = f"""
        SELECT
            {business_key},
            {surrogate_key}
        FROM {table_name}
    """

    dataframe = pd.read_sql(query, engine)

    lookup = dict(
        zip(
            dataframe[business_key],
            dataframe[surrogate_key]
        )
    )

    logger.info(
        "%s lookup created (%d records).",
        table_name,
        len(lookup)
    )

    return lookup

def get_athlete_lookup() -> dict:
    return get_lookup_dictionary(
        DIM_ATHLETE,
        "AthleteID",
        "AthleteKey"
    )

def get_date_lookup() -> dict:
    """
    Create lookup dictionary for Date dimension.

    Key:
        pandas.Timestamp

    Value:
        DateKey (YYYYMMDD)
    """

    engine = get_engine()

    query = f"""
        SELECT
            FullDate,
            DateKey
        FROM {DIM_DATE}
    """

    dataframe = pd.read_sql(query, engine)

    lookup = {
        pd.Timestamp(row["FullDate"]): row["DateKey"]
        for _, row in dataframe.iterrows()
    }

    logger.info(
        "%s lookup created (%d records).",
        DIM_DATE,
        len(lookup)
    )

    return lookup

def get_federation_lookup() -> dict:
    return get_lookup_dictionary(
        DIM_FEDERATION,
        "FederationName",
        "FederationKey"
    )

def get_equipment_lookup() -> dict:
    return get_lookup_dictionary(
        DIM_EQUIPMENT,
        "EquipmentName",
        "EquipmentKey"
    )

def get_event_lookup() -> dict:
    return get_lookup_dictionary(
        DIM_EVENT,
        "EventName",
        "EventKey"
    )

def get_weight_class_lookup() -> dict:
    return get_lookup_dictionary(
        DIM_WEIGHT_CLASS,
        "WeightClassKg",
        "WeightClassKey"
    )

def get_age_class_lookup() -> dict:
    return get_lookup_dictionary(
        DIM_AGE_CLASS,
        "AgeClassName",
        "AgeClassKey"
    )

def get_meet_lookup() -> dict:
    """
    Create lookup dictionary for Meet dimension.

    Key:
        (MeetName, MeetDate)

    Value:
        MeetKey
    """

    engine = get_engine()

    query = f"""
        SELECT
            MeetName,
            MeetDate,
            MeetKey
        FROM {DIM_MEET}
    """

    dataframe = pd.read_sql(query, engine)

    lookup = {
        (
            row["MeetName"],
            pd.Timestamp(row["MeetDate"])
        ): row["MeetKey"]
        for _, row in dataframe.iterrows()
    }

    logger.info(
        "%s lookup created (%d records).",
        DIM_MEET,
        len(lookup)
    )

    return lookup

def get_all_lookups() -> dict:
    """
    Create all lookup dictionaries.
    """

    return {

        "athlete": get_athlete_lookup(),

        "date": get_date_lookup(),

        "meet": get_meet_lookup(),

        "federation": get_federation_lookup(),

        "equipment": get_equipment_lookup(),

        "event": get_event_lookup(),

        "weight_class": get_weight_class_lookup(),

        "age_class": get_age_class_lookup()

    }


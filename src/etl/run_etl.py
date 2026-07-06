"""
==========================================================
PowerLift Analytics
ETL Pipeline Runner
==========================================================

Runs the complete ETL pipeline:

1. Load Dimension Tables
2. Load Fact Table
3. Validate Data Warehouse
==========================================================
"""

import logging
import time

from load_dimensions import load_dimensions
from load_fact import load_fact
from validate import validate

# -------------------------------------------------------
# Logger Configuration
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_etl() -> None:
    """
    Execute the complete ETL pipeline.
    """

    logger.info("=" * 60)
    logger.info("Starting PowerLift Analytics ETL Pipeline")
    logger.info("=" * 60)

    start_time = time.perf_counter()

    try:

        # -------------------------------------------------------
        # Load Dimension Tables
        # -------------------------------------------------------

        logger.info("Step 1/3 : Loading Dimension Tables")

        load_dimensions()

        # -------------------------------------------------------
        # Load Fact Table
        # -------------------------------------------------------

        logger.info("Step 2/3 : Loading Fact Table")

        load_fact()

        # -------------------------------------------------------
        # Validate Warehouse
        # -------------------------------------------------------

        logger.info("Step 3/3 : Validating Data Warehouse")

        validate()

        elapsed_time = time.perf_counter() - start_time

        logger.info("=" * 60)
        logger.info("ETL Pipeline Completed Successfully")
        logger.info("Execution Time : %.2f seconds", elapsed_time)
        logger.info("=" * 60)

    except Exception as error:

        logger.exception("ETL Pipeline Failed")

        raise error


if __name__ == "__main__":
    run_etl()
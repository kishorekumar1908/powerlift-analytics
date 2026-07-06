"""
config.py
----------
Shared database configuration for Python analytics.
"""

from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Add project root to Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Reuse the ETL database connection
# pyrefly: ignore [missing-import]
from src.etl.db_connection import get_engine


# Output folders
OUTPUT_DIR = PROJECT_ROOT / "analytics" / "python" / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
REPORT_DIR = OUTPUT_DIR / "reports"
EXPORT_DIR = OUTPUT_DIR / "exports"

for folder in [OUTPUT_DIR, CHART_DIR, REPORT_DIR, EXPORT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)
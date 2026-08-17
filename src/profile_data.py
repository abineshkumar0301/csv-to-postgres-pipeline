import logging
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/input/Online Retail.csv")

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "profile.log"

def configure_logging() -> None:

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if this function is called again.
    if root_logger.handlers:
        return

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

def load_data(file_path: Path) -> pd.DataFrame:

    logger.info("Loading data from %s", file_path)

    if not file_path.exists():
        logger.error("Input file not found: %s", file_path)
        raise FileNotFoundError(f"Input file not found: {file_path}")

    df = pd.read_csv(file_path)

    logger.info("Loaded %s rows and %s columns", *df.shape)

    return df

def profile_data(df: pd.DataFrame) -> None:

    logger.info("Starting data profiling")

    print("\n========== DATA PROFILE ==========")

    print("\nShape:")
    print(df.shape)

    logger.info("Dataset shape: %s rows and %s columns", *df.shape) # * is for unpacking an iterable. shape returns a tuple of (row, col) 

    print("\nColumns:")
    print(df.columns.tolist())

    logger.info("Dataset contains %s columns", len(df.columns))

    print("\nData Types:")
    print(df.dtypes)

    missing_values = df.isnull().sum()

    print("\nMissing Values:")
    print(missing_values)

    total_missing = int(missing_values.sum())

    logger.info("Total missing values: %s", total_missing)

    # Log individual columns containing missing values.
    for column, count in missing_values.items():
        if count > 0:
            logger.warning("Column '%s' contains %s missing values", column, count)

    duplicate_count = int(df.duplicated().sum())

    print("\nDuplicate Rows:")
    print(duplicate_count)

    if duplicate_count > 0:
        logger.warning("Found %s duplicate rows", duplicate_count)
    else:
        logger.info("No duplicate rows found")

    cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

    cancelled_count = int(cancelled.sum())

    print("\nCancelled Orders:")
    print(cancelled_count)

    if cancelled_count > 0:
        logger.warning("Found %s cancelled transactions", cancelled_count)
    else:
        logger.info("No cancelled transactions found")

    unique_values = {
        "InvoiceNo": int(df["InvoiceNo"].nunique()),
        "StockCode": int(df["StockCode"].nunique()),
        "Description": int(df["Description"].nunique()),
        "CustomerID": int(df["CustomerID"].nunique()),
        "Country": int(df["Country"].nunique()),
    }

    print("\nUnique Values:")

    for column, count in unique_values.items():
        print(f"{column:<12}: {count}")

        logger.debug("Column '%s' contains %s unique values", column, count)

    logger.info("Data profiling completed")

def main() -> None:

    configure_logging()
    logger.info("========== DATA PROFILING PIPELINE STARTED ==========")

    try:
        df = load_data(INPUT_FILE)
        profile_data(df)
        logger.info("========== DATA PROFILING PIPELINE COMPLETED ==========")

    except Exception:
        logger.exception("Data profiling pipeline failed")
        raise        # re raising the exception so that i can know that there is a problem... If it is not re raised, then the error is in log, but the program completes fine.

if __name__ == "__main__":
    main()
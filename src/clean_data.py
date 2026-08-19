import logging
from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/input/Online Retail.csv")

OUTPUT_DIR = Path("data/output")

CLEANED_DIR = OUTPUT_DIR / "cleaned"
REJECTED_DIR = OUTPUT_DIR / "rejected"
CANCELLED_DIR = OUTPUT_DIR / "cancelled"

CLEANED_FILE = CLEANED_DIR / "online_retail_cleaned.csv"
REJECTED_FILE = REJECTED_DIR / "online_retail_rejected.csv"
CANCELLED_FILE = CANCELLED_DIR / "online_retail_cancelled.csv"

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pipeline.log"

CLEANED_FILE = CLEANED_DIR / "online_retail_cleaned.csv"
CLEANED_JSON_FILE = CLEANED_DIR / "online_retail_cleaned.json"

REJECTED_FILE = REJECTED_DIR / "online_retail_rejected.csv"
CANCELLED_FILE = CANCELLED_DIR / "online_retail_cancelled.csv"

def save_json(df: pd.DataFrame) -> None:

    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    df.to_json(
        CLEANED_JSON_FILE,
        orient="records",
        lines=True,
        date_format="iso",
        force_ascii=False
    )

    logger.info(
        "Saved %s records to %s",
        len(df),
        CLEANED_JSON_FILE,
    )

def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

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


def validate_records(df: pd.DataFrame) -> pd.DataFrame:

    logger.info("Starting data validation")

    validation_df = df.copy()

    validation_df["rejection_reason"] = ""

    cancelled = validation_df["InvoiceNo"].astype(str).str.startswith("C")

    validation_df["is_cancelled"] = cancelled

    cancelled_count = int(cancelled.sum())

    logger.info("Identified %s cancelled transactions", cancelled_count)

    missing_description = validation_df["Description"].isna() & ~cancelled

    validation_df.loc[missing_description, "rejection_reason"] += "Missing Description; "

    logger.info(
        "Found %s non-cancelled records with missing Description",
        int(missing_description.sum())
    )

    missing_customer_id = validation_df["CustomerID"].isna() & ~cancelled

    validation_df.loc[missing_customer_id, "rejection_reason"] += "Missing CustomerID; "

    logger.info(
        "Found %s non-cancelled records with missing CustomerID",
        int(missing_customer_id.sum())
    )

    invalid_quantity = (validation_df["Quantity"] <= 0) & ~cancelled

    validation_df.loc[invalid_quantity, "rejection_reason"] += "Invalid Quantity; "

    logger.info(
        "Found %s non-cancelled records with invalid Quantity",
        int(invalid_quantity.sum())
    )

    invalid_unit_price = (validation_df["UnitPrice"] <= 0) & ~cancelled

    validation_df.loc[invalid_unit_price, "rejection_reason"] += "Invalid UnitPrice; "

    logger.info(
        "Found %s non-cancelled records with invalid UnitPrice",
        int(invalid_unit_price.sum())
    )

    missing_invoice = validation_df["InvoiceNo"].isna()

    validation_df.loc[missing_invoice, "rejection_reason"] += "Missing InvoiceNo; "

    logger.info(
        "Found %s records with missing InvoiceNo",
        int(missing_invoice.sum())
    )

    validation_df["rejection_reason"] = validation_df["rejection_reason"].str.rstrip("; ")

    validation_df["is_valid"] = (validation_df["rejection_reason"] == "")

    valid_count = int((validation_df["is_valid"] & ~validation_df["is_cancelled"]).sum())

    rejected_count = int((~validation_df["is_valid"] & ~validation_df["is_cancelled"]).sum())

    logger.info("Validation completed: %s valid, %s rejected, %s cancelled", valid_count, rejected_count, cancelled_count)

    return validation_df

def separate_records(validation_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    logger.info("Separating records")

    cancelled_df = validation_df[validation_df["is_cancelled"]].copy()

    rejected_df = validation_df[~validation_df["is_cancelled"] & ~validation_df["is_valid"]].copy()

    valid_df = validation_df[~validation_df["is_cancelled"] & validation_df["is_valid"]].copy()

    valid_df.drop(columns=["rejection_reason", "is_valid", "is_cancelled"], inplace=True)

    cancelled_df.drop(columns=["rejection_reason", "is_valid", "is_cancelled"], inplace=True)

    rejected_df.drop(columns=["is_valid", "is_cancelled"], inplace=True)

    logger.info(
        "Separated %s valid records",
        len(valid_df)
    )

    logger.info(
        "Separated %s rejected records",
        len(rejected_df)
    )

    logger.info(
        "Separated %s cancelled records",
        len(cancelled_df)
    )

    return valid_df, rejected_df, cancelled_df

def save_data(valid_df: pd.DataFrame, rejected_df: pd.DataFrame, cancelled_df: pd.DataFrame) -> None:
    
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    REJECTED_DIR.mkdir(parents=True, exist_ok=True)
    CANCELLED_DIR.mkdir(parents=True, exist_ok=True)

    valid_df.to_csv(CLEANED_FILE, index=False)

    logger.info(
        "Saved %s valid records to %s",
        len(valid_df),
        CLEANED_FILE,
    )

    rejected_df.to_csv(REJECTED_FILE, index=False)

    logger.info(
        "Saved %s rejected records to %s",
        len(rejected_df),
        REJECTED_FILE,
    )

    cancelled_df.to_csv(CANCELLED_FILE, index=False)

    logger.info(
        "Saved %s cancelled records to %s",
        len(cancelled_df),
        CANCELLED_FILE,
    )

def validate_reconciliation(original_count: int, valid_count: int, rejected_count: int, cancelled_count: int) -> None:

    classified_count = valid_count + rejected_count + cancelled_count

    logger.info(
        "Record reconciliation: "
        "%s valid + %s rejected + %s cancelled = %s",
        valid_count,
        rejected_count,
        cancelled_count,
        classified_count,
    )

    if classified_count != original_count:
        logger.error(
            "Record reconciliation failed: "
            "original=%s, classified=%s",
            original_count,
            classified_count,
        )

        raise ValueError(
            "Record reconciliation failed. "
            "Some records were lost or classified more than once."
        )

    logger.info("Record reconciliation successful")

def main() -> None:

    configure_logging()

    logger.info(
        "========== DATA CLEANING PIPELINE STARTED =========="
    )

    try:
        df = load_data(INPUT_FILE)

        original_count = len(df)

        validation_df = validate_records(df)

        valid_df, rejected_df, cancelled_df = separate_records(validation_df)

        validate_reconciliation(original_count=original_count, valid_count=len(valid_df), rejected_count=len(rejected_df), cancelled_count=len(cancelled_df))

        save_data(valid_df=valid_df, rejected_df=rejected_df, cancelled_df=cancelled_df)

        save_json(valid_df)

        logger.info("Original records: %s", original_count)

        logger.info("Cleaned records: %s", len(valid_df))

        logger.info("Rejected records: %s", len(rejected_df))

        logger.info("Cancelled records: %s", len(cancelled_df))

        logger.info("========== DATA CLEANING PIPELINE COMPLETED ==========")


    except Exception:
        logger.exception("Data cleaning pipeline failed")
        raise

if __name__ == "__main__":
    main()
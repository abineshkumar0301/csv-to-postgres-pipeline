import json
import logging
from pathlib import Path
from datetime import datetime
import psycopg
from psycopg import Connection
from psycopg import Error


OUTPUT_DIR = Path("data/output")

CLEANED_DIR = OUTPUT_DIR / "cleaned"

CLEANED_JSON_FILE = CLEANED_DIR / "online_retail_cleaned.json"

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pipeline.log"

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "online_retail_db"

#I have replaced the DB_USER and DB_PASSWORD with placeholders before pushing. Please replace them with your actual database credentials.

DB_USER = "user"
DB_PASSWORD = "password"

BATCH_SIZE = 5000

def configure_logging() -> None:

    LOG_DIR.mkdir(parents=True, exist_ok=True) #Creates the logs directory if it doesn't exist
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    if not root_logger.handlers:

        root_logger.addHandler(console_handler)

        root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)


def create_connection() -> Connection:

    logger.info(
        "Connecting to PostgreSQL database '%s'",
        DB_NAME,
    )

    try:

        connection = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        logger.info(
            "PostgreSQL connection established successfully"
        )

        return connection

    except Error:
        logger.exception("Failed to connect to PostgreSQL")
        raise


def test_connection() -> None:

    connection = None

    try:
        connection = create_connection()
        with connection.cursor() as cursor:

            cursor.execute("SELECT version();")

            version = cursor.fetchone()

            logger.info(
                "PostgreSQL connection test successful"
            )

            logger.info(
                "PostgreSQL version: %s",
                version[0],
            )

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'online_retail'
                );
                """
            )

            table_exists = cursor.fetchone()[0]

            if table_exists:
                logger.info("Table 'online_retail' exists")

            else:
                logger.warning("Table 'online_retail' does not exist")

    except Error:
        logger.exception("PostgreSQL connection test failed")
        raise

    finally:
        if connection is not None:

            connection.close()

            logger.info("PostgreSQL connection closed")


def load_json(file_path: Path) -> list[dict]:

    logger.info("Loading JSON data from %s", file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    data = []

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                data.append(json.loads(line))

    logger.info("Loaded %s records from JSON", len(data))
    return data

def prepare_records(data: list[dict]) -> list[tuple]:
    records = []
    for row in data:
        invoice_date = datetime.strptime(row["InvoiceDate"], "%d-%m-%Y %H:%M")
        records.append(
            (
                row.get("InvoiceNo"),
                row.get("StockCode"),
                row.get("Description"),
                row.get("Quantity"),
                invoice_date,
                row.get("UnitPrice"),
                row.get("CustomerID"),
                row.get("Country"),
            )
        )

    logger.info("Prepared %s records for PostgreSQL", len(records))
    return records

def insert_data(records: list[tuple]) -> None:

    connection = None

    insert_query = """
        INSERT INTO online_retail (
            invoice_no,
            stock_code,
            description,
            quantity,
            invoice_date,
            unit_price,
            customer_id,
            country
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            logger.info("Clearing existing records from online_retail")
            cursor.execute("TRUNCATE TABLE online_retail;")
            logger.info("Existing records cleared")
            total_records = len(records)
            logger.info("Starting batch insertion of %s records", total_records)

            for start in range(0, total_records, BATCH_SIZE):
                batch = records[
                    start:start + BATCH_SIZE
                ]
                cursor.executemany(insert_query, batch)
                inserted_count = min(start + len(batch), total_records)
                logger.info("Inserted %s / %s records", inserted_count, total_records)

            connection.commit()

            logger.info("Transaction committed successfully")

    except Error:
        if connection is not None:
            connection.rollback()
            logger.error("Transaction rolled back")

        logger.exception("Data insertion failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("PostgreSQL connection closed")


def validate_loaded_count(expected_count: int) -> None:
    connection = None
    try:
        connection = create_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM online_retail;")
            actual_count = cursor.fetchone()[0]

        logger.info("Expected records: %s", expected_count )

        logger.info("Loaded records: %s", actual_count)

        if actual_count != expected_count:
            logger.error("Record count validation failed")

            raise ValueError(
                "PostgreSQL record count does not "
                "match JSON record count"
            )
        logger.info("Record count validation successful")

    except Error:
        logger.exception("Failed to validate PostgreSQL record count")
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("PostgreSQL connection closed")

def main() -> None:
    configure_logging()
    logger.info("========== POSTGRESQL DATA LOAD STARTED ==========")
    try:
        test_connection()
        data = load_json(CLEANED_JSON_FILE)
        records = prepare_records(data)
        insert_data(records)
        validate_loaded_count(len(records))
        logger.info("========== POSTGRESQL DATA LOAD COMPLETED ==========")

    except Exception:
        logger.exception("PostgreSQL data loading pipeline failed")
        raise

if __name__ == "__main__":
    main()
# CSV to JSON to PostgreSQL Data Pipeline

A hands-on Data Engineering project where I process real-world retail
transaction data through a simple ETL pipeline.

## Project Overview

In this project, I:

1. Read raw transactional data from a CSV file
2. Inspect and profile the data for quality issues
3. Clean and validate the data
4. Separate cancelled and rejected transactions
5. Convert the cleaned data into JSON format
6. Load the processed data into a PostgreSQL database
7. Query and analyze the data using SQL

## Pipeline

CSV → Inspection → Cleaning → JSON → PostgreSQL → SQL Analysis

## Dataset

I use the Online Retail dataset containing transaction records from a
UK-based online retailer.

The dataset contains information such as:

- Invoice number
- Product code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

## Data Quality

As part of the project, I investigate real-world data quality
problems such as:

- Missing Customer IDs
- Duplicate records
- Cancelled orders
- Invalid quantities
- Invalid unit prices
- Missing product descriptions
- Missing invoice numbers

The cleaning pipeline validates the records and separates them into:

- Cleaned records
- Rejected records
- Cancelled transactions

Record reconciliation is also performed to ensure that no records are
lost during the cleaning process.

## PostgreSQL

The cleaned JSON data is loaded into PostgreSQL using Python and
Psycopg.

The database loading process includes:

- PostgreSQL connection testing
- JSON data loading
- Batch insertion
- Transaction management
- Rollback on failure
- Record count validation
- Idempotent full-refresh loading

## SQL Analysis

After loading the data into PostgreSQL, I perform SQL analysis using
queries involving:

- `SELECT`
- `WHERE`
- `ORDER BY`
- Aggregate functions
- `GROUP BY`
- `HAVING`
- `CASE`
- Date analysis
- Revenue analysis
- Customer analysis
- Product analysis
- Country-level analysis

## Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- Psycopg
- Git
- GitHub

## Project Structure

```text
csv-to-postgres-pipeline/
│
├── data/
│   ├── input/
│   └── output/
│       ├── cleaned/
│       ├── rejected/
│       └── cancelled/
│
├── src/
│   ├── profile_data.py
│   ├── clean_data.py
│   └── load_data.py
│
├── logs/
│   ├── pipeline.log
│   └── db.log
│
├── sql/
│   └── analysis.sql
│
├── README.md
└── requirements.txt

# CSV to JSON to PostgreSQL Data Pipeline

A hands-on Data Engineering project where I process real-world retail
transaction data through a simple ETL pipeline.

## Project Overview

In this project, I will:

1. Read raw transactional data from a CSV file
2. Inspect and profile the data for quality issues
3. Convert the data into JSON format
4. Load the processed data into a PostgreSQL database
5. Query the data using SQL

## Pipeline

CSV → JSON → PostgreSQL

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
- Missing product descriptions

The goal is to understand how these issues can affect a data pipeline
and how they can be identified and handled.

## Technologies

- Python
- PostgreSQL
- SQL
- Git
- GitHub

## Project Structure

```text
csv-to-postgres-pipeline/
│
├── data/
│   ├── input/
│   └── raw/
│
├── src/
│
├── sql/
│
├── README.md
└── requirements.txt
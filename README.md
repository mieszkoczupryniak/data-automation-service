# data-automation-service

Production-style data & automation service – fetch real-world data, store it, and generate simple reports. First portfolio project in my AI/infra journey.

## Features

- HTTP JSON pipeline that fetches data from a public API, stores raw daily snapshots and generates summary reports.
- Real estate ETL pipeline that reads CSV transactions, computes per‑district stats, average price and price per m².
- Simple CLI to choose which pipeline to run (`--job http_pipeline` or `--job real_estate_etl`).
- Clear project structure with separate `data/` and `reports/` folders, ready to plug into larger data/infra stacks.
- AI‑ready design for adding LLM summaries and alerting agents on top of the generated reports.

## How to run

1. Clone the repository:

   ```bash
   git clone https://github.com/mieszkoczupryniak/data-automation-service.git
   cd data-automation-service
Install dependencies (inside a virtual environment if you prefer):

bash
pip install -r requirements.txt
Run the HTTP JSON pipeline:

bash
python -m src.main --job http_pipeline
This will create:

data/raw_YYYYMMDD.json

reports/summary_YYYYMMDD.json

Run the real estate ETL pipeline:

bash
python -m src.main --job real_estate_etl
This will create:

reports/real_estate_summary_YYYYMMDD.json

Data pipeline (HTTP JSON)
This repository contains a small data pipeline that:

fetches sample JSON data from a public HTTP API,

stores the raw payload under data/raw_YYYYMMDD.json,

generates a daily summary report under reports/summary_YYYYMMDD.json.

The summary report currently includes:

record_count – total number of records fetched,

sample_ids – a small sample of record IDs to quickly inspect the dataset,

posts_by_user_1 – basic user-level aggregation example,

fetched_at and source – metadata for traceability.

In a future iteration this placeholder API can be replaced with real estate open‑data (Dubai / EU) to demonstrate a full external‑API ETL.

Real estate ETL
The project also includes a small real estate ETL pipeline:

Input: data/real_estate_transactions.csv with columns
transaction_id,date,price,city,district,area_m2,rooms

Processing: load rows, cast numeric fields, compute global stats and per‑district aggregates.

Output: reports/real_estate_summary_YYYYMMDD.json with:

record_count, avg_price, avg_price_per_m2, avg_area_m2,

city (example market),

by_district (record count, average price and price per m² per district).

Future AI extensions
Use an LLM to generate human‑readable daily summaries from the JSON reports (for managers or investors).

Add alerting logic or an AI agent that notifies when average price per m² crosses a threshold or unusual patterns appear.

Replace the placeholder HTTP API with real Dubai / EU open‑data sources and combine multiple markets in one report.

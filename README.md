# data-automation-service

Production-style data & automation service – fetch real-world data, store it, and generate simple reports. First portfolio project in my AI/infra journey.

## Goal

Build a small, realistic backend-style service that:
- pulls real data from a public API,
- stores it in a local database or CSV,
- generates simple analytical reports (daily/weekly),
- can be extended later with alerts, dashboards or ML.

## Tech stack (initial)

- Python 3.x
- `requests` for HTTP calls
- `pandas` for data processing
- SQLite or CSV for storage

## Roadmap

1. Basic project structure (src/, config, simple script).
2. Fetch data from one public API and save it locally.
3. Add simple reporting (aggregations, summaries).
4. Package the service as a CLI/cron-friendly script.
5. Add tests, logging and better error handling.
6. (Later) Docker + basic CI.

## Status

- [ ] Step 1 – project skeleton  
- [ ] Step 2 – basic data fetch and save  
- [ ] Step 3 – first report  
- [ ] Step 4 – packaging and cleanup

## Data pipeline

This repository contains a small data pipeline that:

- fetches sample JSON data from a public HTTP API,
- stores the raw payload under `data/raw_YYYYMMDD.json`,
- generates a daily summary report under `reports/summary_YYYYMMDD.json`.

The summary report currently includes:

- `record_count` – total number of records fetched,
- `sample_ids` – a small sample of record IDs to quickly inspect the dataset,
- `posts_by_user_1` – basic user-level aggregation example,
- `fetched_at` and `source` – metadata for traceability.

In the next iteration this fake API will be replaced with real estate open-data (Dubai / EU) to demonstrate a simple ETL pipeline for property transactions.

## Real estate ETL

The project also includes a small real estate ETL pipeline:

- Input: `data/real_estate_transactions.csv` with columns  
  `transaction_id,date,price,city,district,area_m2,rooms`.
- Processing: load rows, cast numeric fields, compute global stats and per‑district aggregates.
- Output: `reports/real_estate_summary_YYYYMMDD.json` with:
  - `record_count`, `avg_price`, `avg_price_per_m2`, `avg_area_m2`,
  - `city` (example market),
  - `by_district` (record count, average price and price per m² per district).

You can run the ETL with:

```bash
python scripts/real_estate_etl.py


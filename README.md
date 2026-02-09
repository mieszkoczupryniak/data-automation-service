# data-automation-service

Production-style data & automation service – fetch real-world data, store it, and generate simple reports. First portfolio project in my AI/infra journey.

## Features

- HTTP JSON pipeline that fetches data from a public API, stores raw daily snapshots and generates summary reports.
- Real estate ETL pipeline that reads CSV transactions, computes per‑district stats, average price and price per m².
- Simple CLI to choose which pipeline to run (`--job http_pipeline` or `--job real_estate_etl`).
- Clear project structure with separate `data/` and `reports/` folders, ready to plug into larger data/infra stacks.
- AI‑ready design for adding LLM summaries and alerting agents on top of the generated reports.

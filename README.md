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

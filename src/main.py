"""
data-automation-service

Small pipeline that fetches sample data from an HTTP API,
saves it to data/raw_YYYYMMDD.json and logs how many records were stored.
Later this will be wired to a real estate open-data API (Dubai / EU).
"""
import datetime
import json
from pathlib import Path

import requests


DATA_DIR = Path("data")


def fetch_real_estate_data() -> dict:
    """Fetch sample real estate data from an open API and return it as Python dict."""

    # Na początek użyjemy tymczasowego, prostego endpointu JSON jako „stand-in”
    # (prawdziwy endpoint z danymi nieruchomości z Dubai Pulse/DLD podmienimy w kolejnym kroku,
    # jak już przejdziemy przez cały pipeline).
    url = "https://jsonplaceholder.typicode.com/posts"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return {"fetched_at": datetime.datetime.utcnow().isoformat(), "data": data}


def save_data_to_file(payload: dict) -> Path:
    """Save fetched data to data/raw_YYYYMMDD.json and return the path."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().strftime("%Y%m%d")
    output_path = DATA_DIR / f"raw_{today}.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return output_path


def generate_report(payload: dict, output_dir: Path = Path("reports")) -> Path:
    """
    Generate a simple summary report from fetched data and save it to reports/summary_YYYYMMDD.json.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    data = payload.get("data", [])
    fetched_at = payload.get("fetched_at", "")

    record_count = len(data)

    report = {
        "fetched_at": fetched_at,
        "record_count": record_count,
        "source": "jsonplaceholder.typicode.com/posts",
    }

    date_tag = datetime.datetime.utcnow().strftime("%Y%m%d")
    report_path = output_dir / f"summary_{date_tag}.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report_path


def main() -> None:
    today = datetime.date.today()
    print(f"[data-automation-service] Running pipeline for {today}")

    payload = fetch_real_estate_data()
    raw_path = save_data_to_file(payload)

    num_records = len(payload.get("data", []))
    print(
        f"[data-automation-service] Saved {num_records} records "
        f"to {raw_path}"
    )

    report_path = generate_report(payload, Path("reports"))
    print(f"[data-automation-service] Generated report at {report_path}")


if __name__ == "__main__":
    main()

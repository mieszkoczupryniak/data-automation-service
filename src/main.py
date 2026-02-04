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


def main() -> None:
    today = datetime.date.today()
    print(f"[data-automation-service] Running pipeline for {today}")

    payload = fetch_real_estate_data()
    output_path = save_data_to_file(payload)

    num_records = len(payload.get("data", []))
    print(
        f"[data-automation-service] Saved {num_records} records "
        f"to {output_path}"
    )


if __name__ == "__main__":
    main()

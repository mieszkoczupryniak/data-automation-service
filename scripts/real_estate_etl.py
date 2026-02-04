"""
real_estate_etl.py

Simple ETL pipeline for real estate transaction data.

- Input:  CSV file under data/real_estate_transactions.csv
- Output: JSON summary report under reports/real_estate_summary_YYYYMMDD.json
"""

import csv
import datetime
import json
from pathlib import Path
from typing import List, Dict, Any


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


def load_transactions(csv_path: Path) -> List[Dict[str, Any]]:
    """
    Load real estate transactions from a CSV file.

    Expected columns:
    transaction_id,date,price,city,district,area_m2,rooms
    """
    transactions: List[Dict[str, Any]] = []

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                txn = {
                    "transaction_id": int(row["transaction_id"]),
                    "date": row["date"],
                    "price": float(row["price"]),
                    "city": row["city"],
                    "district": row["district"],
                    "area_m2": float(row["area_m2"]),
                    "rooms": int(row["rooms"]),
                }
                transactions.append(txn)
            except (KeyError, ValueError) as exc:
                print(f"[real-estate-etl] Skipping invalid row {row}: {exc}")

    return transactions


def compute_summary(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute simple summary statistics for the dataset.
    """
    total_tx = len(transactions)

    if total_tx == 0:
        return {
            "record_count": 0,
            "avg_price": None,
            "avg_price_per_m2": None,
            "avg_area_m2": None,
            "city": None,
            "by_district": {},
        }

    total_price = sum(t["price"] for t in transactions)
    total_area = sum(t["area_m2"] for t in transactions)

    avg_price = total_price / total_tx
    avg_area = total_area / total_tx
    avg_price_per_m2 = total_price / total_area if total_area > 0 else None

    by_district: Dict[str, Dict[str, float]] = {}
    for t in transactions:
        district = t["district"]
        if district not in by_district:
            by_district[district] = {
                "record_count": 0,
                "total_price": 0.0,
                "total_area_m2": 0.0,
            }

        by_district[district]["record_count"] += 1
        by_district[district]["total_price"] += t["price"]
        by_district[district]["total_area_m2"] += t["area_m2"]

    for district, stats in by_district.items():
        count = stats["record_count"]
        area_sum = stats["total_area_m2"]
        stats["avg_price"] = stats["total_price"] / count if count > 0 else None
        stats["avg_price_per_m2"] = (
            stats["total_price"] / area_sum if area_sum > 0 else None
        )

    example_city = transactions[0]["city"]

    return {
        "record_count": total_tx,
        "avg_price": avg_price,
        "avg_price_per_m2": avg_price_per_m2,
        "avg_area_m2": avg_area,
        "city": example_city,
        "by_district": by_district,
    }


def save_summary(summary: Dict[str, Any], reports_dir: Path) -> Path:
    """
    Save summary statistics to a JSON file under reports/.
    """
    reports_dir.mkdir(parents=True, exist_ok=True)
    date_tag = datetime.date.today().strftime("%Y%m%d")
    report_path = reports_dir / f"real_estate_summary_{date_tag}.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return report_path


def run_etl() -> None:
    """
    Run the end-to-end ETL for real estate transactions.
    """
    csv_path = DATA_DIR / "real_estate_transactions.csv"
    print(f"[real-estate-etl] Loading data from {csv_path}")

    if not csv_path.exists():
        print(
            "[real-estate-etl] ERROR: input CSV not found. "
            "Place real_estate_transactions.csv under data/."
        )
        return

    transactions = load_transactions(csv_path)
    print(f"[real-estate-etl] Loaded {len(transactions)} transactions")

    summary = compute_summary(transactions)
    report_path = save_summary(summary, REPORTS_DIR)

    print(f"[real-estate-etl] Saved summary report to {report_path}")


if __name__ == "__main__":
    run_etl()

import csv
from pathlib import Path

SUMMARY_FIELDS = [
    "run_id", "entity", "start_time", "end_time", "status", "failure_reason",
    "input_count", "valid_count", "rejected_count",
    "exact_duplicate_count", "probable_duplicate_count",
    "master_count", "review_queue_count",
]


def write_run_summary(path: Path, run_id, start_time, end_time,
                      status, failure_reason, metrics: dict) -> None:
    """Append one row per entity. File is kept across runs as run history."""
    path = Path(path)
    write_header = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        if write_header:
            writer.writeheader()
        for entity in ("customers", "products"):
            m = metrics.get(entity, {})
            writer.writerow({
                "run_id": run_id,
                "entity": entity,
                "start_time": start_time,
                "end_time": end_time,
                "status": status,
                "failure_reason": failure_reason,
                **{k: m.get(k, "") for k in SUMMARY_FIELDS[6:]},
            })

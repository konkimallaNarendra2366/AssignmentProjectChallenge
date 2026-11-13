from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def utc_now_iso() -> str:
    """ISO-8601 UTC timestamp, e.g. 2026-11-13T10:30:00+00:00"""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_run_id() -> str:
    """Readable, sortable run id, e.g. run_20261113T103000Z"""
    return "run_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass(frozen=True)
class Config:
    run_id: str
    data_dir: Path = BASE_DIR / "data"
    output_dir: Path = BASE_DIR / "output"
    customers_file: str = "customers.csv"
    products_file: str = "products.csv"
    fuzzy_threshold: int = 85      # use the value already in your probable_detector.py
    random_seed: int = 42

    @property
    def customers_path(self) -> Path:
        return self.data_dir / self.customers_file

    @property
    def products_path(self) -> Path:
        return self.data_dir / self.products_file


def load_config() -> Config:
    return Config(run_id=new_run_id())

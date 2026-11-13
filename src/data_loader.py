
import pandas as pd
from pathlib import Path


REQUIRED_CUSTOMER_COLUMNS = [
    "customer_id",
    "name",
    "email",
    "phone",
    "city",
    "updated_at",
    "source"
]

REQUIRED_PRODUCT_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "brand",
    "price",
    "updated_at",
    "source"
]


def load_and_validate(file_path, required_columns, id_column):
    """Load a CSV file and validate its structure."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {file_path}")

    df = pd.read_csv(file_path, dtype=str)

    if df.empty:
        raise ValueError(f"No records found in: {file_path}")

    # Remove accidental spaces from column names
    df.columns = df.columns.str.strip()

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {file_path.name}: {missing_columns}"
        )

    # Check missing IDs
    if df[id_column].isna().any():
        raise ValueError(f"Missing IDs found in {id_column}")

    # Check duplicate IDs
    if df[id_column].duplicated().any():
        raise ValueError(f"Duplicate IDs found in {id_column}")

    return df


def load_customers(file_path):
    return load_and_validate(
        file_path,
        REQUIRED_CUSTOMER_COLUMNS,
        "customer_id"
    )


def load_products(file_path):
    return load_and_validate(
        file_path,
        REQUIRED_PRODUCT_COLUMNS,
        "product_id"
    )

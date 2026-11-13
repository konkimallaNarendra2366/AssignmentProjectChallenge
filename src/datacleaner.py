
import re
import pandas as pd
from pathlib import Path


def normalize_text(value):
    """Remove extra spaces and convert text to lowercase."""
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_name(value):
    """Standardize names by removing unnecessary punctuation."""
    value = normalize_text(value)
    value = re.sub(r"[^a-z0-9 ]", "", value)
    return value


def normalize_phone(value):
    """Keep only digits in phone numbers."""
    if pd.isna(value):
        return ""

    return re.sub(r"\D", "", str(value))


def clean_customers(df):
    """Create normalized customer columns without changing raw data."""
    cleaned = df.copy()

    cleaned["normalized_name"] = cleaned["name"].apply(normalize_name)
    cleaned["normalized_email"] = cleaned["email"].apply(normalize_text)
    cleaned["normalized_phone"] = cleaned["phone"].apply(normalize_phone)
    cleaned["normalized_city"] = cleaned["city"].apply(normalize_text)

    cleaned["updated_at"] = pd.to_datetime(
        cleaned["updated_at"], errors="coerce"
    )

    return cleaned


def clean_products(df):
    """Create normalized product columns without changing raw data."""
    cleaned = df.copy()

    cleaned["normalized_product_name"] = (
        cleaned["product_name"].apply(normalize_text)
    )
    cleaned["normalized_brand"] = cleaned["brand"].apply(normalize_text)
    cleaned["normalized_category"] = (
        cleaned["category"].apply(normalize_text)
    )

    cleaned["price"] = pd.to_numeric(
        cleaned["price"], errors="coerce"
    )

    cleaned["updated_at"] = pd.to_datetime(
        cleaned["updated_at"], errors="coerce"
    )

    return cleaned


def save_cleaned_data(customers, products, output_dir):
    """Save cleaned datasets without overwriting original CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    customers.to_csv(
        output_dir / "cleaned_customers.csv", index=False
    )

    products.to_csv(
        output_dir / "cleaned_products.csv", index=False
    )

    print("Cleaned datasets saved successfully!")

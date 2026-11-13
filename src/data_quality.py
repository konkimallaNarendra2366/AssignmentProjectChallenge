
import pandas as pd
from pathlib import Path


def validate_customer_records(df):
    data = df.copy()

    data["rejection_reason"] = ""

    # Check missing customer IDs
    data.loc[
        data["customer_id"].isna(),
        "rejection_reason"
    ] += "Missing customer ID; "

    # Check missing names
    data.loc[
        data["name"].isna() |
        data["name"].astype(str).str.strip().eq(""),
        "rejection_reason"
    ] += "Missing name; "

    # Check invalid email format
    invalid_email = ~data["email"].astype(str).str.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        na=False
    )

    data.loc[
        invalid_email,
        "rejection_reason"
    ] += "Invalid email; "

    valid = data[data["rejection_reason"] == ""].copy()

    rejected = data[data["rejection_reason"] != ""].copy()

    return valid, rejected


def validate_product_records(df):
    data = df.copy()

    data["rejection_reason"] = ""

    # Check missing product IDs
    data.loc[
        data["product_id"].isna(),
        "rejection_reason"
    ] += "Missing product ID; "

    # Check missing product names
    data.loc[
        data["product_name"].isna() |
        data["product_name"].astype(str).str.strip().eq(""),
        "rejection_reason"
    ] += "Missing product name; "

    # Check invalid prices
    data["price"] = pd.to_numeric(
        data["price"], errors="coerce"
    )

    invalid_price = (
        data["price"].isna() |
        (data["price"] < 0)
    )

    data.loc[
        invalid_price,
        "rejection_reason"
    ] += "Invalid price; "

    valid = data[data["rejection_reason"] == ""].copy()

    rejected = data[data["rejection_reason"] != ""].copy()

    return valid, rejected


def save_quality_results(
    valid_customers,
    rejected_customers,
    valid_products,
    rejected_products,
    output_dir
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    valid_customers.to_csv(
        output_dir / "valid_customers.csv",
        index=False
    )

    rejected_customers.to_csv(
        output_dir / "rejected_customers.csv",
        index=False
    )

    valid_products.to_csv(
        output_dir / "valid_products.csv",
        index=False
    )

    rejected_products.to_csv(
        output_dir / "rejected_products.csv",
        index=False
    )

    print("\nDATA QUALITY RESULTS")
    print("Valid customers:", len(valid_customers))
    print("Rejected customers:", len(rejected_customers))
    print("Valid products:", len(valid_products))
    print("Rejected products:", len(rejected_products))

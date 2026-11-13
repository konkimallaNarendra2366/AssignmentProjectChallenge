
import pandas as pd
from pathlib import Path


def find_exact_duplicates(df, match_columns, id_column, prefix):
    data = df.copy()

    # Exclude records with missing matching information
    valid = data[match_columns].notna().all(axis=1)

    for column in match_columns:
        valid &= data[column].astype(str).str.strip().ne("")

    # Find records with matching values
    duplicate_data = data[valid].copy()

    duplicate_data["duplicate_count"] = (
        duplicate_data.groupby(match_columns)[id_column]
        .transform("size")
    )

    duplicate_data = duplicate_data[
        duplicate_data["duplicate_count"] > 1
    ].copy()

    # Assign a group ID to each duplicate group
    if not duplicate_data.empty:
        group_numbers = (
            duplicate_data.groupby(match_columns, sort=True)
            .ngroup() + 1
        )

        duplicate_data["duplicate_group_id"] = [
            f"{prefix}_{number:04d}"
            for number in group_numbers
        ]

    return duplicate_data


def detect_all_exact_duplicates(customers, products, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    customer_duplicates = find_exact_duplicates(
        customers,
        ["normalized_email", "normalized_phone"],
        "customer_id",
        "CUST"
    )

    product_duplicates = find_exact_duplicates(
        products,
        [
            "normalized_product_name",
            "normalized_brand",
            "normalized_category"
        ],
        "product_id",
        "PROD"
    )

    customer_duplicates.to_csv(
        output_dir / "exact_customer_duplicates.csv",
        index=False
    )

    product_duplicates.to_csv(
        output_dir / "exact_product_duplicates.csv",
        index=False
    )

    print("\nEXACT DUPLICATE DETECTION COMPLETED!")
    print("Customer duplicate records:", len(customer_duplicates))
    print("Product duplicate records:", len(product_duplicates))

    return customer_duplicates, product_duplicates

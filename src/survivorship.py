
import pandas as pd
from pathlib import Path


def select_best_record(group, id_column):
    records = group.copy()

    # Count non-empty fields in each record
    records["completeness_score"] = (
        records.notna().sum(axis=1)
    )

    # Prefer records with more complete information
    records = records.sort_values(
        by=["completeness_score", "updated_at"],
        ascending=[False, False],
        na_position="last"
    )

    return records.iloc[0]


def apply_survivorship(df, id_column, output_dir, file_prefix):
    df = df.copy()

    # Initially treat each record as its own group.
    # Exact duplicate groups will be handled together.
    df["survivorship_group"] = df[id_column].astype(str)

    # Group exact duplicates using their matching columns
    if id_column == "customer_id":
        match_columns = ["normalized_email", "normalized_phone"]
    else:
        match_columns = [
            "normalized_product_name",
            "normalized_brand",
            "normalized_category"
        ]

    valid = df[match_columns].notna().all(axis=1)

    for column in match_columns:
        valid &= df[column].astype(str).str.strip().ne("")

    duplicate_mask = df.loc[valid].duplicated(
        subset=match_columns,
        keep=False
    )

    duplicate_indices = df.loc[valid].index[duplicate_mask]

    duplicate_rows = df.loc[duplicate_indices]

    for _, group in duplicate_rows.groupby(match_columns):
        group_id = f"{file_prefix}_GROUP_{group.index.min()}"
        df.loc[group.index, "survivorship_group"] = group_id

    # Select the best record from each group
    winners = []

    for group_id, group in df.groupby("survivorship_group"):
        winner = select_best_record(group, id_column)
        winner["merged_record_ids"] = ", ".join(
            group[id_column].astype(str).tolist()
        )
        winner["survivorship_reason"] = (
            "Selected using completeness and latest update date"
            if len(group) > 1
            else "No duplicate detected; original record retained"
        )
        winners.append(winner)

    final_df = pd.DataFrame(winners)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    final_df.to_csv(
        output_dir / f"{file_prefix}_survivorship.csv",
        index=False
    )

    print(f"\n{file_prefix} survivorship completed!")
    print("Original records:", len(df))
    print("Master records:", len(final_df))

    return final_df


def run_survivorship(customers, products, output_dir):
    master_customers = apply_survivorship(
        customers,
        "customer_id",
        output_dir,
        "customer"
    )

    master_products = apply_survivorship(
        products,
        "product_id",
        output_dir,
        "product"
    )

    return master_customers, master_products

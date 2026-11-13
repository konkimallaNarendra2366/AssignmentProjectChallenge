
import pandas as pd
from pathlib import Path


def build_lineage(original_df, master_df, id_column, entity_type):
    lineage_records = []

    for _, master in master_df.iterrows():

        master_id = str(master[id_column])

        original_ids = str(
            master.get("merged_record_ids", master_id)
        ).split(",")

        for original_id in original_ids:
            original_id = original_id.strip()

            original_record = original_df[
                original_df[id_column].astype(str) == original_id
            ]

            source = ""

            if not original_record.empty:
                source = original_record.iloc[0]["source"]

            lineage_records.append({
                "entity_type": entity_type,
                "original_record_id": original_id,
                "master_record_id": master_id,
                "source": source,
                "record_status": (
                    "Selected as Master"
                    if original_id == master_id
                    else "Merged into Master"
                ),
                "survivorship_reason": master.get(
                    "survivorship_reason", ""
                )
            })

    return pd.DataFrame(lineage_records)


def save_lineage(
    customers,
    products,
    master_customers,
    master_products,
    output_dir
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    customer_lineage = build_lineage(
        customers,
        master_customers,
        "customer_id",
        "Customer"
    )

    product_lineage = build_lineage(
        products,
        master_products,
        "product_id",
        "Product"
    )

    all_lineage = pd.concat(
        [customer_lineage, product_lineage],
        ignore_index=True
    )

    all_lineage.to_csv(
        output_dir / "data_lineage.csv",
        index=False
    )

    print("\nDATA LINEAGE CREATED!")
    print("Customer lineage records:", len(customer_lineage))
    print("Product lineage records:", len(product_lineage))
    print("Total lineage records:", len(all_lineage))

    return all_lineage

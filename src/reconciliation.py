
import pandas as pd
from pathlib import Path


def reconcile_entity(
    entity_name,
    original_count,
    valid_count,
    rejected_count,
    master_count
):
    merged_count = valid_count - master_count

    input_check = (
        original_count == valid_count + rejected_count
    )

    master_check = (
        valid_count == master_count + merged_count
    )

    status = (
        "PASSED"
        if input_check and master_check and merged_count >= 0
        else "FAILED"
    )

    return {
        "entity": entity_name,
        "original_records": original_count,
        "valid_records": valid_count,
        "rejected_records": rejected_count,
        "master_records": master_count,
        "merged_away_records": merged_count,
        "input_reconciliation": input_check,
        "master_reconciliation": master_check,
        "overall_status": status
    }


def run_reconciliation(
    customers,
    products,
    valid_customers,
    valid_products,
    rejected_customers,
    rejected_products,
    master_customers,
    master_products,
    output_dir
):

    customer_result = reconcile_entity(
        "Customer",
        len(customers),
        len(valid_customers),
        len(rejected_customers),
        len(master_customers)
    )

    product_result = reconcile_entity(
        "Product",
        len(products),
        len(valid_products),
        len(rejected_products),
        len(master_products)
    )

    results = pd.DataFrame([
        customer_result,
        product_result
    ])

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results.to_csv(
        output_dir / "reconciliation_report.csv",
        index=False
    )

    print("\nDATA RECONCILIATION")
    print("=" * 40)
    print(results.to_string(index=False))

    if not (results["overall_status"] == "PASSED").all():
        raise ValueError(
            "Data reconciliation failed. Check record counts."
        )

    print("\nAll reconciliation checks passed!")

    return results

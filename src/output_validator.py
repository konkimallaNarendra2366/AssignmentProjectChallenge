
import pandas as pd
from pathlib import Path


def validate_outputs(output_dir):
    output_dir = Path(output_dir)

    required_files = [
        "cleaned_customers.csv",
        "cleaned_products.csv",
        "exact_customer_duplicates.csv",
        "exact_product_duplicates.csv",
        "probable_customer_duplicates.csv",
        "probable_product_duplicates.csv",
        "customer_survivorship.csv",
        "product_survivorship.csv",
        "review_queue.csv",
        "data_lineage.csv"
    ]

    print("\nFINAL OUTPUT VALIDATION")
    print("=" * 40)

    # Check whether all required files exist
    missing_files = [
        filename for filename in required_files
        if not (output_dir / filename).exists()
    ]

    if missing_files:
        print("Missing output files:", missing_files)
        raise FileNotFoundError("Some output files are missing.")

    print("All required output files are present.")

    # Load main datasets
    customers = pd.read_csv(output_dir / "cleaned_customers.csv")
    products = pd.read_csv(output_dir / "cleaned_products.csv")

    master_customers = pd.read_csv(
        output_dir / "customer_survivorship.csv"
    )
    master_products = pd.read_csv(
        output_dir / "product_survivorship.csv"
    )

    lineage = pd.read_csv(output_dir / "data_lineage.csv")
    review = pd.read_csv(output_dir / "review_queue.csv")

    # Validate master record IDs
    assert master_customers["customer_id"].is_unique
    assert master_products["product_id"].is_unique

    # Validate record counts
    assert len(master_customers) <= len(customers)
    assert len(master_products) <= len(products)

    # Validate lineage references
    assert lineage["original_record_id"].notna().all()
    assert lineage["master_record_id"].notna().all()

    # Display validation summary
    print("\nCUSTOMER VALIDATION")
    print("Original records:", len(customers))
    print("Master records:", len(master_customers))

    print("\nPRODUCT VALIDATION")
    print("Original records:", len(products))
    print("Master records:", len(master_products))

    print("\nLINEAGE RECORDS:", len(lineage))
    print("REVIEW QUEUE RECORDS:", len(review))

    print("\nAll validation checks passed!")

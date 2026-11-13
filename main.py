
from pathlib import Path

from src.data_loader import load_customers, load_products
from src.datacleaner import (
    clean_customers,
    clean_products,
    save_cleaned_data
)

from src.duplicate_detector import detect_all_exact_duplicates

from src.probable_detector import detect_probable_duplicates


from src.survivorship import run_survivorship



from src.review_queue import create_review_queue




from src.lineage import save_lineage




from src.output_validator import validate_outputs



from src.schema_validator import (
    validate_customers,
    validate_products
)



from src.data_quality import (
    validate_customer_records,
    validate_product_records,
    save_quality_results
)


from src.reconciliation import run_reconciliation
from src.config import load_config, utc_now_iso

from src.pipeline_logger import setup_logger
BASE_DIR = Path(__file__).resolve().parent

CUSTOMER_FILE = BASE_DIR / "data" / "customers.csv"
PRODUCT_FILE = BASE_DIR / "data" / "products.csv"


def main():

    print("SMARTDEDUP DATA PIPELINE")
    print("=" * 40)

    # Load data
    customers = load_customers(CUSTOMER_FILE)
    products = load_products(PRODUCT_FILE)
    # Schema validation
    print("\nStarting schema validation...")

    validate_customers(customers)
    validate_products(products)

    print("Customers loaded:", len(customers))
    print("Products loaded:", len(products))
    # Data quality validation
    print("\nStarting data quality validation...")

    valid_customers, rejected_customers = (
        validate_customer_records(customers)
    )

    valid_products, rejected_products = (
        validate_product_records(products)
    )

    save_quality_results(
        valid_customers,
        rejected_customers,
        valid_products,
        rejected_products,
        BASE_DIR / "output"
    )
    # Clean data
    print("\nStarting data cleaning...")

    cleaned_customers = clean_customers(valid_customers)
    cleaned_products = clean_products(valid_products)

    # Save data
    save_cleaned_data(
        cleaned_customers,
        cleaned_products,
        BASE_DIR / "output"
    )

    print("\nCleaning completed successfully!")

    # Step 5: Exact duplicate detection
    print("\nStarting exact duplicate detection...")

    customer_duplicates, product_duplicates = (
        detect_all_exact_duplicates(
            cleaned_customers,
            cleaned_products,
            BASE_DIR / "output"
        )
    )

    # Step 6: Probable duplicate detection
    print("\nStarting probable duplicate detection...")

    probable_customers, probable_products = (
        detect_probable_duplicates(
            cleaned_customers,
            cleaned_products,
            BASE_DIR / "output"
        )
    )
    #step6
    print("\nStarting survivorship process...")

    master_customers, master_products = run_survivorship(
        cleaned_customers,
        cleaned_products,
        BASE_DIR / "output"
    )

    # Step 7: Create review queue
    print("\nCreating review queue...")

    review_queue = create_review_queue(
        BASE_DIR / "output"
    )
    # Step 8: Data lineage
    print("\nStarting data lineage tracking...")

    lineage = save_lineage(
        cleaned_customers,
        cleaned_products,
        master_customers,
        master_products,
        BASE_DIR / "output"
    )
    print("\nStarting data reconciliation...")

    reconciliation_report = run_reconciliation(
        customers,
        products,
        valid_customers,
        valid_products,
        rejected_customers,
        rejected_products,
        master_customers,
        master_products,
        BASE_DIR / "output"
    )

    logger = setup_logger(BASE_DIR / "output")

    logger.info("SMARTDEDUP DATA PIPELINE STARTED")


    def main():
    cfg = load_config()
    start_time = utc_now_iso()
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Starting {cfg.run_id} at {start_time}")





    from src.config import load_config, utc_now_iso
from src.run_summary import write_run_summary

def main():
    cfg = load_config()
    start_time = utc_now_iso()
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    logger = get_logger(cfg.output_dir / "pipeline.log", cfg.run_id)

    metrics = {"customers": {}, "products": {}}
    status, failure_reason = "SUCCESS", ""

    try:
        logger.info("Run started")
        logger.info("Run finished successfully")
    except Exception as exc:
        status = "FAILED"
        failure_reason = f"{type(exc).__name__}: {exc}"
        logger.exception("Run failed")
        raise
    finally:
        write_run_summary(cfg.output_dir / "run_summary.csv", cfg.run_id,
                          start_time, utc_now_iso(), status, failure_reason, metrics)

    
    # Step 10: Final output validation
    validate_outputs(BASE_DIR / "output")



if __name__ == "__main__":
    main()

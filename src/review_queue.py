
import pandas as pd
from pathlib import Path


def create_review_queue(output_dir):

    output_dir = Path(output_dir)

    customer_file = (
        output_dir / "probable_customer_duplicates.csv"
    )

    product_file = (
        output_dir / "probable_product_duplicates.csv"
    )

    queue_file = output_dir / "review_queue.csv"

    review_items = []

    # Load customer candidates
    if customer_file.exists():
        customers = pd.read_csv(customer_file)

        if not customers.empty:
            customers["record_type"] = "Customer"
            review_items.append(customers)

    # Load product candidates
    if product_file.exists():
        products = pd.read_csv(product_file)

        if not products.empty:
            products["record_type"] = "Product"
            review_items.append(products)

    # Combine customer and product candidates
    if review_items:
        queue = pd.concat(
            review_items,
            ignore_index=True,
            sort=False
        )
    else:
        queue = pd.DataFrame(columns=[
            "record_type",
            "record_id_1",
            "record_id_2",
            "similarity_score"
        ])

    # Add review fields
    if "review_status" not in queue.columns:
        queue["review_status"] = "Pending"

    if "review_decision" not in queue.columns:
        queue["review_decision"] = ""

    if "reviewed_by" not in queue.columns:
        queue["reviewed_by"] = ""

    if "reviewed_at" not in queue.columns:
        queue["reviewed_at"] = ""

    # Preserve previous human decisions when rerunning
    if queue_file.exists():
        previous = pd.read_csv(queue_file)

        keys = [
            "record_type",
            "record_id_1",
            "record_id_2"
        ]

        if all(column in previous.columns for column in keys):
            previous = previous.drop_duplicates(
                subset=keys,
                keep="last"
            )

            # Add missing columns for older review queue files
            for column in [
                "review_status",
                "review_decision",
                "reviewed_by",
                "reviewed_at"
            ]:
                if column not in previous.columns:
                    previous[column] = ""

            previous = previous[
                keys + [
                    "review_status",
                    "review_decision",
                    "reviewed_by",
                    "reviewed_at"
                ]
                ]

            queue = queue.drop(
                columns=[
                    "review_status",
                    "review_decision",
                    "reviewed_by",
                    "reviewed_at"
                ],
                errors="ignore"
            )

            queue = queue.merge(
                previous,
                on=keys,
                how="left"
            )

            queue["review_status"] = (
                queue["review_status"]
                .replace(r"^\s*$", "Pending", regex=True)
                .fillna("Pending")
            )

            queue["review_decision"] = (
                queue["review_decision"].fillna("")
            )

            queue["reviewed_by"] = (
                queue["reviewed_by"].fillna("")
            )

            queue["reviewed_at"] = (
                queue["reviewed_at"].fillna("")
            )

    queue.to_csv(queue_file, index=False)

    print("\nHUMAN REVIEW QUEUE CREATED")
    print("Total candidates:", len(queue))
    print(
        "Pending:",
        (queue["review_status"] == "Pending").sum()
    )
    print(
        "Approved:",
        (queue["review_status"] == "Approved").sum()
    )
    print(
        "Rejected:",
        (queue["review_status"] == "Rejected").sum()
    )

    return queue


def update_review_decision(
    output_dir,
    record_type,
    record_id_1,
    record_id_2,
    decision,
    reviewer
):

    output_dir = Path(output_dir)
    queue_file = output_dir / "review_queue.csv"

    if not queue_file.exists():
        raise FileNotFoundError("Review queue not found.")

    decision = decision.strip().capitalize()

    if decision not in ["Approved", "Rejected"]:
        raise ValueError(
            "Decision must be Approved or Rejected."
        )

    queue = pd.read_csv(queue_file)

    mask = (
        (queue["record_type"] == record_type) &
        (queue["record_id_1"].astype(str) == str(record_id_1)) &
        (queue["record_id_2"].astype(str) == str(record_id_2))
    )

    if not mask.any():
        raise ValueError("Candidate pair not found.")

    from datetime import datetime, timezone

    queue.loc[mask, "review_status"] = decision
    queue.loc[mask, "review_decision"] = decision
    queue.loc[mask, "reviewed_by"] = reviewer
    queue.loc[mask, "reviewed_at"] = (
        datetime.now(timezone.utc).isoformat()
    )

    queue.to_csv(queue_file, index=False)

    print("Review decision updated successfully!")

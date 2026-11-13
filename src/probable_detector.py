
import pandas as pd
from pathlib import Path
from itertools import combinations
from collections import defaultdict
from rapidfuzz import fuzz


THRESHOLD = 75


def create_blocks(df, columns):
    """
    Group records using selected blocking columns.
    Records in different blocks are not compared.
    """
    blocks = defaultdict(list)

    for index, row in df.iterrows():
        key = tuple(
            str(row[column]).strip()
            if pd.notna(row[column]) else ""
            for column in columns
        )

        if all(value and value.lower() != "nan" for value in key):
            blocks[key].append(index)

    return blocks


def find_customer_candidates(customers):
    pairs = set()

    # Block 1: Same normalized phone
    phone_blocks = create_blocks(
        customers,
        ["normalized_phone"]
    )

    for records in phone_blocks.values():
        pairs.update(combinations(records, 2))

    # Block 2: Same email domain and city
    data = customers.copy()

    data["email_domain"] = (
        data["normalized_email"]
        .astype(str)
        .str.split("@")
        .str[-1]
    )

    email_blocks = create_blocks(
        data,
        ["email_domain", "normalized_city"]
    )

    for records in email_blocks.values():
        pairs.update(combinations(records, 2))

    return sorted(pairs)


def compare_customers(customers, pairs):
    results = []

    for index1, index2 in pairs:
        record1 = customers.loc[index1]
        record2 = customers.loc[index2]

        name_score = fuzz.ratio(
            record1["normalized_name"],
            record2["normalized_name"]
        )

        email_score = fuzz.ratio(
            record1["normalized_email"],
            record2["normalized_email"]
        )

        phone_score = (
            100
            if record1["normalized_phone"]
            == record2["normalized_phone"]
            else 0
        )

        similarity = (
            name_score * 0.60
            + email_score * 0.25
            + phone_score * 0.15
        )

        if similarity >= THRESHOLD:
            results.append({
                "record_id_1": record1["customer_id"],
                "record_id_2": record2["customer_id"],
                "name_similarity": round(name_score, 2),
                "email_similarity": round(email_score, 2),
                "phone_similarity": phone_score,
                "similarity_score": round(similarity, 2),
                "match_reason": "Customer field similarity",
                "review_status": "Pending Review"
            })

    return pd.DataFrame(results)


def find_product_candidates(products):
    pairs = set()

    # Compare products with the same brand and category
    blocks = create_blocks(
        products,
        ["normalized_brand", "normalized_category"]
    )

    for records in blocks.values():
        pairs.update(combinations(records, 2))

    return sorted(pairs)


def compare_products(products, pairs):
    results = []

    for index1, index2 in pairs:
        record1 = products.loc[index1]
        record2 = products.loc[index2]

        name_score = fuzz.ratio(
            record1["normalized_product_name"],
            record2["normalized_product_name"]
        )

        if name_score >= THRESHOLD:
            results.append({
                "record_id_1": record1["product_id"],
                "record_id_2": record2["product_id"],
                "name_similarity": round(name_score, 2),
                "similarity_score": round(name_score, 2),
                "match_reason": "Similar product names with same brand and category",
                "review_status": "Pending Review"
            })

    return pd.DataFrame(results)


def detect_probable_duplicates(
    customers,
    products,
    output_dir
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Customer probable duplicates
    customer_pairs = find_customer_candidates(customers)

    probable_customers = compare_customers(
        customers,
        customer_pairs
    )

    # Product probable duplicates
    product_pairs = find_product_candidates(products)

    probable_products = compare_products(
        products,
        product_pairs
    )

    # Save results
    probable_customers.to_csv(
        output_dir / "probable_customer_duplicates.csv",
        index=False
    )

    probable_products.to_csv(
        output_dir / "probable_product_duplicates.csv",
        index=False
    )

    print("\nADVANCED PROBABLE DUPLICATE DETECTION")
    print("Customer candidate pairs:", len(customer_pairs))
    print("Probable customer duplicates:", len(probable_customers))
    print("Product candidate pairs:", len(product_pairs))
    print("Probable product duplicates:", len(probable_products))

    return probable_customers, probable_products

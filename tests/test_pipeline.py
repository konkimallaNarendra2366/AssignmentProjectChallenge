
import pandas as pd

from src.datacleaner import clean_customers, clean_products
from src.duplicate_detector import find_exact_duplicates


def test_customer_cleaning():
    data = pd.DataFrame({
        "customer_id": ["C101"],
        "name": [" Narendra Kumar "],
        "email": [" NARENDRA@GMAIL.COM "],
        "phone": ["987-654-3210"],
        "city": [" Hyderabad "],
        "updated_at": ["2026-11-01"],
        "source": ["CRM"]
    })

    result = clean_customers(data)

    assert result.iloc[0]["normalized_name"] == "narendra kumar"
    assert result.iloc[0]["normalized_email"] == "narendra@gmail.com"
    assert result.iloc[0]["normalized_phone"] == "9876543210"


def test_exact_customer_duplicates():
    data = pd.DataFrame({
        "customer_id": ["C101", "C102", "C103"],
        "normalized_email": [
            "narendra@gmail.com",
            "narendra@gmail.com",
            "rahul@gmail.com"
        ],
        "normalized_phone": [
            "9876543210",
            "9876543210",
            "9123456780"
        ]
    })

    result = find_exact_duplicates(
        data,
        ["normalized_email", "normalized_phone"],
        "customer_id",
        "CUST"
    )

    assert len(result) == 2
    assert set(result["customer_id"]) == {"C101", "C102"}


def test_product_cleaning():
    data = pd.DataFrame({
        "product_id": ["P101"],
        "product_name": [" Laptop Model X "],
        "category": [" Electronics "],
        "brand": [" ABC "],
        "price": ["45000"],
        "updated_at": ["2026-11-01"],
        "source": ["Store"]
    })

    result = clean_products(data)

    assert result.iloc[0]["normalized_product_name"] == "laptop model x"
    assert result.iloc[0]["normalized_brand"] == "abc"
    assert result.iloc[0]["price"] == 45000


def test_product_duplicate_detection():
    data = pd.DataFrame({
        "product_id": ["P101", "P102", "P103"],
        "normalized_product_name": [
            "laptop model x",
            "laptop model x",
            "mobile model y"
        ],
        "normalized_brand": ["abc", "abc", "xyz"],
        "normalized_category": [
            "electronics",
            "electronics",
            "mobile"
        ]
    })

    result = find_exact_duplicates(
        data,
        [
            "normalized_product_name",
            "normalized_brand",
            "normalized_category"
        ],
        "product_id",
        "PROD"
    )

    assert len(result) == 2
    assert set(result["product_id"]) == {"P101", "P102"}


# Test 5: Empty customer input
def test_empty_customer_input():
    data = pd.DataFrame({
        "customer_id": pd.Series(dtype="object"),
        "normalized_email": pd.Series(dtype="object"),
        "normalized_phone": pd.Series(dtype="object")
    })

    result = find_exact_duplicates(
        data,
        ["normalized_email", "normalized_phone"],
        "customer_id",
        "CUST"
    )

    assert result.empty


# Test 6: Customer null values
def test_customer_null_values():
    data = pd.DataFrame({
        "customer_id": ["C101", "C102", "C103"],
        "normalized_email": ["narendra@gmail.com", None, "rahul@gmail.com"],
        "normalized_phone": ["9876543210", "9876543210", ""]
    })

    result = find_exact_duplicates(
        data,
        ["normalized_email", "normalized_phone"],
        "customer_id",
        "CUST"
    )

    assert result.empty


# Test 7: Empty customer matching fields
def test_customer_empty_matching_fields():
    data = pd.DataFrame({
        "customer_id": ["C101", "C102"],
        "normalized_email": ["", "   "],
        "normalized_phone": ["9876543210", "9876543210"]
    })

    result = find_exact_duplicates(
        data,
        ["normalized_email", "normalized_phone"],
        "customer_id",
        "CUST"
    )

    assert result.empty


# Test 8: Product records with missing brand
def test_product_missing_brand():
    data = pd.DataFrame({
        "product_id": ["P101", "P102"],
        "normalized_product_name": ["laptop model x", "laptop model x"],
        "normalized_brand": [None, None],
        "normalized_category": ["electronics", "electronics"]
    })

    result = find_exact_duplicates(
        data,
        ["normalized_product_name", "normalized_brand", "normalized_category"],
        "product_id",
        "PROD"
    )

    assert result.empty


# Test 9: Different product categories
def test_products_with_different_categories():
    data = pd.DataFrame({
        "product_id": ["P101", "P102"],
        "normalized_product_name": ["model x", "model x"],
        "normalized_brand": ["abc", "abc"],
        "normalized_category": ["electronics", "accessories"]
    })

    result = find_exact_duplicates(
        data,
        ["normalized_product_name", "normalized_brand", "normalized_category"],
        "product_id",
        "PROD"
    )

    assert result.empty



    


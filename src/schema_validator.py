
import pandas as pd


CUSTOMER_REQUIRED_COLUMNS = [
    "customer_id",
    "name",
    "email",
    "phone",
    "city",
    "updated_at",
    "source"
]

PRODUCT_REQUIRED_COLUMNS = [
    "product_id",
    "product_name",
    "brand",
    "category",
    "price",
    "updated_at",
    "source"
]


def validate_schema(df, required_columns, entity_name):

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{entity_name} is missing required columns: "
            f"{missing_columns}"
        )

    print(f"{entity_name} schema validation successful!")

    return True


def validate_customers(df):
    return validate_schema(
        df,
        CUSTOMER_REQUIRED_COLUMNS,
        "Customer"
    )


def validate_products(df):
    return validate_schema(
        df,
        PRODUCT_REQUIRED_COLUMNS,
        "Product"
    )

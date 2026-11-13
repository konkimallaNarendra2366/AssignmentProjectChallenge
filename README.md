# SmartDedup – Data Deduplication Pipeline

## 1. Project Overview

SmartDedup is a Python-based data engineering project designed to identify and manage duplicate customer and product records from multiple data sources.

The pipeline uses data validation, cleaning, exact matching, fuzzy matching, survivorship rules, review queues, reconciliation, and data lineage to improve data quality.

Its objective is to identify duplicate records, select reliable master records, preserve original record information, and generate validated output datasets.

## 2. Problem Statement

Customer and product information may be stored multiple times across different systems.

Duplicate records can cause:
- Incorrect customer information
- Repeated product entries
- Inconsistent business reports
- Poor data quality

SmartDedup addresses these problems through a structured data deduplication pipeline.

## 3. Project Objectives

- Load and validate customer and product datasets.
- Clean and normalize input data.
- Identify exact duplicate records.
- Identify probable duplicate records using fuzzy matching.
- Apply survivorship rules to select master records.
- Generate a review queue for probable duplicates.
- Maintain data lineage.
- Reconcile original and final record counts.
- Validate generated output files.

## 4. Technologies Used

- Python
- Pandas
- RapidFuzz
- Pytest
- CSV

## 5. Project Architecture

```text
Input CSV Files
      |
      v
Data Loading
      |
      v
Schema Validation
      |
      v
Data Quality Validation
      |
      v
Data Cleaning
      |
      v
Duplicate Detection
   /          \
Exact       Probable
Matching    Matching
   \          /
      v
Survivorship
      |
      v
Review Queue and Data Lineage
      |
      v
Reconciliation
      |
      v
Output Validation
      |
      v
Final Output Files
```

## 6. Project Structure

```text
AssignmentProject/
|
|-- data/
|   |-- customers.csv
|   |-- products.csv
|
|-- docs/
|
|-- output/
|   |-- cleaned_customers.csv
|   |-- cleaned_products.csv
|   |-- valid_customers.csv
|   |-- valid_products.csv
|   |-- rejected_customers.csv
|   |-- rejected_products.csv
|   |-- exact_customer_duplicates.csv
|   |-- exact_product_duplicates.csv
|   |-- probable_customer_duplicates.csv
|   |-- probable_product_duplicates.csv
|   |-- customer_survivorship.csv
|   |-- product_survivorship.csv
|   |-- review_queue.csv
|   |-- data_lineage.csv
|   |-- reconciliation_report.csv
|   |-- pipeline.log
|
|-- src/
|   |-- data_loader.py
|   |-- schema_validator.py
|   |-- data_quality.py
|   |-- datacleaner.py
|   |-- duplicate_detector.py
|   |-- probable_detector.py
|   |-- survivorship.py
|   |-- review_queue.py
|   |-- lineage.py
|   |-- output_validator.py
|   |-- reconciliation.py
|   |-- pipeline_logger.py
|
|-- tests/
|   |-- test_pipeline.py
|
|-- generate_data.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## 7. Pipeline Implementation

### Step 1: Data Loading
Loads customer and product CSV datasets.

### Step 2: Schema Validation
Checks the required dataset structure and columns.

### Step 3: Data Quality Validation
Identifies invalid or incomplete records and separates valid and rejected records.

### Step 4: Data Cleaning
Normalizes names, emails, phone numbers, product names, brands, and categories.

### Step 5: Exact Duplicate Detection
Identifies records with matching customer email and phone or matching product name, brand, and category.

### Step 6: Probable Duplicate Detection
Uses RapidFuzz similarity scores to identify potentially matching records.

### Step 7: Survivorship Rules
Selects master records based on data completeness and the latest update date.

### Step 8: Review Queue
Stores probable duplicate pairs for manual review.

### Step 9: Data Lineage
Tracks original record IDs, master record IDs, source information, and merge status.

### Step 10: Reconciliation
Compares original, valid, rejected, and master record counts to verify record consistency.

### Step 11: Output Validation
Checks required output files, master record uniqueness, record counts, and basic lineage references.

## 8. How to Run the Project

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AssignmentProject
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Generate sample datasets

```bash
python generate_data.py
```

This generates reproducible customer and product sample CSV files inside the `data/` folder.

### Step 6: Run the pipeline

```bash
python main.py
```

### Step 7: Run automated tests

```bash
python -m pytest tests -v
```

## 9. Output Files

The pipeline generates the following outputs inside the `output/` folder:

- Cleaned customer and product datasets.
- Valid customer and product records.
- Rejected customer and product records.
- Exact customer and product duplicate results.
- Probable customer and product duplicate results.
- Customer and product survivorship datasets.
- Review queue.
- Data lineage report.
- Reconciliation report.
- Pipeline execution log.

## 10. Key Features

- Automated data cleaning and validation.
- Exact duplicate identification.
- Fuzzy matching using RapidFuzz.
- Survivorship rules for master record selection.
- Review queue generation.
- Data lineage tracking.
- Record count reconciliation.
- Automated testing and output validation.
- Reproducible sample data generation.

## 11. Assumptions and Limitations

- Input datasets are provided in CSV format.
- Customer and product datasets follow predefined schemas.
- Fuzzy matching depends on configured similarity rules and thresholds.
- Probable duplicate pairs may require manual review.
- The pipeline currently processes local datasets rather than a live database.
- The sample data generator creates synthetic records for demonstration and testing.

## 12. Future Enhancements

- Add configurable source priority rules.
- Improve fuzzy matching with additional matching fields.
- Implement a dedicated human approval and rejection workflow.
- Support larger datasets with scalable processing.
- Add detailed data quality reports and dashboards.

## 13. Conclusion

SmartDedup provides a structured approach to customer and product data deduplication. It combines data quality validation, duplicate identification, survivorship rules, review workflows, reconciliation, and lineage tracking to produce more reliable master datasets.
# SmartDedup – Smart Data Deduplication Pipeline

## Final Project Submission Documentation

---

## 1. Project Overview

SmartDedup is a Python-based data engineering pipeline designed to identify and handle duplicate customer and product records.

The pipeline performs data ingestion, schema validation, data quality checks, cleaning, exact duplicate detection, probable duplicate detection, survivorship, human review queue generation, data lineage tracking, reconciliation, and output validation.

The main objective is to improve data consistency and produce reliable master datasets while maintaining traceability of original records.

**Execution environment:** Local machine
**Input format:** CSV
**Output format:** CSV and log files

## 2. Business Context and Problem Statement

Customer and product datasets can contain duplicate records, inconsistent values, spelling variations, missing information, and formatting differences.

These issues can affect data quality and create problems for downstream analytical systems.

The SmartDedup pipeline addresses these challenges by:

- Identifying exact duplicate records.
- Detecting probable duplicates using fuzzy matching.
- Applying survivorship rules to select master records.
- Maintaining a human review queue for duplicate candidates.
- Tracking the relationship between original and master records.
- Reconciling input and output record counts.

The solution is designed as a reproducible local batch-processing pipeline.

## 3. Project Objectives

The primary objectives are:

1. Load customer and product datasets.
2. Validate input schemas and data quality.
3. Clean and normalize records.
4. Identify exact duplicate records.
5. Identify probable duplicate records.
6. Select master records using survivorship logic.
7. Generate a human review queue.
8. Maintain data lineage.
9. Reconcile original and processed records.
10. Validate generated output files.

## 4. Technologies Used

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python     | Pipeline implementation            |
| Pandas     | Data processing and transformation |
| RapidFuzz  | Fuzzy matching                     |
| Pytest     | Automated testing                  |
| CSV        | Input and output storage           |
| Logging    | Execution logging                  |
| Git        | Version control                    |
| GitHub     | Source code repository             |
| PyCharm    | Development environment            |

## 5. System Architecture

The pipeline follows a modular processing architecture.

Source CSV files
↓
Data Loading
↓
Schema Validation
↓
Data Quality Validation
↓
Data Cleaning and Normalization
↓
Exact Duplicate Detection
↓
Probable Duplicate Detection
↓
Survivorship and Master Record Selection
↓
Human Review Queue
↓
Data Lineage Tracking
↓
Data Reconciliation
↓
Final Output Validation
↓
Generated CSV Files and Pipeline Logs

Each processing stage is implemented in a separate Python module to improve readability and maintainability.

## 6. Project Structure

```text
AssignmentProjectChallenge/
│
├── data/
│   ├── customers.csv
│   └── products.csv
│
├── output/
│   ├── cleaned_customers.csv
│   ├── cleaned_products.csv
│   ├── valid_customers.csv
│   ├── valid_products.csv
│   ├── rejected_customers.csv
│   ├── rejected_products.csv
│   ├── exact_customer_duplicates.csv
│   ├── exact_product_duplicates.csv
│   ├── probable_customer_duplicates.csv
│   ├── probable_product_duplicates.csv
│   ├── customer_survivorship.csv
│   ├── product_survivorship.csv
│   ├── review_queue.csv
│   ├── data_lineage.csv
│   ├── reconciliation_report.csv
│   └── pipeline.log
│
├── src/
│   ├── data_loader.py
│   ├── schema_validator.py
│   ├── data_quality.py
│   ├── datacleaner.py
│   ├── duplicate_detector.py
│   ├── probable_detector.py
│   ├── survivorship.py
│   ├── review_queue.py
│   ├── lineage.py
│   ├── reconciliation.py
│   ├── output_validator.py
│   └── pipeline_logger.py
│
├── tests/
│   ├── test_pipeline.py
│   └── test_setup.py
│
├── main.py
├── genratedata.py
├── requirements.txt
├── README.md
├── .gitignore
└── FINAL_SUBMISSION_DOCUMENTATION.md
```

Note: This structure reflects the project files currently committed to GitHub. Update it if filenames change.

## 7. Data Entities and Data Dictionary

### Customer entity

Represents an individual customer record.

Important fields include:

- `customer_id`: Customer record identifier.
- Customer name and contact information: Used for identification and matching.
- Other source attributes: Used during cleaning, comparison, and survivorship.

### Product entity

Represents an individual product record.

Important fields include:

- `product_id`: Product record identifier.
- Product name: Used for matching.
- Brand: Used as a product attribute.
- Category: Used for product classification and matching.
- Other source attributes: Used during cleaning and survivorship.

### Output entities

| Output                | Description                                        |
| --------------------- | -------------------------------------------------- |
| Valid records         | Records that pass data quality validation          |
| Rejected records      | Records that fail validation                       |
| Exact duplicates      | Records identified through exact matching          |
| Probable duplicates   | Similar records identified through fuzzy matching  |
| Survivorship datasets | Selected master records                            |
| Review queue          | Duplicate candidates requiring review              |
| Data lineage          | Relationships between original and master records  |
| Reconciliation report | Summary of record counts and reconciliation checks |

**Schema note:** Refer to the actual CSV headers and validation rules in the source code for the complete field-level schema, data types, nullability, and matching keys. Do not assume every field is mandatory.

## 8. Core Implementation Details

### 8.1 Data Loading

The pipeline loads customer and product CSV files from the data directory.

### 8.2 Schema Validation

The schema validator checks whether input datasets contain the expected structure and required columns.

### 8.3 Data Quality Validation

The data quality module checks records for missing or invalid information according to the implemented rules.

Valid and rejected records are handled separately.

### 8.4 Data Cleaning

The cleaning module normalizes selected fields and prepares records for duplicate detection.

### 8.5 Exact Duplicate Detection

Exact duplicate detection identifies records that have identical values in the configured matching columns.

### 8.6 Probable Duplicate Detection

RapidFuzz is used to compare similar text values and identify potential duplicate records.

The results are candidate matches, not automatically confirmed duplicates.

### 8.7 Survivorship

The survivorship module selects master records according to implemented selection rules.

The objective is to reduce duplicate records while retaining a consistent representation of each entity.

### 8.8 Human Review Queue

Probable duplicate candidates are stored in a review queue.

The queue includes review-related fields such as:

- `review_status`
- `review_decision`
- `reviewed_by`
- `reviewed_at`

The review process supports decisions such as Pending, Approved, and Rejected.

### 8.9 Data Lineage

Data lineage maintains the relationship between original records and master records.

This makes it possible to trace how records were consolidated.

### 8.10 Data Reconciliation

Reconciliation compares original, valid, rejected, and master record counts.

The purpose is to identify unexplained differences in the processing results.

### 8.11 Output Validation

The output validator checks the presence of required output files, master record uniqueness, record counts, and lineage references.

## 9. Technical Decisions and Trade-offs

### Python and Pandas

Python and Pandas were selected because they provide suitable tools for structured data processing, transformation, and validation.

### RapidFuzz

RapidFuzz was selected to identify probable duplicates where exact string matching is insufficient.

The trade-off is that fuzzy matching can generate false positives and false negatives.

### CSV Storage

CSV was selected because the assignment can be completed locally without requiring database infrastructure.

The trade-off is that CSV is less suitable than a database for concurrent updates and large production workloads.

### Modular Design

The pipeline is separated into modules so that validation, cleaning, matching, survivorship, and reconciliation can be maintained independently.

### Human Review

A review queue is used to avoid treating every probable duplicate as a confirmed duplicate.

This improves transparency but requires review decisions for uncertain candidates.

## 10. Assumptions

- Customer and product data are provided as CSV files.
- Input files follow the expected schemas.
- Sample datasets are synthetic.
- Matching uses configured fields and similarity thresholds.
- Survivorship follows the rules implemented in the project.
- The pipeline is designed for local batch processing.
- Human review is needed for uncertain duplicate candidates.

## 11. Testing Approach

The project contains automated tests using Pytest.

The testing scenarios include:

- Data cleaning.
- Exact duplicate detection.
- Empty customer input.
- Customer null values.
- Empty matching fields.
- Missing product brand information.
- Products with different categories.

The pipeline was also executed using generated customer and product datasets.

### Observed execution results

| Metric              | Customers | Products |
| ------------------- | --------: | -------: |
| Original records    |     2,000 |    2,000 |
| Valid records       |     2,000 |    2,000 |
| Rejected records    |         0 |        0 |
| Master records      |     1,788 |    1,789 |
| Merged-away records |       212 |      211 |

The reconciliation checks passed for both entities in the reported execution.

The output validator reported that all required output files were present.

**Testing evidence:** The above figures are from a development execution. Rerun the pipeline and test suite in a clean environment before treating them as final submission evidence.

## 12. Known Limitations and Future Improvements

The current implementation is a local batch-processing solution.

Potential improvements include:

- Configurable processing parameters.
- Stronger run-level operational metrics.
- Explicit run identifiers and execution timestamps.
- Safe reruns and idempotent publishing.
- Retry and restart support.
- More malformed-input and schema-change tests.
- Performance benchmarking on larger datasets.
- Database integration for production-scale processing.
- More advanced survivorship rules.
- Improved review queue reporting.

These are possible future improvements and should not be described as completed features unless implemented and tested.

## 13. AI / LLM Usage Disclosure

AI tools, including ChatGPT, were used as development assistance during this project.

AI assistance supported understanding assignment requirements, learning Python and data engineering concepts, reviewing code, troubleshooting errors, and preparing documentation.

AI-generated suggestions were treated as guidance and were reviewed before being applied.

### Where AI accelerated development

- Breaking the assignment into manageable development stages.
- Explaining Python, Pandas, and RapidFuzz concepts.
- Suggesting modular project organization.
- Helping understand duplicate detection and survivorship.
- Explaining data lineage and reconciliation.
- Reviewing code and troubleshooting execution errors.
- Suggesting test scenarios.
- Preparing README and submission documentation.

### Where I relied heavily on AI

AI assistance was particularly useful for understanding fuzzy matching, probable duplicate generation, survivorship logic, review queue handling, lineage, reconciliation, and output validation.

### My personal contribution

I personally created and managed the project in PyCharm, organized its files, generated sample datasets, integrated the modules, executed the pipeline, reviewed the output files, and pushed the source code to GitHub.

I reviewed AI suggestions, applied changes, investigated reported errors, and examined pipeline execution and reconciliation results.

I do not claim that every implementation idea originated independently; AI was used as a development assistant.

## 14. Prompt History

The following is a summary of the main prompt topics used during development. It is not a verbatim transcript of every conversation.

1. Help me understand the data deduplication assignment and divide it into development stages.
2. Guide me step by step to create the project in PyCharm.
3. Help generate reproducible customer and product sample datasets.
4. Explain and implement schema validation.
5. Help implement data quality checks and rejected records.
6. Explain data cleaning and normalization using Pandas.
7. Help implement exact duplicate detection.
8. Explain probable duplicate detection using RapidFuzz.
9. Help implement survivorship and master record selection.
10. Help create and troubleshoot the human review queue.
11. Help implement data lineage.
12. Help implement data reconciliation.
13. Review the output validation code.
14. Help interpret execution results and troubleshoot errors.
15. Help prepare README and GitHub submission documentation.

For a complete prompt history, retain or export the actual ChatGPT conversation history. This section is a summary and must not be presented as the verbatim prompt transcript.

## 15. Installation and Execution

### Prerequisites

- Python installed.
- Git installed.
- Internet access for installing dependencies.

### Clone the repository

```bash
git clone https://github.com/konkimallaNarendra2366/AssignmentProjectChallenge.git
cd AssignmentProjectChallenge
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate on Windows

```powershell
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Generate sample data

The currently committed generator filename is `genratedata.py`.

```bash
python genratedata.py
```

If you rename it to `generate_data.py`, update this command and the project structure accordingly.

### Execute the pipeline

```bash
python main.py
```

### Run automated tests

```bash
python -m pytest tests -v
```

### Verify outputs

Check the generated CSV files in the `output/` directory and inspect:

- `reconciliation_report.csv`
- `review_queue.csv`
- `data_lineage.csv`
- `pipeline.log`

## 16. GitHub Repository

**Repository URL:**

[https://github.com/konkimallaNarendra2366/AssignmentProjectChallenge](https://github.com/konkimallaNarendra2366/AssignmentProjectChallenge)

The repository contains the project source code, tests, sample data, generated output files, dependencies, and project documentation.



## 17. Conclusion

SmartDedup demonstrates a modular data engineering solution for customer and product deduplication.

It com

bines data validation, cleaning, exact matching, fuzzy matching, survivorship, human review, lineage, and reconciliation.

The solution focuses on data quality, traceability, maintainability, and reproducibility.

AI tools supported the development process, while code review, project integration, execution, and validation were performed as part of the development work.

The project provides a foundation for further improvements in operational observability, idempotency, recovery, and large-scale data processing.

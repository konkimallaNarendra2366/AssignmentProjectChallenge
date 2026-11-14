# SmartDedup – Smart Data Deduplication Pipeline

A Python batch pipeline that finds exact and probable duplicates in customer and product records, applies transparent survivorship rules, keeps lineage back to the source records, and produces merged (master) records plus a human review queue.

- **Author:** Narendra Konkimalla
- **Environment:** local machine (Python 3, no external services)
- **Input / output:** CSV in, CSV and log files out

---

## 1. Quick start

```bash
git clone https://github.com/konkimallaNarendra2366/AssignmentProjectChallenge.git
cd AssignmentProjectChallenge

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

python genratedata.py           # generate synthetic sample data into data/
python main.py                  # run the pipeline, results go to output/
python -m pytest tests -v       # run automated tests
```



---

## 2. Business problem

Customer and product data often contains exact duplicates, spelling variations, missing values and formatting differences. These hurt downstream analytics.

SmartDedup:

1. Validates and cleans the input.
2. Finds exact duplicates and probable (fuzzy) duplicates.
3. Picks a surviving master record using explicit rules.
4. Sends uncertain matches to a review queue instead of merging them silently.
5. Records which source records were merged into which master (lineage).
6. Reconciles input counts against output counts.

---

## 3. Architecture / data flow

```
data/customers.csv, data/products.csv
        |
        v
  Data loading  (data_loader.py)
        |
        v
  Schema validation  (schema_validator.py)
        |
        v
  Data-quality checks  (data_quality.py)  ---->  rejected_*.csv
        |
        v
  Cleaning and normalisation  (datacleaner.py)
        |
        v
  Exact duplicate detection  (duplicate_detector.py)
        |
        v
  Probable duplicate detection, RapidFuzz  (probable_detector.py)
        |
        v
  Survivorship / master selection  (survivorship.py)
        |
        +--> Review queue  (review_queue.py)
        +--> Lineage  (lineage.py)
        |
        v
  Reconciliation  (reconciliation.py)
        |
        v
  Output validation  (output_validator.py)
        |
        v
  output/*.csv  +  output/pipeline.log
```


---

## 4. Project structure

```
AssignmentProjectChallenge/
├── data/                    input CSVs (synthetic)
│   ├── customers.csv
│   └── products.csv
├── output/                  generated results and logs
├── src/                     pipeline modules (one per stage)
├── tests/
│   ├── test_pipeline.py
│   └── test_setup.py
├── main.py                  pipeline entry point
├── genratedata.py           synthetic data generator
├── requirements.txt
└── README.md
```

---

## 5. Data dictionary



### 5.1 Input: `customers.csv`

| Column | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | string | yes | Source record identifier, should be unique per source row |
| `name` | string | yes | Used for matching |
| `email` | string | no | Used for matching, normalised to lower case |
| `phone` | string | no | Used for matching, digits only after cleaning |
| `city` | string | no | Descriptive attribute |

### 5.2 Input: `products.csv`

| Column | Type | Required | Notes |
|---|---|---|---|
| `product_id` | string | yes | Source record identifier |
| `product_name` | string | yes | Used for matching |
| `brand` | string | no | Missing brand is allowed and handled |
| `category` | string | yes | Products in different categories are not matched as duplicates |

### 5.3 Output files

| File | Description |
|---|---|
| `valid_customers.csv`, `valid_products.csv` | Records that passed validation |
| `rejected_customers.csv`, `rejected_products.csv` | Records that failed validation, kept for traceability |
| `cleaned_customers.csv`, `cleaned_products.csv` | Normalised records |
| `exact_customer_duplicates.csv`, `exact_product_duplicates.csv` | Exact duplicate groups |
| `probable_customer_duplicates.csv`, `probable_product_duplicates.csv` | Fuzzy-match candidate pairs |
| `customer_survivorship.csv`, `product_survivorship.csv` | Merged master records |
| `review_queue.csv` | Probable duplicates awaiting a human decision |
| `data_lineage.csv` | Source record to master record mapping |
| `reconciliation_report.csv` | Input / valid / rejected / master / merged-away counts |
| `run_summary.csv` | One row per run: run_id, start / end time, counts, status |
| `pipeline.log` | Execution log |

### 5.4 Review queue fields

`review_status`, `review_decision`, `reviewed_by`, `reviewed_at`. Status values: `Pending`, `Approved`, `Rejected`.

---

## 6. Naming conventions

- Tables and columns use `snake_case`.
- Timestamps use ISO-8601.
- Each run carries a `run_id`; output rows carry `source_file` where applicable.
- Master IDs are generated deterministically from the source data so the same input gives the same IDs.

---

## 7. How it works

**Validation.** The schema validator checks expected columns. The data-quality module checks required fields and basic format rules. Failing rows go to `rejected_*.csv` and are not dropped silently.

**Cleaning.** Text fields are trimmed and normalised (case, whitespace, punctuation) so that matching compares like with like.

**Exact duplicates.** Records with identical values in the configured matching columns are grouped together.

**Probable duplicates.** RapidFuzz computes text similarity on the matching fields. Pairs above the similarity threshold become *candidates*, not confirmed duplicates. The threshold is set in code.

**Survivorship.** One record per duplicate group is chosen as the master using explicit, deterministic rules defined in `survivorship.py`.

**Review queue.** Uncertain candidates are written to `review_queue.csv` with status `Pending`.

**Lineage.** `data_lineage.csv` records which source records were merged into which master record.

**Reconciliation.** `input = valid + rejected`, and `valid = master records + merged-away records`. Differences are reported.

**Run metrics.** Each run produces a `run_id`, start and end times, input / output / rejected counts and a status in `run_summary.csv`. Failures are logged with a reason.

---

## 8. Testing

Run with `python -m pytest tests -v`.

Covered scenarios:

- data cleaning
- exact duplicate detection
- empty customer input
- null values in customer data
- empty matching fields
- missing product brand
- products in different categories (must not merge)

### Sample run results (development execution)

| Metric | Customers | Products |
|---|---|---|
| Original records | 2,000 | 2,000 |
| Valid records | 2,000 | 2,000 |
| Rejected records | 0 | 0 |
| Master records | 1,788 | 1,789 |
| Merged-away records | 212 | 211 |

Reconciliation checks passed for both entities, and the output validator found all required output files.

---

## 9. Design decisions and trade-offs

| Decision | Why | Trade-off |
|---|---|---|
| Python + pandas | Simple, readable data processing | Holds data in memory, so not suited to very large volumes |
| RapidFuzz | Fast fuzzy string matching | Can produce false positives and false negatives |
| CSV storage | Runs locally with no infrastructure | No concurrent writes, no transactions |
| One module per stage | Each stage is easy to test and change | More files to navigate |
| Review queue for probable matches | Avoids merging uncertain records automatically | Needs a human decision |

---

## 10. Assumptions

- Input is CSV and broadly follows the expected schema.
- Sample data is synthetic and generated by `genratedata.py`.
- Matching uses configured fields and a similarity threshold.
- Processing is local and single-run batch.
- Output files are overwritten on each run.

---

## 11. Known limitations

These are **not** implemented yet:

- Formal idempotent publishing, retry, restart and backfill handling.
- Handling of late-arriving or out-of-order data.
- Tests for malformed rows, unexpected schema changes, partial failure and invalid reference keys.
- Labelled invalid records and a separate expected-answer file.
- Large-scale run (100,000+ records) and a performance measurement.
- Database storage; CSV is used instead.

## 12. Possible next steps

1. Add safe reruns (deterministic run handling and replace-on-rerun publishing).
2. Add a generator option for 100,000+ rows with a fixed random seed and labelled invalid records.
3. Add a validation report that compares results against the expected labels (precision and recall).
4. Measure runtime on the large dataset and apply one optimisation, for example blocking on a key before fuzzy matching.
5. Add the missing edge-case tests listed above.
6. Move storage to MySQL for production-style use.

---

## 13. AI usage disclosure

I used AI tools (ChatGPT and Claude) as development assistants for understanding the assignment, learning Python and data-engineering concepts, reviewing code, troubleshooting errors and preparing documentation. I reviewed the suggestions, applied the changes myself in PyCharm, generated the data, ran the pipeline and tests, checked the outputs and pushed the code to GitHub. I do not claim every idea originated independently.

---

## 14. Repository

https://github.com/konkimallaNarendra2366/AssignmentProjectChallenge

# Power BI Data Preparation & Pipeline Specification

## 1. Architecture: Single Source of Cleaning Truth

In production analytics, conflicting data-cleaning logic between Python and Power BI creates reporting discrepancies. This project enforces a **Single Source of Truth** architecture:

```
Raw CSV / Excel Upload 
         │
         ▼
modules/data_processor.py (Python / Pandas)
  ├── 1. Column normalization (lowercase, stripped, snake_case)
  ├── 2. Date parsing (errors='coerce') + dropna
  ├── 3. Rating numeric coercion + dropna + .clip(1, 5)
  ├── 4. Categorical whitespace stripping & missing fill ("Unknown")
  ├── 5. Deterministic sentiment derivation (4-5: Positive, 3: Neutral, 1-2: Negative)
  ├── 6. Deduplication on composite key (feedback_id, customer_name, date, text)
  └── 7. Chronological sorting
         │
         ▼
modules/power_bi_export.py
  ├── Generates single flat analytical table (cleaned_customer_feedback.csv/.xlsx)
  └── Generates Star Schema tables (Fact_CustomerFeedback + Dim_*)
         │
         ▼
Power BI Reporting Layer (Import Mode / Power Query)
```

Power BI does **not** re-implement cleaning rules. Power Query simply loads the validated dataset and assigns strong types.

---

## 2. Validation & Business Rules

### Rule 1: Date Integrity
- **Logic:** Raw strings like `"2025/01/15"`, `"15-01-2025"`, or `"InvalidDate"` are parsed using `pd.to_datetime(errors='coerce')`.
- **Handling:** Unparseable dates become `NaT` and are dropped (`dropna(subset=['date'])`).
- **Power BI Guarantee:** Guarantees a continuous date timeline without blank dates that would break Time Intelligence DAX functions (`DATESMTD`, `PREVIOUSMONTH`).

### Rule 2: Rating Boundary Enforcement
- **Logic:** Customer ratings are converted to numeric. Any typos such as `-1` or `98` are clamped using `.clip(1, 5).astype(int)`.
- **Handling:** Ratings missing entirely are dropped before bounding.
- **Power BI Guarantee:** Guarantees ratings strictly fall within 1, 2, 3, 4, or 5 stars, preventing skewed averages.

### Rule 3: Deduplication
- **Logic:** Duplicate submissions (often caused by double-clicking survey buttons or redundant data warehouse syncs) are filtered via `drop_duplicates(subset=['feedback_id', 'customer_name', 'date', 'feedback_text'])`.
- **Power BI Guarantee:** Ensures Total Feedback count is not inflated by duplicate rows.

### Rule 4: Sentiment Consistency
- **Logic:** If sentiment is blank or `"Unknown"`, it is derived deterministically from the rating:
  - Rating $\ge 4 \implies$ **Positive**
  - Rating $= 3 \implies$ **Neutral**
  - Rating $\le 2 \implies$ **Negative**
- **Power BI Guarantee:** 100% of feedback rows have a valid sentiment category matching the company's CSAT standards.

---

## 3. Data Dictionary: `cleaned_customer_feedback.csv`

| Column Name | Power BI Data Type | Description | Example |
|---|---|---|---|
| `feedback_id` | Text | Unique identifier for the feedback submission | `FB0001` |
| `date` | Date/Time | Submission timestamp (ISO format) | `2025-01-01 00:00:00` |
| `date_formatted` | Text / Date | Formatted date string (`YYYY-MM-DD`) | `2025-01-01` |
| `year` | Whole Number | Calendar year | `2025` |
| `quarter` | Text | Calendar quarter | `Q1` |
| `month_number` | Whole Number | Month index (1-12) used for sorting month names | `1` |
| `month_name` | Text | Full English month name | `January` |
| `year_month` | Text | Year and month for trend sorting | `2025-01` |
| `customer_name` | Text | Name or anonymized customer identifier | `Customer 1` |
| `product` | Text | Product or service name | `Mobile App` |
| `channel` | Text | Feedback submission touchpoint | `Support Ticket` |
| `region` | Text | Geographic operational region | `North America` |
| `rating` | Whole Number | Customer rating bounded to 1–5 | `4` |
| `sentiment` | Text | Standardized sentiment (`Positive`, `Neutral`, `Negative`) | `Positive` |
| `is_positive` | Whole Number | Binary flag (1 if Positive, 0 otherwise) | `1` |
| `is_negative` | Whole Number | Binary flag (1 if Negative, 0 otherwise) | `0` |
| `is_neutral` | Whole Number | Binary flag (1 if Neutral, 0 otherwise) | `0` |
| `is_promoter` | Whole Number | Binary flag for NPS Promoters (Rating 4-5) | `1` |
| `is_passive` | Whole Number | Binary flag for NPS Passives (Rating 3) | `0` |
| `is_detractor` | Whole Number | Binary flag for NPS Detractors (Rating 1-2) | `0` |
| `feedback_char_count`| Whole Number | Character length of the feedback text | `52` |
| `has_text_comment` | Whole Number | Binary indicator (1 if comment present, 0 if empty) | `1` |
| `feedback_text` | Text | Raw customer feedback text | `Really happy with the Mobile App...` |

---

## 4. Power Query (M) Ingestion Script

If importing directly via Power Query Advanced Editor, use the following M code:

```powerquery
let
    Source = Csv.Document(File.Contents("powerbi/cleaned_customer_feedback.csv"),[Delimiter=",", Columns=22, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"feedback_id", type text},
        {"date", type datetime},
        {"date_formatted", type date},
        {"year", Int64.Type},
        {"quarter", type text},
        {"month_number", Int64.Type},
        {"month_name", type text},
        {"year_month", type text},
        {"customer_name", type text},
        {"product", type text},
        {"channel", type text},
        {"region", type text},
        {"rating", Int64.Type},
        {"sentiment", type text},
        {"is_positive", Int64.Type},
        {"is_negative", Int64.Type},
        {"is_neutral", Int64.Type},
        {"is_promoter", Int64.Type},
        {"is_passive", Int64.Type},
        {"is_detractor", Int64.Type},
        {"feedback_char_count", Int64.Type},
        {"has_text_comment", Int64.Type},
        {"feedback_text", type text}
    })
in
    #"Changed Type"
```

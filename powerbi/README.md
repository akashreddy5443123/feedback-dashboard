# Microsoft Power BI Enterprise Reporting Layer
### Customer Feedback Analytics Platform
**Repository:** [github.com/akashreddy5443123/feedback-dashboard](https://github.com/akashreddy5443123/feedback-dashboard)  
**Tech Stack:** Microsoft Power BI, DAX, Power Query (M), Python 3.11+, Pandas, Streamlit

---

## 1. Executive Summary

This folder provides a complete, production-grade **Microsoft Power BI reporting layer** integrated with the existing Python & Streamlit customer feedback dashboard.

```
┌─────────────────────────────────┐
│ Raw Feedback (CSV / Excel)      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Python & Pandas Processing      │
│ • Date parsing (errors='coerce')│
│ • Rating clipping to [1, 5]     │
│ • Text cleanup & Deduplication  │
│ • Deterministic Sentiment Logic │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Cleaned Analytical Datasets     │
│ • Single Table: cleaned_*.csv   │
│ • Star Schema: Fact + 5 Dims    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Power BI Reporting Layer        │
│ • 5 Professional Report Pages   │
│ • 14 Production DAX Measures    │
│ • VertiPaq Columnar Model       │
└─────────────────────────────────┘
```

---

## 2. Deliverables Index

| File | Purpose |
|---|---|
| [`cleaned_customer_feedback.csv`](cleaned_customer_feedback.csv) | Import-ready flat analytical dataset (CSV format). |
| [`cleaned_customer_feedback.xlsx`](cleaned_customer_feedback.xlsx) | Import-ready flat analytical dataset (Excel format). |
| [`Fact_CustomerFeedback.csv`](Fact_CustomerFeedback.csv) | Central Star Schema fact table with foreign keys & numeric metrics. |
| [`Dim_Date.csv`](Dim_Date.csv) | Date dimension enabling Time Intelligence DAX functions. |
| [`Dim_Product.csv`](Dim_Product.csv) | Product dimension with tiers and categories. |
| [`Dim_Channel.csv`](Dim_Channel.csv) | Channel touchpoint dimension with classification types. |
| [`Dim_Region.csv`](Dim_Region.csv) | Geographic operational dimension. |
| [`Dim_Sentiment.csv`](Dim_Sentiment.csv) | Sentiment reference dimension with score weights and hex color codes. |
| [`dax_measures.dax`](dax_measures.dax) | Raw DAX code package ready to copy/paste into Power BI Desktop. |
| [`DATA_PREPARATION.md`](DATA_PREPARATION.md) | Data cleaning pipeline, validation rules, and schema definitions. |
| [`DATA_MODEL.md`](DATA_MODEL.md) | Architectural comparison: Single Table vs. Star Schema, Cardinality & Relationships. |
| [`DAX_MEASURES.md`](DAX_MEASURES.md) | Line-by-line explanation of all business DAX calculations. |
| [`REPORT_SPECIFICATIONS.md`](REPORT_SPECIFICATIONS.md) | Detailed 5-page report design, field mappings, visual styling, and layouts. |
| [`SETUP_AND_REFRESH_GUIDE.md`](SETUP_AND_REFRESH_GUIDE.md) | Step-by-step setup in Power BI Desktop and future scheduled refresh workflow. |
| [`TECHNICAL_INTERVIEW_GUIDE.md`](TECHNICAL_INTERVIEW_GUIDE.md) | 15 core architectural questions + answers for Data Analyst & BI interviews. |

---

## 3. Quick Start (Setting Up Power BI Desktop)

1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data** > **Text/CSV** (or **Excel Workbook**).
3. Select either:
   - **Option A (Quick Single Table):** Load [`cleaned_customer_feedback.csv`](cleaned_customer_feedback.csv).
   - **Option B (Recommended Star Schema):** Load [`Fact_CustomerFeedback.csv`](Fact_CustomerFeedback.csv) and the 5 dimension tables (`Dim_*.csv`).
4. In **Model View**, verify the 1-to-many relationships (refer to [`DATA_MODEL.md`](DATA_MODEL.md)).
5. Copy the measures from [`dax_measures.dax`](dax_measures.dax) into `Fact_CustomerFeedback`.
6. Build the 5 report pages described in [`REPORT_SPECIFICATIONS.md`](REPORT_SPECIFICATIONS.md).

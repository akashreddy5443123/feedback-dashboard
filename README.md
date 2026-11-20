# Customer Feedback Dashboard

Interactive dashboard to manage and visualize customer feedback.

**Tech stack:** Python, Pandas, Streamlit, Plotly, Matplotlib, Scikit-learn, Microsoft Power BI

## Features
- Upload your own feedback CSV / Excel or use the bundled sample dataset
- Reusable data processing module (`modules/data_processor.py`) that cleans, deduplicates, and standardizes raw feedback data
- Reusable chart module (`modules/charts.py`) with Plotly interactive charts + a Matplotlib chart for static export/reports
- Machine Learning sentiment analysis module (`modules/ml_sentiment.py`) using TF-IDF + Logistic Regression
- **Microsoft Power BI Integration Layer (`powerbi/`):** Clean analytical datasets (CSV & Excel), full Star Schema dimensional model, DAX measures package, and 5-page report design specifications
- Sidebar filters: date range, product, channel, region, sentiment
- KPI cards: total feedback, avg rating, % positive, % negative, Net Promoter Score (NPS), CSAT
- Charts: sentiment breakdown (pie), sentiment trend over time (line), rating distribution (bar), avg rating by product (bar), feedback by channel (donut), monthly avg rating (Matplotlib, downloadable PNG), NPS gauge, and product-channel matrix
- Filtered data table with CSV and Power BI package exports

## Project structure
```
feedback-dashboard/
├── app.py                           # Streamlit entrypoint / UI layer
├── modules/
│   ├── data_processor.py            # Cleaning, filtering, aggregation, and NPS engine
│   ├── charts.py                    # Plotly + Matplotlib chart builders
│   ├── ml_sentiment.py              # TF-IDF + Logistic Regression text classification
│   ├── hf_sentiment.py              # Optional Hugging Face sentiment pipeline
│   └── power_bi_export.py           # Power BI Star Schema & DAX export engine
├── powerbi/                         # Dedicated Power BI deliverables directory
│   ├── cleaned_customer_feedback.csv# Cleaned flat analytical dataset
│   ├── cleaned_customer_feedback.xlsx
│   ├── Fact_CustomerFeedback.csv    # Central fact table
│   ├── Dim_Date.csv                 # Full date dimension table
│   ├── Dim_Product.csv              # Product tiers & categories
│   ├── Dim_Channel.csv              # Channel touchpoint catalog
│   ├── Dim_Region.csv               # Geographic operational territories
│   ├── Dim_Sentiment.csv            # Sentiment classification & hex colors
│   ├── dax_measures.dax             # Production DAX measures package
│   ├── DATA_PREPARATION.md          # ETL pipeline & data dictionary
│   ├── DATA_MODEL.md                # Star schema vs flat table comparison
│   ├── DAX_MEASURES.md              # Line-by-line explanation of DAX formulas
│   ├── REPORT_SPECIFICATIONS.md     # 5-page report layout & visual blueprints
│   ├── SETUP_AND_REFRESH_GUIDE.md   # Power BI Desktop setup & refresh instructions
│   └── TECHNICAL_INTERVIEW_GUIDE.md # 15 core architectural Q&A for BI interviews
├── data/
│   ├── generate_sample_data.py      # Creates a synthetic sample dataset
│   ├── customer_feedback.csv        # Sample data (600 rows)
│   └── feedback_template.xlsx       # Blank template
├── docs/                            # Deep-dive system documentation
├── verify_powerbi_pipeline.py       # Automated validation test suite
├── run_offline_check.py             # Offline verification check script
├── requirements.txt
└── README.md
```

## Setup
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```
This opens the dashboard at http://localhost:8501. It loads the bundled sample
dataset automatically — or upload your own CSV from the sidebar.

## CSV format
Your CSV should have these columns (missing ones are handled gracefully):
```
date, customer_name, product, channel, region, rating, sentiment, feedback_text
```
`rating` should be 1–5. If `sentiment` is missing, it's derived from `rating`
(4-5 → Positive, 3 → Neutral, 1-2 → Negative).

## Regenerating the sample dataset
```bash
python data/generate_sample_data.py
```

## Notes for your resume/interview talk-track
- `data_processor.py` is deliberately separated from the UI (`app.py`) so the
  cleaning/aggregation logic is reusable and unit-testable independent of Streamlit.
- Plotly is used for interactivity (hover, zoom, filtering) inside the app;
  Matplotlib is included to show static/report-style chart generation and
  a downloadable PNG export — a common ask in feedback/reporting tools.
- `st.cache_data` is used on the load step so re-filtering doesn't re-read/re-clean the CSV each time.

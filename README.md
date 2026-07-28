# Customer Feedback Dashboard

Interactive dashboard to manage and visualize customer feedback.

**Tech stack:** Python, Pandas, Streamlit, Plotly, Matplotlib

## Features
- Upload your own feedback CSV or use the bundled sample dataset
- Reusable data processing module (`modules/data_processor.py`) that cleans, deduplicates, and standardizes raw feedback data
- Reusable chart module (`modules/charts.py`) with Plotly interactive charts + a Matplotlib chart for static export/reports
- Sidebar filters: date range, product, channel, region, sentiment
- KPI cards: total feedback, avg rating, % positive, % negative
- Charts: sentiment breakdown (pie), sentiment trend over time (line), rating distribution (bar), avg rating by product (bar), feedback by channel (donut), monthly avg rating (Matplotlib, downloadable PNG)
- Filtered data table with CSV export

## Project structure
```
feedback-dashboard/
├── app.py                        # Streamlit entrypoint / UI layer
├── modules/
│   ├── data_processor.py         # cleaning, filtering, aggregation
│   └── charts.py                 # Plotly + Matplotlib chart builders
├── data/
│   ├── generate_sample_data.py   # creates a synthetic sample dataset
│   └── customer_feedback.csv     # sample data (generated)
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

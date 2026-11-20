# Customer Feedback Analytics Dashboard
## Master Study & Interview Preparation Guide (Mu Sigma Trainee Decision Scientist / AI Bot Interview)

---

> **Honesty & Implementation Notice:**
> - **Project Covered:** **Customer Feedback Dashboard** (100% focused on this workspace codebase).
> - **Codebase Files Analyzed:**
>   - `app.py` (Streamlit UI & Orchestration Layer)
>   - `modules/data_processor.py` (Data Ingestion, Cleaning, Filtering, KPI & Aggregation Engine)
>   - `modules/charts.py` (Plotly Interactive Charts & Matplotlib Static Export Figure Builder)
>   - `modules/ml_sentiment.py` (Scikit-Learn TF-IDF + Logistic Regression NLP Classifier)
>   - `modules/hf_sentiment.py` (Optional Pretrained Hugging Face Transformer Pipeline)
>   - `data/generate_sample_data.py` (Synthetic Data Generator)
>   - `data/customer_feedback.csv` (Sample Dataset — 600 records)
> - **Status Tags Used Across This Guide:**
>   - `[IMPLEMENTED]`: Written and active in the Python codebase.
>   - `[OPTIONAL / EXPERIMENTAL]`: Present in codebase as an optional module/layer.
>   - `[PLANNED / NOT IMPLEMENTED]`: Future enhancements (e.g., persistent PostgreSQL database, PDF report compiler, real-time webhook listeners).
>   - `[NOT CLEAR FROM CODE]`: Items where explicit codebase evidence is absent.

---

# 1. PROJECT OVERVIEW

### What is the Customer Feedback Dashboard?
The **Customer Feedback Dashboard** is an interactive, web-based data analytics and decision-support application built with **Python, Pandas, Streamlit, Plotly, Matplotlib, and Scikit-Learn**. It allows business managers and decision scientists to upload raw, messy customer feedback datasets (in CSV or Excel format), automatically cleans and standardizes the records, calculates headline business KPIs, renders 6 interactive and report-ready charts, and classifies customer sentiment using both transparent rules and machine learning.

### What problem does it solve?
Companies collect customer reviews and feedback across many disconnected channels: emails, in-app surveys, app store reviews, support tickets, and social media. Raw feedback exports are notoriously messy:
- Inconsistent date formats (e.g., `2025/01/15`, `15-01-2025`, invalid text strings).
- Missing or invalid ratings (e.g., blanks, negative numbers, or typos like `98`).
- Duplicate records caused by sync errors or user double-clicks.
- Inconsistent column names (e.g., `"Customer Name"` vs `"customer_name"`).
- Unstructured text comments with no quick sentiment summary.

Manually analyzing hundreds or thousands of rows in Excel is slow, prone to formula errors, and cannot answer critical business questions in real time.

### Why did I build it?
I built it to solve three practical challenges:
1. **Automate Data Cleaning:** Build a resilient, non-destructive data-cleaning pipeline that handles corrupted dates, typos, and missing values without crashing.
2. **Accelerate Business Decisions:** Give product managers, support teams, and executives instant visibility into product ratings, channel bottlenecks, regional satisfaction, and sentiment trends over time.
3. **Bridge Heuristics and Machine Learning:** Provide a transparent, rule-based baseline for sentiment classification while implementing an n-gram TF-IDF machine learning model to uncover contradictions between star ratings and review text (e.g., a 5-star rating with an angry review).

### Who can use it?
- **Product Managers:** To track satisfaction across product tiers (Basic Plan, Pro Plan, Enterprise Plan, Mobile App, Browser Extension) and prioritize feature fixes.
- **Customer Support Leads:** To monitor ticket volume, identify struggling support channels, and spot sudden drops in customer satisfaction.
- **Decision Scientists / Data Analysts:** To explore rating distributions, detect anomalies, test text classification models, and export clean data for downstream modeling.
- **Regional Business Heads:** To compare regional satisfaction across North America, Europe, APAC, LATAM, and MEA.

### What is the input?
- **User Upload:** A CSV or Excel file (`.csv`, `.xlsx`, `.xls`) uploaded via the sidebar.
- **Default Fallback:** The bundled synthetic sample dataset (`data/customer_feedback.csv`, 600 records).
- **Expected Columns (handled gracefully if missing):**
  `feedback_id`, `date`, `customer_name`, `product`, `channel`, `region`, `rating`, `sentiment`, `feedback_text`.

### What happens to the input?
1. Ingested via `load_data()` which detects file type (CSV vs Excel).
2. Cleaned via `clean_data()`: column names normalized, dates parsed, ratings coerced and clipped to `[1, 5]`, text stripped, missing sentiment derived, duplicates removed, and sorted chronologically.
3. Filtered dynamically via `apply_filters()` based on user selections.
4. Aggregated into headline KPIs and time-series/categorical summaries.
5. Visualized into 5 interactive Plotly charts and 1 exportable Matplotlib chart.
6. Analyzed by an optional Scikit-Learn TF-IDF + Logistic Regression model.

### What is the output?
- **4 Headline Metric Cards:** Total Feedback, Average Rating / 5, Positive %, Negative %.
- **6 Visual Charts:**
  1. Sentiment Breakdown (Plotly Donut Chart).
  2. Sentiment Trend Over Time (Plotly Multi-Line Chart, weekly frequency).
  3. Rating Distribution (Plotly Bar Chart for ratings 1–5).
  4. Average Rating by Product (Plotly Horizontal Bar Chart sorted by score).
  5. Feedback by Channel (Plotly Donut Chart).
  6. Monthly Average Rating Trend (Matplotlib Static Line Chart).
- **Interactive Data Table:** Filterable, searchable raw records.
- **Exportable Files:** `filtered_feedback.csv` and `monthly_rating_trend.png`.
- **ML Evaluation Report:** Accuracy %, train/test sizes, per-class Precision/Recall/F1 table, and a table of rating-vs-text disagreements.

### What is the business value?
- **Drastic Time Savings:** Reduces weekly feedback analysis time from hours in spreadsheets to under 5 seconds.
- **Early Churn Prevention:** Detects downward sentiment trends early before customer attrition spikes.
- **Root Cause Isolation:** Slices data across products, channels, and regions to pinpoint broken releases or support bottlenecks.
- **High Decision Integrity:** Prevents calculation errors caused by corrupted dates, invalid ratings, or duplicate records.

### What technologies are actually used?
- **Python (3.9+):** Core language.
- **Pandas (2.0+):** Tabular data manipulation, time-series bucketing, cleaning, and aggregation.
- **Streamlit (1.32+):** Reactive web framework, widget layout, caching (`@st.cache_data`), session state.
- **Plotly Express & Graph Objects (5.18+):** Interactive vector charts with hover tooltips and responsive styling.
- **Matplotlib (3.8+):** Static report-style plotting and PNG buffer rendering.
- **Scikit-Learn (1.4+):** NLP text vectorization (`TfidfVectorizer`), classification (`LogisticRegression`), and evaluation metrics.
- **openpyxl (3.1+):** Engine dependency used by Pandas to read `.xlsx` files.
- **Hugging Face Transformers (`transformers`, `torch`):** `[OPTIONAL / EXPERIMENTAL]` Reference module for DistilBERT sentiment pipeline.

---

### Spoken Elevator Pitches

#### 30-Second Explanation:
> *"I built an interactive **Customer Feedback Analytics Platform** using Python, Pandas, Streamlit, Plotly, and Scikit-Learn. It takes messy multi-channel feedback exports in CSV or Excel, automatically cleans bad dates, clips invalid ratings, removes duplicates, and standardizes sentiment. The app computes business KPIs, renders 6 interactive and report-ready charts, and features a machine learning text-classification module using TF-IDF and Logistic Regression to catch contradictions between star ratings and text reviews."*

#### 1-Minute Explanation:
> *"Customer feedback arrives from emails, app store reviews, support tickets, and surveys in messy spreadsheets with inconsistent dates, missing ratings, and duplicates. Analyzing this manually in Excel takes hours and risks calculation errors.*
> 
> *I built a full-stack data application with a clean 3-layer architecture. The data layer, written in pure Pandas, handles loading, date coercion, rating clipping, and deduplication. The visualization layer builds 5 interactive Plotly charts and an exportable Matplotlib report chart. The Streamlit UI layer coordinates filtering, KPI cards, and exports.*
> 
> *I also implemented an NLP module using TF-IDF bigrams with custom stop words that preserve negation like 'not good' and trained a Logistic Regression classifier. This allows businesses to detect sarcasm or user errors where someone gave 5 stars but wrote an angry complaint. The app runs in memory, caches I/O operations, and exports clean data and charts."*

#### 2-Minute Explanation:
> *"In my Customer Feedback Analytics project, I wanted to solve the complete end-to-end data problem: from raw, corrupted spreadsheet ingestion to executive decision support and machine learning validation.*
> 
> *The system is structured into three decoupled layers:*
> *First, the **Data Processing Layer** (`data_processor.py`) contains pure, testable Pandas functions with zero UI code. It parses `.csv` and `.xlsx` files, normalizes column casing, coerces dates with `errors='coerce'`, clips invalid ratings to a strict 1-to-5 scale, derives missing sentiment deterministically, and removes duplicates across composite keys.*
> 
> *Second, the **Visualization Layer** (`charts.py`) constructs five interactive Plotly charts—including a weekly sentiment trend line, rating distribution bar, and horizontal product performance chart—plus a Matplotlib time-series chart resampled to monthly averages (`resample('ME')`) for downloadable PNG reports.*
> 
> *Third, the **Streamlit UI Layer** (`app.py`) manages application state, sidebar multi-select filters, four headline KPI cards, and data export buttons. I decorated the sample dataset loader with `@st.cache_data` to ensure smooth UI performance without redundant re-reading on every filter interaction.*
> 
> *Finally, I built a machine learning module (`ml_sentiment.py`) using scikit-learn. It uses `TfidfVectorizer` with bigrams and a modified stop-words list that preserves negation words like 'not', 'no', and 'never', followed by a `LogisticRegression` classifier. This compares text sentiment against star ratings, flagging anomalies where customers accidentally leave 5 stars on negative reviews.*
> 
> *This project demonstrates data engineering rigor, statistical aggregation, interactive storytelling, and practical machine learning."*

---

# 2. COMPLETE PROJECT ARCHITECTURE

### Actual System Architecture Flow

```
[Raw File: CSV / Excel Upload  OR  Sample Dataset (600 rows)]
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 DATA LAYER: data_processor.py               │
│  - load_data(): Detects format (.csv / .xlsx via openpyxl)  │
│  - clean_data():                                            │
│      ├── Normalizes headers (lowercase, snake_case)         │
│      ├── Fills missing required columns with pd.NA          │
│      ├── pd.to_datetime(errors="coerce") & drops NaT        │
│      ├── pd.to_numeric(errors="coerce") & drops NaN         │
│      ├── .clip(1, 5).astype(int) on ratings                 │
│      ├── Strips whitespace on text & categoricals           │
│      ├── rating_to_sentiment() for blank sentiment          │
│      ├── drop_duplicates(subset=[id, name, date, text])     │
│      └── sort_values("date")                                │
│  - apply_filters(): Multi-criteria boolean slicing          │
│  - Aggregations: compute_kpis(), sentiment_over_time(),     │
│    top_products_by_rating(), rating_distribution(),         │
│    channel_breakdown()                                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────────────┐    ┌──────────────────────────────┐
│  VISUALIZATION: charts.py    │    │      NLP / ML LAYER:         │
│  - sentiment_pie() (Donut)   │    │       ml_sentiment.py        │
│  - sentiment_trend_line()    │    │  - TfidfVectorizer(1, 2)     │
│  - rating_bar() (1-5)        │    │    (custom negation stoplist)│
│  - product_rating_bar() (h)  │    │  - LogisticRegression        │
│  - channel_donut()           │    │  - classification_report()   │
│  - matplotlib_summary()      │    │  - compare_with_rule_based() │
│    (.resample("ME").mean())  │    │  - predict_sentiment()       │
└──────────────┬───────────────┘    └──────────────┬───────────────┘
               │                                   │
               └─────────────────┬─────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER: app.py                 │
│  - Streamlit Wide Layout & Custom Header                    │
│  - Sidebar: File Uploader, Date Input, Multiselects         │
│  - Status Messages & st.stop() Error Guards                 │
│  - 4 KPI Metric Cards (st.metric in 4 columns)              │
│  - 6 Responsive Chart Containers                            │
│  - In-Memory PNG Chart Export (io.BytesIO + download_button)│
│  - Scikit-Learn Model Training Expander & Live Test Input   │
│  - Filtered Data Table (st.dataframe) & CSV Download        │
│  - @st.cache_data Performance Optimization                  │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown Table

| Component Name | File Name | Purpose | Input | Processing | Output | Libraries Used | Connection to Next Component |
|---|---|---|---|---|---|---|---|
| **Data Ingestion** | `modules/data_processor.py` | Load raw tabular data from file path or file uploader | CSV or Excel file (`UploadedFile` or path) | Detects extension; calls `pd.read_csv()` or `pd.read_excel()` | Raw `pd.DataFrame` | `pandas`, `openpyxl` | Passes raw DataFrame to `clean_data()` |
| **Data Cleaning** | `modules/data_processor.py` | Clean, coerce, validate, and deduplicate | Raw `pd.DataFrame` | Header normalization, date parsing, rating clipping `[1, 5]`, sentiment derivation, deduplication | Clean `pd.DataFrame` | `pandas` | Feeds `apply_filters()` and cached loader in `app.py` |
| **Filter Engine** | `modules/data_processor.py` | Filter clean data by sidebar parameters | Clean DataFrame + filter parameters (tuples, lists) | Multi-column boolean masking (`&`) across dates, products, channels, regions, sentiments | Filtered `pd.DataFrame` | `pandas` | Feeds all KPI and chart aggregation functions |
| **Statistical Aggregator** | `modules/data_processor.py` | Compute summary statistics and time groupings | Filtered `pd.DataFrame` | Computes means, percentages, frequency counts, and weekly time groupings (`pd.Grouper`) | Dict of KPIs & Aggregated DataFrames | `pandas` | Feeds chart building functions in `modules/charts.py` |
| **Interactive Chart Builder** | `modules/charts.py` | Build interactive Plotly chart objects | Aggregated DataFrames | Constructs Plotly Express & Graph Objects with custom color palettes and layout templates | Plotly `Figure` objects | `plotly.express`, `plotly.graph_objects` | Rendered via `st.plotly_chart()` in `app.py` |
| **Report Chart Builder** | `modules/charts.py` | Build static publication-quality trend chart | Filtered `pd.DataFrame` | Resamples ratings monthly (`.resample("ME")`), plots trend with markers | Matplotlib `Figure` | `matplotlib.pyplot` | Rendered via `st.pyplot()` and converted to PNG via `io.BytesIO` |
| **ML Sentiment Classifier** | `modules/ml_sentiment.py` | NLP text feature extraction and sentiment classification | `feedback_text` and `sentiment` Series | TF-IDF (1, 2) bigrams, custom negation stop-words, Logistic Regression training, test split | Model dict (vectorizer, model, metrics report) | `scikit-learn`, `numpy` | Displayed in Streamlit expander in `app.py` |
| **Contradiction Detector** | `modules/ml_sentiment.py` | Find mismatches between star ratings and text | Filtered DataFrame, vectorizer, model | Predicts sentiment on all rows; compares `sentiment == ml_sentiment` | DataFrame with `agrees_with_rule` column | `scikit-learn`, `pandas` | Displayed as a table of anomalies in `app.py` |
| **UI & Orchestrator** | `app.py` | User interface, layout, state, rendering, and export | User inputs, uploaded files | Manages execution flow, calls data/chart/ML modules, handles errors | Web page HTML/JS rendered by Streamlit | `streamlit`, `io`, `os` | User's web browser |

---

# 3. COMPLETE DATA FLOW

### Step-by-Step Numbered Execution Flow

1. **Application Starts:** User runs `streamlit run app.py`. Streamlit initializes `st.set_page_config(layout="wide", page_title="Customer Feedback Dashboard")`.
2. **Data Source Resolution:**
   - If user uploads a file (`.csv`, `.xlsx`, `.xls`), `dp.load_data()` reads it and `dp.clean_data()` cleans it fresh.
   - If no upload, `load_and_clean(DEFAULT_DATA_PATH)` loads the bundled 600-row CSV via `@st.cache_data`.
3. **Data Inspection & Row Count Validation:**
   - Raw row count is compared against cleaned row count.
   - If 0 rows survive cleaning, a sidebar error is shown and `st.stop()` halts execution.
   - If some rows were dropped, a sidebar warning indicates how many were dropped and why.
4. **Schema Normalization:** Column names are stripped, lowercased, and spaces replaced with underscores. All 9 required columns are verified; missing ones filled with `pd.NA`.
5. **Missing Value Identification & Handling:**
   - `date` missing/corrupted $\rightarrow$ converted to `NaT` via `pd.to_datetime(errors="coerce")` and dropped.
   - `rating` missing/corrupted $\rightarrow$ converted to `NaN` via `pd.to_numeric(errors="coerce")` and dropped.
   - `feedback_text` missing $\rightarrow$ filled with `""`.
   - Categorical fields (`product`, `channel`, `region`, `sentiment`) missing $\rightarrow$ filled with `"Unknown"`.
6. **Invalid Value Bounding:** Ratings are clipped to `[1, 5]` via `.clip(1, 5).astype(int)` to eliminate out-of-range typos (e.g., `98`).
7. **Deduplication:** Duplicate rows matching on composite key (`feedback_id`, `customer_name`, `date`, `feedback_text`) are removed with `drop_duplicates()`.
8. **Sentiment Derivation:** Blank or `"Unknown"` sentiment entries are populated deterministically from ratings using `rating_to_sentiment()` ($4\text{--}5 \rightarrow \text{Positive}$, $3 \rightarrow \text{Neutral}$, $1\text{--}2 \rightarrow \text{Negative}$) using `.loc` masking.
9. **Chronological Sorting:** Dataset is sorted by date using `.sort_values("date").reset_index(drop=True)`.
10. **Sidebar Filter Widgets Populated:**
    - `date_input()` bounded between `min_date` and `max_date`.
    - `multiselect()` populated with unique sorted values for Product, Channel, Region, and Sentiment.
11. **Dynamic Filtering:** `dp.apply_filters()` applies boolean masks across all active selections, returning `filtered`.
12. **KPI Calculation:** `dp.compute_kpis()` calculates Total Feedback, Average Rating, Positive %, and Negative % with empty DataFrame guards.
13. **Chart Data Aggregation & Plotting:**
    - `charts.sentiment_pie()` builds Plotly donut chart.
    - `dp.sentiment_over_time(freq="W")` $\rightarrow$ `charts.sentiment_trend_line()` builds weekly multi-line chart.
    - `dp.rating_distribution()` $\rightarrow$ `charts.rating_bar()` builds 1–5 bar chart.
    - `dp.top_products_by_rating()` $\rightarrow$ `charts.product_rating_bar()` builds horizontal product ranking bar chart.
    - `dp.channel_breakdown()` $\rightarrow$ `charts.channel_donut()` builds channel volume donut chart.
    - `charts.matplotlib_summary()` resamples data to monthly averages (`resample("ME")`) for static report plotting.
14. **Report & Data Export:**
    - Matplotlib figure saved to in-memory `io.BytesIO()` binary buffer for PNG download button.
    - Filtered table displayed with `st.dataframe()` and downloadable as CSV via `st.download_button()`.
15. **Optional ML Training & Evaluation:**
    - User clicks "Train model on current filtered data".
    - `ml.train_sentiment_model()` fits TF-IDF (1,2) + Logistic Regression, displaying Accuracy and Precision/Recall/F1 metrics.
    - `ml.compare_with_rule_based()` displays rows where ML text sentiment contradicts star ratings.
    - `st.text_input()` allows real-time prediction testing on custom sentences.

---

# 4. FILE-BY-FILE EXPLANATION

### File: `modules/data_processor.py`
- **Purpose:** Standalone, pure data processing module. It contains zero UI code and zero Streamlit dependencies, making it completely decoupled, reusable, and unit-testable.
- **Important Functions:**
  - `load_data(file) -> pd.DataFrame`: Reads CSV or Excel files (`.xlsx`/`.xls` via `pd.read_excel()` using `openpyxl`, otherwise `pd.read_csv()`).
  - `clean_data(df: pd.DataFrame) -> pd.DataFrame`: Comprehensive 8-step cleaning pipeline (normalizes headers, ensures 9 required columns, coerces dates, coerces and clips ratings to `[1, 5]`, strips text, derives missing sentiment, drops duplicates, sorts by date).
  - `rating_to_sentiment(rating: int) -> str`: Heuristic mapping: $4\text{--}5 \rightarrow \text{"Positive"}$, $3 \rightarrow \text{"Neutral"}$, $1\text{--}2 \rightarrow \text{"Negative"}$.
  - `apply_filters(df, date_range, products, channels, regions, sentiments) -> pd.DataFrame`: Applies multi-criteria boolean filtering across active sidebar selections.
  - `compute_kpis(df) -> dict`: Computes total feedback volume, average rating, positive %, and negative % with zero-division guards.
  - `sentiment_over_time(df, freq="W") -> pd.DataFrame`: Aggregates sentiment frequency over time using `pd.Grouper(freq=freq)`.
  - `top_products_by_rating(df) -> pd.DataFrame`: Groups by product, calculates mean rating and total feedback count, and sorts descending.
  - `rating_distribution(df) -> pd.DataFrame`: Calculates frequency counts for discrete ratings 1 through 5.
  - `channel_breakdown(df) -> pd.DataFrame`: Aggregates feedback volume count by submission channel.
- **Important Variables:** `REQUIRED_COLUMNS` (list of 9 mandatory column strings).
- **Libraries Imported:** `pandas` (tabular operations).
- **Connections:** Imported by `app.py` as `dp`.
- **Interview Explanation:** *"I deliberately separated `data_processor.py` from `app.py`. It contains pure Pandas functions that handle all loading, cleaning, and aggregation logic independently of Streamlit, making it fully unit-testable and reusable across other frameworks."*

---

### File: `modules/charts.py`
- **Purpose:** Pure visualization module that constructs Plotly and Matplotlib figure objects from aggregated DataFrames. It does not render anything directly; it simply returns figures.
- **Important Functions:**
  - `sentiment_pie(df)`: Builds a Plotly donut chart (`hole=0.45`) with fixed, semantic colors (`#2ecc71` Green for Positive, `#f1c40f` Yellow for Neutral, `#e74c3c` Red for Negative).
  - `sentiment_trend_line(trend_df)`: Builds an interactive multi-line time-series Plotly chart with markers showing sentiment volume trends over time.
  - `rating_bar(dist_df)`: Constructs a vertical Plotly bar chart displaying counts for ratings 1 to 5 with linear integer ticks.
  - `product_rating_bar(product_df)`: Constructs a horizontal Plotly bar chart (`orientation="h"`) ranking products by average rating on a 0–5 scale.
  - `channel_donut(channel_df)`: Builds a Plotly donut chart showing submission volume shares across channels.
  - `matplotlib_summary(df)`: Constructs a static Matplotlib line chart resampling ratings to monthly averages (`resample("ME")`) with gridlines and formatted date axes.
- **Important Variables:** `PLOTLY_TEMPLATE = "plotly_white"`.
- **Libraries Imported:** `matplotlib.pyplot`, `plotly.express`, `plotly.graph_objects`, `pandas`.
- **Connections:** Imported by `app.py` as `charts`.
- **Interview Explanation:** *"I used Plotly for interactive web exploration (hover tooltips, zooming) and Matplotlib for static, exportable figures. Matplotlib allows non-technical managers to download high-resolution PNG charts directly for slide decks and executive PDF reports."*

---

### File: `modules/ml_sentiment.py`
- **Purpose:** Machine learning module implementing text-based sentiment classification using scikit-learn to validate heuristic rating labels.
- **Important Functions:**
  - `train_sentiment_model(df) -> dict`: Cleans text, checks sample size ($\ge 10$) and class count ($\ge 2$), performs stratified train/test split (80/20), builds `TfidfVectorizer(max_features=2500, ngram_range=(1,2))` with a custom stop-words list that preserves negation words (`not`, `no`, `never`, `cannot`), trains `LogisticRegression(max_iter=500)`, and computes accuracy, precision, recall, and F1-score.
  - `predict_sentiment(vectorizer, model, texts: list) -> list`: Vectorizes raw text strings and predicts sentiment labels.
  - `compare_with_rule_based(df, vectorizer, model) -> pd.DataFrame`: Predicts sentiment across the entire dataset and flags rows where ML text sentiment contradicts the rating-based heuristic (`agrees_with_rule == False`).
- **Libraries Imported:** `pandas`, `numpy`, `sklearn.feature_extraction.text.TfidfVectorizer`, `sklearn.feature_extraction.text.ENGLISH_STOP_WORDS`, `sklearn.linear_model.LogisticRegression`, `sklearn.model_selection.train_test_split`, `sklearn.metrics` (`accuracy_score`, `classification_report`).
- **Connections:** Imported by `app.py` as `ml` and rendered in the experimental ML expander.
- **Interview Explanation:** *"Standard stop-word lists strip out words like 'not', causing 'not good' to look like 'good'. In my TF-IDF vectorizer, I explicitly preserved negation words and enabled bigrams, ensuring negative customer sentiment in text is accurately classified."*

---

### File: `modules/hf_sentiment.py`
- **Purpose:** `[OPTIONAL / EXPERIMENTAL]` Reference module implementing deep learning sentiment analysis using Hugging Face Transformers (`DistilBERT` fine-tuned on SST-2).
- **Important Functions:**
  - `classify_feedback(texts: pd.Series, batch_size=16) -> tuple[list[str], list[float]]`: Batches text through the Hugging Face `sentiment-analysis` pipeline and returns binary labels (`POSITIVE`/`NEGATIVE`) and confidence scores.
  - `flag_rating_text_mismatches(df) -> pd.DataFrame`: Filters rows where star ratings ($\ge 4$) conflict with `NEGATIVE` model predictions or low ratings ($\le 2$) conflict with `POSITIVE` predictions.
- **Libraries Imported:** `transformers` (pipeline), `torch`, `pandas`.
- **Connections:** Standalone reference module for benchmarking classical ML against deep learning transformers.
- **Interview Explanation:** *"This module demonstrates how modern pretrained transformer models (DistilBERT) can be integrated for transfer learning and compared against lightweight classical linear models."*

---

### File: `app.py`
- **Purpose:** The main application entrypoint and UI orchestration layer built with Streamlit.
- **Important Functions:**
  - `load_and_clean(file_or_path) -> pd.DataFrame`: Wrapped with `@st.cache_data` to cache the initial load and cleaning of the bundled dataset, preventing redundant disk reads on filter reruns.
  - `main()`: Orchestrates the entire application lifecycle: page configuration, sidebar file uploads, validation error reporting, dynamic filter widgets, KPI metrics, responsive 2-column chart rendering, Matplotlib PNG export via `io.BytesIO`, scikit-learn ML training playground, and CSV data export.
- **Libraries Imported:** `streamlit`, `pandas`, `io`, `os`, `modules.data_processor`, `modules.charts`, `modules.ml_sentiment`.
- **Connections:** Entrypoint executed by running `streamlit run app.py`.
- **Interview Explanation:** *"app.py serves strictly as the presentation and controller layer. It collects user input, invokes the underlying business logic in `data_processor.py`, and passes the resulting data to `charts.py` for rendering."*

---

### File: `data/generate_sample_data.py`
- **Purpose:** Reproducible synthetic dataset generator that populates `data/customer_feedback.csv` with 600 realistic customer feedback records.
- **Important Logic:** Sets seed `random.seed(42)` for deterministic generation; defines 5 products, 5 channels, 5 regions, and 540 days of date spread; formats text templates across Positive (55%), Neutral (25%), and Negative (20%) distributions.
- **Libraries Imported:** `random`, `datetime`, `pandas`.
- **Interview Explanation:** *"This script provides a reproducible, realistic synthetic dataset so the dashboard functions out of the box without requiring manual user uploads during demonstrations."*

---

# 5. PYTHON CONCEPTS IN THE CODEBASE

### 1. Variables & Basic Types
- **Definition:** Named memory locations holding references to objects (strings, integers, floats, booleans).
- **Why Used:** To hold user inputs, counts, averages, and configuration paths.
- **Where Used:** `DEFAULT_DATA_PATH` (`app.py`), `total` (`data_processor.py`).
- **Example:** `avg_rating = round(df["rating"].mean(), 2)`
- **Follow-up:** *What is the difference between mutable and immutable types in Python?*
  **Answer:** Immutable types (integers, strings, tuples) cannot be altered in place after creation; mutable types (lists, dictionaries, DataFrames) can be modified in place.

### 2. Lists & List Comprehensions
- **Definition:** Ordered, mutable sequences of elements. List comprehensions provide a concise syntax for generating lists.
- **Why Used:** Normalizing column names and filtering stop words.
- **Where Used:** `df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]` (`data_processor.py`), `custom_stop_words = [w for w in ENGLISH_STOP_WORDS if w not in negation_words]` (`ml_sentiment.py`).
- **Example:** `[x.strip() for x in raw_categories]`
- **Follow-up:** *Why use a list comprehension instead of a for-loop?*
  **Answer:** List comprehensions are more concise, readable, and execute faster at the C-bytecode level.

### 3. Dictionaries
- **Definition:** Unordered key-value mapping structures with $O(1)$ average-time lookup.
- **Why Used:** Storing KPI metrics, chart color maps, and classification reports.
- **Where Used:** `compute_kpis()` return dict (`data_processor.py`), `color_map` in `sentiment_pie()` (`charts.py`).
- **Example:** `color_map = {"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"}`
- **Follow-up:** *What happens if you access a non-existent dictionary key?*
  **Answer:** `dict[key]` raises `KeyError`; `dict.get(key, default)` returns `None` or a specified fallback value safely.

### 4. Sets
- **Definition:** Unordered collections of unique, hashable elements.
- **Why Used:** Fast $O(1)$ membership testing for negation stop words and column subset validation.
- **Where Used:** `negation_words = {"not", "no", "never", "neither", "nor", "none", "cannot"}` (`ml_sentiment.py`).
- **Follow-up:** *Why use a set over a list for word lookup?*
  **Answer:** Set membership testing `x in my_set` is $O(1)$ average time complexity, whereas list lookup `x in my_list` is $O(n)$.

### 5. Tuples
- **Definition:** Immutable, ordered sequences of elements.
- **Why Used:** Streamlit date range widgets return a 2-element tuple `(start_date, end_date)`.
- **Where Used:** `isinstance(date_range, tuple)` in `app.py` and `apply_filters()` in `data_processor.py`.
- **Follow-up:** *Why does date_input return a tuple instead of a list?*
  **Answer:** Tuples represent fixed-length records with immutable integrity.

### 6. Functions & Default Arguments
- **Definition:** Reusable, callable blocks of code encapsulating specific operations.
- **Why Used:** Decoupling business logic, cleaning steps, and chart builders into pure functions.
- **Where Used:** `sentiment_over_time(df: pd.DataFrame, freq: str = "W")` (`data_processor.py`).
- **Follow-up:** *Why should you avoid mutable default arguments in Python?*
  **Answer:** Default arguments are evaluated once at function definition time. A mutable default (like `def func(a=[])`) persists modifications across subsequent calls.

### 7. Exception Handling (`try / except`)
- **Definition:** Structured blocks to intercept and gracefully manage runtime errors.
- **Why Used:** Handling stratified train-test split failures when a sentiment class has very few records, and loading optional dependencies.
- **Where Used:** `train_sentiment_model()` in `modules/ml_sentiment.py`.
- **Example:**
  ```python
  try:
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
  except ValueError:
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  ```
- **Follow-up:** *Why does stratified split raise ValueError?*
  **Answer:** If any class has fewer than 2 samples, `stratify=y` cannot split at least one sample into both train and test partitions.

### 8. In-Memory Byte Streams (`io.BytesIO`)
- **Definition:** In-memory binary stream buffer in Python's standard library.
- **Why Used:** Saving Matplotlib figures as PNG images in memory for the download button without writing temporary files to disk.
- **Where Used:** `app.py` line 148.
- **Example:** `buf = io.BytesIO(); fig.savefig(buf, format="png"); buf.getvalue()`
- **Follow-up:** *Why avoid saving temporary files to disk?*
  **Answer:** Avoids disk I/O latency, file permission conflicts, and orphaned temporary files on the web server.

---

# 6. PANDAS OPERATIONS IN THE CODEBASE

| Pandas Operation | What It Does | Input | Output | Exact Code Location |
|---|---|---|---|---|
| `pd.read_csv()` | Parses comma-separated file into DataFrame | File path / Streamlit `UploadedFile` | `pd.DataFrame` | `data_processor.py` line 22 |
| `pd.read_excel()` | Parses Excel `.xlsx`/`.xls` file into DataFrame | File path / Streamlit `UploadedFile` | `pd.DataFrame` | `data_processor.py` line 20 |
| `pd.to_datetime()` | Converts strings to DatetimeIndex | Date series, `errors="coerce"` | Datetime Series with `NaT` | `data_processor.py` line 44 |
| `pd.to_numeric()` | Converts strings to numbers | Rating series, `errors="coerce"` | Float/Int Series with `NaN` | `data_processor.py` line 48 |
| `.clip(1, 5)` | Clamps values to lower and upper bounds | Lower bound $1$, Upper bound $5$ | Bounded Series | `data_processor.py` line 50 |
| `.dropna()` | Removes rows with missing values in subset | `subset=["date"]`, `subset=["rating"]` | Filtered DataFrame | `data_processor.py` lines 45, 49 |
| `.fillna()` | Replaces `NaN` with default scalar value | `""` for text, `"Unknown"` for categoricals | Cleaned Series | `data_processor.py` lines 53, 57 |
| `.drop_duplicates()` | Removes duplicate rows matching subset keys | `subset=["feedback_id", "customer_name", "date", "feedback_text"]` | Deduplicated DataFrame | `data_processor.py` line 64 |
| `.sort_values()` | Sorts DataFrame by specified column | `"date"`, `ascending=True` | Sorted DataFrame | `data_processor.py` line 66 |
| `.reset_index()` | Resets row index to $0 \dots N-1$ | `drop=True` | Re-indexed DataFrame | `data_processor.py` line 66 |
| `.isin()` | Returns boolean mask for element matching | List/array of target values | Boolean Series | `data_processor.py` line 60 |
| `.loc[mask, col]` | Label-based indexing and conditional assignment | Boolean mask and column name | Target DataFrame subset | `data_processor.py` line 61 |
| `.groupby()` | Groups DataFrame by category or Grouper | Column name / `pd.Grouper` | GroupBy object | `data_processor.py` line 135 |
| `pd.Grouper()` | Groups time-series by frequency interval | `freq="W"` (Weekly) | Time grouping specification | `data_processor.py` line 135 |
| `.agg()` | Computes custom aggregations per group | `avg_rating=("rating", "mean"), feedback_count=("rating", "size")` | Aggregated DataFrame | `data_processor.py` line 147 |
| `.resample("ME")` | Resamples time-series at Month-End frequency | `"ME"` frequency string | Resampler object | `charts.py` line 89 |
| `.mean()` | Computes arithmetic average | Numeric Series | Float scalar | `data_processor.py` line 116 |
| `.value_counts()` | Computes frequency counts of unique values | Series (`rating`, `channel`, `sentiment`) | Count Series | `data_processor.py` lines 157, 165 |
| `.nunique()` | Counts distinct unique values | Series | Integer | `ml_sentiment.py` line 30 |
| `.to_csv()` | Serializes DataFrame to CSV string/bytes | `index=False` | CSV string / bytes | `app.py` line 230 |

---

# 7. DATA CLEANING DEEP DIVE

### 1. Missing Values
- **Definition:** Missing values (`NaN`, `NaT`, `None`, empty strings) occur when data was omitted or corrupted during entry.
- **How I Found Them:** Checked with `isna()`, `errors="coerce"`, and `.isin(["", "Unknown", "nan", "None"])`.
- **How I Handled Them:**
  - Critical fields (`date`, `rating`): dropped using `dropna(subset=[...])` because dates and ratings cannot be accurately imputed without skewing time-series and satisfaction metrics.
  - Text fields (`feedback_text`): imputed with `""` via `fillna("")`.
  - Categorical fields (`product`, `channel`, `region`): imputed with `"Unknown"` via `fillna("Unknown")`.
  - Sentiment: deterministically derived from star ratings via `rating_to_sentiment()`.

### 2. Duplicates
- **Definition:** Identical records recorded multiple times due to network retries, form double-submissions, or database export sync errors.
- **How I Found Them:** Applied `drop_duplicates(subset=["feedback_id", "customer_name", "date", "feedback_text"])`.
- **How I Handled Them:** Retained the first unique occurrence and eliminated redundant rows, preventing artificial volume inflation.

### 3. Incorrect Data Types
- **Definition:** Columns stored under improper data types (e.g., date strings stored as object strings, numbers stored as text).
- **How I Detected & Converted Them:**
  - Date strings coerced to `datetime64[ns]` via `pd.to_datetime(df["date"], errors="coerce")`.
  - Rating strings coerced to integers via `pd.to_numeric(df["rating"], errors="coerce").astype(int)`.

### 4. Inconsistent Values & Header Casing
- **Definition:** Structural inconsistencies across column casing and spacing (e.g., `"Customer Name "` vs `"customer_name"`).
- **How I Standardized Them:** Executed list comprehension `df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]`, normalizing all variations automatically.

### 5. Invalid Values
- **Definition:** Values outside legitimate domain constraints (e.g., star rating of `-5` or `98` on a 1–5 scale).
- **How I Handled Them:** Applied `.clip(1, 5)`. Negative values become 1; values above 5 become 5.

### 6. Outliers
- **Definition:** Extreme observations far removed from the mass of the distribution.
- **Handling in Code:** Star ratings are bounded discrete values in `[1, 5]`; standard 3-sigma outlier removal is not applied because all 1–5 ratings represent legitimate customer voices. Extreme anomalies in text length are handled by stripping whitespace.

---

# 8. DATA TRANSFORMATION DEEP DIVE

### Exact Transformations in Code

1. **Header Normalization:**
   - *Before:* `["Date", "Customer Name", "Product Tier", "Rating "]`
   - *Code:* `df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]`
   - *After:* `["date", "customer_name", "product_tier", "rating"]`
2. **Date Parsing:**
   - *Before:* String `"2025-06-12"` or `"invalid"`
   - *Code:* `df["date"] = pd.to_datetime(df["date"], errors="coerce")`
   - *After:* `Timestamp('2025-06-12 00:00:00')` or `NaT` (dropped)
3. **Rating Bounding:**
   - *Before:* Floats or invalid numbers `98`, `-1`, `"4.0"`
   - *Code:* `df["rating"] = pd.to_numeric(df["rating"], errors="coerce").clip(1, 5).astype(int)`
   - *After:* Integer `5`, `1`, `4`
4. **Sentiment Derivation Rule (Exact Code):**
   ```python
   def rating_to_sentiment(rating: int) -> str:
       if rating >= 4:
           return "Positive"
       if rating == 3:
           return "Neutral"
       return "Negative"
   ```
   - *Before:* `sentiment` is `""`, `"Unknown"`, or `NaN` with `rating = 5`
   - *After:* `sentiment = "Positive"`

---

# 9. EXPLORATORY DATA ANALYSIS (EDA)

### What is EDA?
**Exploratory Data Analysis (EDA)** is the analytical process of inspecting, summarizing, and visualizing datasets to understand their underlying distributions, detect anomalies, uncover relationships, and test initial hypotheses before formal modeling.

### What did I inspect in this project?
1. **Central Tendency & Spread:** Evaluated mean rating across products and standard deviation.
2. **Class Distribution:** Evaluated percentage of Positive (55.2%), Neutral (25.0%), and Negative (19.8%) feedback.
3. **Time-Series Volatility:** Grouped weekly sentiment trends to spot sudden negative spikes.
4. **Channel Discrepancies:** Compared feedback volumes and rating distributions across Email, Support Tickets, App Reviews, In-App Surveys, and Social Media.

---

# 10. STATISTICS CONCEPTS IN THE PROJECT

- **Mean ($\mu$):** `df["rating"].mean()` — Arithmetic average rating. Used in headline KPI and product rankings. Sensitive to extreme ratings.
- **Percentage (%):** Positive % = $(N_{\text{Positive}} / N_{\text{Total}}) \times 100$. Used in headline KPI metrics.
- **Frequency Distribution:** `df["rating"].value_counts().sort_index()` — Counts of discrete 1–5 ratings.
- **Median:** *[Not directly computed in active code; basic knowledge]* — The 50th percentile middle rating. Robust against extreme skewness.
- **Standard Deviation ($\sigma$):** *[Basic knowledge]* — Measures rating dispersion. High standard deviation on a product indicates bimodal customer polarization (many 1s and 5s).
- **Variance ($\sigma^2$):** *[Basic knowledge]* — Squared deviation from the mean rating.
- **Correlation ($r$):** *[Basic knowledge]* — Measures the linear association between continuous variables.

---

# 11. VISUALIZATION DEEP DIVE (6 CHARTS)

### 1. Sentiment Breakdown (Plotly Donut Chart)
- **Function:** `charts.sentiment_pie(df)`
- **Data Used:** Filtered `df["sentiment"].value_counts()`
- **Visual Design:** `px.pie(hole=0.45)` with fixed semantic palette (`Positive: #2ecc71`, `Neutral: #f1c40f`, `Negative: #e74c3c`).
- **Business Insight:** Shows overall voice-of-customer satisfaction share at a glance.
- **Why Donut over Bar?** Best for part-to-whole categorical proportion comparison.

### 2. Sentiment Trend Over Time (Plotly Multi-Line Chart)
- **Function:** `charts.sentiment_trend_line(trend_df)`
- **Data Used:** `dp.sentiment_over_time(filtered, freq="W")`
- **Visual Design:** `px.line(markers=True)` with 3 colored lines for Positive, Neutral, and Negative.
- **Business Insight:** Identifies weekly sentiment shifts, isolating post-release satisfaction drops.
- **Why Line Chart?** Displays continuous time-series trajectories and rate of change.

### 3. Rating Distribution (Plotly Bar Chart)
- **Function:** `charts.rating_bar(dist_df)`
- **Data Used:** `dp.rating_distribution(filtered)`
- **Visual Design:** `px.bar()` displaying discrete rating bars (1 through 5) with data labels.
- **Business Insight:** Reveals whether ratings follow a normal bell curve, a positive skew, or a polarized bimodal distribution.

### 4. Average Rating by Product (Plotly Horizontal Bar Chart)
- **Function:** `charts.product_rating_bar(product_df)`
- **Data Used:** `dp.top_products_by_rating(filtered)`
- **Visual Design:** `px.bar(orientation="h")` bounded to `[0, 5]` scale, sorted with highest-rated product on top.
- **Business Insight:** Ranks product portfolio performance, instantly identifying underperforming offerings.

### 5. Feedback by Channel (Plotly Donut Chart)
- **Function:** `charts.channel_donut(channel_df)`
- **Data Used:** `dp.channel_breakdown(filtered)`
- **Visual Design:** `px.pie(hole=0.45)` showing submission shares across channels.
- **Business Insight:** Identifies dominant customer communication channels to optimize support staffing.

### 6. Monthly Average Rating Trend (Matplotlib Static Line Chart)
- **Function:** `charts.matplotlib_summary(df)`
- **Data Used:** `df.set_index("date")["rating"].resample("ME").mean().dropna()`
- **Visual Design:** `ax.plot(monthly.index, monthly.values, marker="o", color="#2c3e50")`
- **Business Insight:** Macroeconomic monthly satisfaction trend; downloadable as a PNG for executive decks.

---

# 12. STREAMLIT FRAMEWORK & UI DEEP DIVE

### Streamlit Execution Model
- **Top-to-Bottom Execution:** Streamlit reruns `app.py` from top to bottom on every user interaction (filter click, upload, or button press).
- **Widgets Used in Code:**
  - `st.sidebar.file_uploader(type=["csv", "xlsx", "xls"])`: Interactive upload widget.
  - `st.sidebar.date_input()`: Two-value tuple date range selector.
  - `st.sidebar.multiselect()`: Multi-item dropdowns for Product, Channel, Region, Sentiment.
  - `st.columns(4)`: Responsive 4-column layout for headline KPI cards.
  - `st.metric()`: Formatted KPI cards displaying label and value.
  - `st.plotly_chart(use_container_width=True)`: Renders interactive Plotly figures.
  - `st.pyplot(fig)`: Renders static Matplotlib figures.
  - `st.download_button()`: Offers binary file downloads (CSV and PNG).
  - `st.expander()`: Collapsible container for optional ML playground.
  - `st.stop()`: Halts execution immediately when an unrecoverable error occurs.
  - `@st.cache_data`: Caches DataFrame return values in RAM based on input parameter hashes.

---

# 13. PLOTLY FUNCTIONS USED

- **`px.pie(counts, names="sentiment", values="count", color="sentiment", color_discrete_map=color_map, hole=0.45, template="plotly_white")`:**
  Constructs donut charts with specified color mappings and cutout holes.
- **`fig.update_traces(textinfo="percent+label")`:**
  Forces slice percentage and category labels to display inside chart segments.
- **`px.line(trend_df, x="date", y="count", color="sentiment", markers=True)`:**
  Renders interactive time-series line charts with circle markers at each weekly data point.
- **`px.bar(dist_df, x="rating", y="count", text="count")`:**
  Renders vertical bar charts with count labels above each bar.
- **`px.bar(product_df, x="avg_rating", y="product", orientation="h", hover_data=["feedback_count"])`:**
  Renders horizontal bar charts with hover tooltips displaying total feedback sample size.

---

# 14. MATPLOTLIB FUNCTIONS USED

- **`fig, ax = plt.subplots(figsize=(8, 4))`:**
  Initializes an explicit Matplotlib figure and single axes object.
- **`ax.plot(monthly.index, monthly.values, marker="o", color="#2c3e50", linewidth=2)`:**
  Plots continuous line chart connecting monthly average rating points.
- **`ax.set_title("Average Rating by Month")` & `ax.set_ylabel("Avg rating")`:**
  Sets chart title and vertical axis label.
- **`ax.set_ylim(1, 5)`:**
  Locks the vertical axis to the full 1–5 star rating scale.
- **`ax.grid(alpha=0.3)`:**
  Adds subtle gridlines at 30% opacity.
- **`fig.autofmt_xdate()`:**
  Rotates date labels on the horizontal axis to prevent overlap.
- **`fig.tight_layout()`:**
  Adjusts padding to prevent label clipping.
- **`fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")`:**
  Renders figure to in-memory binary stream at 150 DPI resolution.

---

# 15. BUSINESS INSIGHTS GENERATION

### Insight 1: Low Rating on Mobile App
- **Observation:** "Mobile App" average rating is 2.8/5, significantly below the portfolio average (3.78/5).
- **Investigation:** Filter by Product: Mobile App and inspect weekly sentiment trend and review text.
- **Possible Cause:** Review text frequently contains `"crashing"`, `"slow"`, and `"laggy"`, indicating mobile performance issues.
- **Business Action:** Allocate mobile engineering resources to memory optimization and stability bug fixes.
- **Expected Impact:** Mobile app rating improvement from 2.8 to 3.8+ within two release cycles.

### Insight 2: High Negative Feedback in Support Tickets
- **Observation:** "Support Ticket" channel has 45% negative feedback share.
- **Investigation:** Compare average rating across channels.
- **Possible Cause:** Inherent negative selection bias combined with complaints about response latency (`"took too long to respond"`).
- **Business Action:** Introduce automated tier-1 triage bots and expand support staffing during peak hours.
- **Expected Impact:** Reduction in negative support sentiment from 45% to under 25%.

---

# 16. INVESTIGATOR-STYLE SCENARIOS (20 SCENARIOS)

### Scenario 1: Product A Rating Decreases
- **Step 1 — Identify:** Headline average rating for Product A drops from 4.2 to 3.1 over a 30-day window.
- **Step 2 — Validate:** Verify that feedback volume is statistically significant ($N > 30$) and not caused by a single isolated complaint.
- **Step 3 — Investigate:** Filter by Product A and review negative text comments to identify recurring keywords.
- **Step 4 — Action:** Escalate root cause (e.g., recent UI update) to the product engineering lead.
- **Interview Answer:** *"I first validate volume to confirm statistical significance, then slice by channel and date to isolate when the drop began, and inspect feedback text for recurring bug patterns."*
- **Follow-Up:** *What chart shows the drop fastest?*
  **Answer:** The weekly `sentiment_trend_line` and monthly `matplotlib_summary` charts.

### Scenario 2: High Rating Variance on Enterprise Plan
- **Step 1 — Identify:** Rating Distribution bar chart for Enterprise Plan shows many 1s and 5s with zero 3s.
- **Step 2 — Validate:** Confirm bimodal distribution across multiple regions.
- **Step 3 — Investigate:** Check if negative ratings originate from a specific region or integration channel.
- **Step 4 — Action:** Schedule direct customer success check-ins with dissatisfied enterprise accounts.
- **Interview Answer:** *"A bimodal distribution indicates polarized satisfaction: the core product delivers value (5 stars), but a critical flaw (like billing or SSO login) causes severe 1-star complaints."*
- **Follow-Up:** *Why is mean rating misleading here?*
  **Answer:** An average of 3.0 hides the fact that zero users had an average experience; users either loved or hated the product.

### Scenario 3: Spike in Negative Feedback After Release
- **Step 1 — Identify:** Negative sentiment line in `sentiment_trend_line` jumps from 15% to 50% in Week 24.
- **Step 2 — Validate:** Cross-reference Week 24 date with the engineering release calendar.
- **Step 3 — Investigate:** Extract feedback text for Week 24 to isolate breaking release bugs.
- **Step 4 — Action:** Issue a hotfix patch or roll back the problematic release.
- **Interview Answer:** *"I align the date inflection on the weekly trend chart with release deployment timestamps to confirm cause-and-effect."*

### Scenario 4: User Upload Contains Rating "98"
- **Step 1 — Identify:** User uploads a CSV with typos like `98`.
- **Step 2 — Validate:** `clean_data()` identifies out-of-bounds numbers via `to_numeric()`.
- **Step 3 — Investigate:** Check if `98` was intended as a percentage (98/100) or typo.
- **Step 4 — Action:** `.clip(1, 5)` clamps the value to 5, preserving positive intent while protecting the scale.
- **Interview Answer:** *"Our data cleaning layer uses `.clip(1, 5)` to bound numeric ratings to the valid 1–5 scale, preventing calculation distortion."*

### Scenario 5: Review Text Contradicts 5-Star Rating
- **Step 1 — Identify:** Review text says `"Terrible billing issues, never using again"` with a 5-star rating.
- **Step 2 — Validate:** `ml.compare_with_rule_based()` flags `agrees_with_rule == False`.
- **Step 3 — Investigate:** Review flagged anomalies in the ML contradiction table.
- **Step 4 — Action:** Re-classify row for customer support follow-up.
- **Interview Answer:** *"We use our TF-IDF + Logistic Regression model to flag reviews where text sentiment contradicts star ratings, catching sarcasm or accidental 5-star taps."*

### Scenario 6: Missing Dates in 30% of Uploaded Rows
- **Step 1 — Identify:** `clean_data()` drops 30% of rows due to unparseable dates.
- **Step 2 — Validate:** Sidebar warning alerts user: `"Loaded X of Y rows (dropped unparseable dates)"`.
- **Step 3 — Investigate:** Check date format in raw file (e.g., non-standard epoch timestamps).
- **Step 4 — Action:** Notify data engineering team to standardize source export date formats.

### Scenario 7: All Ratings in Dataset Are 5 Stars
- **Step 1 — Identify:** Rating distribution bar chart shows 100% volume at 5 stars.
- **Step 2 — Validate:** Average rating is 5.0; ML module returns single-class warning.
- **Step 3 — Investigate:** Check sampling methodology (e.g., survey only triggered after successful purchase).
- **Step 4 — Action:** Advise business to trigger surveys at neutral touchpoints to capture unbiased feedback.

### Scenario 8: Support Ticket Channel Has 2.1 Average Rating
- **Step 1 — Identify:** Horizontal bar chart shows Support Tickets ranked lowest.
- **Step 2 — Validate:** Check if this is channel selection bias or operational failure.
- **Step 3 — Investigate:** Compare against email survey ratings for the same product.
- **Step 4 — Action:** Optimize support response times and ticket resolution workflows.

### Scenario 9: Duplicate Submissions from Webhook Error
- **Step 1 — Identify:** Raw upload contains 1,200 rows; cleaned dataset contains 600 rows.
- **Step 2 — Validate:** `drop_duplicates()` identifies duplicate composite keys.
- **Step 3 — Investigate:** Confirm identical customer names, dates, and text strings.
- **Step 4 — Action:** Clean data automatically and patch webhook retry logic.

### Scenario 10: Ratings Stored as Text Strings ("5", "4.0", "N/A")
- **Step 1 — Identify:** `clean_data()` encounters object dtype in `rating` column.
- **Step 2 — Validate:** `pd.to_numeric(errors="coerce")` converts valid strings to numbers and text to `NaN`.
- **Step 3 — Investigate:** Valid ratings are cast to integers; corrupt rows dropped.
- **Step 4 — Action:** Dataset cleaned seamlessly without app crash.

### Scenario 11: APAC Region Experiences Sharp Rating Drop
- **Step 1 — Identify:** Slicing by Region: APAC reveals average rating drop to 2.4.
- **Step 2 — Validate:** Confirm drop across all products in APAC.
- **Step 3 — Investigate:** Check text for mentions of server latency, language translation, or currency billing.
- **Step 4 — Action:** Deploy local APAC edge server infrastructure and local payment gateways.

### Scenario 12: Basic Plan Negative Sentiment Spikes After Price Increase
- **Step 1 — Identify:** Basic Plan negative sentiment % increases from 12% to 48%.
- **Step 2 — Validate:** Date aligns with pricing change announcement.
- **Step 3 — Investigate:** Review feedback text for price-sensitivity complaints.
- **Step 4 — Action:** Introduce grandfathered pricing or enhance Basic Plan feature limits.

### Scenario 13: Zero Rows Match Selected Filters
- **Step 1 — Identify:** User selects mutually exclusive filters (e.g., non-existent product-channel pair).
- **Step 2 — Validate:** `filtered.empty == True`.
- **Step 3 — Investigate:** `compute_kpis()` catches empty DataFrame and returns safe zeros.
- **Step 4 — Action:** Chart containers display `st.info("No data for current filters")` without crashing.

### Scenario 14: Sarcastic Review Detection
- **Step 1 — Identify:** Review: `"Oh fantastic, another crash while saving my work!"` with 5 stars.
- **Step 2 — Validate:** Star rating rule maps to Positive; TF-IDF bigrams (`"another crash"`) predict Negative.
- **Step 3 — Investigate:** ML contradiction detector isolates row for manual review.
- **Step 4 — Action:** Re-assign sentiment to Negative and log bug ticket.

### Scenario 15: Product With High Rating but Low Volume
- **Step 1 — Identify:** "Browser Extension" has a 4.8 rating but only 12 reviews.
- **Step 2 — Validate:** Compare against Pro Plan with a 4.1 rating on 350 reviews.
- **Step 3 — Investigate:** High score may suffer from low sample size bias.
- **Step 4 — Action:** Do not declare Browser Extension as the best product until sample size reaches $N \ge 100$.

### Scenario 16: Monthly Trend Shows Gradual Decay
- **Step 1 — Identify:** Matplotlib monthly trend chart shows steady decline from 4.5 in Jan to 3.2 in June.
- **Step 2 — Validate:** Confirm downward trend across multiple products.
- **Step 3 — Investigate:** Indicates accumulating technical debt or worsening customer support backlogs.
- **Step 4 — Action:** Executive leadership initiates quality-focused stabilization sprint.

### Scenario 17: User Uploads Excel File (.xlsx)
- **Step 1 — Identify:** User uploads `.xlsx` spreadsheet instead of CSV.
- **Step 2 — Validate:** `load_data()` detects `.xlsx` extension.
- **Step 3 — Investigate:** Routes parsing to `pd.read_excel()` using `openpyxl`.
- **Step 4 — Action:** Ingests data seamlessly without user conversion.

### Scenario 18: Feedback Text Contains International Characters & Emojis
- **Step 1 — Identify:** Customer reviews include UTF-8 characters and emojis (e.g., "Love it! ❤️").
- **Step 2 — Validate:** Text cleaning preserves unicode encoding.
- **Step 3 — Investigate:** CSV export uses `encode('utf-8')`.
- **Step 4 — Action:** Data exported cleanly without corrupting symbols.

### Scenario 19: Missing Product Names in Feedback
- **Step 1 — Identify:** Raw CSV contains blank product entries.
- **Step 2 — Validate:** `clean_data()` imputes missing products with `"Unknown"`.
- **Step 3 — Investigate:** Allows filtering on `"Unknown"` product segment without dropping rows.
- **Step 4 — Action:** Review unassigned tickets to trace origin.

### Scenario 20: Stakeholders Disagree on Action Priorities
- **Step 1 — Identify:** Sales team argues Pro Plan is fine; Support team argues it is broken.
- **Step 2 — Validate:** Filter by Pro Plan: Support Tickets show 2.4 rating; In-App Surveys show 4.5 rating.
- **Step 3 — Investigate:** Proves core functionality works, but onboarding/billing generates support friction.
- **Step 4 — Action:** Align teams around objective channel-segmented data to fix onboarding workflows.

---

# 17. DEFINITION QUESTIONS (MASTER GLOSSARY)

- **Data:** Raw, unformatted facts, statistics, and observations collected for reference or analysis.
- **Dataset:** A structured collection of data organized into tables with rows and columns.
- **Data Cleaning:** The process of detecting and correcting corrupted, inaccurate, missing, or irrelevant records from a dataset.
- **Data Transformation:** Converting data from one format, type, or structure into another to facilitate analysis.
- **Data Analysis:** Inspecting, cleansing, transforming, and modeling data to discover useful information and support decision-making.
- **Data Analytics:** The systematic computational analysis of data or statistics to identify trends and patterns.
- **EDA (Exploratory Data Analysis):** The critical initial step of analyzing datasets to summarize main characteristics, uncover distributions, and test hypotheses visually.
- **DataFrame:** A two-dimensional, size-mutable, tabular data structure with labeled axes (rows and columns) in Pandas.
- **Series:** A one-dimensional labeled array in Pandas capable of holding data of any type.
- **Missing Value:** The absence of a data value for a variable in an observation (represented as `NaN`, `NaT`, or `None`).
- **Duplicate:** An identical or redundant observation recorded multiple times in a dataset.
- **Outlier:** A data point that differs significantly from other observations in a dataset.
- **Mean:** The arithmetic average calculated by dividing the sum of values by the total count.
- **Median:** The 50th percentile value separating the higher half from the lower half of a dataset.
- **Mode:** The most frequently occurring value in a dataset.
- **Variance:** A statistical measurement of the spread between numbers in a data set from their average value.
- **Standard Deviation:** The square root of variance, measuring the dispersion of data points around the mean.
- **Correlation:** A statistical measure expressing the extent to which two variables change together linearly.
- **Sentiment:** An attitude, emotion, or opinion expressed in text or ratings (Positive, Neutral, Negative).
- **Visualization:** The graphical representation of data and information using charts, graphs, and maps.
- **Dashboard:** A visual interface displaying key performance indicators (KPIs) and metrics to track organizational health.
- **Streamlit:** An open-source Python framework used to build interactive web data applications rapidly.
- **Plotly:** An interactive graphing library that creates vector charts with hover tooltips and dynamic zooming.
- **Matplotlib:** A comprehensive Python plotting library for creating static, publication-quality figures.
- **Python:** A high-level, interpreted, general-purpose programming language widely used in data science and web development.
- **Pandas:** A fast, powerful, and flexible open-source data manipulation and analysis library for Python.

---

# 18. "WHY DID YOU USE X?" DEFENSE GUIDE

- **Why Python?** Best data science ecosystem, extensive libraries (Pandas, Scikit-Learn), and rapid prototyping.
- **Why Pandas?** Vectorized operations allow high-performance data cleaning, type coercion, time-series bucketing, and grouping.
- **Why DataFrame?** Provides structured 2D tabular representation with labeled rows and columns, matching real-world spreadsheets.
- **Why Streamlit?** Allows building full-stack reactive data web apps purely in Python without frontend boilerplate.
- **Why Plotly?** Provides out-of-the-box web interactivity (hover data labels, zooming, responsive resizing).
- **Why Matplotlib?** Generates static, publication-quality figures that export reliably to PNG byte buffers for executive slides and PDF reports.
- **Why a Dashboard?** Enables non-technical decision-makers to explore data visually without writing SQL or Python code.
- **Why Visualization?** Visual patterns (like bimodal distributions or downward trends) are recognized 10x faster than raw spreadsheet numbers.
- **Why EDA?** Prevents building models on corrupted data, validates assumptions, and uncovers underlying distributions.
- **Why Mean?** Gives the exact arithmetic portfolio satisfaction benchmark across ratings.
- **Why Standard Deviation?** Highlights polarized products where customers are split between 1-star and 5-star ratings.
- **Why Rule-Based Sentiment Baseline?** Instant, free, 100% consistent, and fully explainable baseline derived directly from star ratings.
- **Why Clean Data First?** Garbage in, garbage out: downstream KPIs, charts, and ML models are completely invalid without clean data.

---

# 19. "WHAT IF?" QUESTIONS

- **What if 20% of ratings are missing in an upload?**
  `clean_data()` drops the unrated rows via `dropna(subset=["rating"])`, surfaces a sidebar warning, and computes KPIs on surviving valid rows.
- **What if all ratings in the dataset are 5 stars?**
  The KPI displays 5.0 / 5; the ML module surfaces a warning that at least 2 distinct sentiment classes are required to train a model.
- **What if a rating value is 98?**
  `.clip(1, 5)` clamps the value to 5, preserving positive intent while protecting scale integrity.
- **What if duplicate records exist?**
  `drop_duplicates()` removes redundant rows matching on customer name, date, and text, keeping the first occurrence.
- **What if mean and median diverge significantly?**
  Indicates heavy skewness; a low mean with a high median means a small group of severe 1-star reviews is pulling down the average.
- **What if standard deviation is very high for a product?**
  Signals a bimodal distribution; customers love the product (5 stars) or hate a critical bug (1 star).
- **What if one channel performs poorly?**
  Investigate channel-specific friction (e.g., support ticket response times) rather than blaming product quality.
- **What if the dataset is completely empty?**
  `clean_data()` returns empty DataFrame; `app.py` catches `df.empty`, shows an error notification, and calls `st.stop()`.

---

# 20. PROJECT CHALLENGES & RESOLUTIONS

1. **Pandas Frequency Alias Deprecation (`'M'` $\rightarrow$ `'ME'`):**
   - *What Went Wrong:* Pandas 2.2+ raised `FutureWarning` and broke time-series resampling in `matplotlib_summary()`.
   - *How I Solved It:* Refactored code to use `'ME'` (Month End), preserving weekly `'W'` frequencies.
2. **Handling Diverse Upload Formats (CSV vs Excel):**
   - *What Went Wrong:* Users uploaded `.xlsx` files that failed standard CSV readers.
   - *How I Solved It:* Built automatic extension routing in `load_data()` using `openpyxl`.
3. **Preventing Silent Data Loss on Bad Uploads:**
   - *What Went Wrong:* If all rows failed cleaning, the app originally showed empty graphs without explanation.
   - *How I Solved It:* Added pre-cleaning and post-cleaning row count comparisons, surfacing explicit warnings and invoking `st.stop()`.
4. **Non-Destructive Missing Sentiment Derivation:**
   - *What Went Wrong:* Deriving missing sentiment without overwriting pre-labeled rows or raising `SettingWithCopyWarning`.
   - *How I Solved It:* Implemented conditional boolean masking via `df.loc[missing_sentiment, "sentiment"] = ...`.
5. **Managing Streamlit Script Rerun Performance:**
   - *What Went Wrong:* Streamlit reruns scripts on every UI interaction, causing redundant disk reads.
   - *How I Solved It:* Wrapped data loading in `@st.cache_data` to cache DataFrames in RAM.

---

# 21. PROJECT LIMITATIONS

1. **In-Memory Session Storage:**
   - *Limitation:* Data lives in RAM as a Pandas DataFrame; changes do not persist across app restarts.
   - *Impact:* Historical trends across separate sessions cannot be saved without re-uploading.
   - *Improvement:* Connect to a persistent database (PostgreSQL / SQLite).
2. **Rule-Based Sentiment Nuances:**
   - *Limitation:* Rating-based heuristics cannot detect subtle sarcasm in review text.
   - *Impact:* A sarcastic 5-star review is labeled Positive by default.
   - *Improvement:* Layer the scikit-learn ML model or an LLM pipeline to flag rating-text contradictions.
3. **Synthetic Dataset Template Bias:**
   - *Limitation:* Synthetic sample data uses repeated sentence templates, causing text classifiers to achieve near 100% accuracy.
   - *Impact:* High accuracy reflects template learning rather than real-world generalization.
   - *Improvement:* Benchmark on real-world, messy customer feedback datasets.
4. **Single-Node Execution:**
   - *Limitation:* Designed for single-user analytics; datasets larger than server RAM cannot be loaded.
   - *Improvement:* Migrate heavy aggregations to DuckDB or Polars.

---

# 22. FUTURE IMPROVEMENTS ROADMAP

### [IMPLEMENTED]
- Reusable, decoupled data cleaning and aggregation engine (`data_processor.py`).
- 5 interactive Plotly charts and 1 static Matplotlib exportable chart (`charts.py`).
- Multi-criteria dynamic filtering, headline KPIs, and CSV data export (`app.py`).
- Performance caching via `@st.cache_data`.
- TF-IDF + Logistic Regression text sentiment model with negation preservation (`ml_sentiment.py`).
- Rating vs Text contradiction anomaly detector.

### [OPTIONAL / EXPERIMENTAL]
- Hugging Face DistilBERT deep learning sentiment pipeline (`hf_sentiment.py`).

### [PLANNED / NOT IMPLEMENTED]
- **Persistent Database:** SQLite / PostgreSQL storage to save uploads and filter presets across sessions.
- **Automated PDF Executive Report Generator:** Compiles KPIs, charts, and top customer complaints into a formatted PDF.
- **Thematic Clustering / Topic Modeling:** Uses LDA or BERTopic to group complaints into automatic categories (e.g., "Billing", "UI Lag", "Login Bug").
- **Live Webhook Ingestion:** Connects directly to Zendesk, App Store, and Stripe APIs for real-time streaming feedback ingestion.

---

# 23. RAPID REVISION TABLE

| Term | Definition | How I Used It | Scenario |
|---|---|---|---|
| **Pandas** | Tabular data manipulation library in Python. | Core engine for all cleaning, filtering, and aggregation. | Cleaning corrupted CSV uploads. |
| **Streamlit** | Reactive Python framework for data web apps. | Presentation and orchestration layer (`app.py`). | Building interactive filters and KPI cards. |
| **Plotly** | Interactive vector charting library. | 5 interactive charts (donut, trend line, bars). | Hovering over data points for sample size counts. |
| **Matplotlib** | Static plotting library in Python. | Monthly average rating trend chart with PNG export. | Downloading chart image for executive slides. |
| **`@st.cache_data`** | Streamlit function caching decorator. | Caches dataset loading across reruns in RAM. | Preventing disk re-reads on filter clicks. |
| **`openpyxl`** | Python library for reading Excel `.xlsx` files. | Dependency used by `pd.read_excel()` in `load_data()`. | Ingesting Excel spreadsheet exports. |
| **`errors="coerce"`** | Parameter converting invalid entries to `NaN`/`NaT`. | Used in `pd.to_datetime()` and `pd.to_numeric()`. | Handling corrupt dates and text ratings. |
| **`.clip(1, 5)`** | Clamps numbers to lower/upper bounds. | Bounding ratings in `clean_data()`. | Correcting invalid ratings like `98`. |
| **`pd.Grouper`** | Time-series grouping operator for dual-axis aggregation. | Used in `sentiment_over_time(freq="W")`. | Aggregating weekly sentiment volume. |
| **`resample("ME")`** | Resamples DatetimeIndex at Month-End frequency. | Used in `matplotlib_summary()` for monthly averages. | Plotting monthly rating trajectories. |
| **`io.BytesIO`** | In-memory binary stream buffer. | Saves Matplotlib PNG figures for download button. | Exporting charts without disk I/O. |
| **TF-IDF** | Term Frequency-Inverse Document Frequency. | Extracts n-gram features in `modules/ml_sentiment.py`. | Text feature extraction for review sentiment. |
| **Logistic Regression** | Linear classification algorithm predicting class probabilities. | Trained on TF-IDF features to predict sentiment. | Classifying text reviews into Positive/Neutral/Negative. |
| **Precision** | $\text{TP} / (\text{TP} + \text{FP})$ — Accuracy of positive predictions. | Evaluated in `ml_sentiment.py` classification report. | Minimizing false alarms in negative reviews. |
| **Recall** | $\text{TP} / (\text{TP} + \text{FN})$ — Fraction of true positives captured. | Evaluated in `ml_sentiment.py` classification report. | Catching 100% of angry customer complaints. |
| **F1-Score** | Harmonic mean of precision and recall. | Balances precision and recall on sentiment classes. | Evaluating model performance on imbalanced data. |
| **`drop_duplicates`** | Removes redundant rows matching subset keys. | Eliminates duplicate submissions in `clean_data()`. | Dropping double-clicked survey submissions. |
| **`st.stop()`** | Halts Streamlit script execution immediately. | Prevents crashes when uploaded data has 0 valid rows. | Halting execution on unparseable files. |
| **Bimodal Distribution**| A distribution with two distinct peaks. | Occurs when ratings split between 1s and 5s. | Identifying polarized customer satisfaction. |
| **Decision Science** | Transforming data and models into business decisions. | Core methodology connecting charts to business actions. | Prioritizing engineering bug fixes from review trends. |

---

# 24. AI BOT FOLLOW-UP TREE

```
Tell Me About Yourself
│
├── Data Analytics & Decision Science
│   ├── What is decision science? ────────► Transforming raw data into structured business decisions
│   ├── Explain your project approach ────► Resilient Ingestion → Deterministic Cleaning → Visual Storytelling → ML Validation
│   └── How do you prioritize metrics? ───► Volume impact first, followed by rating variance and trend direction
│
├── Python & Pandas Ecosystem
│   ├── Why Pandas? ──────────────────────► Vectorized operations, clean time-series APIs, and missing-value coercion
│   ├── How do you handle messy data? ───► errors='coerce', clipping [1, 5], dropna, and composite deduplication
│   └── Explain @st.cache_data ───────────► In-memory caching based on input parameter hashing to avoid disk I/O
│
├── Customer Feedback Dashboard Architecture
│   ├── 3-layer design? ─────────────────► Decoupled data_processor.py, charts.py, and app.py
│   ├── Why Plotly & Matplotlib? ────────► Plotly for interactive web UI; Matplotlib for static PNG reports
│   └── How does filtering work? ────────► Multi-column boolean masks (&) across date ranges and categories
│
└── Machine Learning & NLP
    ├── Why TF-IDF + Logistic Regression? ► Lightweight, explainable, fast, and runs without GPU overhead
    ├── Why preserve negation words? ─────► Retains 'not' and 'never' so 'not good' is classified as Negative
    └── What are rating contradictions? ──► Sarcasm or user errors where 5-star ratings contain negative text
```

---

# 25. FINAL 50 QUESTIONS & SHORT ANSWERS

1. **What is the project objective?** Clean, analyze, visualize, and model multi-channel customer feedback to support business decisions.
2. **What is the tech stack?** Python, Pandas, Streamlit, Plotly, Matplotlib, Scikit-Learn, openpyxl.
3. **What architecture is used?** 3-layer decoupled design: Data Layer (`data_processor.py`), Visualization Layer (`charts.py`), UI Layer (`app.py`).
4. **Why separate data logic from UI?** To ensure business logic is pure, unit-testable, and reusable across any web framework.
5. **How are files loaded?** `load_data()` routes `.xlsx`/`.xls` to `pd.read_excel()` and `.csv` to `pd.read_csv()`.
6. **Why is openpyxl needed?** Pandas requires `openpyxl` as its engine dependency to decode XML-based `.xlsx` files.
7. **How are column names normalized?** Lowercased, stripped of spaces, and converted to snake_case (`c.strip().lower().replace(" ", "_")`).
8. **What if a required column is missing?** `clean_data()` initializes missing required columns with `pd.NA`.
9. **How are dates cleaned?** `pd.to_datetime(df["date"], errors="coerce")` followed by `dropna(subset=["date"])`.
10. **What does `errors="coerce"` do?** Converts unparseable strings to `NaT` or `NaN` without raising exceptions.
11. **How are ratings validated?** Coerced to numeric, dropped if missing, and clamped with `.clip(1, 5).astype(int)`.
12. **Why clip ratings to `[1, 5]`?** Preserves positive/negative intent while protecting statistical calculations from typos like 98.
13. **How are duplicates handled?** `df.drop_duplicates(subset=["feedback_id", "customer_name", "date", "feedback_text"])`.
14. **How is missing sentiment derived?** Heuristic: 4–5 $\rightarrow$ Positive, 3 $\rightarrow$ Neutral, 1–2 $\rightarrow$ Negative.
15. **How does `.loc` prevent bugs in sentiment derivation?** It conditionally updates only blank rows without overwriting valid data or raising `SettingWithCopyWarning`.
16. **How are headline KPIs computed?** `compute_kpis()` calculates Total, Avg Rating, Positive %, and Negative %.
17. **How is zero-division prevented in KPIs?** Returns safe zeros if `df.empty` before dividing.
18. **How is weekly trend calculated?** Groups by `pd.Grouper(freq="W")` and `"sentiment"`.
19. **How is monthly rating trend calculated?** Resamples DatetimeIndex at Month-End frequency with `.resample("ME").mean()`.
20. **Why was `"M"` replaced with `"ME"`?** In Pandas 2.2+, `"M"` was deprecated to separate period frequencies from timestamp offsets.
21. **What charts are built with Plotly?** Sentiment donut, weekly trend line, rating bar, horizontal product ranking, and channel donut.
22. **Why use Matplotlib alongside Plotly?** To generate static report figures that export cleanly to PNG buffers for slide decks.
23. **How is PNG export handled?** Matplotlib saves to an in-memory `io.BytesIO()` buffer passed to `st.download_button()`.
24. **Why avoid writing temporary PNG files to disk?** Eliminates disk I/O latency, permission errors, and server storage accumulation.
25. **What is `@st.cache_data`?** Caches function outputs in RAM based on input parameter hashes, speeding up UI reruns.
26. **What is Streamlit's execution model?** Reruns the entire Python script top-to-bottom on every widget interaction.
27. **What does `st.stop()` do?** Halts script execution immediately when unrecoverable data errors occur.
28. **What ML model is implemented?** TF-IDF Vectorizer with unigrams/bigrams + Logistic Regression.
29. **Why preserve negation stop words?** Retains `"not"`, `"no"`, and `"never"` so phrases like `"not good"` are classified as Negative.
30. **What is TF-IDF?** Term Frequency $\times$ Inverse Document Frequency; measures word importance relative to a corpus.
31. **What is Precision?** $\text{TP} / (\text{TP} + \text{FP})$ — Accuracy of positive predictions.
32. **What is Recall?** $\text{TP} / (\text{TP} + \text{FN})$ — Fraction of true positive samples captured.
33. **What is F1-Score?** Harmonic mean of precision and recall.
34. **What is `stratify=y` in train_test_split?** Preserves class distribution proportions across train and test sets.
35. **How are rating-text contradictions detected?** `compare_with_rule_based()` flags rows where `sentiment != ml_sentiment`.
36. **Why does high ML accuracy occur on synthetic data?** The synthetic dataset uses repeated sentence templates that the model memorizes.
37. **What is a bimodal distribution in feedback?** Ratings clustering at 1 and 5 stars with few 3-stars, indicating customer polarization.
38. **What is the difference between mean and median?** Mean is sensitive to outliers; median represents the 50th percentile.
39. **Why does the support ticket channel have lower ratings?** Channel selection bias: customers only open tickets when experiencing problems.
40. **How do you normalize for channel bias?** Track sentiment trends within each channel individually over time.
41. **How is filtered data exported?** `st.download_button()` containing `filtered.to_csv(index=False).encode('utf-8')`.
42. **Why encode CSV export as UTF-8?** Preserves international characters and emojis in review text.
43. **What is stored in session state?** Trained ML vectorizers and models to allow real-time custom sentence testing.
44. **What is the optional Hugging Face module?** `modules/hf_sentiment.py` uses DistilBERT fine-tuned on SST-2 for deep learning sentiment classification.
45. **What are the limitations of the project?** In-memory session storage, synthetic template bias, and single-node architecture.
46. **What is the planned future persistence layer?** PostgreSQL / SQLite database with user accounts and saved filter presets.
47. **How do you translate insights into business action?** Identify struggling products/channels, isolate root causes in text, and deploy engineering fixes.
48. **How do you measure business ROI?** Track reduction in negative feedback % and sustained increases in 30-day moving average ratings.
49. **Why is deterministic data cleaning prioritized?** Garbage in, garbage out: downstream KPIs and ML models are worthless without clean data.
50. **What makes you a good fit for Mu Sigma?** Strong foundational data engineering, statistical rigor, clear visual communication, and decision-driven problem solving.

---

# 26. FINAL ONE-DAY CHEAT SHEET

### Project in 30 Seconds
> *"An interactive data analytics platform built with Python, Pandas, Streamlit, Plotly, and Scikit-Learn that automates messy customer feedback cleaning, computes headline business KPIs, renders 6 interactive and report-ready charts, and classifies sentiment using both deterministic rules and TF-IDF machine learning."*

### Architecture in One Line
> *"3-layer decoupled architecture: pure Pandas Data Layer (`data_processor.py`), pure visualization Chart Layer (`charts.py`), and a reactive Streamlit UI Orchestration Layer (`app.py`)."*

### Data Cleaning in 5 Words
> *"Normalize, coerce, clip, deduplicate, derive."*

### Key Formulas to Memorize
- **Rating Derivation:** $4\text{--}5 \rightarrow \text{Positive}$, $3 \rightarrow \text{Neutral}$, $1\text{--}2 \rightarrow \text{Negative}$.
- **Rating Bounding:** $\text{rating} = \min(5, \max(1, \text{rating}))$.
- **Positive %:** $(N_{\text{Positive}} / N_{\text{Total}}) \times 100$.
- **Precision:** $\text{TP} / (\text{TP} + \text{FP})$.
- **Recall:** $\text{TP} / (\text{TP} + \text{FN})$.
- **F1-Score:** $2 \times (\text{Precision} \times \text{Recall}) / (\text{Precision} + \text{Recall})$.

### Top 5 Mistakes to Avoid in Interview
1. **Never claim you used an external SQL server in this project:** The app operates in-memory for fast slicing and exports a normalized Star Schema for Power BI.
2. **Never claim 100% real-world text model accuracy:** The ~100% accuracy on sample data is due to synthetic template memorization.
3. **Never confuse correlation with causation:** A price change correlating with negative sentiment requires validation against review text.
4. **Never say you drop outliers blindly in feedback ratings:** 1-star ratings are legitimate customer feedback, not measurement errors.
5. **Never forget why negation stop words were preserved:** Default stop words remove `"not"`, which turns `"not good"` into `"good"`.

---

# 27. POWER BI ENTERPRISE INTEGRATION & DAX MASTER CHEAT SHEET

### 1. Why Integrate Power BI with Python Analytics?
- **Python's Superpower:** Ingestion of corrupt files, advanced regex text cleaning, custom NLP machine learning (TF-IDF + negation stop-words), and anomaly contradiction detection.
- **Power BI's Superpower:** Self-service executive reporting, interactive slicing, sub-second aggregations via the in-memory **VertiPaq** columnar engine, enterprise Row-Level Security (RLS), and scheduled cloud refresh.
- **The Synergy:** Python cleans and enriches the messy feedback into a normalized **Star Schema**; Power BI models the data and serves interactive decision dashboards to non-technical executives.

### 2. Star Schema vs. Flat Table in Power BI
- **Why NOT a flat single table?** In Power BI, repeating long strings (like product descriptions and review text) in every row degrades VertiPaq dictionary encoding and inflates RAM usage.
- **Star Schema Design:**
  - **`Fact_CustomerFeedback`:** Numeric foreign keys (`DateKey`, `ProductKey`, `ChannelKey`, `RegionKey`, `SentimentKey`), facts (`Rating`, `FeedbackLength`), and boolean flags (`IsPromoter`, `IsPassive`, `IsDetractor`).
  - **Dimension Tables:** `Dim_Date`, `Dim_Product`, `Dim_Channel`, `Dim_Region`, `Dim_Sentiment`.
  - **Relationship Cardinality:** 1-to-many ($1 \rightarrow *$) with Single Cross-Filter Direction, preventing ambiguous filter propagation and circular dependencies.

### 3. Core DAX Formulas (Memorize for Interview)
- **Net Promoter Score (NPS) [-100 to +100]:**
  $$\text{NPS} = \frac{\text{Promoters (4-5\text{ stars})} - \text{Detractors (1-2\text{ stars})}}{\text{Total Feedback}} \times 100$$
  ```dax
  NPS Score = 
  VAR TotalCount = COUNTROWS(Fact_CustomerFeedback)
  VAR Promoters = CALCULATE(COUNTROWS(Fact_CustomerFeedback), Fact_CustomerFeedback[IsPromoter] = 1)
  VAR Detractors = CALCULATE(COUNTROWS(Fact_CustomerFeedback), Fact_CustomerFeedback[IsDetractor] = 1)
  RETURN
  IF(TotalCount > 0, ROUND(DIVIDE(Promoters - Detractors, TotalCount, 0) * 100, 1), 0)
  ```
- **Customer Satisfaction (CSAT %):**
  ```dax
  CSAT Percentage = 
  DIVIDE(
      CALCULATE(COUNTROWS(Fact_CustomerFeedback), Fact_CustomerFeedback[IsPromoter] = 1),
      COUNTROWS(Fact_CustomerFeedback),
      0
  )
  ```
- **Month-over-Month (MoM) Rating Delta (Time Intelligence):**
  ```dax
  MoM Rating Delta = 
  VAR CurrentAvg = AVERAGE(Fact_CustomerFeedback[Rating])
  VAR PriorAvg = CALCULATE(AVERAGE(Fact_CustomerFeedback[Rating]), PREVIOUSMONTH(Dim_Date[Date]))
  RETURN
  IF(ISBLANK(PriorAvg), BLANK(), CurrentAvg - PriorAvg)
  ```

### 4. Key Power BI Concepts Asked in Interviews
1. **Calculated Columns vs. Measures:**
   - *Calculated Column:* Evaluated during data refresh, stored row-by-row in RAM, uses row context.
   - *Measure:* Evaluated on-the-fly at query time, consumes no RAM storage, responds dynamically to slicer/filter context.
2. **Import Mode vs. DirectQuery:**
   - *Import Mode:* Data loaded into Power BI RAM (VertiPaq). Blazing fast performance; supports full DAX library.
   - *DirectQuery:* Queries remain in underlying database; data is not imported. Ideal for multi-billion-row real-time telemetry.
3. **Row-Level Security (RLS):**
   - Restricts data visibility by user identity using `USERPRINCIPALNAME()`. For example, Regional Managers only see records where `Dim_Region[RegionName] = LOOKUPVALUE(...)`.
4. **Decomposition Tree:**
   - An AI-powered Power BI visual used to break down Detractors (1-2 stars) across dimensions to isolate root-cause bottlenecks (e.g., Detractors $\rightarrow$ Mobile App $\rightarrow$ MEA Region $\rightarrow$ Crash Complaints).


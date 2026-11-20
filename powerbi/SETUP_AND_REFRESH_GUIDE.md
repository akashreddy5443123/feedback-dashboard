# Power BI Desktop Setup & Refresh Operations Guide

This guide provides instructions to connect Microsoft Power BI Desktop to the cleaned feedback data, establish relationships, copy DAX measures, and configure data refreshes.

---

## 1. Step-by-Step Setup in Power BI Desktop

### Step 1: Import the Cleaned Datasets
1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data** on the Home ribbon $\rightarrow$ select **Text/CSV**.
3. Browse to this project's `powerbi/` folder and import:
   - `Fact_CustomerFeedback.csv`
   - `Dim_Date.csv`
   - `Dim_Product.csv`
   - `Dim_Channel.csv`
   - `Dim_Region.csv`
   - `Dim_Sentiment.csv`
   *(Alternatively, for a single flat table, import `cleaned_customer_feedback.csv`).*
4. In the preview window, click **Load**.

### Step 2: Establish Star Schema Relationships
1. Switch to the **Model View** (icon on the left navigation bar).
2. Create 1-to-many relationships by dragging keys from the dimension tables to the fact table:
   - `Dim_Date[DateKey]` $\longrightarrow$ `Fact_CustomerFeedback[DateKey]`
   - `Dim_Product[ProductKey]` $\longrightarrow$ `Fact_CustomerFeedback[ProductKey]`
   - `Dim_Channel[ChannelKey]` $\longrightarrow$ `Fact_CustomerFeedback[ChannelKey]`
   - `Dim_Region[RegionKey]` $\longrightarrow$ `Fact_CustomerFeedback[RegionKey]`
   - `Dim_Sentiment[SentimentKey]` $\longrightarrow$ `Fact_CustomerFeedback[SentimentKey]`
3. Double-click each relationship line and verify:
   - **Cardinality:** `One to Many (1:*)`
   - **Cross filter direction:** `Single`
   - **Make this relationship active:** Checked $\checkmark$

### Step 3: Designate the Official Date Table
1. In the Fields pane on the right, right-click `Dim_Date`.
2. Select **Mark as Date Table** $\rightarrow$ **Mark as Date Table**.
3. In the dialog, select `Date` as the date column $\rightarrow$ click **OK**.
4. *(This step enables native DAX Time Intelligence functions like `DATESMTD` and `PREVIOUSMONTH`).*

### Step 4: Add DAX Measures
1. Right-click `Fact_CustomerFeedback` in the Fields list $\rightarrow$ select **New Measure**.
2. Open `powerbi/dax_measures.dax` in any text editor.
3. Copy each measure formula into the formula bar and press **Enter**.
4. Set formatting on each measure (e.g. `[Average Rating]` to `0.00`, `[Positive Feedback Percentage]` to `0.0%`).

### Step 5: Build Report Pages
Follow the layout blueprints in [`REPORT_SPECIFICATIONS.md`](REPORT_SPECIFICATIONS.md) to build the 5 report pages.

---

## 2. Data Refresh Workflows

### Method 1: Local File Refresh (Current Implementation)
When new feedback arrives via the Streamlit dashboard or CSV upload:
1. In the Streamlit app, navigate to the **Power BI Enterprise Portal** tab.
2. Click **Generate & Save to Local Workspace (`powerbi/`)** to update the CSV files with the newly cleaned data.
3. In **Power BI Desktop**, click the **Refresh** button on the Home ribbon.
4. Power BI re-reads the updated CSVs and recalculates all visuals and DAX measures instantly.

### Method 2: Power Query Dynamic Parameterization (Best Practice)
To prevent hardcoded file paths when sharing `.pbix` files between team members:
1. In Power BI Desktop, click **Transform Data** (Power Query Editor).
2. Click **Manage Parameters** $\rightarrow$ **New Parameter**.
   - **Name:** `DataFolderPath`
   - **Type:** Text
   - **Current Value:** `C:\Users\...\feedback-dashboard\powerbi`
3. Modify the M code of each table to use the parameter:
   ```powerquery
   Source = Csv.Document(File.Contents(DataFolderPath & "\Fact_CustomerFeedback.csv"), [Delimiter=",", Encoding=65001])
   ```

---

## 3. Future Enterprise Cloud Architecture

To transition from local file-based refreshes to an enterprise corporate pipeline:

```
┌─────────────────────────────────┐
│ Live Ingestion API (FastAPI)    │
└────────────────┬────────────────┘
                 │ (Streaming / Webhooks)
                 ▼
┌─────────────────────────────────┐
│ PostgreSQL / Azure SQL DB       │
│ • Transactional feedback store  │
└────────────────┬────────────────┘
                 │ (Scheduled ETL / DirectQuery)
                 ▼
┌─────────────────────────────────┐
│ Power BI Service (Cloud)        │
│ • Daily / Hourly auto-refresh   │
│ • Enterprise Gateway            │
│ • Row-Level Security (RLS)      │
│ • Executive Mobile Apps         │
└─────────────────────────────────┘
```

1. **On-Premises Data Gateway:** For local file systems or private servers, install the Power BI Standard Gateway to allow `app.powerbi.com` to refresh local CSV files on a schedule.
2. **Cloud Storage (OneDrive / SharePoint Online / Azure Blob):** Store `cleaned_customer_feedback.csv` in OneDrive for Business or Azure Blob Storage; Power BI Service can refresh cloud-hosted files automatically without requiring a gateway.
3. **Database Migration (PostgreSQL / Snowflake / Databricks):** Direct connection to an enterprise database supporting both **Import Mode** (high-speed in-memory) and **DirectQuery** (real-time streaming without size limits).

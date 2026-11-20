# Power BI Enterprise Integration Guide
### Customer Feedback Analytics - Star Schema Implementation

## 1. Overview
This package transforms the raw customer feedback data into a high-performance **Star Schema** optimized for Microsoft Power BI's **VertiPaq** in-memory columnar storage engine.

## 2. Included Tables
1. **`Fact_CustomerFeedback.csv`**: Central fact table with ratings, NPS indicator flags, and surrogate foreign keys.
2. **`Dim_Date.csv`**: Comprehensive date dimension table enabling Time Intelligence DAX functions (MoM, YoY, YTD).
3. **`Dim_Product.csv`**: Product dimension with tiers (Enterprise, Professional, Starter) and categories.
4. **`Dim_Channel.csv`**: Channel dimension classified into Direct Support, Storefront, In-Product, and Social.
5. **`Dim_Region.csv`**: Geographic dimension for regional slicing.
6. **`Dim_Sentiment.csv`**: Sentiment classification dimension with score weights.

## 3. Power BI Desktop Setup Steps
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV** and import all 6 CSV files.
3. In the **Model View**, establish the following 1-to-many relationships (Single Cross-Filter Direction):
   - `Dim_Date[DateKey]` (1) ────► `Fact_CustomerFeedback[DateKey]` (*)
   - `Dim_Product[ProductKey]` (1) ────► `Fact_CustomerFeedback[ProductKey]` (*)
   - `Dim_Channel[ChannelKey]` (1) ────► `Fact_CustomerFeedback[ChannelKey]` (*)
   - `Dim_Region[RegionKey]` (1) ────► `Fact_CustomerFeedback[RegionKey]` (*)
   - `Dim_Sentiment[SentimentKey]` (1) ────► `Fact_CustomerFeedback[SentimentKey]` (*)
4. Mark `Dim_Date` as the official **Date Table** (`Dim_Date[Date]`).
5. Open `PowerBI_DAX_Measures.dax` and create the core measures in `Fact_CustomerFeedback`.
6. Add the following visuals:
   - **NPS Gauge**: Value = `[NPS Score]`, Min = -100, Max = 100, Target = 50.
   - **CSAT Card**: Format as Percentage (`[CSAT Percentage]`).
   - **Matrix Visual**: Rows = `Dim_Product[ProductName]`, Columns = `Dim_Channel[ChannelName]`, Values = `[Average Rating]`.
   - **Slicers**: `Dim_Date[Year]`, `Dim_Region[RegionName]`, `Dim_Product[ProductTier]`.

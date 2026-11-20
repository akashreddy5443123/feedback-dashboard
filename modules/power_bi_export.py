"""
Power BI Integration & Data Export Engine
Tech Stack: Python, Pandas, OpenPyXL

Provides clean, validated data export pipelines for Microsoft Power BI:
1. Single Analytical Table: 'cleaned_customer_feedback.csv' / '.xlsx'
2. Enterprise Star Schema: Fact_CustomerFeedback + Dim_Date, Dim_Product,
   Dim_Channel, Dim_Region, Dim_Sentiment
3. Complete DAX Measures Package matching all business reporting requirements.
"""
from __future__ import annotations
import io
import os
import zipfile
import pandas as pd


def prepare_powerbi_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares a clean, validated analytical table specifically formatted for Power BI.
    Ensures standard datatypes, formatted date strings, numeric bounds, and explicit flags.
    """
    if df.empty:
        return pd.DataFrame()

    bi_df = df.copy()
    bi_df["date"] = pd.to_datetime(bi_df["date"])
    bi_df["date_formatted"] = bi_df["date"].dt.strftime("%Y-%m-%d")
    bi_df["year"] = bi_df["date"].dt.year
    bi_df["month_number"] = bi_df["date"].dt.month
    bi_df["month_name"] = bi_df["date"].dt.strftime("%B")
    bi_df["year_month"] = bi_df["date"].dt.strftime("%Y-%m")
    bi_df["quarter"] = "Q" + bi_df["date"].dt.quarter.astype(str)

    # Coerce rating to strictly 1-5 integer
    bi_df["rating"] = bi_df["rating"].astype(int).clip(1, 5)

    # Boolean/numeric satisfaction indicator flags
    bi_df["is_positive"] = (bi_df["sentiment"] == "Positive").astype(int)
    bi_df["is_negative"] = (bi_df["sentiment"] == "Negative").astype(int)
    bi_df["is_neutral"] = (bi_df["sentiment"] == "Neutral").astype(int)

    # NPS Classification (Standard: 4-5 Promoter, 3 Passive, 1-2 Detractor)
    bi_df["is_promoter"] = (bi_df["rating"] >= 4).astype(int)
    bi_df["is_passive"] = (bi_df["rating"] == 3).astype(int)
    bi_df["is_detractor"] = (bi_df["rating"] <= 2).astype(int)

    # Feedback length
    bi_df["feedback_char_count"] = bi_df["feedback_text"].astype(str).str.len()
    bi_df["has_text_comment"] = (bi_df["feedback_char_count"] > 0).astype(int)

    # Order columns logically
    ordered_cols = [
        "feedback_id", "date", "date_formatted", "year", "quarter", "month_number", "month_name", "year_month",
        "customer_name", "product", "channel", "region", "rating",
        "sentiment", "is_positive", "is_negative", "is_neutral",
        "is_promoter", "is_passive", "is_detractor",
        "feedback_char_count", "has_text_comment", "feedback_text"
    ]
    available = [c for c in ordered_cols if c in bi_df.columns]
    return bi_df[available]


def create_star_schema(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Transforms cleaned customer feedback data into a normalized Star Schema
    optimized for Power BI's VertiPaq columnar in-memory storage engine.
    """
    if df.empty:
        return {}

    work_df = df.copy()
    work_df["date"] = pd.to_datetime(work_df["date"])

    # 1. Dim_Date
    min_date = work_df["date"].min()
    max_date = work_df["date"].max()
    date_range = pd.date_range(start=min_date, end=max_date, freq="D")
    dim_date = pd.DataFrame({"Date": date_range})
    dim_date["DateKey"] = dim_date["Date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["DateFormatted"] = dim_date["Date"].dt.strftime("%Y-%m-%d")
    dim_date["Year"] = dim_date["Date"].dt.year
    dim_date["Quarter"] = dim_date["Date"].dt.quarter
    dim_date["QuarterName"] = "Q" + dim_date["Quarter"].astype(str)
    dim_date["MonthNumber"] = dim_date["Date"].dt.month
    dim_date["MonthName"] = dim_date["Date"].dt.strftime("%B")
    dim_date["MonthShort"] = dim_date["Date"].dt.strftime("%b")
    dim_date["YearMonth"] = dim_date["Date"].dt.strftime("%Y-%m")
    dim_date["WeekNumber"] = dim_date["Date"].dt.isocalendar().week.astype(int)
    dim_date["DayOfWeek"] = dim_date["Date"].dt.dayofweek + 1
    dim_date["DayName"] = dim_date["Date"].dt.strftime("%A")
    dim_date["IsWeekend"] = dim_date["DayOfWeek"].apply(lambda d: 1 if d in [6, 7] else 0)

    # 2. Dim_Product
    unique_products = sorted(work_df["product"].dropna().unique().tolist())
    product_tiers = {
        "Enterprise Plan": "Enterprise",
        "Pro Plan": "Professional",
        "Basic Plan": "Starter",
        "Mobile App": "Consumer Mobile",
        "Browser Extension": "Productivity Add-on",
    }
    product_categories = {
        "Enterprise Plan": "Subscription Tier",
        "Pro Plan": "Subscription Tier",
        "Basic Plan": "Subscription Tier",
        "Mobile App": "Client Software",
        "Browser Extension": "Client Software",
    }
    dim_product = pd.DataFrame({
        "ProductKey": [f"P{i+1:03d}" for i in range(len(unique_products))],
        "ProductName": unique_products,
        "ProductTier": [product_tiers.get(p, "Standard") for p in unique_products],
        "Category": [product_categories.get(p, "General") for p in unique_products],
    })

    # 3. Dim_Channel
    unique_channels = sorted(work_df["channel"].dropna().unique().tolist())
    channel_types = {
        "Email": "Direct Support",
        "Support Ticket": "Direct Support",
        "In-App Survey": "In-Product Telemetry",
        "App Store Review": "Public Storefront",
        "Twitter/X": "Social Media",
    }
    dim_channel = pd.DataFrame({
        "ChannelKey": [f"C{i+1:03d}" for i in range(len(unique_channels))],
        "ChannelName": unique_channels,
        "ChannelType": [channel_types.get(c, "Other") for c in unique_channels],
    })

    # 4. Dim_Region
    unique_regions = sorted(work_df["region"].dropna().unique().tolist())
    dim_region = pd.DataFrame({
        "RegionKey": [f"R{i+1:03d}" for i in range(len(unique_regions))],
        "RegionName": unique_regions,
        "Territory": ["Global Operations" for _ in unique_regions],
    })

    # 5. Dim_Sentiment
    dim_sentiment = pd.DataFrame([
        {"SentimentKey": 1, "Sentiment": "Negative", "ScoreWeight": -1, "HexColor": "#E74C3C"},
        {"SentimentKey": 2, "Sentiment": "Neutral", "ScoreWeight": 0, "HexColor": "#F1C40F"},
        {"SentimentKey": 3, "Sentiment": "Positive", "ScoreWeight": 1, "HexColor": "#2ECC71"},
    ])

    # 6. Fact_CustomerFeedback
    prod_map = dict(zip(dim_product["ProductName"], dim_product["ProductKey"]))
    chan_map = dict(zip(dim_channel["ChannelName"], dim_channel["ChannelKey"]))
    reg_map = dict(zip(dim_region["RegionName"], dim_region["RegionKey"]))
    sent_map = {"Negative": 1, "Neutral": 2, "Positive": 3}

    fact = work_df.copy()
    fact["DateKey"] = fact["date"].dt.strftime("%Y%m%d").astype(int)
    fact["ProductKey"] = fact["product"].map(prod_map).fillna("P000")
    fact["ChannelKey"] = fact["channel"].map(chan_map).fillna("C000")
    fact["RegionKey"] = fact["region"].map(reg_map).fillna("R000")
    fact["SentimentKey"] = fact["sentiment"].map(sent_map).fillna(2).astype(int)

    fact["Rating"] = fact["rating"].astype(int).clip(1, 5)
    fact["IsPositive"] = (fact["sentiment"] == "Positive").astype(int)
    fact["IsNegative"] = (fact["sentiment"] == "Negative").astype(int)
    fact["IsNeutral"] = (fact["sentiment"] == "Neutral").astype(int)

    fact["IsPromoter"] = (fact["Rating"] >= 4).astype(int)
    fact["IsPassive"] = (fact["Rating"] == 3).astype(int)
    fact["IsDetractor"] = (fact["Rating"] <= 2).astype(int)
    fact["FeedbackLength"] = fact["feedback_text"].astype(str).str.len()

    fact_cols = [
        "feedback_id", "DateKey", "ProductKey", "ChannelKey", "RegionKey", "SentimentKey",
        "customer_name", "Rating", "IsPositive", "IsNegative", "IsNeutral",
        "IsPromoter", "IsPassive", "IsDetractor", "FeedbackLength", "feedback_text"
    ]
    available_cols = [c for c in fact_cols if c in fact.columns]
    fact_table = fact[available_cols].rename(columns={
        "feedback_id": "FeedbackID",
        "customer_name": "CustomerName",
        "feedback_text": "FeedbackText",
    })

    return {
        "Fact_CustomerFeedback": fact_table,
        "Dim_Date": dim_date,
        "Dim_Product": dim_product,
        "Dim_Channel": dim_channel,
        "Dim_Region": dim_region,
        "Dim_Sentiment": dim_sentiment,
    }


def get_dax_measures() -> str:
    """
    Returns complete, fully annotated DAX measures required for all 5 Power BI report pages.
    Written for both Single Flat Table and Star Schema architectures.
    """
    return """/* =========================================================================
   CUSTOMER FEEDBACK POWER BI REPORT - PRODUCTION DAX MEASURES PACKAGE
   Repository: https://github.com/akashreddy5443123/feedback-dashboard
   ========================================================================= */

// -------------------------------------------------------------------------
// 1. CORE VOLUME & GENERAL MEASURES
// -------------------------------------------------------------------------

// Total count of customer feedback entries
Total Feedback = 
COUNTROWS('Fact_CustomerFeedback')

// Count of distinct products receiving feedback
Total Products = 
DISTINCTCOUNT('Fact_CustomerFeedback'[ProductKey])

// Total count of distinct customers
Total Customers = 
DISTINCTCOUNT('Fact_CustomerFeedback'[CustomerName])


// -------------------------------------------------------------------------
// 2. RATING & SATISFACTION MEASURES
// -------------------------------------------------------------------------

// Average customer rating (1.00 to 5.00)
Average Rating = 
ROUND(AVERAGE('Fact_CustomerFeedback'[Rating]), 2)

// Average rating specifically for a selected product (respects outer filters)
Average Rating by Product = 
CALCULATE(
    [Average Rating],
    ALLEXCEPT('Fact_CustomerFeedback', 'Dim_Product'[ProductName])
)


// -------------------------------------------------------------------------
// 3. SENTIMENT COUNTS & PERCENTAGES
// -------------------------------------------------------------------------

// Count of feedback rows classified as Positive
Positive Feedback Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[IsPositive] = 1
)

// Count of feedback rows classified as Negative
Negative Feedback Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[IsNegative] = 1
)

// Count of feedback rows classified as Neutral
Neutral Feedback Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[IsNeutral] = 1
)

// Percentage of total feedback that is Positive
Positive Feedback Percentage = 
VAR TotalCount = [Total Feedback]
VAR PosCount = [Positive Feedback Count]
RETURN
IF(
    TotalCount > 0,
    DIVIDE(PosCount, TotalCount, 0),
    0
)

// Percentage of total feedback that is Negative
Negative Feedback Percentage = 
VAR TotalCount = [Total Feedback]
VAR NegCount = [Negative Feedback Count]
RETURN
IF(
    TotalCount > 0,
    DIVIDE(NegCount, TotalCount, 0),
    0
)

// Percentage of total feedback that is Neutral
Neutral Feedback Percentage = 
VAR TotalCount = [Total Feedback]
VAR NeuCount = [Neutral Feedback Count]
RETURN
IF(
    TotalCount > 0,
    DIVIDE(NeuCount, TotalCount, 0),
    0
)


// -------------------------------------------------------------------------
// 4. CHANNEL & PRODUCT AGGREGATIONS
// -------------------------------------------------------------------------

// Feedback count by touchpoint channel
Feedback Count by Channel = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    ALLEXCEPT('Fact_CustomerFeedback', 'Dim_Channel'[ChannelName])
)

// Feedback count by individual product
Feedback Count by Product = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    ALLEXCEPT('Fact_CustomerFeedback', 'Dim_Product'[ProductName])
)


// -------------------------------------------------------------------------
// 5. TIME INTELLIGENCE & MONTHLY TRENDS
// -------------------------------------------------------------------------

// Monthly volume of feedback records
Monthly Feedback Count = 
CALCULATE(
    [Total Feedback],
    DATESMTD('Dim_Date'[Date])
)

// Monthly average rating
Monthly Average Rating = 
CALCULATE(
    [Average Rating],
    DATESMTD('Dim_Date'[Date])
)

// Prior Month Average Rating
Prior Month Average Rating = 
CALCULATE(
    [Average Rating],
    PREVIOUSMONTH('Dim_Date'[Date])
)

// Month-over-Month (MoM) Rating Trajectory Delta
MoM Rating Delta = 
VAR CurrentRating = [Average Rating]
VAR PriorRating = [Prior Month Average Rating]
RETURN
IF(
    ISBLANK(PriorRating),
    BLANK(),
    CurrentRating - PriorRating
)


// -------------------------------------------------------------------------
// 6. EXECUTIVE DECISION METRICS (NPS & CSAT)
// -------------------------------------------------------------------------

// Promoters (Ratings 4-5)
Promoter Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[Rating] >= 4
)

// Detractors (Ratings 1-2)
Detractor Count = 
CALCULATE(
    COUNTROWS('Fact_CustomerFeedback'),
    'Fact_CustomerFeedback'[Rating] <= 2
)

// Net Promoter Score [-100 to +100]
NPS Score = 
VAR TotalCount = [Total Feedback]
VAR Promoters = [Promoter Count]
VAR Detractors = [Detractor Count]
RETURN
IF(
    TotalCount > 0,
    ROUND(DIVIDE(Promoters - Detractors, TotalCount, 0) * 100, 1),
    0
)

// Customer Satisfaction (CSAT %)
CSAT Percentage = 
DIVIDE([Promoter Count], [Total Feedback], 0)
"""


def export_powerbi_bundle(df: pd.DataFrame, output_dir: str = "powerbi") -> dict[str, str]:
    """
    Exports the complete Power BI deliverable set into the target directory:
    - cleaned_customer_feedback.csv
    - cleaned_customer_feedback.xlsx
    - Fact_CustomerFeedback.csv
    - Dim_Date.csv
    - Dim_Product.csv
    - Dim_Channel.csv
    - Dim_Region.csv
    - Dim_Sentiment.csv
    - dax_measures.dax
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_files = {}

    # 1. Single analytical dataset (CSV & XLSX)
    flat_df = prepare_powerbi_dataset(df)
    flat_csv_path = os.path.join(output_dir, "cleaned_customer_feedback.csv")
    flat_df.to_csv(flat_csv_path, index=False)
    generated_files["cleaned_csv"] = flat_csv_path

    flat_xlsx_path = os.path.join(output_dir, "cleaned_customer_feedback.xlsx")
    flat_df.to_excel(flat_xlsx_path, index=False, engine="openpyxl")
    generated_files["cleaned_xlsx"] = flat_xlsx_path

    # 2. Star Schema tables
    star_schema = create_star_schema(df)
    for table_name, table_df in star_schema.items():
        table_path = os.path.join(output_dir, f"{table_name}.csv")
        table_df.to_csv(table_path, index=False)
        generated_files[table_name] = table_path

    # 3. DAX measures file
    dax_path = os.path.join(output_dir, "dax_measures.dax")
    with open(dax_path, "w", encoding="utf-8") as f:
        f.write(get_dax_measures())
    generated_files["dax_measures"] = dax_path

    return generated_files


def export_powerbi_zip(df: pd.DataFrame) -> bytes:
    """Creates an in-memory zip archive containing all Power BI files for 1-click Streamlit download."""
    flat_df = prepare_powerbi_dataset(df)
    star_schema = create_star_schema(df)
    dax_code = get_dax_measures()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("cleaned_customer_feedback.csv", flat_df.to_csv(index=False).encode("utf-8"))
        for tname, tdf in star_schema.items():
            zf.writestr(f"{tname}.csv", tdf.to_csv(index=False).encode("utf-8"))
        zf.writestr("dax_measures.dax", dax_code.encode("utf-8"))

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def save_star_schema_to_disk(df: pd.DataFrame, output_dir: str = "powerbi") -> str:
    """Convenience alias to export the complete Power BI bundle to disk."""
    export_powerbi_bundle(df, output_dir)
    return output_dir


def export_star_schema_zip(df: pd.DataFrame) -> bytes:
    """Convenience alias to export the complete Power BI zip package."""
    return export_powerbi_zip(df)


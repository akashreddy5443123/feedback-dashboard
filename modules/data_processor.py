"""
Reusable data processing module.
Handles loading, cleaning, and aggregating customer feedback data
so the Streamlit app stays presentation-only.
"""
from __future__ import annotations
import pandas as pd


REQUIRED_COLUMNS = [
    "feedback_id", "date", "customer_name", "product",
    "channel", "region", "rating", "sentiment", "feedback_text",
]


def load_data(file) -> pd.DataFrame:
    """Load feedback data from a CSV/XLSX path or an uploaded file-like object."""
    name = getattr(file, "name", str(file))
    if str(name).lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize raw feedback data.

    - Normalizes column names
    - Parses dates
    - Drops rows missing critical fields
    - Deduplicates
    - Fills/standardizes sentiment and text fields
    """
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure required columns exist even if source data is missing some
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    # Parse dates, drop rows we can't make sense of
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Ratings: coerce to numeric, clip to valid 1-5 range
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])
    df["rating"] = df["rating"].clip(1, 5).astype(int)

    # Text cleanup
    df["feedback_text"] = df["feedback_text"].fillna("").astype(str).str.strip()

    # Standardize categorical text fields
    for col in ["product", "channel", "region", "sentiment"]:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    # Derive sentiment from rating if missing/blank
    missing_sentiment = df["sentiment"].isin(["", "Unknown", "nan", "None"])
    df.loc[missing_sentiment, "sentiment"] = df.loc[missing_sentiment, "rating"].apply(rating_to_sentiment)

    # Drop exact duplicates
    df = df.drop_duplicates(subset=["feedback_id", "customer_name", "date", "feedback_text"])

    df = df.sort_values("date").reset_index(drop=True)
    return df


def rating_to_sentiment(rating: int) -> str:
    if rating >= 4:
        return "Positive"
    if rating == 3:
        return "Neutral"
    return "Negative"


def apply_filters(
    df: pd.DataFrame,
    date_range=None,
    products=None,
    channels=None,
    regions=None,
    sentiments=None,
) -> pd.DataFrame:
    """Apply sidebar filter selections to the cleaned dataframe."""
    filtered = df.copy()

    if date_range and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

    if products:
        filtered = filtered[filtered["product"].isin(products)]
    if channels:
        filtered = filtered[filtered["channel"].isin(channels)]
    if regions:
        filtered = filtered[filtered["region"].isin(regions)]
    if sentiments:
        filtered = filtered[filtered["sentiment"].isin(sentiments)]

    return filtered


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute headline KPIs for the current filtered dataset."""
    if df.empty:
        return {
            "total_feedback": 0,
            "avg_rating": 0.0,
            "positive_pct": 0.0,
            "negative_pct": 0.0,
            "nps_score": 0.0,
            "csat_pct": 0.0,
        }

    total = len(df)
    avg_rating = round(df["rating"].mean(), 2)
    positive_pct = round((df["sentiment"] == "Positive").sum() / total * 100, 1)
    negative_pct = round((df["sentiment"] == "Negative").sum() / total * 100, 1)

    # Net Promoter Score (NPS): Promoters (4-5) minus Detractors (1-2)
    promoters = (df["rating"] >= 4).sum()
    detractors = (df["rating"] <= 2).sum()
    nps_score = round(((promoters - detractors) / total) * 100, 1)
    csat_pct = round((promoters / total) * 100, 1)

    return {
        "total_feedback": total,
        "avg_rating": avg_rating,
        "positive_pct": positive_pct,
        "negative_pct": negative_pct,
        "nps_score": nps_score,
        "csat_pct": csat_pct,
    }


def compute_nps(df: pd.DataFrame) -> dict:
    """Detailed Net Promoter Score (NPS) breakdown."""
    if df.empty:
        return {
            "nps_score": 0.0,
            "promoter_count": 0,
            "passive_count": 0,
            "detractor_count": 0,
            "promoter_pct": 0.0,
            "passive_pct": 0.0,
            "detractor_pct": 0.0,
            "csat_pct": 0.0,
        }

    total = len(df)
    promoters = int((df["rating"] >= 4).sum())
    passives = int((df["rating"] == 3).sum())
    detractors = int((df["rating"] <= 2).sum())

    return {
        "nps_score": round(((promoters - detractors) / total) * 100, 1),
        "promoter_count": promoters,
        "passive_count": passives,
        "detractor_count": detractors,
        "promoter_pct": round((promoters / total) * 100, 1),
        "passive_pct": round((passives / total) * 100, 1),
        "detractor_pct": round((detractors / total) * 100, 1),
        "csat_pct": round((promoters / total) * 100, 1),
    }


def product_channel_matrix_data(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot table of average rating across products and channels."""
    if df.empty or "product" not in df.columns or "channel" not in df.columns:
        return pd.DataFrame()
    pivot = df.pivot_table(
        index="product",
        columns="channel",
        values="rating",
        aggfunc="mean",
    ).round(2)
    return pivot


def sentiment_over_time(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """Aggregate sentiment counts over time at the given frequency (D/W/M)."""
    if df.empty:
        return pd.DataFrame(columns=["date", "sentiment", "count"])

    grouped = (
        df.set_index("date")
        .groupby([pd.Grouper(freq=freq), "sentiment"])
        .size()
        .reset_index(name="count")
    )
    return grouped


def top_products_by_rating(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["product", "avg_rating", "feedback_count"])
    return (
        df.groupby("product")
        .agg(avg_rating=("rating", "mean"), feedback_count=("rating", "size"))
        .round(2)
        .sort_values("avg_rating", ascending=False)
        .reset_index()
    )


def rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["rating", "count"])
    return df["rating"].value_counts().sort_index().reset_index(
        name="count"
    ).rename(columns={"index": "rating"})


def channel_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["channel", "count"])
    return df["channel"].value_counts().reset_index(name="count").rename(
        columns={"index": "channel"}
    )

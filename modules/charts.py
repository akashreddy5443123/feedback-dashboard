"""
Reusable chart-building module.
Plotly for the interactive Streamlit dashboard, Matplotlib for a
static exportable summary chart (e.g. for reports/PDF export).
"""
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


PLOTLY_TEMPLATE = "plotly_white"


def sentiment_pie(df: pd.DataFrame):
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    color_map = {"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"}
    fig = px.pie(
        counts, names="sentiment", values="count",
        color="sentiment", color_discrete_map=color_map,
        hole=0.45, template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
    return fig


def sentiment_trend_line(trend_df: pd.DataFrame):
    color_map = {"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"}
    fig = px.line(
        trend_df, x="date", y="count", color="sentiment",
        color_discrete_map=color_map, markers=True,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis_title="", yaxis_title="Feedback count",
        legend_title="",
    )
    return fig


def rating_bar(dist_df: pd.DataFrame):
    fig = px.bar(
        dist_df, x="rating", y="count",
        template=PLOTLY_TEMPLATE, text="count",
    )
    fig.update_traces(marker_color="#3498db")
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis_title="Rating", yaxis_title="Feedback count",
        xaxis=dict(tickmode="linear"),
    )
    return fig


def product_rating_bar(product_df: pd.DataFrame):
    fig = px.bar(
        product_df.sort_values("avg_rating"),
        x="avg_rating", y="product", orientation="h",
        template=PLOTLY_TEMPLATE, text="avg_rating",
        hover_data=["feedback_count"],
    )
    fig.update_traces(marker_color="#9b59b6")
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis_title="Average rating", yaxis_title="",
        xaxis_range=[0, 5],
    )
    return fig


def channel_donut(channel_df: pd.DataFrame):
    fig = px.pie(
        channel_df, names="channel", values="count",
        hole=0.45, template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
    return fig


def matplotlib_summary(df: pd.DataFrame):
    """Static Matplotlib chart (e.g. for export/report generation),
    showing average rating trend by month."""
    monthly = (
        df.set_index("date")["rating"]
        .resample("ME")
        .mean()
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly.index, monthly.values, marker="o", color="#2c3e50", linewidth=2)
    ax.set_title("Average Rating by Month")
    ax.set_ylabel("Avg rating")
    ax.set_ylim(1, 5)
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

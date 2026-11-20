"""
Reusable chart-building module.
Plotly for the interactive Streamlit dashboard, Matplotlib for a
static exportable summary chart (e.g. for reports/PDF export).
"""
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


COLOR_POSITIVE = "#2ECC71"
COLOR_NEUTRAL = "#F1C40F"
COLOR_NEGATIVE = "#E74C3C"

SENTIMENT_COLORS = {
    "Positive": COLOR_POSITIVE,
    "Neutral": COLOR_NEUTRAL,
    "Negative": COLOR_NEGATIVE,
}


def apply_theme_styling(fig: go.Figure) -> go.Figure:
    """Applies modern transparent backgrounds so charts look gorgeous in both dark and light modes."""
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Inter, Roboto, sans-serif", size=12),
        margin=dict(t=25, b=25, l=25, r=25),
    )
    return fig


def sentiment_pie(df: pd.DataFrame):
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    fig = px.pie(
        counts, names="sentiment", values="count",
        color="sentiment", color_discrete_map=SENTIMENT_COLORS,
        hole=0.55,
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        insidetextorientation="horizontal",
        marker=dict(line=dict(color="rgba(0,0,0,0.2)", width=1.5)),
    )
    fig.update_layout(
        showlegend=False,
        annotations=[dict(text="Sentiment", x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(weight="bold"))],
    )
    return apply_theme_styling(fig)


def sentiment_trend_line(trend_df: pd.DataFrame):
    fig = px.line(
        trend_df, x="date", y="count", color="sentiment",
        color_discrete_map=SENTIMENT_COLORS, markers=True,
    )
    fig.update_traces(
        line=dict(shape="spline", width=2.5),
        marker=dict(size=6),
    )
    fig.update_layout(
        xaxis_title="", yaxis_title="Feedback Volume",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=""),
        hovermode="x unified",
        xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
    )
    return apply_theme_styling(fig)


def rating_bar(dist_df: pd.DataFrame):
    # Professional color scale for 1-5 stars
    star_colors = {1: "#E74C3C", 2: "#E67E22", 3: "#F1C40F", 4: "#3498DB", 5: "#2ECC71"}
    dist_df = dist_df.copy()
    dist_df["color"] = dist_df["rating"].map(star_colors).fillna("#3498db")
    dist_df["star_label"] = dist_df["rating"].apply(lambda r: f"{r} ★")

    fig = go.Figure(go.Bar(
        x=dist_df["star_label"],
        y=dist_df["count"],
        text=dist_df["count"],
        textposition="auto",
        marker=dict(
            color=dist_df["color"],
            line=dict(color="rgba(0,0,0,0.15)", width=1),
            cornerradius=6,
        ),
    ))
    fig.update_layout(
        xaxis_title="Star Rating", yaxis_title="Number of Reviews",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
    )
    return apply_theme_styling(fig)


def product_rating_bar(product_df: pd.DataFrame):
    sorted_df = product_df.sort_values("avg_rating", ascending=True)
    fig = px.bar(
        sorted_df,
        x="avg_rating", y="product", orientation="h",
        text="avg_rating",
        hover_data=["feedback_count"],
        color="avg_rating",
        color_continuous_scale="Tealgrn",
        range_color=[1, 5],
    )
    fig.update_traces(
        texttemplate="%{text:.2f} ★",
        textposition="inside",
        marker=dict(cornerradius=4),
    )
    fig.update_layout(
        xaxis_title="Average Rating", yaxis_title="",
        xaxis_range=[0, 5.2],
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.15)"),
        yaxis=dict(showgrid=False),
    )
    return apply_theme_styling(fig)


def channel_donut(channel_df: pd.DataFrame):
    colors = ["#3498DB", "#9B59B6", "#E67E22", "#1ABC9C", "#E74C3C"]
    fig = px.pie(
        channel_df, names="channel", values="count",
        hole=0.55,
        color_discrete_sequence=colors,
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        marker=dict(line=dict(color="rgba(0,0,0,0.2)", width=1.5)),
    )
    fig.update_layout(
        showlegend=False,
        annotations=[dict(text="Channels", x=0.5, y=0.5, font_size=13, showarrow=False, font=dict(weight="bold"))],
    )
    return apply_theme_styling(fig)


def matplotlib_summary(df: pd.DataFrame):
    """Static Matplotlib chart showing average rating trend by month."""
    monthly = (
        df.set_index("date")["rating"]
        .resample("ME")
        .mean()
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#F8F9FA")
    ax.set_facecolor("white")
    ax.plot(monthly.index.strftime("%b %y"), monthly.values, marker="o", color="#2C3E50", linewidth=2.5, markersize=5)
    ax.axhline(3.5, color="#27AE60", linestyle="--", alpha=0.6, label="Benchmark (3.50)")
    ax.set_title("Average Customer Rating by Month", fontsize=12, fontweight="bold", pad=10, color="#2C3E50")
    ax.set_ylabel("Avg Rating", fontsize=10, color="#2C3E50")
    ax.set_ylim(1, 5)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.tick_params(axis="x", rotation=35, labelsize=8)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    return fig


def nps_gauge(nps_score: float):
    """Power BI style Net Promoter Score (NPS) Gauge Visual."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=nps_score,
        domain={"x": [0, 1], "y": [0, 1]},
        delta={"reference": 0, "increasing": {"color": "#2ecc71"}, "decreasing": {"color": "#e74c3c"}},
        gauge={
            "axis": {"range": [-100, 100], "tickwidth": 1, "tickcolor": "#888888"},
            "bar": {"color": "#2C3E50", "thickness": 0.26},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1,
            "bordercolor": "rgba(128,128,128,0.2)",
            "steps": [
                {"range": [-100, 0], "color": "rgba(231, 76, 60, 0.25)"},   # Detractor zone
                {"range": [0, 50], "color": "rgba(241, 196, 15, 0.25)"},     # Passive zone
                {"range": [50, 100], "color": "rgba(46, 204, 113, 0.25)"},   # Promoter zone
            ],
            "threshold": {
                "line": {"color": "#27AE60", "width": 4},
                "thickness": 0.75,
                "value": 30,
            },
        },
    ))
    fig.update_layout(
        height=270,
        margin=dict(t=30, b=20, l=30, r=30),
    )
    return apply_theme_styling(fig)


def nps_breakdown_bar(nps_dict: dict):
    """Horizontal stacked bar showing Promoters, Passives, and Detractors percentage."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=["Audience Mix"],
        x=[nps_dict.get("detractor_pct", 0)],
        name=f"Detractors ({nps_dict.get('detractor_pct', 0)}%)",
        orientation="h",
        marker=dict(color="#E74C3C"),
        text=f"{nps_dict.get('detractor_pct', 0)}%",
        textposition="inside",
    ))
    fig.add_trace(go.Bar(
        y=["Audience Mix"],
        x=[nps_dict.get("passive_pct", 0)],
        name=f"Passives ({nps_dict.get('passive_pct', 0)}%)",
        orientation="h",
        marker=dict(color="#F1C40F"),
        text=f"{nps_dict.get('passive_pct', 0)}%",
        textposition="inside",
    ))
    fig.add_trace(go.Bar(
        y=["Audience Mix"],
        x=[nps_dict.get("promoter_pct", 0)],
        name=f"Promoters ({nps_dict.get('promoter_pct', 0)}%)",
        orientation="h",
        marker=dict(color="#2ECC71"),
        text=f"{nps_dict.get('promoter_pct', 0)}%",
        textposition="inside",
    ))
    fig.update_layout(
        barmode="stack",
        height=130,
        margin=dict(t=15, b=15, l=15, r=15),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 100]),
        yaxis=dict(showticklabels=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    return apply_theme_styling(fig)


def product_channel_heatmap(pivot_df: pd.DataFrame):
    """Power BI style Matrix Heatmap of Product vs Channel Rating."""
    if pivot_df.empty:
        return go.Figure()

    fig = px.imshow(
        pivot_df,
        labels=dict(x="Channel", y="Product", color="Avg Rating"),
        x=pivot_df.columns.tolist(),
        y=pivot_df.index.tolist(),
        color_continuous_scale="RdYlGn",
        range_color=[1, 5],
        text_auto=".2f",
        aspect="auto",
    )
    fig.update_layout(
        margin=dict(t=25, b=20, l=25, r=20),
        coloraxis_colorbar=dict(title="Rating", len=0.8),
    )
    return apply_theme_styling(fig)

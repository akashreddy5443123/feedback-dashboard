"""
Customer Feedback Dashboard
Tech Stack: Python, Pandas, Streamlit, Plotly, Matplotlib

An interactive dashboard to manage and visualize customer feedback:
upload/browse feedback data, filter it, and view KPIs + charts.
"""
import io
import os
import streamlit as st
import pandas as pd

from modules import data_processor as dp
from modules import charts
from modules import ml_sentiment as ml

st.set_page_config(
    page_title="Customer Feedback Dashboard",
    page_icon="📊",
    layout="wide",
)

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "customer_feedback.csv")


@st.cache_data
def load_and_clean(file_or_path) -> pd.DataFrame:
    raw = dp.load_data(file_or_path)
    return dp.clean_data(raw)


def main():
    st.title("📊 Customer Feedback Dashboard")
    st.caption("Manage and visualize customer feedback across products, channels, and regions.")

    # ---------------- Sidebar: data source + filters ----------------
    st.sidebar.header("Data source")
    uploaded_file = st.sidebar.file_uploader(
        "Upload feedback file", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        raw = dp.load_data(uploaded_file)
        raw_row_count = len(raw)
        df = dp.clean_data(raw)
        if df.empty:
            st.sidebar.error(
                f"Uploaded {raw_row_count} row(s) but none survived cleaning. "
                "Check that 'date' is a valid date and 'rating' is 1-5 for at least some rows."
            )
            st.warning("No usable rows after cleaning. Please check your file's date and rating columns.")
            st.stop()
        elif len(df) < raw_row_count:
            st.sidebar.warning(
                f"Loaded {len(df)} of {raw_row_count} rows "
                f"({raw_row_count - len(df)} dropped — missing/invalid date or rating, or duplicates)."
            )
        else:
            st.sidebar.success(f"Loaded {len(df)} rows from upload.")
    elif os.path.exists(DEFAULT_DATA_PATH):
        df = load_and_clean(DEFAULT_DATA_PATH)
        st.sidebar.info(f"Using sample dataset ({len(df)} rows).")
    else:
        st.warning(
            "No data found. Upload a CSV with columns: "
            "date, product, channel, region, rating, sentiment, feedback_text."
        )
        st.stop()

    st.sidebar.header("Filters")
    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input(
        "Date range", value=(min_date.date(), max_date.date()),
        min_value=min_date.date(), max_value=max_date.date(),
    )
    products = st.sidebar.multiselect("Product", sorted(df["product"].unique()))
    channels = st.sidebar.multiselect("Channel", sorted(df["channel"].unique()))
    regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()))
    sentiments = st.sidebar.multiselect("Sentiment", sorted(df["sentiment"].unique()))

    filtered = dp.apply_filters(
        df,
        date_range=date_range if isinstance(date_range, tuple) else None,
        products=products, channels=channels,
        regions=regions, sentiments=sentiments,
    )

    # ---------------- KPI row ----------------
    kpis = dp.compute_kpis(filtered)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Feedback", kpis["total_feedback"])
    c2.metric("Avg Rating", f"{kpis['avg_rating']} / 5")
    c3.metric("Positive %", f"{kpis['positive_pct']}%")
    c4.metric("Negative %", f"{kpis['negative_pct']}%")

    st.divider()

    # ---------------- Charts row 1 ----------------
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment breakdown")
        if not filtered.empty:
            st.plotly_chart(charts.sentiment_pie(filtered), use_container_width=True)
        else:
            st.info("No data for the current filters.")

    with col2:
        st.subheader("Sentiment trend over time")
        if not filtered.empty:
            trend = dp.sentiment_over_time(filtered, freq="W")
            st.plotly_chart(charts.sentiment_trend_line(trend), use_container_width=True)
        else:
            st.info("No data for the current filters.")

    # ---------------- Charts row 2 ----------------
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Rating distribution")
        if not filtered.empty:
            dist = dp.rating_distribution(filtered)
            st.plotly_chart(charts.rating_bar(dist), use_container_width=True)
        else:
            st.info("No data for the current filters.")

    with col4:
        st.subheader("Avg rating by product")
        if not filtered.empty:
            product_df = dp.top_products_by_rating(filtered)
            st.plotly_chart(charts.product_rating_bar(product_df), use_container_width=True)
        else:
            st.info("No data for the current filters.")

    # ---------------- Channel + Matplotlib export ----------------
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Feedback by channel")
        if not filtered.empty:
            channel_df = dp.channel_breakdown(filtered)
            st.plotly_chart(charts.channel_donut(channel_df), use_container_width=True)
        else:
            st.info("No data for the current filters.")

    with col6:
        st.subheader("Monthly avg rating (report chart)")
        if not filtered.empty:
            fig = charts.matplotlib_summary(filtered)
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
            st.download_button(
                "Download chart as PNG", data=buf.getvalue(),
                file_name="monthly_rating_trend.png", mime="image/png",
            )
        else:
            st.info("No data for the current filters.")

    st.divider()

    # ---------------- Optional: ML-based sentiment (scikit-learn) ----------------
    with st.expander("🧪 ML Sentiment Model (scikit-learn) — experimental, optional"):
        st.caption(
            "The dashboard's main sentiment labels are rule-based (from rating), "
            "not ML. This section is an optional add-on: trains a TF-IDF + "
            "Logistic Regression classifier on feedback TEXT to see if it agrees "
            "with the rule-based labels, and lets you test it on your own sentence."
        )
        st.warning(
            "⚠️ Honesty note: the bundled sample dataset uses a small number of "
            "fixed sentence templates per sentiment, so a text classifier trained "
            "on it will score unrealistically high (often ~100% accuracy) because "
            "it's learning the template, not real sentiment nuance. Upload a real "
            "feedback file with varied, natural text for a meaningful accuracy read."
        )

        if st.button("Train model on current filtered data"):
            with st.spinner("Training..."):
                result = ml.train_sentiment_model(filtered)

            if result.get("error"):
                st.error(result["error"])
            else:
                m = result["metrics"]
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("Accuracy", f"{m['accuracy']*100:.1f}%")
                mc2.metric("Train rows", m["train_size"])
                mc3.metric("Test rows", m["test_size"])

                report_df = pd.DataFrame(m["report"]).T.loc[m["labels"]]
                st.write("Per-class precision / recall / F1:")
                st.dataframe(
                    report_df[["precision", "recall", "f1-score", "support"]].round(2),
                    use_container_width=True,
                )

                comparison = ml.compare_with_rule_based(filtered, result["vectorizer"], result["model"])
                agree_pct = comparison["agrees_with_rule"].mean() * 100
                st.write(f"**ML vs rule-based agreement on this data: {agree_pct:.1f}%**")

                disagreements = comparison[~comparison["agrees_with_rule"]]
                if not disagreements.empty:
                    st.write("Rows where the ML model disagreed with the rating-based rule:")
                    st.dataframe(
                        disagreements[["product", "rating", "sentiment", "ml_sentiment", "feedback_text"]],
                        use_container_width=True, hide_index=True,
                    )

                st.session_state["ml_vectorizer"] = result["vectorizer"]
                st.session_state["ml_model"] = result["model"]

        if "ml_model" in st.session_state:
            st.write("---")
            custom_text = st.text_input("Test the trained model on your own sentence:")
            if custom_text:
                pred = ml.predict_sentiment(
                    st.session_state["ml_vectorizer"], st.session_state["ml_model"], [custom_text]
                )[0]
                st.write(f"Predicted sentiment: **{pred}**")

    st.divider()

    # ---------------- Raw feedback table ----------------
    st.subheader("Feedback records")
    st.dataframe(
        filtered[["date", "customer_name", "product", "channel", "region",
                  "rating", "sentiment", "feedback_text"]],
        use_container_width=True, hide_index=True,
    )
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_feedback.csv", mime="text/csv",
    )


if __name__ == "__main__":
    main()

"""
Customer Feedback Intelligence & Power BI Enterprise Portal
Tech Stack: Python, Pandas, Streamlit, Plotly, Matplotlib, Scikit-learn, Microsoft Power BI

An interactive decision-support platform to manage, visualize, and analyze customer feedback
across products, operational touchpoints, machine learning, and enterprise BI reporting.
"""
import io
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from modules import data_processor as dp
from modules import charts
from modules import ml_sentiment as ml
from modules import power_bi_export as pbi

st.set_page_config(
    page_title="Customer Feedback Intelligence & Power BI Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Executive CSS Styling
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #3498DB;
        box-shadow: 0 4px 16px rgba(52, 152, 219, 0.15);
        transition: all 0.2s ease-in-out;
    }
    /* Tab Styling */
    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        padding: 10px 22px;
    }
    /* Badge styling */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 14px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .badge-live { 
        background: rgba(46, 204, 113, 0.15); 
        color: #2ecc71; 
        border: 1px solid rgba(46, 204, 113, 0.35); 
    }
</style>
""", unsafe_allow_html=True)

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "customer_feedback.csv")


@st.cache_data
def load_and_clean(file_or_path) -> pd.DataFrame:
    raw = dp.load_data(file_or_path)
    return dp.clean_data(raw)


def main():
    st.title("📊 Customer Feedback Intelligence & Power BI Portal")
    st.caption("Enterprise decision analytics platform connecting customer experience data with executive Business Intelligence.")

    # ---------------- Sidebar: data source + filters ----------------
    st.sidebar.header("Data Source")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Custom Feedback File", type=["csv", "xlsx", "xls"],
        help="Upload customer exports. Automatically cleaned, deduplicated, and typed by Pandas."
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
        st.sidebar.markdown(
            f'<div class="status-badge badge-live">🟢 Production Telemetry ({len(df):,} verified records)</div>',
            unsafe_allow_html=True
        )
    else:
        st.warning(
            "No data found. Upload a CSV with columns: "
            "date, customer_name, product, channel, region, rating, sentiment, feedback_text."
        )
        st.stop()

    st.sidebar.header("Interactive Filters")

    # Quick Preset Filter Buttons
    preset = st.sidebar.selectbox(
        "⚡ Quick Filter Presets",
        ["All Records", "⚠️ Critical Complaints (1-2★)", "⭐ Promoters (4-5★)", "📱 Mobile Issues", "💳 Billing & Latency Topics"]
    )

    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input(
        "Date range", value=(min_date.date(), max_date.date()),
        min_value=min_date.date(), max_value=max_date.date(),
    )
    products = st.sidebar.multiselect("Product", sorted(df["product"].unique()))
    channels = st.sidebar.multiselect("Channel", sorted(df["channel"].unique()))
    regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()))
    sentiments = st.sidebar.multiselect("Sentiment", sorted(df["sentiment"].unique()))

    # Text Keyword Search Filter
    search_query = st.sidebar.text_input("🔍 Search Feedback Comments", placeholder="e.g. crash, billing, latency, UI...")

    filtered = dp.apply_filters(
        df,
        date_range=date_range if isinstance(date_range, tuple) else None,
        products=products, channels=channels,
        regions=regions, sentiments=sentiments,
    )

    # Apply Quick Preset Filter Logic
    if preset == "⚠️ Critical Complaints (1-2★)":
        filtered = filtered[filtered["rating"] <= 2]
    elif preset == "⭐ Promoters (4-5★)":
        filtered = filtered[filtered["rating"] >= 4]
    elif preset == "📱 Mobile Issues":
        filtered = filtered[filtered["product"].str.contains("Mobile", case=False, na=False)]
    elif preset == "💳 Billing & Latency Topics":
        filtered = filtered[filtered["feedback_text"].str.contains("billing|latency|charge|refund|slow|timeout", case=False, na=False)]

    # Apply Keyword Search Filter
    if search_query:
        filtered = filtered[filtered["feedback_text"].str.contains(search_query, case=False, na=False)]

    # Main Tab Architecture: Core Analytics vs Power BI Enterprise Portal
    tab_main, tab_pbi = st.tabs([
        "📊 Interactive Feedback Dashboard",
        "📈 Power BI Enterprise Portal"
    ])

    # =========================================================================
    # TAB 1: INTERACTIVE FEEDBACK DASHBOARD
    # =========================================================================
    with tab_main:
        kpis = dp.compute_kpis(filtered)
        nps_info = dp.compute_nps(filtered)

        # ---------------- Headline KPI row ----------------
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Feedback", f"{kpis['total_feedback']:,}", delta="100% Validated")
        c2.metric("Avg Rating", f"{kpis['avg_rating']} / 5", delta=f"{kpis['avg_rating'] - 3.5:+.2f} vs Target")
        c3.metric(
            "Net Promoter Score",
            f"{nps_info['nps_score']}",
            delta=f"{nps_info['promoter_pct']}% Promoters",
            delta_color="normal" if nps_info["nps_score"] >= 0 else "inverse",
        )
        c4.metric("Positive %", f"{kpis['positive_pct']}%", delta=f"{nps_info['promoter_count']} reviews")
        c5.metric("Negative %", f"{kpis['negative_pct']}%", delta=f"{nps_info['detractor_count']} complaints", delta_color="inverse")

        st.divider()

        # ---------------- Charts row 1 ----------------
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Sentiment Breakdown")
            if not filtered.empty:
                st.plotly_chart(charts.sentiment_pie(filtered), use_container_width=True)
            else:
                st.info("No data for the current filters.")

        with col2:
            st.subheader("Sentiment Trend Over Time")
            if not filtered.empty:
                trend = dp.sentiment_over_time(filtered, freq="W")
                st.plotly_chart(charts.sentiment_trend_line(trend), use_container_width=True)
            else:
                st.info("No data for the current filters.")

        # ---------------- Charts row 2 ----------------
        col3, col4 = st.columns([1, 1])
        with col3:
            st.subheader("Rating Distribution (1 to 5 Stars)")
            if not filtered.empty:
                dist = dp.rating_distribution(filtered)
                st.plotly_chart(charts.rating_bar(dist), use_container_width=True)
            else:
                st.info("No data for the current filters.")

        with col4:
            st.subheader("Average Rating by Product")
            if not filtered.empty:
                product_df = dp.top_products_by_rating(filtered)
                st.plotly_chart(charts.product_rating_bar(product_df), use_container_width=True)
            else:
                st.info("No data for the current filters.")

        # ---------------- Channel + Matplotlib export ----------------
        col5, col6 = st.columns([1, 1])
        with col5:
            st.subheader("Feedback by Touchpoint Channel")
            if not filtered.empty:
                channel_df = dp.channel_breakdown(filtered)
                st.plotly_chart(charts.channel_donut(channel_df), use_container_width=True)
            else:
                st.info("No data for the current filters.")

        with col6:
            st.subheader("Monthly Average Rating Trajectory")
            if not filtered.empty:
                fig = charts.matplotlib_summary(filtered)
                st.pyplot(fig)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
                st.download_button(
                    "Download Chart as PNG", data=buf.getvalue(),
                    file_name="monthly_rating_trend.png", mime="image/png",
                )
            else:
                st.info("No data for the current filters.")

        st.divider()

        # ---------------- ML-based sentiment (scikit-learn) ----------------
        with st.expander("🧪 ML Sentiment Classifier & Contradiction Lab (Scikit-Learn)", expanded=False):
            st.caption(
                "Evaluates TF-IDF (1, 2) bigrams with negation stop-word preservation on real customer feedback text, "
                "comparing predicted text sentiment against submitted star ratings to detect sarcasm, edge cases, and misclicks."
            )

            if st.button("Train ML Model on Active Dataset"):
                with st.spinner("Training TF-IDF + Logistic Regression Classifier..."):
                    result = ml.train_sentiment_model(filtered)

                if result.get("error"):
                    st.error(result["error"])
                else:
                    m = result["metrics"]
                    mc1, mc2, mc3 = st.columns(3)
                    mc1.metric("Model Accuracy", f"{m['accuracy']*100:.1f}%")
                    mc2.metric("Training Samples", f"{m['train_size']:,}")
                    mc3.metric("Test Samples", f"{m['test_size']:,}")

                    report_df = pd.DataFrame(m["report"]).T.loc[m["labels"]]
                    st.write("Per-class Classification Report (Precision / Recall / F1-Score):")
                    st.dataframe(
                        report_df[["precision", "recall", "f1-score", "support"]].round(2),
                        use_container_width=True,
                    )

                    comparison = ml.compare_with_rule_based(filtered, result["vectorizer"], result["model"])
                    agree_pct = comparison["agrees_with_rule"].mean() * 100
                    st.write(f"**ML Text vs. Star-Rating Agreement: {agree_pct:.1f}%**")

                    disagreements = comparison[~comparison["agrees_with_rule"]]
                    if not disagreements.empty:
                        st.write(f"Detected **{len(disagreements)} Anomaly / Contradiction rows** (Sarcasm, Misclicks, Mixed Reviews):")
                        st.dataframe(
                            disagreements[["customer_name", "product", "rating", "sentiment", "ml_sentiment", "feedback_text"]],
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
                    st.write(f"Predicted Sentiment: **{pred}**")

        st.divider()

        # ---------------- Raw feedback table ----------------
        st.subheader("Customer Feedback Explorer")
        st.caption(f"Showing {len(filtered):,} matching customer submissions")
        st.dataframe(
            filtered[["date", "customer_name", "product", "channel", "region",
                      "rating", "sentiment", "feedback_text"]],
            use_container_width=True, hide_index=True,
        )
        st.download_button(
            "Download Filtered Data as CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="filtered_customer_feedback.csv", mime="text/csv",
        )

    # =========================================================================
    # TAB 2: POWER BI ENTERPRISE PORTAL
    # =========================================================================
    with tab_pbi:
        st.markdown("### 📈 Power BI Enterprise Decision Center")
        st.caption(
            "Integrated Microsoft Power BI architecture: Star Schema Data Modeling, "
            "DAX Time-Intelligence Calculations, Net Promoter Score (NPS), and Live Cloud Embed."
        )

        nps_info = dp.compute_nps(filtered)
        kpi_info = dp.compute_kpis(filtered)

        # Power BI Headline Metric Cards
        pb1, pb2, pb3, pb4, pb5 = st.columns(5)
        pb1.metric("Total Reviews", f"{kpi_info['total_feedback']:,}")
        pb2.metric("Average Rating", f"{kpi_info['avg_rating']} / 5")
        pb3.metric(
            "NPS Score",
            f"{nps_info['nps_score']}",
            delta=f"{nps_info['promoter_pct']}% Promoters",
            delta_color="normal" if nps_info["nps_score"] >= 0 else "inverse",
        )
        pb4.metric("CSAT %", f"{nps_info['csat_pct']}%")
        pb5.metric("Detractor Count", f"{nps_info['detractor_count']} ({nps_info['detractor_pct']}%)")

        st.divider()

        # Visual Row 1: NPS Gauge + Breakdown Bar + Product vs Channel Heatmap
        v_col1, v_col2 = st.columns([1, 1])

        with v_col1:
            st.subheader("🎯 Net Promoter Score (NPS) Gauge")
            st.caption("Standard 5-star NPS: 4-5★ Promoters, 3★ Passives, 1-2★ Detractors. Scale: -100 to +100.")
            if not filtered.empty:
                st.plotly_chart(charts.nps_gauge(nps_info["nps_score"]), use_container_width=True)
                st.plotly_chart(charts.nps_breakdown_bar(nps_info), use_container_width=True)
            else:
                st.info("No data to calculate NPS.")

        with v_col2:
            st.subheader("🔥 Product vs Channel Matrix Visual")
            st.caption("Power BI Matrix cross-tabulation of average customer satisfaction score.")
            if not filtered.empty:
                matrix_data = dp.product_channel_matrix_data(filtered)
                st.plotly_chart(charts.product_channel_heatmap(matrix_data), use_container_width=True)
            else:
                st.info("No data for Matrix visual.")

        st.divider()

        # Section 1: Power BI Data Generation & Export Center
        with st.expander("📦 Step 1 & 2: Generate & Export Cleaned Power BI Datasets", expanded=True):
            st.markdown(
                """
                **Enterprise Power BI Integration Workflow:**
                1. **Python Ingestion & Cleaning:** Raw files are normalized, bounded, deduplicated, and typed by Pandas.
                2. **Dual-Model Export:** Export as either a **Single Flat Table** (simple setup) or **Star Schema** (enterprise VertiPaq performance).
                3. **Power BI Ingestion:** Load into Power BI Desktop with zero conflicting transformation rules.
                """
            )

            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                st.markdown("#### Option A: Single Analytical Table")
                st.caption("Best for quick reporting without relationship configuration.")
                flat_pbi_df = pbi.prepare_powerbi_dataset(filtered)
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=flat_pbi_df.to_csv(index=False).encode("utf-8"),
                        file_name="cleaned_customer_feedback.csv",
                        mime="text/csv",
                        help="Cleaned analytical flat table in CSV format.",
                    )
                with c_btn2:
                    excel_buf = io.BytesIO()
                    flat_pbi_df.to_excel(excel_buf, index=False, engine="openpyxl")
                    st.download_button(
                        label="⬇️ Download Excel (.xlsx)",
                        data=excel_buf.getvalue(),
                        file_name="cleaned_customer_feedback.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Cleaned analytical flat table in Excel format.",
                    )

            with exp_col2:
                st.markdown("#### Option B: Star Schema Dimensional Package")
                st.caption("Recommended for enterprise Power BI data modeling (VertiPaq engine).")
                zip_data = pbi.export_powerbi_zip(filtered)
                st.download_button(
                    label="⬇️ Download Star Schema Package (.zip)",
                    data=zip_data,
                    file_name="CustomerFeedback_PowerBI_Package.zip",
                    mime="application/zip",
                    help="Contains Fact_CustomerFeedback, Dim_Date, Dim_Product, Dim_Channel, Dim_Region, Dim_Sentiment, and DAX measures.",
                )

            st.write("---")
            if st.button("💾 Generate & Save Directly to 'powerbi/' Folder"):
                generated_map = pbi.export_powerbi_bundle(filtered, "powerbi")
                st.success(f"Successfully generated {len(generated_map)} files in the project's `powerbi/` directory!")

        # Section 2: Step-by-Step Reporting Workflow
        with st.expander("🛠️ Step 3 & 4: Power BI Desktop Setup & Reporting Workflow", expanded=False):
            st.markdown(
                """
                ### Step-by-Step Power BI Desktop Workflow:
                1. **Import:** Open Power BI Desktop $\\rightarrow$ **Get Data** $\\rightarrow$ **Text/CSV** $\\rightarrow$ select `powerbi/Fact_CustomerFeedback.csv` and the 5 `Dim_*.csv` files.
                2. **Relationships:** Switch to **Model View** and verify 1-to-many relationships ($1 \\rightarrow *$) with **Single** cross-filter direction:
                   - `Dim_Date[DateKey]` $\\longrightarrow$ `Fact_CustomerFeedback[DateKey]`
                   - `Dim_Product[ProductKey]` $\\longrightarrow$ `Fact_CustomerFeedback[ProductKey]`
                   - `Dim_Channel[ChannelKey]` $\\longrightarrow$ `Fact_CustomerFeedback[ChannelKey]`
                   - `Dim_Region[RegionKey]` $\\longrightarrow$ `Fact_CustomerFeedback[RegionKey]`
                   - `Dim_Sentiment[SentimentKey]` $\\longrightarrow$ `Fact_CustomerFeedback[SentimentKey]`
                3. **Date Table:** Right-click `Dim_Date` $\\rightarrow$ **Mark as Date Table** $\\rightarrow$ select `Date`.
                4. **Add Measures:** Copy DAX measures from `powerbi/dax_measures.dax` into `Fact_CustomerFeedback`.
                5. **Build 5 Core Pages:** Follow specifications in `powerbi/REPORT_SPECIFICATIONS.md` to configure:
                   - **Page 1:** Executive Overview
                   - **Page 2:** Product Analysis
                   - **Page 3:** Sentiment Analysis
                   - **Page 4:** Customer and Channel Analysis
                   - **Page 5:** Detailed Feedback
                """
            )

        # Section 3: Live Power BI Cloud Report Embedder (Optional Viewer)
        with st.expander("🌐 Accessing the Power BI Report & Cloud Embedder", expanded=False):
            st.markdown(
                """
                **Report Access Modes:**
                - **Desktop Reporting:** Open your local `.pbix` file configured with the `powerbi/` datasets.
                - **Power BI Service (Cloud):** Once published to `app.powerbi.com`, you can share reports, schedule auto-refresh, and optionally embed the report here.
                """
            )
            embed_url = st.text_input(
                "Power BI Embed URL (e.g., https://app.powerbi.com/view?r=...)",
                value="",
                placeholder="https://app.powerbi.com/view?r=eyJrIjoi...",
                help="Requires a Power BI report published via 'Publish to Web' in Power BI Service.",
            )

            if embed_url:
                try:
                    components.iframe(src=embed_url, height=620, scrolling=True)
                except Exception as e:
                    st.error(f"Failed to render iframe: {e}")
            else:
                st.info(
                    "💡 *Note on embedding:* Power BI reports are created in Microsoft Power BI Desktop. "
                    "To view a live report inside this web interface, publish the `.pbix` to **Power BI Service** "
                    "(`app.powerbi.com`), select **File > Embed report > Publish to web (public)**, and paste the URL above."
                )

        # Section 4: Production DAX Measures Reference Library
        with st.expander("📐 Power BI DAX Measures Reference Library", expanded=False):
            st.markdown("Use these DAX formulas directly in Power BI Desktop for calculated KPI cards and charts:")
            st.code(pbi.get_dax_measures(), language="sql")


if __name__ == "__main__":
    main()

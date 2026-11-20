"""
Verification & Validation Test Suite for Power BI Integration Pipeline
Compares Python / Pandas metrics with Power BI DAX formula logic.
"""
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath("."))
import modules.data_processor as dp
import modules.power_bi_export as pbi


def run_validation():
    print("=================================================================")
    print(" POWER BI INTEGRATION PIPELINE - VERIFICATION & VALIDATION TEST")
    print("=================================================================")

    # 1. Ingest raw data
    raw_path = "data/customer_feedback.csv"
    assert os.path.exists(raw_path), f"Raw file not found: {raw_path}"
    raw_df = dp.load_data(raw_path)
    print(f"[✓] Step 1: Raw data loaded successfully ({len(raw_df)} rows)")

    # 2. Clean data
    clean_df = dp.clean_data(raw_df)
    assert len(clean_df) > 0, "Cleaned data is empty"
    print(f"[✓] Step 2: Cleaned data generated ({len(clean_df)} rows)")

    # 3. Validation: Rating bounds [1, 5]
    assert clean_df["rating"].min() >= 1, "Rating below 1 found"
    assert clean_df["rating"].max() <= 5, "Rating above 5 found"
    print(f"[✓] Step 3: Ratings bounded strictly in [1, 5] (Min: {clean_df['rating'].min()}, Max: {clean_df['rating'].max()})")

    # 4. Validation: Deduplication & Dates
    assert clean_df["date"].isna().sum() == 0, "Null dates present in clean data"
    assert clean_df.duplicated(subset=["feedback_id", "customer_name", "date", "feedback_text"]).sum() == 0, "Duplicates found"
    print(f"[✓] Step 4: No null dates or duplicate submissions")

    # 5. Export to powerbi/
    generated = pbi.export_powerbi_bundle(clean_df, "powerbi")
    for key, path in generated.items():
        assert os.path.exists(path), f"Generated file missing: {path}"
        assert os.path.getsize(path) > 0, f"Generated file is empty: {path}"
    print(f"[✓] Step 5: Exported all {len(generated)} Power BI files to powerbi/ directory")

    # 6. Read back and validate powerbi/cleaned_customer_feedback.csv
    flat_csv = pd.read_csv("powerbi/cleaned_customer_feedback.csv")
    assert len(flat_csv) == len(clean_df), f"Row count mismatch: {len(flat_csv)} vs {len(clean_df)}"
    print(f"[✓] Step 6: Flat Power BI analytical CSV verified ({len(flat_csv)} rows, {len(flat_csv.columns)} columns)")

    # 7. Read back and validate Star Schema
    fact_df = pd.read_csv("powerbi/Fact_CustomerFeedback.csv")
    dim_date = pd.read_csv("powerbi/Dim_Date.csv")
    dim_product = pd.read_csv("powerbi/Dim_Product.csv")
    dim_channel = pd.read_csv("powerbi/Dim_Channel.csv")
    dim_region = pd.read_csv("powerbi/Dim_Region.csv")
    dim_sentiment = pd.read_csv("powerbi/Dim_Sentiment.csv")

    assert len(fact_df) == len(clean_df), "Fact table row count mismatch"
    assert len(dim_product) == clean_df["product"].nunique(), "Dim_Product count mismatch"
    assert len(dim_channel) == clean_df["channel"].nunique(), "Dim_Channel count mismatch"
    assert len(dim_region) == clean_df["region"].nunique(), "Dim_Region count mismatch"
    assert len(dim_sentiment) == 3, "Dim_Sentiment count mismatch"
    print(f"[✓] Step 7: Star Schema tables verified (Fact: {len(fact_df)}, Date: {len(dim_date)}, Product: {len(dim_product)}, Channel: {len(dim_channel)}, Region: {len(dim_region)}, Sentiment: {len(dim_sentiment)})")

    # 8. Compare Python KPIs with Power BI DAX Formulas
    py_kpis = dp.compute_kpis(clean_df)
    py_nps = dp.compute_nps(clean_df)

    # Simulated DAX Measures over Fact table
    dax_total_feedback = len(fact_df)
    dax_avg_rating = round(fact_df["Rating"].mean(), 2)
    dax_pos_count = int(fact_df["IsPositive"].sum())
    dax_neg_count = int(fact_df["IsNegative"].sum())
    dax_neu_count = int(fact_df["IsNeutral"].sum())
    dax_pos_pct = round((dax_pos_count / dax_total_feedback) * 100, 1)
    dax_neg_pct = round((dax_neg_count / dax_total_feedback) * 100, 1)

    promoters = int((fact_df["Rating"] >= 4).sum())
    detractors = int((fact_df["Rating"] <= 2).sum())
    dax_nps = round(((promoters - detractors) / dax_total_feedback) * 100, 1)

    print("\n-----------------------------------------------------------------")
    print(" METRICS COMPARISON: PYTHON / PANDAS vs. POWER BI DAX")
    print("-----------------------------------------------------------------")
    print(f" Measure: Total Feedback        | Python: {py_kpis['total_feedback']} | DAX: {dax_total_feedback} | MATCH: {py_kpis['total_feedback'] == dax_total_feedback}")
    print(f" Measure: Average Rating        | Python: {py_kpis['avg_rating']} | DAX: {dax_avg_rating} | MATCH: {py_kpis['avg_rating'] == dax_avg_rating}")
    print(f" Measure: Positive Feedback %   | Python: {py_kpis['positive_pct']}% | DAX: {dax_pos_pct}% | MATCH: {py_kpis['positive_pct'] == dax_pos_pct}")
    print(f" Measure: Negative Feedback %   | Python: {py_kpis['negative_pct']}% | DAX: {dax_neg_pct}% | MATCH: {py_kpis['negative_pct'] == dax_neg_pct}")
    print(f" Measure: Net Promoter Score    | Python: {py_nps['nps_score']} | DAX: {dax_nps} | MATCH: {py_nps['nps_score'] == dax_nps}")
    print(f" Measure: Positive Count        | DAX: {dax_pos_count} rows")
    print(f" Measure: Negative Count        | DAX: {dax_neg_count} rows")
    print(f" Measure: Neutral Count         | DAX: {dax_neu_count} rows")
    print(f" Measure: Total Products        | DAX: {len(dim_product)} products")

    assert py_kpis['total_feedback'] == dax_total_feedback
    assert py_kpis['avg_rating'] == dax_avg_rating
    assert py_kpis['positive_pct'] == dax_pos_pct
    assert py_kpis['negative_pct'] == dax_neg_pct
    assert py_nps['nps_score'] == dax_nps

    print("-----------------------------------------------------------------")
    print(" ALL 8 VALIDATION CHECKS PASSED WITH 100% MATHEMATICAL INTEGRITY!")
    print("=================================================================")


if __name__ == "__main__":
    run_validation()

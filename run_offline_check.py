import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import pandas as pd
import modules.data_processor as dp
import modules.charts as charts
import modules.ml_sentiment as ml

print("========================================")
print(" 1. DATA INGESTION & CLEANING")
print("========================================")
raw = dp.load_data('data/customer_feedback.csv')
clean = dp.clean_data(raw)
print(f"Raw rows: {len(raw)}, Clean rows: {len(clean)}")
print("Clean columns:", clean.columns.tolist())
print("\nSample clean row:")
for k, v in clean.iloc[0].to_dict().items():
    print(f"  {k}: {v}")

print("\n========================================")
print(" 2. HEADLINE BUSINESS KPIS")
print("========================================")
kpis = dp.compute_kpis(clean)
for k, v in kpis.items():
    print(f"  • {k.replace('_', ' ').title()}: {v}")

print("\n========================================")
print(" 3. TOP PRODUCTS BY RATING")
print("========================================")
print(dp.top_products_by_rating(clean).to_string(index=False))

print("\n========================================")
print(" 4. RATING DISTRIBUTION (1 to 5 Stars)")
print("========================================")
print(dp.rating_distribution(clean).to_string(index=False))

print("\n========================================")
print(" 5. FEEDBACK BY CHANNEL")
print("========================================")
print(dp.channel_breakdown(clean).to_string(index=False))

print("\n========================================")
print(" 6. MACHINE LEARNING SENTIMENT MODEL")
print("========================================")
model_dict = ml.train_sentiment_model(clean)
metrics = model_dict["metrics"]
print(f"Model Accuracy: {metrics['accuracy'] * 100:.1f}%")
print(f"Training set: {metrics['train_size']} samples, Test set: {metrics['test_size']} samples")

report_df = pd.DataFrame(metrics["report"]).transpose()
print("\nClassification Report (Precision / Recall / F1-Score):")
print(report_df.round(2).to_string())

print("\n========================================")
print(" 7. STAR RATING VS TEXT CONTRADICTIONS")
print("========================================")
contras = ml.compare_with_rule_based(clean, model_dict['vectorizer'], model_dict['model'])
mismatches = contras[~contras['agrees_with_rule']]
print(f"Total rows where ML text sentiment contradicted star rating: {len(mismatches)}")
if len(mismatches) > 0:
    print("\nSample Mismatches:")
    print(mismatches[['rating', 'sentiment', 'ml_sentiment', 'feedback_text']].head(5).to_string(index=False))

print("\n========================================")
print(" 8. REPORT CHART EXPORT (MATPLOTLIB)")
print("========================================")
fig = charts.matplotlib_summary(clean)
output_chart = os.path.join(os.path.abspath('.'), 'monthly_rating_trend.png')
fig.savefig(output_chart, dpi=150, bbox_inches='tight')
print(f"Saved static high-resolution chart to: {output_chart}")

print("\n========================================")
print(" 9. POWER BI STAR SCHEMA & DAX EXPORT")
print("========================================")
import modules.power_bi_export as pbi
schema = pbi.create_star_schema(clean)
for table_name, t_df in schema.items():
    print(f"  • {table_name}: {len(t_df)} rows, columns: {list(t_df.columns)}")

nps_data = dp.compute_nps(clean)
print(f"\nNet Promoter Score (NPS): {nps_data['nps_score']} | CSAT: {nps_data['csat_pct']}%")
print(f"Promoters: {nps_data['promoter_count']} ({nps_data['promoter_pct']}%), Detractors: {nps_data['detractor_count']} ({nps_data['detractor_pct']}%)")

out_dir = pbi.save_star_schema_to_disk(clean, "power_bi_export")
zip_bytes = pbi.export_star_schema_zip(clean)
print(f"Generated Power BI Star Schema in '{out_dir}/' and ZIP package ({len(zip_bytes)} bytes)")
print("========================================")
print(" ALL PIPELINE & POWER BI STEPS EXECUTED SUCCESSFULLY!")
print("========================================")

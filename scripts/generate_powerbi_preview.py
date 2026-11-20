"""
Generates a visual mockup of the Power BI Customer Feedback Dashboard using Matplotlib.
Creates an executive-ready representation of Page 1: Executive Overview.
"""
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 1. Load data
clean_df = pd.read_csv("powerbi/cleaned_customer_feedback.csv")
total_feedback = len(clean_df)
avg_rating = clean_df["rating"].mean()
pos_count = (clean_df["sentiment"] == "Positive").sum()
neg_count = (clean_df["sentiment"] == "Negative").sum()
neu_count = (clean_df["sentiment"] == "Neutral").sum()
pos_pct = (pos_count / total_feedback) * 100
neg_pct = (neg_count / total_feedback) * 100

promoters = (clean_df["rating"] >= 4).sum()
detractors = (clean_df["rating"] <= 2).sum()
nps_score = ((promoters - detractors) / total_feedback) * 100

# 2. Setup Figure styling (Power BI theme)
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig = plt.figure(figsize=(15, 9), facecolor="#F4F6F9")

gs = gridspec.GridSpec(3, 4, figure=fig, height_ratios=[0.8, 2.2, 2.2], wspace=0.3, hspace=0.45)

# Banner Title
fig.text(0.04, 0.96, "Microsoft Power BI — Customer Feedback Executive Center", fontsize=18, fontweight="bold", color="#1E2A38")
fig.text(0.04, 0.93, "Page 1: Executive Overview | Connected to Python Data Pipeline (600 records)", fontsize=11, color="#6C7A89")

# --- ROW 0: KPI CARDS ---
kpi_specs = [
    ("TOTAL FEEDBACK", f"{total_feedback:,}", "100% Validated Rows", "#1E2A38"),
    ("AVERAGE RATING", f"{avg_rating:.2f} / 5", "Target: 4.00 ★", "#2980B9"),
    ("POSITIVE FEEDBACK", f"{pos_pct:.1f}%", f"{pos_count} Reviews", "#27AE60"),
    ("NET PROMOTER SCORE", f"+{nps_score:.1f}", f"Promoters: {promoters} | Detractors: {detractors}", "#27AE60" if nps_score >= 0 else "#C0392B"),
]

for i, (title, val, sub, col) in enumerate(kpi_specs):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color("#E0E6ED")
        spine.set_linewidth(1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.08, 0.72, title, fontsize=9, fontweight="bold", color="#7F8C8D")
    ax.text(0.08, 0.35, val, fontsize=20, fontweight="bold", color=col)
    ax.text(0.08, 0.12, sub, fontsize=8, color="#95A5A6")

# --- ROW 1, COL 0: SENTIMENT DISTRIBUTION (DONUT) ---
ax_donut = fig.add_subplot(gs[1, 0:2])
ax_donut.set_facecolor("white")
sent_counts = [pos_count, neu_count, neg_count]
sent_labels = [f"Positive ({pos_pct:.1f}%)", f"Neutral ({neu_count/total_feedback*100:.1f}%)", f"Negative ({neg_pct:.1f}%)"]
colors = ["#2ECC71", "#F1C40F", "#E74C3C"]
wedges, texts, autotexts = ax_donut.pie(
    sent_counts, labels=sent_labels, colors=colors, autopct="%1.0f%%",
    startangle=140, pctdistance=0.75, textprops=dict(color="#2C3E50", fontsize=9, fontweight="bold")
)
centre_circle = plt.Circle((0, 0), 0.52, fc="white")
ax_donut.add_artist(centre_circle)
ax_donut.set_title("Overall Sentiment Breakdown", fontsize=11, fontweight="bold", pad=12, color="#2C3E50")

# --- ROW 1, COL 2-3: MONTHLY RATING TRAJECTORY ---
ax_trend = fig.add_subplot(gs[1, 2:4])
ax_trend.set_facecolor("white")
clean_df["date_dt"] = pd.to_datetime(clean_df["date"])
monthly = clean_df.set_index("date_dt")["rating"].resample("ME").mean().dropna()
ax_trend.plot(monthly.index.strftime("%b %y"), monthly.values, marker="o", color="#2980B9", linewidth=2.5, markersize=5)
ax_trend.set_ylim(2.5, 4.5)
ax_trend.axhline(3.5, color="#27AE60", linestyle="--", alpha=0.6, label="Benchmark (3.50)")
ax_trend.set_title("Monthly Average Rating Trajectory (Time Intelligence)", fontsize=11, fontweight="bold", color="#2C3E50")
ax_trend.tick_params(axis="x", rotation=35, labelsize=8)
ax_trend.grid(True, linestyle=":", alpha=0.5)
ax_trend.legend(loc="lower right", fontsize=8)

# --- ROW 2, COL 0-1: RATING DISTRIBUTION (BAR) ---
ax_rating = fig.add_subplot(gs[2, 0:2])
ax_rating.set_facecolor("white")
rating_counts = clean_df["rating"].value_counts().sort_index()
bars = ax_rating.bar([f"{r} ★" for r in rating_counts.index], rating_counts.values, color=["#E74C3C", "#E67E22", "#F1C40F", "#3498DB", "#2ECC71"], width=0.55)
for bar in bars:
    yval = bar.get_height()
    ax_rating.text(bar.get_x() + bar.get_width()/2, yval + 3, f"{int(yval)}", ha="center", va="bottom", fontsize=8, fontweight="bold")
ax_rating.set_title("Rating Distribution (1 to 5 Stars)", fontsize=11, fontweight="bold", color="#2C3E50")
ax_rating.set_ylim(0, max(rating_counts.values) + 25)
ax_rating.grid(axis="y", linestyle=":", alpha=0.5)

# --- ROW 2, COL 2-3: FEEDBACK BY PRODUCT ---
ax_prod = fig.add_subplot(gs[2, 2:4])
ax_prod.set_facecolor("white")
prod_stats = clean_df.groupby("product").agg(avg_rating=("rating", "mean"), count=("rating", "size")).sort_values("avg_rating")
bars_prod = ax_prod.barh(prod_stats.index, prod_stats["avg_rating"], color="#34495E", height=0.55)
for bar in bars_prod:
    xval = bar.get_width()
    ax_prod.text(xval + 0.05, bar.get_y() + bar.get_height()/2, f"{xval:.2f} ★", ha="left", va="center", fontsize=8, fontweight="bold", color="#2C3E50")
ax_prod.set_xlim(0, 5)
ax_prod.set_title("Average Satisfaction Rating by Product Tier", fontsize=11, fontweight="bold", color="#2C3E50")
ax_prod.grid(axis="x", linestyle=":", alpha=0.5)

# Save
output_png = "powerbi/powerbi_report_preview.png"
fig.savefig(output_png, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Generated Power BI preview: {output_png}")

# Also copy to conversation artifact directory if available
art_dir = r"C:\Users\hp\.gemini\antigravity\brain\01dd2fb4-2df4-4fb9-a1e4-4a5034242d29"
if os.path.exists(art_dir):
    dest = os.path.join(art_dir, "powerbi_report_preview.png")
    shutil.copy2(output_png, dest)
    print(f"Copied to artifact directory: {dest}")

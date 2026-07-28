"""
Generates a synthetic customer feedback dataset so the dashboard has
something to load out of the box. Run once: python data/generate_sample_data.py
"""
import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(42)

PRODUCTS = ["Basic Plan", "Pro Plan", "Enterprise Plan", "Mobile App", "Browser Extension"]
CHANNELS = ["Email", "In-App Survey", "App Store Review", "Support Ticket", "Twitter/X"]
REGIONS = ["North America", "Europe", "APAC", "LATAM", "MEA"]

POSITIVE_SNIPPETS = [
    "Really happy with the {p}, it saved me a ton of time.",
    "Great support experience, resolved my issue quickly on the {p}.",
    "Love the new update to the {p}, much smoother now.",
    "The {p} is intuitive and easy to use.",
    "Excellent value for money with the {p}.",
]
NEUTRAL_SNIPPETS = [
    "The {p} works fine, nothing special.",
    "It does what it says, could use more features.",
    "Average experience with the {p} so far.",
    "The {p} is okay but the onboarding was confusing.",
]
NEGATIVE_SNIPPETS = [
    "The {p} keeps crashing on my device.",
    "Support took too long to respond about the {p}.",
    "Billing issue with the {p}, still not resolved.",
    "The {p} is too slow and laggy.",
    "Not happy with recent changes to the {p}.",
]

rows = []
start_date = datetime(2025, 1, 1)

for i in range(1, 601):
    product = random.choice(PRODUCTS)
    channel = random.choice(CHANNELS)
    region = random.choice(REGIONS)
    date = start_date + timedelta(days=random.randint(0, 540))

    sentiment_roll = random.random()
    if sentiment_roll < 0.55:
        rating = random.choice([4, 5])
        text = random.choice(POSITIVE_SNIPPETS).format(p=product)
        sentiment = "Positive"
    elif sentiment_roll < 0.80:
        rating = 3
        text = random.choice(NEUTRAL_SNIPPETS).format(p=product)
        sentiment = "Neutral"
    else:
        rating = random.choice([1, 2])
        text = random.choice(NEGATIVE_SNIPPETS).format(p=product)
        sentiment = "Negative"

    rows.append({
        "feedback_id": f"FB{i:04d}",
        "date": date.strftime("%Y-%m-%d"),
        "customer_name": f"Customer {i}",
        "product": product,
        "channel": channel,
        "region": region,
        "rating": rating,
        "sentiment": sentiment,
        "feedback_text": text,
    })

df = pd.DataFrame(rows)
df.to_csv("data/customer_feedback.csv", index=False)
print(f"Generated {len(df)} rows -> data/customer_feedback.csv")

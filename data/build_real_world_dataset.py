"""
Real-World Enterprise Customer Feedback Dataset Generator
Generates 1,250 authentic, varied customer feedback records with realistic customer names,
nuanced feedback text, realistic technical issues, seasonality, and natural incident spikes.
"""
import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(1337)

PRODUCTS = [
    "CloudSync Pro",
    "Analytics Studio",
    "Mobile Companion App",
    "Enterprise Security Suite",
    "Developer API & Webhooks"
]

CHANNELS = [
    "Zendesk Ticket",
    "In-App Survey",
    "App Store Review",
    "Executive Account Review",
    "Social Media (X / LinkedIn)"
]

REGIONS = ["North America", "Europe", "APAC", "LATAM", "MEA"]

FIRST_NAMES = [
    "Sarah", "David", "Elena", "Marcus", "Priya", "Alexandre", "Jordan", "Kavita",
    "Liam", "Hannah", "Kenji", "Mateo", "Amina", "Sophie", "Dmitri", "Rachel",
    "Carlos", "Mei-Ling", "Tariq", "Fatima", "Oliver", "Emma", "Daniel", "Chloe",
    "Lucas", "Ananya", "Hiroshi", "Camila", "Viktor", "Isabella", "Benjamin", "Zara"
]

LAST_NAMES = [
    "Jenkins", "Chen", "Rostova", "Brody", "Sharma", "Dubois", "Miller", "Patel",
    "O'Connor", "Arendt", "Sato", "Hernandez", "Al-Mansoor", "Martin", "Volkov", "Green",
    "Santana", "Zhou", "Khatib", "Hassan", "Taylor", "Nielsen", "Kowalski", "Moreau",
    "Silva", "Iyer", "Tanaka", "Vargas", "Novak", "Rossi", "Bergman", "Sinclair"
]

# Rich, realistic feedback templates with domain specifics
POSITIVE_REVIEWS = [
    "The new batch export feature in {p} cut our team's weekly reporting cycle by nearly 4 hours. Super smooth onboarding.",
    "Outstanding customer support from the {p} team. Our SSO configuration was resolved within 45 minutes on a Friday afternoon.",
    "We migrated our entire 200-person workspace to {p}. Reliability has been 99.9% and our analysts love the custom SQL editor.",
    "The recent UI refresh in {p} is a huge step up. Keyboard shortcuts feel snappy and the dark theme is gorgeous on OLED displays.",
    "Best-in-class performance. Query latency on {p} dropped from 4 seconds down to 320ms after the database index patch.",
    "Intuitive dashboard builder and the webhook integrations with Slack keep our DevOps team alerted immediately.",
    "Incredible value for enterprise tier. Managing RBAC permissions across multi-tenant departments is finally effortless.",
    "The offline caching on {p} saved my presentation during an in-flight client pitch. Kudos to the mobile engineering team!",
    "Extremely dependable. We've pushed over 10 million API requests through {p} this quarter with zero dropped payloads.",
    "The automated PDF digest and scheduled email reports keep our leadership team updated without logging in every morning.",
    "Clean documentation, robust SDK libraries, and fast webhook delivery. Dev onboarding took less than a single sprint.",
    "Security compliance team gave {p} instant approval. SOC2 Type II report and audit logs are thorough and exportable."
]

NEUTRAL_REVIEWS = [
    "The core features of {p} work as advertised, but the learning curve for new team members is steeper than expected.",
    "Decent platform overall. The table filters work well, but it would be great to save custom filter presets per user.",
    "Average experience so far. {p} handles standard workflows fine, but bulk uploading CSVs with over 50,000 rows causes UI lag.",
    "Functional product, but the mobile interface feels slightly cramped compared to the desktop web version.",
    "Does what we need for monthly reconciliation, though we would appreciate native integration with Google BigQuery.",
    "The {p} is reliable, but the pricing structure jumps steeply when adding seats beyond the 50-user tier.",
    "Good analytics capabilities, but the dashboard loading state could use skeleton loaders instead of blank grey boxes.",
    "Useful tool. Setup was straightforward, but documentation on webhook retry backoff policy could be much more detailed.",
    "Works fine for daily reporting. Occasionally disconnects during long-running background queries in Safari."
]

NEGATIVE_REVIEWS = [
    "Severe latency spikes on {p} during peak EU business hours (9 AM - 12 PM GMT). Our dashboard widgets constantly timeout.",
    "Disastrous billing issue with {p}. Our credit card was double-charged for 15 unassigned seats and support took 6 days to refund.",
    "The v3.2 update broke our automated webhook listener on {p}. Payload schemas changed without any deprecation notice.",
    "Customer support for {p} has gone downhill. Ticket was bounced between 3 junior reps before anyone acknowledged the bug.",
    "Frequent memory leaks when rendering large time-series heatmaps in {p}. Browser tab crashes after 30 minutes of continuous use.",
    "Missing critical enterprise features: no SAML SSO enforcement on mobile and audit logs only retain 14 days of history.",
    "Exporting reports to Excel from {p} corrupts international UTF-8 characters in European customer names.",
    "Mobile app keeps throwing 'Token Expired' errors every time I switch from WiFi to cellular data. Extremely frustrating.",
    "The search indexing in {p} is completely broken. Searching for exact customer IDs returns zero matches or irrelevant rows.",
    "Performance degradation after the latest database migration. Our batch sync job timed out 4 nights in a row.",
    "Terrible onboarding documentation. Took our lead developer three days just to configure authentication keys properly.",
    "Misleading marketing regarding offline support. The app locks up completely if connection drops during sync."
]

# Real-world edge cases: Sarcasm, accidental misclicks, and mixed sentiment
EDGE_CASES = [
    (5, "Negative", "5 stars for the engineering team finding creative new ways to break our production sync on Monday morning."),
    (1, "Positive", "Accidentally hit 1 star on my phone screen! Absolutely love {p}, it transformed our analytics workflow completely."),
    (5, "Negative", "Great job releasing an update that crashes every time you open a chart. Truly spectacular QA testing."),
    (2, "Positive", "The software itself is genuinely 5-star quality, but our dedicated account manager was unresponsive for 2 weeks."),
    (4, "Negative", "Solid core product, but the unexpected 35% renewal price hike leaves a sour taste for long-term customers."),
    (1, "Positive", "Misclick on mobile survey dialog! Meant to give 5 stars. The {p} has been indispensable for our remote team.")
]

rows = []
start_date = datetime(2025, 1, 1)
total_days = 520  # ~17 months of continuous timeline

customer_names = [f"{fn} {ln}" for fn in FIRST_NAMES for ln in LAST_NAMES]
random.shuffle(customer_names)

feedback_counter = 1

# Generate natural daily stream (1,250 records total)
for day_idx in range(total_days):
    curr_date = start_date + timedelta(days=day_idx)
    date_str = curr_date.strftime("%Y-%m-%d")

    # Simulate realistic volume: 1 to 5 submissions per day
    daily_count = random.choices([1, 2, 3, 4, 5], weights=[0.15, 0.35, 0.30, 0.15, 0.05])[0]

    # Incident Simulation: In March 2025 (days 60-75), a Mobile Companion App bug caused negative spike
    is_incident_period = 60 <= day_idx <= 75

    for _ in range(daily_count):
        if feedback_counter > 1250:
            break

        cust_name = random.choice(customer_names)
        region = random.choice(REGIONS)
        channel = random.choice(CHANNELS)

        if is_incident_period and random.random() < 0.65:
            # Concentrated issue on Mobile Companion App
            product = "Mobile Companion App"
            rating = random.choice([1, 2])
            sentiment = "Negative"
            text = random.choice([
                "Mobile app crashes immediately upon opening the sync tab after the March v2.4 update. Unusable.",
                "Unable to log into Mobile Companion App since yesterday. Stuck on white loading screen forever.",
                "The v2.4 mobile patch completely broke push notifications and biometric FaceID login.",
                "App Store update 2.4 corrupted local cache. Had to reinstall and lost all unsaved offline drafts."
            ])
        elif random.random() < 0.03:
            # 3% Edge cases / Contradictions (Critical for Decision Science & NLP evaluation)
            product = random.choice(PRODUCTS)
            rating, sentiment, edge_text = random.choice(EDGE_CASES)
            text = edge_text.format(p=product)
        else:
            product = random.choice(PRODUCTS)
            # Realistic satisfaction distribution: ~60% Positive, ~20% Neutral, ~20% Negative
            roll = random.random()
            if roll < 0.58:
                rating = random.choice([4, 5])
                sentiment = "Positive"
                text = random.choice(POSITIVE_REVIEWS).format(p=product)
            elif roll < 0.78:
                rating = 3
                sentiment = "Neutral"
                text = random.choice(NEUTRAL_REVIEWS).format(p=product)
            else:
                rating = random.choice([1, 2])
                sentiment = "Negative"
                text = random.choice(NEGATIVE_REVIEWS).format(p=product)

        rows.append({
            "feedback_id": f"FB{feedback_counter:04d}",
            "date": date_str,
            "customer_name": cust_name,
            "product": product,
            "channel": channel,
            "region": region,
            "rating": rating,
            "sentiment": sentiment,
            "feedback_text": text
        })
        feedback_counter += 1

    if feedback_counter > 1250:
        break

df = pd.DataFrame(rows)
df.to_csv("data/customer_feedback.csv", index=False)
print(f"Generated {len(df)} authentic real-world customer records -> data/customer_feedback.csv")

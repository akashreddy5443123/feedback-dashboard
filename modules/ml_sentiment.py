"""
ML Sentiment Model (scikit-learn)
TF-IDF + Logistic Regression classifier for text-based sentiment classification.
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_sentiment_model(df: pd.DataFrame) -> dict:
    """
    Trains TF-IDF + Logistic Regression on df['feedback_text'] -> df['sentiment'].
    Uses bigrams (ngram_range=(1, 2)) and preserves negation words (not, no, never)
    so phrases like 'not good product' are accurately classified as Negative.
    Returns a dict with model, vectorizer, metrics, or 'error' if insufficient data.
    """
    if df.empty or "feedback_text" not in df.columns or "sentiment" not in df.columns:
        return {"error": "Dataset must contain 'feedback_text' and 'sentiment' columns."}

    clean_df = df.dropna(subset=["feedback_text", "sentiment"]).copy()
    clean_df["feedback_text"] = clean_df["feedback_text"].astype(str).str.strip()
    clean_df = clean_df[clean_df["feedback_text"] != ""]

    if len(clean_df) < 10:
        return {"error": "Not enough valid data points to train model (at least 10 required)."}

    if clean_df["sentiment"].nunique() < 2:
        return {"error": "Dataset must contain at least 2 distinct sentiment classes for training."}

    X = clean_df["feedback_text"]
    y = clean_df["sentiment"]

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    # Preserve negation words in stop words list so "not", "no", "never" are kept
    negation_words = {"not", "no", "never", "neither", "nor", "none", "cannot"}
    custom_stop_words = [w for w in ENGLISH_STOP_WORDS if w not in negation_words]

    # Use unigrams + bigrams (1, 2) to capture phrases like "not good", "too slow"
    vectorizer = TfidfVectorizer(
        max_features=2500,
        ngram_range=(1, 2),
        stop_words=custom_stop_words,
        lowercase=True,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    labels = sorted(list(y.unique()))

    return {
        "vectorizer": vectorizer,
        "model": model,
        "metrics": {
            "accuracy": float(acc),
            "train_size": len(X_train),
            "test_size": len(X_test),
            "report": report,
            "labels": labels,
        },
    }


def predict_sentiment(vectorizer, model, texts: list) -> list:
    """Predicts sentiment for a list of string inputs."""
    if not texts:
        return []
    vecs = vectorizer.transform(texts)
    preds = model.predict(vecs)
    return list(preds)


def compare_with_rule_based(df: pd.DataFrame, vectorizer, model) -> pd.DataFrame:
    """
    Runs ML model on entire filtered dataframe and compares ML predictions
    against rule-based ratings/sentiment.
    """
    res = df.copy()
    texts = res["feedback_text"].fillna("").astype(str).tolist()
    preds = predict_sentiment(vectorizer, model, texts)
    res["ml_sentiment"] = preds
    res["agrees_with_rule"] = res["sentiment"] == res["ml_sentiment"]
    return res

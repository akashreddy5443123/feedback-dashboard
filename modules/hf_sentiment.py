"""
OPTIONAL Hugging Face sentiment layer.

Not wired into app.py, and NOT tested in the build environment this
project was developed in (that sandbox has no internet access to
huggingface.co, only PyPI/GitHub -- so the model download couldn't be
verified there). This file is written correctly against the documented
transformers API and should work as-is on a machine with normal internet
access, but test it yourself before relying on it or claiming in an
interview that you've run it.

Setup:
    pip install transformers torch

Usage:
    from modules.hf_sentiment import classify_feedback
    df["hf_sentiment"], df["hf_confidence"] = classify_feedback(df["feedback_text"])
"""
from __future__ import annotations
import pandas as pd


def classify_feedback(texts: pd.Series, batch_size: int = 16) -> tuple[list[str], list[float]]:
    """Run a pretrained Hugging Face sentiment model over a Series of
    feedback text. Returns two lists: labels and confidence scores.

    Uses the default sentiment-analysis pipeline model (DistilBERT
    fine-tuned on SST-2), which outputs POSITIVE/NEGATIVE only -- no
    NEUTRAL class, unlike this project's rating-based rule. That's a
    real difference to account for if you compare the two: you'd need to
    either map POSITIVE/NEGATIVE + a confidence threshold onto a 3-class
    scheme, or accept the 2-class output as a different (not directly
    comparable) signal.
    """
    if texts is None or len(texts) == 0:
        return [], []

    try:
        from transformers import pipeline
    except ImportError as e:
        raise ImportError(
            "The 'transformers' or 'torch' package is not installed. "
            "Please run 'pip install transformers torch' to use this optional module."
        ) from e

    try:
        classifier = pipeline("sentiment-analysis")
    except Exception as e:
        raise RuntimeError(
            f"Failed to load Hugging Face sentiment pipeline: {e}. "
            "Ensure you have internet connectivity to download model weights from huggingface.co."
        ) from e

    labels, scores = [], []
    text_list = texts.fillna("").astype(str).tolist()

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        results = classifier(batch)
        labels.extend(r["label"] for r in results)
        scores.extend(round(float(r["score"]), 3) for r in results)

    return labels, scores


def flag_rating_text_mismatches(df: pd.DataFrame) -> pd.DataFrame:
    """Example of the actual use case this is meant for: find rows where
    the star rating and the Hugging Face text-based sentiment disagree
    -- e.g. a 5-star rating with text the model reads as NEGATIVE.

    Requires df to already have 'rating' and 'hf_sentiment' columns.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    required_cols = {"rating", "hf_sentiment"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise KeyError(
            f"DataFrame is missing required column(s): {missing}. "
            "Run classify_feedback() first to add 'hf_sentiment'."
        )

    high_rating_negative_text = df[(df["rating"] >= 4) & (df["hf_sentiment"] == "NEGATIVE")]
    low_rating_positive_text = df[(df["rating"] <= 2) & (df["hf_sentiment"] == "POSITIVE")]

    return pd.concat([high_rating_negative_text, low_rating_positive_text]).drop_duplicates()

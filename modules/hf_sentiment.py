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


def classify_feedback(texts: pd.Series, batch_size: int = 16):
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
    from transformers import pipeline  # imported lazily so this file
    # doesn't hard-fail on import for anyone who hasn't installed
    # transformers/torch and isn't using this optional module.

    classifier = pipeline("sentiment-analysis")

    labels, scores = [], []
    text_list = texts.fillna("").astype(str).tolist()

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        results = classifier(batch)
        labels.extend(r["label"] for r in results)
        scores.extend(round(r["score"], 3) for r in results)

    return labels, scores


def flag_rating_text_mismatches(df: pd.DataFrame) -> pd.DataFrame:
    """Example of the actual use case this is meant for: find rows where
    the star rating and the Hugging Face text-based sentiment disagree
    -- e.g. a 5-star rating with text the model reads as NEGATIVE.

    Requires df to already have an 'hf_sentiment' column from
    classify_feedback().
    """
    high_rating_negative_text = df[(df["rating"] >= 4) & (df["hf_sentiment"] == "NEGATIVE")]
    low_rating_positive_text = df[(df["rating"] <= 2) & (df["hf_sentiment"] == "POSITIVE")]
    return pd.concat([high_rating_negative_text, low_rating_positive_text])

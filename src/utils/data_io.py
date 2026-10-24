"""Shared data loading / prediction-saving utilities for Phase 3.
Single source of truth for frozen-data paths and the fixed label order,
so every script (baselines, transformers, evaluation) stays consistent.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FROZEN = ROOT / "data" / "processed" / "frozen_v1"
PROCESSED = ROOT / "data" / "processed"
PREDICTIONS = ROOT / "results" / "predictions"
PREDICTIONS.mkdir(parents=True, exist_ok=True)

# Fixed label order for every confusion matrix / report -- never changes.
LABEL_ORDER = ["Negative", "Neutral", "Positive"]

SEED = 42


def load_arabic_tourism():
    df = pd.read_csv(FROZEN / "arabic_tourism_frozen.csv")
    assert set(df["split"].unique()) <= {"train", "val", "test"}
    return df


def load_english_matched():
    df = pd.read_csv(FROZEN / "english_matched_frozen.csv")
    assert set(df["split"].unique()) <= {"train", "val", "test"}
    return df


def load_jordan_auxiliary():
    df = pd.read_csv(PROCESSED / "arabic_jordan_v2.csv")
    gold = df[df["label_source"] == "human_annotated"]
    weak = df[df["label_source"] == "llm_weak_label"]
    return gold, weak


def split_xy(df, split):
    sub = df[df["split"] == split]
    return sub["text"].tolist(), sub["sentiment"].tolist(), sub["review_id"].tolist(), sub["label_source"].tolist()


def save_predictions(review_ids, languages, true_labels, pred_labels, scores,
                      label_provenances, experiment_id, run_id, out_name):
    out = pd.DataFrame({
        "review_id": review_ids,
        "experiment_id": experiment_id,
        "run_id": run_id,
        "language": languages,
        "true_label": true_labels,
        "predicted_label": pred_labels,
        "confidence_or_score": scores,
        "label_provenance": label_provenances,
        "correct": [t == p for t, p in zip(true_labels, pred_labels)],
    })
    path = PREDICTIONS / f"{out_name}.csv"
    out.to_csv(path, index=False, encoding="utf-8-sig")
    return path

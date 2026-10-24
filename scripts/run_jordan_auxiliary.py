"""
E_jordan_binary_aux: Jordan dataset binary auxiliary experiment.
Train: 8,364 LLM-weak-labeled reviews (never evaluated on).
Eval: 300 human-gold reviews (binary Positive/Negative -- no Neutral exists
in this source, confirmed in codeswitch_audit.md / known_limitations.md #12).

No group identifier exists in this release (documented limitation), so the
internal train/validation split used for hyperparameter selection is a
plain random split of the 8,364 weak-labeled rows (never touching the 300
gold rows until final evaluation).
"""
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils.data_io import load_jordan_auxiliary, PREDICTIONS
from src.evaluation.metrics import compute_metrics

SEED = 42
ROOT = Path(__file__).resolve().parents[1]

gold, weak = load_jordan_auxiliary()
train_weak, val_weak = train_test_split(weak, test_size=0.15, random_state=SEED, stratify=weak["sentiment"])

best = None
log_lines = []
for ngram in [(1, 1), (1, 2)]:
    for C in [0.1, 1.0, 10.0]:
        for cw in [None, "balanced"]:
            vec = TfidfVectorizer(max_features=20000, min_df=2, sublinear_tf=True, ngram_range=ngram)
            Xtr = vec.fit_transform(train_weak["text"])
            Xval = vec.transform(val_weak["text"])
            clf = LogisticRegression(C=C, max_iter=2000, class_weight=cw, random_state=SEED)
            clf.fit(Xtr, train_weak["sentiment"])
            val_pred = clf.predict(Xval)
            m = compute_metrics(val_weak["sentiment"], val_pred)
            # binary task: Neutral has 0 support, macro-F1 here averages over 3 labels
            # with Neutral forced to 0 -- use a binary-only macro-F1 instead (fairer for this task)
            from sklearn.metrics import f1_score
            binary_macro_f1 = f1_score(val_weak["sentiment"], val_pred, labels=["Positive", "Negative"], average="macro", zero_division=0)
            log_lines.append(f"ngram={ngram} C={C} class_weight={cw} -> val_binary_macro_f1={binary_macro_f1:.6f}")
            if best is None or binary_macro_f1 > best["val_binary_macro_f1"]:
                best = {"ngram": ngram, "C": C, "class_weight": cw, "val_binary_macro_f1": binary_macro_f1}

log_lines.append(f"SELECTED: {best}")
(ROOT / "results" / "tables" / "jordan_auxiliary_gridsearch_log.txt").write_text("\n".join(log_lines), encoding="utf-8")

# retrain on ALL 8364 weak rows with selected hyperparameters, evaluate once on the 300 gold rows
vec = TfidfVectorizer(max_features=20000, min_df=2, sublinear_tf=True, ngram_range=best["ngram"])
Xtr = vec.fit_transform(weak["text"])
Xtest = vec.transform(gold["text"])
clf = LogisticRegression(C=best["C"], max_iter=2000, class_weight=best["class_weight"], random_state=SEED)
clf.fit(Xtr, weak["sentiment"])
test_pred = clf.predict(Xtest)
test_proba = clf.predict_proba(Xtest)
classes = list(clf.classes_)

from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
binary_test_f1 = f1_score(gold["sentiment"], test_pred, labels=["Positive", "Negative"], average="macro", zero_division=0)
acc = accuracy_score(gold["sentiment"], test_pred)
prec = precision_score(gold["sentiment"], test_pred, labels=["Positive", "Negative"], average="macro", zero_division=0)
rec = recall_score(gold["sentiment"], test_pred, labels=["Positive", "Negative"], average="macro", zero_division=0)

import pandas as pd
pred_df = pd.DataFrame({
    "review_id": gold["review_id"].tolist(), "experiment_id": "E_jordan_binary_aux",
    "run_id": "jordan_aux_tfidf_logreg", "language": "arabic",
    "true_label": gold["sentiment"].tolist(), "predicted_label": list(test_pred),
    "confidence_or_score": [test_proba[i, classes.index(p)] for i, p in enumerate(test_pred)],
    "label_provenance": gold["label_source"].tolist(),
})
pred_df["correct"] = pred_df["true_label"] == pred_df["predicted_label"]
pred_df.to_csv(PREDICTIONS / "jordan_aux_tfidf_logreg_test.csv", index=False, encoding="utf-8-sig")

result = {
    "task": "BINARY (Positive/Negative only -- Jordan source has zero Neutral examples, confirmed)",
    "train_n": len(weak), "eval_n": len(gold), "selected_hyperparameters": best,
    "test_binary_macro_f1": binary_test_f1, "test_accuracy": acc,
    "test_precision_macro_binary": prec, "test_recall_macro_binary": rec,
    "note": "NOT comparable to the primary 3-class E1/E2/E3/E4 results -- different task, different label provenance (LLM-weak train, human-gold eval). Report separately, never pooled.",
}
with open(ROOT / "results" / "tables" / "jordan_auxiliary_results.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, default=str)

print(json.dumps(result, indent=2, default=str))

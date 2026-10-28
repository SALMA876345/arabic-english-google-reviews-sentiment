"""E6: run ONE trained model on the 9 verified genuine code-switch examples
(qualitative diagnostic only -- n=9 is far too small for any quantitative
metric, see codeswitch_audit.md). Run once per model (separate process
invocations) to keep memory footprint minimal on this constrained machine.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd
import torch
from peft import PeftModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.metrics import LABEL_ORDER

ID2LABEL = {i: l for i, l in enumerate(LABEL_ORDER)}
LABEL2ID = {l: i for i, l in ID2LABEL.items()}

parser = argparse.ArgumentParser()
parser.add_argument("--adapter", required=True)
parser.add_argument("--base_id", required=True)
parser.add_argument("--model_name", required=True)
args = parser.parse_args()

ROOT = Path(__file__).resolve().parents[1]
cs_df = pd.read_csv(ROOT / "results" / "error_analysis" / "codeswitch_diagnostic_texts.csv")

mixed = pd.read_csv(ROOT / "data" / "processed" / "mixed_candidates_v2.csv")
true_map = dict(zip(mixed["review_id"], mixed["sentiment"]))
source_map = dict(zip(mixed["review_id"], mixed["label_source"]))

tok = AutoTokenizer.from_pretrained(f"experiments/checkpoints/{args.adapter}")
base = AutoModelForSequenceClassification.from_pretrained(args.base_id, num_labels=3, id2label=ID2LABEL, label2id=LABEL2ID)
model = PeftModel.from_pretrained(base, f"experiments/checkpoints/{args.adapter}")
model.eval()

rows = []
for _, row in cs_df.iterrows():
    rid = row["review_id"]
    text = row["review_text"]
    enc = tok(text, truncation=True, padding="max_length", max_length=64, return_tensors="pt")
    with torch.no_grad():
        out = model(**enc)
    probs = torch.softmax(out.logits, dim=1).numpy()[0]
    pred_idx = probs.argmax()
    pred, conf = ID2LABEL[pred_idx], float(probs[pred_idx])
    true_label = true_map.get(rid, "unknown")
    rows.append({
        "review_id": rid, "model": args.model_name, "true_label_source_NOT_gold": true_label,
        "label_provenance": source_map.get(rid, "unknown"), "predicted_label": pred,
        "confidence": round(conf, 4), "matches_source_label": pred == true_label,
    })

out_df = pd.DataFrame(rows)
out_path = ROOT / "results" / "error_analysis" / f"codeswitch_diagnostic_predictions_{args.model_name}.csv"
out_df.to_csv(out_path, index=False, encoding="utf-8-sig")
print(out_df.to_string())
print(f"Wrote {out_path}")

"""
Section J: assembles one machine-readable master results file bundling every
output of this phase. Read-only aggregation -- does not recompute anything.
"""
import json
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent

master = {
    "phase": "human_gold_label_analysis_and_reevaluation",
    "human_gold_source": {
        "path": "paper/annotation/full/human_gold_757.csv",
        "sha256": "7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd",
    },
    "no_retraining_performed": True,
    "section_B_label_agreement": json.load(open(OUT / "label_agreement_overall_by_language.json", encoding="utf-8")),
    "section_C_disagreement_conditional": json.loads(pd.read_csv(OUT / "disagreement_rate_conditional.csv").to_json(orient="records")),
    "section_D_prediction_availability": json.loads(pd.read_csv(OUT / "prediction_availability.csv").to_json(orient="records")),
    "section_D_E_metrics_all_models": json.loads(pd.read_csv(OUT / "human_gold_metrics_all_models.csv").to_json(orient="records")),
    "section_E_original_vs_human_gold_comparison": json.loads(pd.read_csv(OUT / "original_vs_human_gold_comparison.csv").to_json(orient="records")),
    "section_F_statistical_tests": json.load(open(OUT / "statistical_tests_human_gold.json", encoding="utf-8")),
    "section_G_error_analysis_by_class_language": json.loads(pd.read_csv(OUT / "error_analysis_by_class_language.csv").to_json(orient="records")),
}

with open(OUT / "master_results_human_gold.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, default=str)

print(f"Wrote {OUT / 'master_results_human_gold.json'}")

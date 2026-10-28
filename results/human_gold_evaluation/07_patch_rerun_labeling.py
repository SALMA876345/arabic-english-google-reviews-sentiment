"""
Pre-manuscript fix: adds an explicit `realization_<x>` / `realization` column
to every Human-Gold output file that references a model by bare `model_key`
without already carrying the primary/rerun qualifier inline. Does NOT change
any existing metric, score, or p-value -- purely additive columns, sourced
from the already-computed `prediction_availability.csv`. Run once; idempotent.
"""
import json
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent

AVAIL = pd.read_csv(OUT / "prediction_availability.csv")
REALIZATION = dict(zip(AVAIL.model_key, AVAIL.realization))


def tag(key):
    r = REALIZATION.get(key, "UNKNOWN")
    return "RERUN_REALIZATION_not_primary" if r == "RERUN_REALIZATION_not_primary" else r


def patch_error_analysis():
    path = OUT / "error_analysis_by_class_language.csv"
    df = pd.read_csv(path)
    if "realization" not in df.columns:
        df.insert(df.columns.get_loc("phase") + 1, "realization", df.model_key.map(tag))
        df.to_csv(path, index=False)
        print(f"Patched {path.name}: added realization column.")
    else:
        print(f"{path.name}: already patched, skipping.")


def patch_qualitative_examples():
    path = OUT / "qualitative_error_examples.csv"
    df = pd.read_csv(path)
    if "realization" not in df.columns:
        df.insert(df.columns.get_loc("language") + 1, "realization", df.model_key.map(tag))
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"Patched {path.name}: added realization column.")
    else:
        print(f"{path.name}: already patched, skipping.")


def patch_statistical_tests():
    csv_path = OUT / "statistical_tests_human_gold.csv"
    json_path = OUT / "statistical_tests_human_gold.json"
    df = pd.read_csv(csv_path)
    if "realization_a" not in df.columns:
        df.insert(df.columns.get_loc("model_a") + 1, "realization_a", df.model_a.map(tag))
        df.insert(df.columns.get_loc("model_b") + 1, "realization_b", df.model_b.map(tag))
        df.to_csv(csv_path, index=False)
        records = df.to_dict(orient="records")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, default=str)
        print(f"Patched {csv_path.name} and {json_path.name}: added realization_a/realization_b columns.")
    else:
        print(f"{csv_path.name}: already patched, skipping.")


def patch_availability_summary():
    path = OUT / "prediction_availability_summary.json"
    data = json.load(open(path, encoding="utf-8"))
    if "valid_model_keys_with_realization" not in data:
        data["valid_model_keys_with_realization"] = {k: REALIZATION.get(k, "UNKNOWN") for k in data["valid_model_keys"]}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Patched {path.name}: added valid_model_keys_with_realization mapping.")
    else:
        print(f"{path.name}: already patched, skipping.")


def main():
    patch_error_analysis()
    patch_qualitative_examples()
    patch_statistical_tests()
    patch_availability_summary()
    print("\nNo historical metric, score, or p-value was altered by this patch -- only additive realization-tag columns were added.")


if __name__ == "__main__":
    main()

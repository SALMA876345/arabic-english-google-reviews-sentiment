"""
Phase 3 transformer fine-tuning via LoRA adapters (NOT full fine-tuning --
see configs/models.yaml `fine_tuning_method` and docs/decisions.md D14 for
why: full fine-tuning OOMs on this machine's ~1.3GB free RAM during the
Adam optimizer step for the full 270-480M parameter set).

Hyperparameters from configs/training.yaml (transformer_common), as
ACTUALLY run post-OOM-discovery: max_seq_length=64, batch_size=8, epochs=3,
early_stopping patience=1. Not tuned against the test set.

Usage:
  python scripts/run_transformers.py --run smoketest
  python scripts/run_transformers.py --run E1_marbert
  python scripts/run_transformers.py --run E1_xlmr
  python scripts/run_transformers.py --run E2_xlmr
  python scripts/run_transformers.py --run E4_xlmr_combined
"""
import argparse
import gc
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils.data_io import load_arabic_tourism, load_english_matched, load_jordan_auxiliary, PREDICTIONS
from src.evaluation.metrics import compute_metrics, LABEL_ORDER

ROOT = Path(__file__).resolve().parents[1]
MODELS_OUT = ROOT / "experiments" / "checkpoints"
MODELS_OUT.mkdir(parents=True, exist_ok=True)

SEED = 42
LABEL2ID = {l: i for i, l in enumerate(LABEL_ORDER)}
ID2LABEL = {i: l for l, i in LABEL2ID.items()}

MAX_LEN = 64
BATCH_SIZE = 8
EPOCHS = 3
LR = 2e-5
PATIENCE = 1
LORA_CFG = dict(r=8, lora_alpha=16, lora_dropout=0.1, target_modules=["query", "value"])

torch.manual_seed(SEED)
np.random.seed(SEED)


def build_model(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    base = AutoModelForSequenceClassification.from_pretrained(
        model_id, num_labels=len(LABEL_ORDER), id2label=ID2LABEL, label2id=LABEL2ID)
    lora_cfg = LoraConfig(task_type=TaskType.SEQ_CLS, **LORA_CFG)
    model = get_peft_model(base, lora_cfg)
    return tokenizer, model


def encode(tokenizer, texts):
    return tokenizer(list(texts), truncation=True, padding="max_length", max_length=MAX_LEN, return_tensors="pt")


def iterate_batches(n, batch_size, shuffle, seed):
    idx = np.arange(n)
    if shuffle:
        rng = np.random.default_rng(seed)
        rng.shuffle(idx)
    for i in range(0, n, batch_size):
        yield idx[i:i + batch_size]


def evaluate(model, tokenizer, texts, labels):
    model.eval()
    all_logits = []
    enc = encode(tokenizer, texts)
    y_ids = [LABEL2ID[l] for l in labels]
    with torch.no_grad():
        for batch_idx in iterate_batches(len(texts), BATCH_SIZE, shuffle=False, seed=SEED):
            batch = {k: v[batch_idx] for k, v in enc.items()}
            out = model(**batch)
            all_logits.append(out.logits.numpy())
    logits = np.concatenate(all_logits, axis=0)
    preds = np.argmax(logits, axis=1)
    probs = np.exp(logits - logits.max(axis=1, keepdims=True))
    probs = probs / probs.sum(axis=1, keepdims=True)
    y_pred = [ID2LABEL[i] for i in preds]
    m = compute_metrics([ID2LABEL[i] for i in y_ids], y_pred)
    confidences = probs[np.arange(len(preds)), preds]
    return m, y_pred, confidences


def run_one(model_id, train_df, val_df, test_df, out_name, experiment_id, language_for_output):
    t0 = time.time()
    tokenizer, model = build_model(model_id)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=LR)

    train_texts = train_df["text"].tolist()
    train_labels = [LABEL2ID[l] for l in train_df["sentiment"]]
    train_enc = encode(tokenizer, train_texts)

    best_val_f1 = -1
    best_state = None
    epochs_without_improvement = 0
    history = []

    for epoch in range(1, EPOCHS + 1):
        model.train()
        epoch_loss = 0.0
        n_batches = 0
        for batch_idx in iterate_batches(len(train_texts), BATCH_SIZE, shuffle=True, seed=SEED + epoch):
            batch = {k: v[batch_idx] for k, v in train_enc.items()}
            labels = torch.tensor([train_labels[i] for i in batch_idx])
            out = model(**batch, labels=labels)
            out.loss.backward()
            opt.step()
            opt.zero_grad()
            epoch_loss += out.loss.item()
            n_batches += 1
        val_metrics, _, _ = evaluate(model, tokenizer, val_df["text"].tolist(), val_df["sentiment"].tolist())
        val_f1 = val_metrics["macro_f1"]
        history.append({"epoch": epoch, "train_loss": epoch_loss / max(n_batches, 1), "val_macro_f1": val_f1})
        print(f"[{out_name}] epoch {epoch} train_loss={epoch_loss/max(n_batches,1):.4f} val_macro_f1={val_f1:.4f}")

        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            best_state = {k: v.clone() for k, v in model.state_dict().items() if "lora" in k.lower()}
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= PATIENCE:
                print(f"[{out_name}] early stopping at epoch {epoch} (patience={PATIENCE})")
                break

    if best_state is not None:
        model.load_state_dict(best_state, strict=False)

    adapter_path = MODELS_OUT / out_name
    model.save_pretrained(str(adapter_path))
    tokenizer.save_pretrained(str(adapter_path))

    test_metrics, test_preds, test_conf = evaluate(model, tokenizer, test_df["text"].tolist(), test_df["sentiment"].tolist())

    pred_df = pd.DataFrame({
        "review_id": test_df["review_id"].tolist(),
        "experiment_id": experiment_id,
        "run_id": out_name,
        "language": language_for_output,
        "true_label": test_df["sentiment"].tolist(),
        "predicted_label": test_preds,
        "confidence_or_score": test_conf,
        "label_provenance": test_df["label_source"].tolist(),
    })
    pred_df["correct"] = pred_df["true_label"] == pred_df["predicted_label"]
    pred_path = PREDICTIONS / f"{out_name}_test.csv"
    pred_df.to_csv(pred_path, index=False, encoding="utf-8-sig")

    elapsed = time.time() - t0
    print(f"[{out_name}] TEST macro_f1={test_metrics['macro_f1']:.4f} acc={test_metrics['accuracy']:.4f} "
          f"elapsed={elapsed:.1f}s best_val_f1={best_val_f1:.4f}")

    result = {
        "out_name": out_name, "model_id": model_id, "fine_tuning_method": "LoRA",
        "lora_config": LORA_CFG, "epochs_requested": EPOCHS, "epochs_actually_run": len(history),
        "best_val_macro_f1": best_val_f1, "train_n": len(train_df), "val_n": len(val_df), "test_n": len(test_df),
        "elapsed_sec": elapsed, "history": history, "test_metrics": test_metrics,
        "prediction_file": str(pred_path),
    }

    del model, tokenizer, opt, train_enc
    gc.collect()
    return result


def run_cross_lingual_eval(adapter_dir_name, base_model_id, test_df, experiment_id, language_for_output, out_name):
    """Inference-only: load a saved LoRA adapter trained on one language and
    evaluate on the OTHER language's frozen test set. No training, no
    gradient updates -- this is why E5 is cheap once E1/E2 are trained."""
    from peft import PeftModel
    adapter_path = MODELS_OUT / adapter_dir_name
    tokenizer = AutoTokenizer.from_pretrained(str(adapter_path))
    base = AutoModelForSequenceClassification.from_pretrained(
        base_model_id, num_labels=len(LABEL_ORDER), id2label=ID2LABEL, label2id=LABEL2ID)
    model = PeftModel.from_pretrained(base, str(adapter_path))
    model.eval()

    test_metrics, test_preds, test_conf = evaluate(model, tokenizer, test_df["text"].tolist(), test_df["sentiment"].tolist())
    pred_df = pd.DataFrame({
        "review_id": test_df["review_id"].tolist(), "experiment_id": experiment_id, "run_id": out_name,
        "language": language_for_output, "true_label": test_df["sentiment"].tolist(),
        "predicted_label": test_preds, "confidence_or_score": test_conf,
        "label_provenance": test_df["label_source"].tolist(),
    })
    pred_df["correct"] = pred_df["true_label"] == pred_df["predicted_label"]
    pred_path = PREDICTIONS / f"{out_name}_test.csv"
    pred_df.to_csv(pred_path, index=False, encoding="utf-8-sig")
    print(f"[{out_name}] CROSS-LINGUAL (inference only, adapter={adapter_dir_name}) "
          f"test_macro_f1={test_metrics['macro_f1']:.4f}")
    del model, base, tokenizer
    gc.collect()
    return {"out_name": out_name, "adapter_used": adapter_dir_name, "test_metrics": test_metrics,
            "test_n": len(test_df), "prediction_file": str(pred_path)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    results = {}

    if args.run == "smoketest":
        ar = load_arabic_tourism()
        tr = ar[ar.split == "train"].sample(24, random_state=SEED)
        va = ar[ar.split == "val"].sample(8, random_state=SEED)
        te = ar[ar.split == "test"].sample(8, random_state=SEED)
        res = run_one("FacebookAI/xlm-roberta-base", tr, va, te, "SMOKETEST_xlmr", "SMOKETEST", "arabic")
        print(json.dumps({k: v for k, v in res.items() if k != "test_metrics"}, indent=2, default=str))
        return

    if args.run == "E1_marbert":
        ar = load_arabic_tourism()
        results["E1_marbert"] = run_one("UBC-NLP/MARBERT", ar[ar.split == "train"], ar[ar.split == "val"],
                                         ar[ar.split == "test"], "E1_marbert", "E1", "arabic")
    elif args.run == "E1_xlmr":
        ar = load_arabic_tourism()
        results["E1_xlmr"] = run_one("FacebookAI/xlm-roberta-base", ar[ar.split == "train"], ar[ar.split == "val"],
                                      ar[ar.split == "test"], "E1_xlmr", "E1", "arabic")
    elif args.run == "E2_xlmr":
        en = load_english_matched()
        results["E2_xlmr"] = run_one("FacebookAI/xlm-roberta-base", en[en.split == "train"], en[en.split == "val"],
                                      en[en.split == "test"], "E2_xlmr", "E2", "english")
    elif args.run == "E4_xlmr_combined":
        ar = load_arabic_tourism()
        en = load_english_matched()
        gold, weak = load_jordan_auxiliary()
        cols = ["text", "sentiment", "review_id", "label_source"]
        combined_train = pd.concat([ar[ar.split == "train"][cols], en[en.split == "train"][cols], weak[cols]], ignore_index=True)
        combined_val = pd.concat([ar[ar.split == "val"][cols], en[en.split == "val"][cols]], ignore_index=True)
        results["E4_xlmr_combined_evalAR"] = run_one("FacebookAI/xlm-roberta-base", combined_train, combined_val,
                                                      ar[ar.split == "test"], "E4_xlmr_combined_evalAR", "E4", "arabic")
        results["E4_xlmr_combined_evalEN"] = run_one("FacebookAI/xlm-roberta-base", combined_train, combined_val,
                                                      en[en.split == "test"], "E4_xlmr_combined_evalEN", "E4", "english")
    elif args.run == "E5_arTrain_enTest":
        en = load_english_matched()
        results["E5_arTrain_enTest"] = run_cross_lingual_eval(
            "E1_xlmr", "FacebookAI/xlm-roberta-base", en[en.split == "test"], "E5", "english", "E5_arTrain_enTest")
    elif args.run == "E5_enTrain_arTest":
        ar = load_arabic_tourism()
        results["E5_enTrain_arTest"] = run_cross_lingual_eval(
            "E2_xlmr", "FacebookAI/xlm-roberta-base", ar[ar.split == "test"], "E5", "arabic", "E5_enTrain_arTest")
    else:
        raise ValueError(f"Unknown run: {args.run}")

    out_path = ROOT / "results" / "tables" / f"transformer_run_{args.run}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

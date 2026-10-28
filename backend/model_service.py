"""
Loads the deployment XLM-R sentiment model ONCE and exposes a simple
predict() function. Model source: backend/model/ (moved from the Kaggle
deployment export "final_multilingual_sentiment_model" -- see
docs/decisions.md D17 and deployment_info.json in that folder for
provenance: full fine-tuning on 2xT4 GPUs, validation macro-F1=0.7999539.

This is the DEPLOYMENT artifact, distinct from the primary research E4
multilingual results (Arabic test macro-F1=0.767865, English=0.739722,
see paper/notes/phase3b_report.md) -- the deployment run was a separate
training pass optimized for serving, not substituted for the research numbers.
"""
from pathlib import Path
from functools import lru_cache

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_DIR = Path(__file__).resolve().parent / "model"
MAX_LENGTH = 128


class SentimentModel:
    def __init__(self, model_dir: Path):
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
        self.model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
        self.model.eval()
        self.id2label = {int(k): v for k, v in self.model.config.id2label.items()}

    @torch.no_grad()
    def predict(self, text: str) -> dict:
        enc = self.tokenizer(text, truncation=True, padding="max_length", max_length=MAX_LENGTH, return_tensors="pt")
        logits = self.model(**enc).logits
        probs = torch.softmax(logits, dim=1).squeeze(0)
        pred_idx = int(torch.argmax(probs).item())
        return {
            "predicted_sentiment": self.id2label[pred_idx],
            "confidence": float(probs[pred_idx].item()),
            "probabilities": {self.id2label[i]: float(probs[i].item()) for i in range(len(self.id2label))},
        }


@lru_cache(maxsize=1)
def get_model() -> SentimentModel:
    """Loaded once (cached) -- call this at app startup, not per-request."""
    return SentimentModel(MODEL_DIR)

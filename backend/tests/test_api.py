import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


def test_predict_arabic_positive():
    r = client.post("/predict", json={"text": "الخدمة ممتازة والمكان جميل جدا"})
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_sentiment"] in ("Negative", "Neutral", "Positive")
    assert 0.0 <= body["confidence"] <= 1.0
    probs = body["probabilities"]
    assert set(probs.keys()) == {"Negative", "Neutral", "Positive"}
    assert abs(sum(probs.values()) - 1.0) < 1e-3


def test_predict_english_negative():
    r = client.post("/predict", json={"text": "Terrible service, the staff was rude and the food was cold."})
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_sentiment"] in ("Negative", "Neutral", "Positive")
    probs = body["probabilities"]
    assert abs(sum(probs.values()) - 1.0) < 1e-3


def test_predict_code_switched():
    r = client.post("/predict", json={"text": "المكان جميل جدا لكن ال service كان سيء"})
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_sentiment"] in ("Negative", "Neutral", "Positive")


def test_predict_empty_string_errors():
    r = client.post("/predict", json={"text": ""})
    assert r.status_code == 400


def test_predict_whitespace_only_errors():
    r = client.post("/predict", json={"text": "   "})
    assert r.status_code == 400


def test_predict_missing_field_errors():
    r = client.post("/predict", json={})
    assert r.status_code == 422  # pydantic validation error


def test_predict_wrong_type_errors():
    r = client.post("/predict", json={"text": 12345})
    assert r.status_code == 422

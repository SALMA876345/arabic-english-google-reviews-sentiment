"""
FastAPI backend serving the deployment XLM-R sentiment model
(Arabic-English Google Reviews Sentiment Analysis project).

Run:
    cd backend
    uvicorn main:app --host 0.0.0.0 --port 8000

Endpoints:
    GET  /health   -> {"status": "ok", "model_loaded": true}
    POST /predict   -> {"text": "..."}  => {predicted_sentiment, confidence, probabilities}
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model_service import get_model
from schemas import PredictRequest, PredictResponse, HealthResponse

MAX_TEXT_LENGTH_CHARS = 5000  # guard against pathological inputs; model itself truncates at 128 tokens

# Vite's default dev server port is 5173; override/extend via CORS_ALLOWED_ORIGINS
# (comma-separated) for other setups (e.g. a deployed frontend origin).
DEFAULT_DEV_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
_env_origins = os.environ.get("CORS_ALLOWED_ORIGINS")
ALLOWED_ORIGINS = [o.strip() for o in _env_origins.split(",")] if _env_origins else DEFAULT_DEV_ORIGINS


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_model()  # load once at startup, not per-request (cached via lru_cache)
    yield


app = FastAPI(
    title="Arabic-English Sentiment Analysis API",
    description="Multilingual XLM-R sentiment classifier (Negative/Neutral/Positive) for Arabic, English, and code-switched Google Maps-style reviews.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    try:
        get_model()
        return HealthResponse(status="ok", model_loaded=True)
    except Exception:
        return HealthResponse(status="error", model_loaded=False)


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    text = request.text.strip() if request.text is not None else ""
    if not text:
        raise HTTPException(status_code=400, detail="`text` must be a non-empty string.")
    if len(text) > MAX_TEXT_LENGTH_CHARS:
        raise HTTPException(status_code=400, detail=f"`text` exceeds {MAX_TEXT_LENGTH_CHARS} characters.")

    model = get_model()
    result = model.predict(text)
    return PredictResponse(**result)

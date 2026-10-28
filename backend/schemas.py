from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., description="Arabic, English, or code-switched review text")


class PredictResponse(BaseModel):
    predicted_sentiment: str
    confidence: float
    probabilities: dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool

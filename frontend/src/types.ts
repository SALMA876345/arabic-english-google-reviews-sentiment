// Mirrors backend/schemas.py exactly -- keep in sync if the backend contract changes.

export interface PredictRequest {
  text: string;
}

export interface PredictResponse {
  predicted_sentiment: string;
  confidence: number;
  probabilities: Record<string, number>;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
}

export type Sentiment = "Positive" | "Neutral" | "Negative";

export const SENTIMENT_ORDER: Sentiment[] = ["Negative", "Neutral", "Positive"];

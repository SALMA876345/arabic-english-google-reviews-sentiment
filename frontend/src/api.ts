import type { PredictRequest, PredictResponse, HealthResponse } from "./types";

// Never hard-code a production host -- VITE_API_BASE_URL, falling back to the
// local FastAPI dev default so `npm run dev` works out of the box.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function predictSentiment(text: string): Promise<PredictResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text } satisfies PredictRequest),
    });
  } catch {
    // Network-level failure -- backend unreachable (not running, wrong host, CORS, etc.)
    throw new ApiError(
      "Could not reach the sentiment analysis backend. Make sure the FastAPI server is running and VITE_API_BASE_URL is correct."
    );
  }

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (typeof body?.detail === "string") detail = body.detail;
    } catch {
      // response body wasn't JSON -- fall back to the generic message above
    }
    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as PredictResponse;
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new ApiError(`Health check failed with status ${response.status}`, response.status);
  return (await response.json()) as HealthResponse;
}

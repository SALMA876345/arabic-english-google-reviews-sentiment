import { useState } from "react";
import { Header } from "./components/Header";
import { ReviewInput } from "./components/ReviewInput";
import { ExampleReviews } from "./components/ExampleReviews";
import { PredictionResult } from "./components/PredictionResult";
import { ModelInfo } from "./components/ModelInfo";
import { ErrorBanner } from "./components/ErrorBanner";
import { predictSentiment, ApiError } from "./api";
import type { PredictResponse } from "./types";
import "./App.css";

export default function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  function handleTextChange(value: string) {
    setText(value);
    if (validationError && value.trim()) setValidationError(null);
  }

  function handleExampleSelect(exampleText: string) {
    setText(exampleText);
    setValidationError(null);
    // Does NOT auto-call the API -- only populates the text box, per spec.
  }

  async function handleAnalyze() {
    const trimmed = text.trim();
    if (!trimmed) {
      setValidationError("Please enter a review before analyzing.");
      setResult(null);
      return;
    }
    setValidationError(null);
    setError(null);
    setLoading(true);
    try {
      const prediction = await predictSentiment(trimmed);
      setResult(prediction);
    } catch (err) {
      setResult(null);
      setError(err instanceof ApiError ? err.message : "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <Header />
      <main className="app__main">
        <section className="card">
          <ReviewInput
            value={text}
            onChange={handleTextChange}
            onAnalyze={handleAnalyze}
            loading={loading}
            validationError={validationError}
          />
          <ExampleReviews onSelect={handleExampleSelect} disabled={loading} />
        </section>

        {error && <ErrorBanner message={error} />}

        {result && (
          <section className="card">
            <PredictionResult result={result} />
          </section>
        )}

        <section className="card card--muted">
          <ModelInfo />
        </section>
      </main>
      <footer className="app__footer">
        Arabic-English Google Reviews Sentiment Analysis &mdash; research demonstration interface.
      </footer>
    </div>
  );
}

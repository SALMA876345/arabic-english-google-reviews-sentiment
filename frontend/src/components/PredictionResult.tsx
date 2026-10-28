import type { PredictResponse } from "../types";
import { SENTIMENT_ORDER } from "../types";

interface PredictionResultProps {
  result: PredictResponse;
}

const SENTIMENT_CLASS: Record<string, string> = {
  Positive: "sentiment--positive",
  Neutral: "sentiment--neutral",
  Negative: "sentiment--negative",
};

function formatPct(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export function PredictionResult({ result }: PredictionResultProps) {
  const badgeClass = SENTIMENT_CLASS[result.predicted_sentiment] ?? "";

  return (
    <section className="result" aria-live="polite">
      <div className={`result__badge ${badgeClass}`}>
        <span className="result__badge-label">{result.predicted_sentiment}</span>
        <span className="result__confidence">Confidence: {formatPct(result.confidence)}</span>
      </div>

      <div className="result__probabilities">
        {SENTIMENT_ORDER.map((label) => {
          const value = result.probabilities[label] ?? 0;
          return (
            <div className="prob-bar" key={label}>
              <div className="prob-bar__header">
                <span>{label}</span>
                <span>{formatPct(value)}</span>
              </div>
              <div className="prob-bar__track" role="progressbar" aria-valuenow={Math.round(value * 100)} aria-valuemin={0} aria-valuemax={100} aria-label={`${label} probability`}>
                <div
                  className={`prob-bar__fill ${SENTIMENT_CLASS[label] ?? ""}`}
                  style={{ width: `${Math.max(value * 100, 1.5)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

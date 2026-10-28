import { detectDirection } from "../textDirection";

interface ReviewInputProps {
  value: string;
  onChange: (value: string) => void;
  onAnalyze: () => void;
  loading: boolean;
  validationError: string | null;
}

export function ReviewInput({ value, onChange, onAnalyze, loading, validationError }: ReviewInputProps) {
  const direction = detectDirection(value);

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    // Ctrl/Cmd+Enter submits -- keyboard-friendly without hijacking plain Enter (reviews are multi-line)
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      onAnalyze();
    }
  }

  return (
    <div className="review-input">
      <label htmlFor="review-text" className="review-input__label">
        Enter a review (Arabic, English, or mixed)
      </label>
      <textarea
        id="review-text"
        className="review-input__textarea"
        dir={direction}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={"مثال: المكان جميل والخدمة سريعة\nExample: Great food, but the wait was too long."}
        rows={6}
        aria-invalid={validationError ? "true" : "false"}
        aria-describedby={validationError ? "review-input-error" : undefined}
      />
      {validationError && (
        <p id="review-input-error" className="review-input__error" role="alert">
          {validationError}
        </p>
      )}
      <div className="review-input__actions">
        <button
          type="button"
          className="btn btn--primary"
          onClick={onAnalyze}
          disabled={loading}
          aria-busy={loading}
        >
          {loading ? "Analyzing…" : "Analyze Sentiment"}
        </button>
        <span className="review-input__hint">Ctrl/Cmd + Enter to analyze</span>
      </div>
    </div>
  );
}

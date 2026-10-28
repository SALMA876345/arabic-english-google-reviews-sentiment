export function Header() {
  return (
    <header className="app-header">
      <div className="app-header__inner">
        <h1>Arabic-English Review Sentiment Analyzer</h1>
        <p className="app-header__subtitle">
          Analyzes Arabic, English, and mixed Arabic-English location/business reviews using a trained
          multilingual XLM-R model, classifying each review as Positive, Neutral, or Negative.
        </p>
      </div>
    </header>
  );
}

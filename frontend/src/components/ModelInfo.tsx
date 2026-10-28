export function ModelInfo() {
  return (
    <section className="model-info" aria-labelledby="model-info-heading">
      <h2 id="model-info-heading">About This Model</h2>
      <dl className="model-info__grid">
        <div>
          <dt>Model</dt>
          <dd>Multilingual XLM-R</dd>
        </div>
        <div>
          <dt>Languages</dt>
          <dd>Arabic &amp; English</dd>
        </div>
        <div>
          <dt>Task</dt>
          <dd>3-class sentiment classification</dd>
        </div>
        <div>
          <dt>Classes</dt>
          <dd>Positive / Neutral / Negative</dd>
        </div>
      </dl>
      <p className="model-info__caveat">
        This model was trained and validated on a research dataset of Google Maps-style location/business
        reviews. Reported validation performance describes behavior on that dataset and is not a guarantee
        of accuracy for any individual prediction, especially for text very different from typical reviews.
      </p>
    </section>
  );
}

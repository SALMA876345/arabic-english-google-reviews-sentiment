# Label Provenance Policy

## Terminology (binding — use consistently everywhere, including the eventual manuscript)

| Term | Definition | Example in this corpus |
|---|---|---|
| **human_annotated** | A person read the review text and assigned the sentiment label, with a documented protocol and (where available) inter-annotator agreement | Zenodo 17011574 (κ=0.87); Zenodo 22061934's 300-review gold subset |
| **rating_derived** | The label was mechanically derived from a star rating the reviewer gave, via a documented conversion rule, with NO one reading the text to confirm the label | UCSD/McAuley English sample (1★–2★=Negative, 3★=Neutral, 4★–5★=Positive) |
| **llm_weak_label** | A large language model read the text and assigned the label; no human confirmed each label individually (validation against a small human-gold subsample does not upgrade the remainder to human-annotated) | Zenodo 22061934's non-gold 8,364 rows (Claude Sonnet 4.6 / GPT-5) |

**Binding rule:** rating-derived labels must never be described as "manually annotated sentiment ground truth." LLM-weak labels must never be described as "human labels." This applies to every table, figure, and sentence in the eventual manuscript, not just this document.

## Policy: training labels vs. evaluation ground truth

These are **not interchangeable categories** and must be kept separate in every experiment design.

### Training labels (anything may be used, with the source declared)
All three provenance types may be used for model **training**, because training can tolerate label noise that evaluation cannot — the model's job is to learn a signal, not to define what "true" sentiment is. Every training manifest must record each example's label_source so that label-noise ablations (e.g. "train without llm_weak_label rows") remain possible later.

### Evaluation ground truth (human_annotated only, by default)
A result reported as measuring real model accuracy must be scored against **human_annotated** labels. Concretely:
- **Zenodo 17011574** (human-annotated, κ=0.87): its held-out portion is acceptable evaluation ground truth for Arabic.
- **Zenodo 22061934's 300-review human gold subset**: acceptable evaluation ground truth for the Jordan binary auxiliary experiment ONLY (see `experimental_dataset_protocol.md` for why the other 8,364 rows are training-only).
- **UCSD/McAuley rating-derived labels**: **NOT acceptable as final evaluation ground truth** on their own. They may be used as a large-scale training signal and as a *secondary*, explicitly-caveated evaluation view, but any claim about "accuracy on English reviews" that is not cross-checked against the manually-validated test slice (`annotation_guidelines.md`) must be labeled "rating-derived evaluation, not human-verified" everywhere it is reported — tables, figures, and text.
- **The manually-validated test slice** (`annotation_guidelines.md`, pending completion) is intended to become the primary cross-language evaluation ground truth once annotation is complete, precisely because it is the only source that is both human-annotated AND built with a single consistent protocol across Arabic and English.

### Rationale
This separation exists because the corpus is currently 98.8% rating-derived and 0.8% LLM-weak by volume (`known_limitations.md` #13) — if evaluation ground truth were allowed to be anything other than human-annotated, "accuracy" would mostly be measuring agreement with star ratings or an LLM's own judgment, not genuine sentiment-classification correctness. This policy keeps those distinct.

# Manual Annotation Guidelines — Matched-Protocol Validation Slice

**Status: PROTOCOL AND CANDIDATE SUBSET PREPARED. ACTUAL HUMAN ANNOTATION NOT YET PERFORMED — PENDING.**
No labels in `data/annotations/annotation_template_pending.csv` have been filled in. This document and the candidate subset exist so that annotation can begin immediately once a human annotator (or annotator team) is available; nothing here should be read as completed work.

## Purpose

This slice exists to close the specific gap identified in `dataset_audit.md` §7: the Arabic and English primary pools were labeled under *different* processes (Arabic: human-annotated by the dataset's original authors; English: rating-derived by this project). A model-performance gap between languages measured only on those pools cannot distinguish a real language-difficulty effect from a labeling-process difference. This slice applies **one consistent annotation protocol, by the same annotator(s), across both languages**, so it becomes the only comparison point in the eventual paper that is not confounded by differing label provenance.

## Candidate subset

809 total candidates selected (seed=42, see `src/preprocessing/build_validation_slice.py`):
- **800 main stratified slice**: 400 Arabic (from the tourism primary pool) + 400 English (from the matched subset), each stratified to its own pool's natural sentiment proportions (Positive 61.3%, Negative 21.3%, Neutral 17.5% per language — not artificially rebalanced, per project policy on never rebalancing evaluation data).
- **9 code-switch diagnostic addendum**: the verified genuine code-switch reviews from `codeswitch_audit.md`, kept separate and excluded from the main slice's statistics — too few for quantitative use, included only for qualitative error-analysis illustration (RQ4).

Full ID list: `data/annotations/validation_slice_candidate_ids.csv`. Blank template ready for annotation: `data/annotations/annotation_template_pending.csv` (columns: review_id, language, text, word_count, slice_type, is_difficult_short, annotator_label, annotator_confidence, annotator_notes — the last three are empty, to be filled).

**Star ratings and any pre-existing label are deliberately excluded from the annotation template** so the annotator judges the text itself, not the rating — consistent with the project's distinction between rating-derived and human-annotated labels (`label_provenance_policy.md`).

## Label definitions (to be given to the annotator verbatim)

- **Positive**: the reviewer's overall sentiment toward the business/place/experience described is favorable, even if specific details are criticized, as long as the net impression is positive (e.g. "parking was annoying but the food was amazing, would go again" = Positive).
- **Negative**: the reviewer's overall sentiment is unfavorable, even if some details are praised, as long as the net impression is negative (e.g. "food was fine but service was so rude we're never going back" = Negative).
- **Neutral**: the review is genuinely mixed with no clear net lean, purely factual/descriptive with no evaluative sentiment, or so short/ambiguous that no confident Positive/Negative call can be made.

Annotators should judge the **net overall impression of the review as a whole**, not any single sentence in isolation — a review is not automatically Neutral just because it contains both praise and criticism.

## Protocol

1. One annotator (or, resourcing permitting, two annotators on an overlapping subsample for a reported Cohen's κ, following the same reliability-reporting standard as Zenodo 17011574 and the code-switch audit in this project) reads each review's text only (no rating, no prior label) and assigns Positive/Neutral/Negative, a confidence level (high/medium/low), and optional notes.
2. Annotation order should be randomized (not grouped by language or sentiment) to avoid order effects.
3. Annotators should flag (via `annotator_notes`) any review they found genuinely difficult — sarcasm, mixed sentiment, very short text, unclear reference — to seed the RQ4 error-analysis categories with real examples rather than manufactured ones.
4. Once complete, compute agreement between the annotator's label and the pool's existing label (human-annotated for Arabic; rating-derived for English) as a **diagnostic**, not a correction — disagreements are expected and informative (e.g. they may reveal rating/text disagreement in the English rating-derived labels), not errors to be resolved away.

## What happens to this slice once annotated

Per `decisions.md` D11, the 800 main-slice review IDs are **already frozen as TEST set membership** for the primary Arabic/English/matched comparison (E1–E3) — see `experimental_dataset_protocol.md` and `data/splits/frozen_v1/`. They were never part of train or validation. Once annotation is complete, these labels become the primary evaluation ground truth for that test set, per `label_provenance_policy.md`. If annotation cannot be completed before Phase 3 begins, the existing pool labels (human-annotated for Arabic, rating-derived for English, each explicitly flagged by type) are used as an interim, clearly-caveated substitute — never silently treated as equivalent to the matched-protocol annotation this document defines.

# Phase 2.5 Report — Experimental Dataset Freeze

**Date:** 2026-10-24
**Status:** Phase 2.5 complete. No model trained. No test-set performance inspected. No Results/Conclusion written.

## 1. Final Arabic experimental sample size?
**3,525** (Zenodo 17011574, tourism, human-annotated, 3-class) — the PRIMARY Arabic pool, split train/val/test = 2,786/370/369 (group-aware by place, see `experimental_dataset_protocol.md` §2). This is smaller than the raw combined Arabic figure (12,189) because the Jordan dataset (8,664) was deliberately excluded from the primary 3-class comparison (`decisions.md` D10, D12) — it is retained separately as auxiliary data (Q6).

## 2. Final English main experimental sample size?
**3,525** (matched subset) — deliberately sized and stratified to match the Arabic primary pool, not the full 1,038,643-row English corpus. Split train/val/test = 2,785/352/388. The full corpus (minus the matched subset, 1,035,118 rows) is reserved separately for the supplementary scale experiment E8.

## 3. Final class distribution for EACH language?
See `results/tables/final_dataset_statistics.md` for the authoritative per-split breakdown. Pool-level: Arabic primary = 61.4% Positive / 21.2% Negative / 17.4% Neutral (native distribution, unmodified). English matched = identical by construction (stratified to match). Achieved per-split proportions differ slightly from these pool-level figures because group-aware splitting (no place/business crosses a split boundary) could not hit the sentiment target exactly — e.g. the Arabic test split came out 64.5% Positive vs. the pool's 61.4%. This was not corrected, per the instruction to never rebalance validation/test data.

## 4. Final verified genuine code-switch count?
**9**, out of 109 heuristic candidates and 1,050,832 total usable documents, after a two-reviewer blind audit (κ=0.853 overall, κ=0.809 on the genuine/not-genuine binary) with lead-researcher arbitration on 6 disagreements. Full process and reasoning: `codeswitch_audit.md`. **This is too small for any quantitative model comparison — E6 is not run as a quantitative experiment.**

## 5. How many translation-pair false positives were removed?
**84 of 109** (77.1%) were `bilingual_translation_pair` — overwhelmingly Google Maps' own "(Translated by Google)/(Original)" display structure, not genuine code-switching. A further 13 were `other` (including heuristic language-ID errors — Persian/Farsi and other non-Arabic scripts misidentified as Arabic — and non-semantic gibberish), 2 `named_entity_or_brand`, 1 `incidental_english`. Full breakdown: `codeswitch_audit.md`.

## 6. How will the Jordan dataset be used?
Split by its own natural structure, per `decisions.md` D12:
- **8,364 LLM-weak-labeled rows**: training-augmentation only, never evaluation.
- **300 human-gold rows**: reserved for a **binary** (Positive/Negative — zero Neutral exists in this source, confirmed) auxiliary evaluation experiment (`E_jordan_binary_aux` in `configs/experiments.yaml`), reported separately from the primary 3-class results, never pooled with them.

## 7. What data is allowed for training?
Per `label_provenance_policy.md`: all three provenance types (human_annotated, rating_derived, llm_weak_label) may be used for training, with label_source always recorded per example so label-noise ablations remain possible. Concretely: Arabic tourism train split, English matched train split, Jordan's 8,364 LLM-weak rows (augmentation only), and — for E8 only — the full English scale pool (excluding the matched subset's rows).

## 8. What data is considered high-confidence evaluation?
Human-annotated data only, per `label_provenance_policy.md`: the Arabic tourism val/test splits (already human-annotated, κ=0.87) and the Jordan 300-row gold set (binary auxiliary only). English matched val/test (rating_derived) is explicitly **not** high-confidence evaluation on its own — it is usable only as a secondary, caveated view until the pending manual annotation (Q9) is complete.

## 9. Is manual validation completed or pending?
**PENDING.** 766 candidates prepared (757 main-stratified — exactly the Arabic+English frozen test splits — plus 9 code-switch diagnostic rows), protocol defined in `annotation_guidelines.md`, blank template at `data/annotations/annotation_template_pending.csv`. No labels have been filled in. No manual labels were fabricated.

## 10. Are train/validation/test splits frozen?
**Yes**, for the two primary pools (Arabic tourism, English matched) and for the Jordan auxiliary split. Group-aware (place/business never crosses a split boundary), seed=42, immutable JSON manifests in `data/splits/frozen_v1/`. Per `decisions.md` D11, test membership must not change after this point regardless of model performance.

## 11. Is duplicate leakage confirmed absent?
**Confirmed absent for the two primary pools** — checked by normalized-text MD5 hash across all split pairs after group-aware assignment; 0 cross-split duplicate-hash groups found for both Arabic tourism and English matched (`freeze_splits.py` output). Not independently re-checked for Jordan (no group identifier available to split on in the first place) or for the full English scale pool against the matched subset — the latter is handled by explicit ID exclusion (§4 of `experimental_dataset_protocol.md`) rather than a hash check, since the matched subset was sampled directly from that pool by construction.

## 12. What is the exact Phase-3 experiment matrix?
Defined in `configs/experiments.yaml`, status `PREPARED_NOT_RUN` for every experiment:
- **Primary:** E1 (Arabic-only), E2 (English-only), E3 (matched Arabic-vs-English, the central RQ3 experiment), E4 (combined multilingual training), E5 (cross-lingual robustness)
- **Supplementary:** E6 (real-world code-switch — marked `NOT_FEASIBLE_QUANTITATIVELY`), E7 (external SESA-CSD — marked `BLOCKED_NO_CONFIRMED_ACCESS`), E8 (full-English scale), E_jordan_binary_aux (Jordan binary auxiliary)

## Readiness verdict

**READY FOR PHASE 3**

All data-engineering commitments required to start Phase 3 are complete, documented, and verified: stable IDs, a scientifically defensible (not literally-instructed) matching target with the reasoning logged, group-aware leak-free frozen splits, a fully manually-audited code-switch count with inter-rater reliability reported, a correctly-scoped Jordan dataset usage policy, and a label-provenance policy separating training from evaluation use. The one open item — manual annotation of the 766-row validation slice — is explicitly allowed to remain pending per the project's own instruction and does not block E1/E2/E4/E5/E8 from proceeding; it specifically gates the "clean, non-confounded" version of the **E3/RQ3** cross-language claim, which must stay labeled exploratory/confounded (per `dataset_audit.md` §7) until that annotation is completed. No model has been trained, no test-set performance has been inspected, and no Results or Conclusion text has been written.

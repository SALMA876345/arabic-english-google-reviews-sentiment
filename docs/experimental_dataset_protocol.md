# Experimental Dataset Protocol (Phase 2.5 — Frozen)

This document defines the exact datasets, splits, and usage rules for Phase 3. It supersedes any looser description in `methodology_plan.md` where the two disagree — this document is the authoritative, frozen version.

## 1. Primary matched comparison pool (E1–E3)

| Pool | N | Label source | Role |
|---|---|---|---|
| Arabic tourism (Zenodo 17011574) | 3,525 | human_annotated (κ=0.87) | Arabic primary |
| English matched subset | 3,525 | rating_derived | English primary |

**Why 3,525, not 12,189:** see `decisions.md` D10. The combined Arabic figure (12,189) includes the Jordan dataset, which is binary-only and majority LLM-weak-labeled — pooling it into a "3-class Arabic" matching target would misrepresent what's being compared. Only the tourism pool is genuinely 3-class and human-annotated, so it is the correct match target.

**How the English subset was matched** (`src/preprocessing/build_matched_english_subset.py`, `results/tables/arabic_vs_matched_english_comparability.md`):
- Sample count: exactly 3,525
- Sentiment distribution: stratified to match the Arabic pool exactly (Positive 61.4%, Negative 21.2%, Neutral 17.4%)
- Domain: restricted to a tourism/park/museum/historical-site category proxy (111,527-row candidate pool before sampling) — the closest available match to the Arabic tourism domain
- Review length: stratified by quartile bin within each sentiment class to approximate the Arabic pool's word-count distribution (medians align closely: 17 vs. 16 words; the English subset retains a longer right tail — max 731 vs. 255 words)

**Explicitly NOT matched** (documented, not hidden):
- **Geography**: English = Wyoming/Vermont (US); Arabic = Saudi Arabia. The UCSD/McAuley 2021 release has no Middle East/Gulf coverage (confirmed in Phase 2) — true geographic matching was not possible with this data source.
- **Star-rating distribution**: the Arabic pool has no star ratings at all (aspect-sentiment annotated, not rating-based), so there is nothing to match the English subset's own rating distribution against.

## 2. Frozen splits (group-aware, no business/place leakage)

`src/preprocessing/freeze_splits.py`, seed=42. Both pools were split by whole group (place name for Arabic, `gmap_id`/business for English) so no place or business appears in more than one split — a place/business is assigned entirely to train, val, or test.

| Pool | Train | Val | Test |
|---|---|---|---|
| Arabic tourism | 2,786 (79.0%) | 370 (10.5%) | 369 (10.5%) |
| English matched | 2,785 (79.0%) | 352 (10.0%) | 388 (11.0%) |

Achieved sentiment proportions per split are reported in `results/tables/final_dataset_statistics.md` — they are close to but not exactly the overall pool proportions (group-aware assignment cannot hit both the count target and the sentiment target exactly with only 42 Arabic place-groups). Confirmed zero cross-split exact-duplicate text leakage (checked by normalized-text hash, see script output).

Immutable manifests (review_id lists per split): `data/splits/frozen_v1/arabic_tourism_{train,val,test}_ids.json`, `data/splits/frozen_v1/english_matched_{train,val,test}_ids.json`. **Test membership in these manifests must not change after this point, regardless of any model's performance** (`decisions.md` D11).

## 3. Jordan dataset (Zenodo 22061934) — auxiliary use only

Per `decisions.md` D12:
- **8,364 LLM-weak-labeled reviews**: training-augmentation use only. Never evaluation ground truth. Manifest: `data/splits/frozen_v1/jordan_auxiliary_train_weak_ids.json`.
- **300 human-gold reviews**: reserved for a **binary** (Positive/Negative — no Neutral exists in this source) auxiliary evaluation experiment. Never used for training. Manifest: `data/splits/frozen_v1/jordan_auxiliary_eval_gold_ids.json`.
- No business/place identifier exists in this release, so group-aware splitting could not be applied here — documented as a limitation, not resolved.
- Results from the Jordan binary auxiliary experiment must be reported separately from the primary 3-class figures, never pooled with them.

## 4. Full English corpus — reserved for the scale experiment (E8) only

`data/processed/english_ucsd_v2.csv` (1,038,643 usable rows) minus the 3,525 rows already committed to the matched subset = **1,035,118 rows** available for E8. This exclusion is mandatory: training E8 on the full, unfiltered corpus would silently include the English matched subset's frozen test set in E8's training data, leaking across experiments. Rule recorded in `data/splits/frozen_v1/english_e8_scale_pool_exclusion_rule.json`.

## 5. Code-switch diagnostic set — qualitative only, not a quantitative experiment

9 verified genuine code-switched reviews (`codeswitch_audit.md`). Too few for any train/test split or statistical comparison. Used only for qualitative illustration in error analysis (RQ4). **E6 (quantitative real-world code-switch evaluation) is not feasible with current data** — see `codeswitch_audit.md` for the full reasoning and recommended path (new, dedicated data collection, out of scope for this sprint).

## 6. Manually validated test slice — pending

757 main-stratified candidates (369 Arabic test-split rows + 388 English test-split rows) + 9 code-switch diagnostic rows = 766 total, prepared in `data/annotations/annotation_template_pending.csv`. **Labels are blank — annotation has not been performed.** See `annotation_guidelines.md` for the protocol. These rows are already the frozen test set for the primary comparison (§2); annotation, once complete, upgrades their evaluation status per `label_provenance_policy.md` but does not change which rows they are.

## 7. Label-use summary (cross-reference to `label_provenance_policy.md`)

| Data | Allowed for training? | Allowed as final evaluation ground truth? |
|---|---|---|
| Arabic tourism (human_annotated) | Yes | Yes (already human-annotated) |
| English matched (rating_derived) | Yes | Only as a secondary, explicitly-caveated view — not primary, until the manual annotation (§6) is complete |
| Jordan weak (llm_weak_label) | Yes, training-augmentation only | No |
| Jordan gold (human_annotated) | No (reserved) | Yes, for the binary auxiliary experiment only |
| English full scale pool (rating_derived) | Yes, E8 only | Only as a secondary, caveated view (same caveat as matched English) |

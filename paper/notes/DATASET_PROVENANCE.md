# Consolidated Dataset Provenance

One authoritative table per dataset/process. All counts are taken directly from `results/tables/phase2_corpus_stats.md`, `docs/codeswitch_audit.md`, `docs/decisions.md`, and `data/splits/frozen_v1/manifest.json` -- none are recomputed or estimated here. Nothing below is fabricated; where a figure is not on file, it is marked as such.

## 1. Saudi Arabic tourism dataset (primary Arabic)

| Field | Value |
|---|---|
| Source | Zenodo record **17011574** |
| DOI/identifier | Zenodo 17011574 (resolvable as `10.5281/zenodo.17011574`) |
| License | **CC-BY-4.0**, confirmed via Zenodo API (`docs/decisions.md` D1) |
| Number initially obtained (raw) | 3,543 reviews |
| Number retained/used (usable) | 3,525 (6 dropped, no derivable label; 12 removed as duplicates) |
| Language | Arabic |
| Label source | `human_annotated` (original single-pass annotation at dataset-release time; κ=0.87 as reported by the dataset's own documentation, not independently re-verified by this project) |
| Task role | Primary Arabic 3-class sentiment pool; frozen split train=2,786 / val=370 / test=369 (`data/splits/frozen_v1/arabic_tourism_*_ids.json`) |
| License/status | Open (CC-BY-4.0) -- safe to redistribute derivatives with attribution |
| Release restrictions | Attribution required; none beyond that |

## 2. Jordan Arabic restaurant dataset (auxiliary)

| Field | Value |
|---|---|
| Source | Zenodo record **22061934** |
| DOI/identifier | Zenodo 22061934 |
| License | **CC-BY-4.0** [updated 2026, per `paper/notes/LITERATURE_VERIFICATION.md`: live-verified via direct inspection of the official Zenodo record page, which states this license explicitly. Supersedes this row's earlier "not independently re-confirmed" status.] |
| Number initially obtained (raw) | 8,671 reviews |
| Number retained/used (usable) | 8,664 (6 removed as duplicates) |
| Language | Arabic (Jordanian dialect) |
| Label source | 300 reviews `human_annotated` (gold, binary Positive/Negative only -- confirmed zero Neutral examples); 8,364 reviews `llm_weak_label` (Claude Sonnet 4.6 / GPT-5, per `docs/label_provenance_policy.md`) |
| Task role | 8,364 LLM-weak rows: training-augmentation only, never evaluation. 300 human-gold rows: evaluation-only ground truth for a separate **binary** auxiliary experiment (`E_jordan_binary_aux`), never pooled into the primary 3-class comparison (`docs/decisions.md` D10, D12). Note: this source's own "human-gold" subset is a pre-existing dataset-level term, unrelated to and not to be confused with this project's own 757-review Human-Gold reference set (`paper/annotation/full/human_gold_757.csv`) -- see the disambiguation note below. |
| License/status | **CC-BY-4.0, confirmed** (live-verified 2026, see above) |
| Release restrictions | Attribution required; releasable on the same basis as the Arabic tourism dataset (row 1) |

**Disambiguation note (added this phase):** the term "human-gold" appears twice in this project with two unrelated referents -- (a) Zenodo 22061934's own pre-existing 300-review binary gold subset (used only for the Jordan auxiliary experiment), and (b) this project's own 757-review, 3-annotator + blind-adjudicator Human-Gold reference set (`paper/annotation/full/human_gold_757.csv`, Section 6 below). The manuscript must distinguish these explicitly on first mention of either.

## 3. English Google Local Reviews source (primary English)

| Field | Value |
|---|---|
| Source | UCSD/McAuley Google Local Review Dataset (Google Maps reviews + business metadata, US-only, collected through September 2021) |
| DOI/identifier | No DOI found on the official source page (verified live this phase -- see `DATA_LICENSING_AND_RELEASE.md`); official URL: https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/ |
| Number initially obtained (raw) | 1,993,624 raw lines (Wyoming + Vermont subset only, not the full multi-state dump) |
| Number retained/used (usable) | 1,170,942 after requiring non-null text+rating; 1,038,643 after deduplication (132,299 removed as duplicates) |
| Number in the primary matched comparison pool | 3,525 (domain-filtered -- tourism/park/museum/historical-site category proxy -- and length-stratified sample; `docs/decisions.md` D13); frozen split train=2,785 / val=352 / test=388 |
| Language | English |
| Label source | `rating_derived` (1-2 stars -> Negative, 3 -> Neutral, 4-5 -> Positive; `docs/decisions.md` D3) -- explicitly not human-annotated at the original-label stage |
| Task role | Primary English 3-class sentiment pool, matched (sentiment distribution exact, length approximate) to the Arabic primary pool |
| License/status | **No confirmed license** (verified live this phase; see `DATA_LICENSING_AND_RELEASE.md`) |
| Release restrictions | **Raw text, review IDs, and labels keyed to review IDs must not be redistributed publicly** pending explicit permission from the data provider; see `DATA_LICENSING_AND_RELEASE.md` for the full release plan |

## 4. Code-switch candidate source/process

| Field | Value |
|---|---|
| Source | The project's own combined usable corpus (Arabic usable 12,189 + English usable 1,038,643 = 1,050,832 documents), not an external code-switch dataset (none with a confirmed public download path was found; `docs/decisions.md` D4) |
| Process | Character-script-fraction heuristic (`methodology_plan.md` §4-5) flagged 109 candidate documents; all 109 (not a sample) were manually classified by two independent blind reviewers, with a third-pass arbitration of 6 disagreements (`docs/codeswitch_audit.md`) |
| Number initially flagged | 109 |
| Number confirmed genuine code-switch | **9** (review IDs on file in `docs/codeswitch_audit.md`) |
| Root cause of the other 100 | 84 (77.1%) were a Google Maps UI translation-display artifact (bilingual translation pairs, not organic code-switching); 13 (11.9%) were script-misidentification (Farsi/Hebrew/other) or noise; 2 (1.8%) named entities/brands; 1 (0.9%) incidental English |
| Language | Mixed Arabic-English (where genuine) |
| Label source | N/A -- retained as a qualitative diagnostic set only, never labeled for a quantitative task |
| Task role | Qualitative case-study / error-analysis illustration only; explicitly not usable for a quantitative E6 experiment (`docs/codeswitch_audit.md`) |
| License/status | Inherits the license status of whichever source corpus each of the 9 examples came from (7 Jordan Arabic, 2 English Vermont -- both already covered above) |
| Release restrictions | Same as the respective source dataset per example; the 2 English-sourced examples fall under the English dataset's unresolved-license restriction above |

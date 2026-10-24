# Methodology Plan (Design Only — No Training in Phase 1)

## 1. Task definition and research questions

**Task:** 3-class sentiment classification (Positive / Neutral / Negative) at the document (full-review) level, for Arabic, English, and Arabic-English code-switched Google Maps-style location/business reviews.

**Research questions — validated against the literature and dataset evidence (see `research_gap.md`, `dataset_audit.md`):**

- **RQ1** (unchanged): How accurately can sentiment be classified from Arabic and English real-world location/business reviews? — Supported: datasets exist for both languages in-domain.
- **RQ2** (unchanged): Do transformer-based models outperform traditional machine-learning approaches? — Supported: standard, answerable comparison.
- **RQ3** (**revised framing required**): *As originally worded* ("how does performance differ across Arabic, English, and code-switched reviews") risks an unsupported causal claim, because the Arabic and English data differ in label-generation process, sub-domain, and scale (confound documented in `dataset_audit.md` §7). **Revised wording:** *"How does sentiment classification performance differ across Arabic, English, and Arabic-English code-switched reviews, and to what extent can observed differences be attributed to language versus dataset-origin and label-source confounds?"* This must be answered primarily on the small matched-protocol validation slice (§5 below), with the larger pooled-dataset results reported as exploratory and explicitly flagged as confounded.
- **RQ4** (unchanged, strengthened): Which linguistic phenomena cause sentiment classification errors? — See §7 (error analysis categories) — grounded in real, observed phenomena, not manufactured examples.

## 2. Label scheme

Positive / Neutral / Negative, document-level. For every data source used, the label's provenance must be recorded and reported using one of these three terms, never conflated:
- **Human-annotated sentiment ground truth** (e.g., Zenodo 17011574 — 2 annotators, κ = 0.87)
- **Rating-derived sentiment labels** (e.g., UCSD/McAuley, if used — explicit rule: 1–2★ = Negative, 3★ = Neutral, 4–5★ = Positive; this rule must be validated, not assumed, against a hand-labeled gold sample before trusting it at scale, since sarcastic 5★ and apologetic 1★ reviews are a known failure mode)
- **Weak/automatically-generated labels** (e.g., Zenodo 22061934's majority LLM-generated labels — used only as weak supervision, validation always performed on the human gold subset)

Zenodo 17011574's native labels are aspect-level (6 aspects); using its "overall experience" aspect as the document-level label is a deliberate, documented methodological choice, validated by spot-checking agreement between the aspect label and a holistic read of a sample of reviews before relying on it at scale.

## 3. Data acquisition constraints (no uncontrolled scraping)

Per project instruction, no uncontrolled Google Maps scraping will be performed. Phase 1's recommended primary sources (Zenodo 17011574, Zenodo 22061934, UCSD/McAuley) are **already-collected, existing research releases** — no new scraping is required to proceed. If, in Phase 2, the matched-protocol validation slice (§5) requires fresh reviews, the only acceptable mechanism is the **official Google Places API** (or Google's documented data-licensing terms for research use), with the specific usage terms reviewed and documented in `decisions.md` before any collection begins. If an API-based or otherwise ToS-compliant collection mechanism cannot be confirmed within the sprint, the matched-protocol slice will instead be built by sub-sampling and dual-annotating existing in-pool reviews rather than collecting new ones — this fallback must be stated explicitly if invoked.

**Title/claims constraint:** the manuscript title and claims may only describe the data as "Google Maps reviews" for the portion that is genuinely Google-Maps-sourced (true for the current primary Arabic and English picks). If the final pipeline substitutes a non-Google-Maps source (e.g., Yelp) as a primary training source rather than a reserved/robustness set, the title and all claims must be revised accordingly — this must be re-checked at the start of Phase 2 before any data finalization.

## 4. Preprocessing

- Unicode normalization (NFKC), Arabic-specific normalization (alef/hamza/ta-marbuta variants — applied carefully, documented, and never applied in a way that would erase genuine code-switching signal, e.g. do not strip Latin-script tokens during Arabic normalization)
- Deduplication by normalized-text hash, both within and across pooled sources (required given the leakage risks documented in `dataset_audit.md` §6)
- Script/language identification per token and per document (Arabic script, Latin script, Arabizi/transliterated Arabic heuristics, emoji/punctuation handling)
- Code-Mixing Index (CMI) computation per document, following Mixat's methodology as a calibration reference, to support the language-group stratification in §5
- Removal of exact boilerplate/spam patterns where identifiable; no removal of short reviews by default (short reviews are a planned error-analysis category, not noise to discard)

## 5. Language-group stratification (replaces an external code-switch dataset)

Since no accessible external Arabic-English code-switched sentiment dataset exists (`dataset_audit.md` §5), every document in the pooled corpus is assigned to one of four groups via the CMI/script-ID pipeline above, not by source dataset:
- **A — Arabic-only**
- **B — English-only**
- **C — Arabizi / transliterated Arabic** (reported separately from D; linguistically distinct)
- **D — Genuine intra-sentence/intra-document code-switching** (mixed Arabic-script + Latin-script, or Arabic + embedded English terms, within the same document)

All evaluation (per-language F1, confusion matrices, error analysis) is reported per group, not only per source dataset — this is what allows RQ3 to be answered at all, since the source datasets themselves are monolingual.

**Matched-protocol validation slice:** a small (target: low hundreds per language/group, resourcing permitting) human-annotated slice, same 2-annotator protocol with Cohen's κ reported (modeled on Zenodo 17011574's protocol), built from Groups A, B, and D, used as the one methodologically clean cross-language comparison point referenced in RQ3.

## 6. Split strategy

- Stratified by: label class, language group (A/B/C/D), and source dataset (to prevent one sub-domain dominating a split)
- Deduplication enforced **before** splitting (never split a near-duplicate pair across train/test)
- No same-reviewer or same-business leakage across train/test where that metadata is available (documented as unresolved/unavailable where it is not — e.g., UCSD/McAuley's business IDs could support business-level splitting if adopted)
- Test set construction prioritizes the matched-protocol validation slice (§5) plus a held-out portion of the primary pools; any reserved/external-evaluation dataset (HARD, SemEval ABSA, etc.) is used only as out-of-domain robustness check, never blended into the primary train/test split
- Fixed random seed policy: a single project-wide seed value defined in `configs/`, reused for every split/shuffle operation, with the seed value itself logged in every experiment's output metadata (see §9)

## 7. Models (design only — not trained in Phase 1)

| Tier | Model | Why included |
|---|---|---|
| Classical baseline | TF-IDF + Logistic Regression | Fast, interpretable floor; answers RQ2 |
| Classical baseline | TF-IDF + Linear SVM | Standard second classical baseline |
| Arabic-oriented transformer | MARBERT (preferred over AraBERT per the 2026 DialectSentEval shared-task finding that MARBERTv2 > AraBERT on dialectal 3-class sentiment — see `research_gap.md`) | Domain/dialect-matched pretraining |
| Arabic-oriented transformer (secondary) | AraBERT | Comparison point / ablation, not primary |
| Multilingual transformer | XLM-RoBERTa | Directly answers RQ3; also the model the SESA-CSD paper found to outperform bilingual LLMs on Saudi-English code-switched text — relevant precedent for our Group D evaluation |

No LLM-prompting arm is included by default (insufficient literature grounding per `research_gap.md` §4's open question) — may be added in Phase 2 only if it is scoped to answer a specific RQ, not for model-zoo completeness.

## 8. Evaluation plan

- Metrics: Accuracy, Precision, Recall, Macro-F1, Weighted-F1, per-class F1, **per-language-group F1 (A/B/C/D)**, confusion matrices
- Bootstrap resampling for confidence intervals on Macro-F1 and per-group F1
- Significance testing (e.g., paired bootstrap or McNemar's test) when comparing model pairs, applied only on held-out test data, never used to select hyperparameters
- Explicit safeguards: deduplication before split (§6), no hyperparameter tuning on the test set (dev set only), no same-source contamination across train/test (§6), reserved datasets never blended into primary splits (§6)

## 9. Error analysis plan

Categories, applied to real observed errors only (never manufactured examples) once a trained model exists in Phase 2:
negation, sarcasm, Arabic dialect variation, spelling variation, emojis, code-switching (Group D), Arabizi/transliteration (Group C), mixed/ambivalent sentiment within one review, very short reviews, rating/text disagreement (where star ratings are available alongside text).

## 10. Reproducibility controls

- Single project-wide random seed, defined in `configs/`, logged per experiment
- Directory conventions: `data/raw/` (untouched source files), `data/processed/` (cleaned/split, versioned by a processing-script hash or date), `data/annotations/` (the matched-protocol slice and any gold subsets), `results/predictions/`, `results/tables/`, `results/figures/`, `experiments/` (one subdirectory per run with its exact config snapshot)
- Every experiment run must record: dataset version/hash, split seed, model name + checkpoint/version, hyperparameters, and evaluation metrics together in one machine-readable file — exact schema to be defined at the start of Phase 2, not in Phase 1
- No model training occurs in Phase 1; this section defines conventions only

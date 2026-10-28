> **SUPERSEDED (2026-10-27):** see `final_publication_readiness_audit.md` for the current audit, performed after the 3-annotator + blind-adjudicator Human-Gold study this file's §7/RQ3 section describes as "still unannotated." This file is retained as a historical record of pre-Human-Gold readiness, not as the current assessment.

# Publication Readiness Audit

**Role:** Senior peer reviewer / associate editor / NLP researcher, evaluating pre-manuscript readiness for a Q1-journal submission.
**Scope:** Evidence-based audit of the repository as it stands on 2026-10-26. No models retrained, no results modified, no new statistical tests run beyond what already exists. Every numeric claim below was checked against an actual file in this repository (cited inline); nothing is taken on the user's word alone, including the "expected" values given in the audit brief.
**Companion reading:** `docs/decisions.md` (D1–D18), `docs/known_limitations.md` (24 items across 4 phase addenda), `paper/notes/phase3_report.md`, `paper/notes/phase3b_report.md`, `docs/error_analysis.md`, `docs/codeswitch_audit.md`.

---

## 1. The Complete Research Story (as reconstructed from the repository)

**Problem:** 3-class (Positive/Neutral/Negative) sentiment classification of Arabic, English, and Arabic-English code-switched location/business reviews.

**Motivation / gap** (`docs/research_gap.md`): Arabic dialect sentiment, English review sentiment, and Arabic transformer baselines are each individually saturated. Arabic-English code-switched sentiment classification *exists* (EESA/Sherif & Sabty 2024; SwitchEmbed/Rizkallah et al. 2026; SESA-CSD/Alghamdi et al. 2026) — the project's own Phase 1 review correctly self-corrected away from an initial "first ever" framing. Arabic Google Maps review mining exists but is aspect-based and monolingual (AraMAMS; tourism ABSA paper). **The defensible, narrow gap**: no identified prior work performs sentiment classification on Arabic-English *code-switched* **Google Maps/location-review-domain** text. This gap is explicitly flagged as *provisional* on (a) a Phase 2 code-switch yield that turned out to be far too small (§9 below), and (b) an undisclosed English-venue-only literature search blind spot (`known_limitations.md` #11).

**Research questions** (`docs/methodology_plan.md` §1):
- RQ1: accuracy of sentiment classification on real-world Arabic/English reviews.
- RQ2: do transformers outperform classical ML?
- RQ3 (revised wording, pre-built in): language differences vs. dataset-origin/label-source confounds.
- RQ4: which linguistic phenomena drive errors?

**Datasets**: Arabic primary = Zenodo 17011574 tourism reviews (3,525 usable, human-annotated κ=0.87) — `docs/dataset_audit.md` §3. English primary = a 3,525-row subset of the UCSD/McAuley Google Local corpus, domain/sentiment/length-matched to the Arabic pool (`docs/experimental_dataset_protocol.md` §1). Jordan restaurant dataset (Zenodo 22061934, 8,664 usable) redirected to training-augmentation + a separate binary auxiliary task after direct inspection found it has **zero Neutral examples** and is majority LLM-labeled (`decisions.md` D10, D12). Labels are tracked by a three-way provenance taxonomy — human_annotated / rating_derived / llm_weak_label — with a binding rule never to call the latter two "ground truth" (`docs/label_provenance_policy.md`).

**Frozen splits**: group-aware (by place for Arabic, by business for English) train/val/test, independently re-verified to have zero review-ID overlap and zero group overlap across splits (`docs/experimental_dataset_protocol.md` §2; re-confirmed by the adversarial reviewer per `decisions.md` D16).

**Sample sizes**: Arabic 2,786/370/369 (train/val/test); English 2,785/352/388.

**Experiments run**: E1 (Arabic-only: 2 classical + MARBERT-LoRA + XLM-R-LoRA, Phase 3A; + MARBERT-full-FT + XLM-R-full-FT, Phase 3B), E2 (English-only, same pattern), E3 (reporting exercise over E1+E2, not a separate run), E4 (combined multilingual: **failed 3× OOM on Phase 3A**; **completed on Phase 3B** as "XLM-R Multilingual"), E5 (bidirectional zero-shot cross-lingual, both phases), E6 (9-example code-switch qualitative diagnostic only), E7 (external SESA-CSD — not run, no access), E8 (full-English scale — not run), E_jordan_binary_aux (classical only, binary task).

**Statistical analysis**: paired bootstrap (resample test rows with replacement, recompute Δmacro-F1 each iteration) + Holm-Bonferroni correction, family-defined per (experiment, language) — `src/evaluation/metrics.py`, `scripts/evaluate.py` (Phase 3A); externally-run Kaggle bootstrap with 10,000 iterations (Phase 3B, implementation code not in this repository — see §5).

**Error analysis**: two independent agent passes read all 327 Phase 3A error rows against a fixed 13-category list; `mixed_sentiment` dominates everywhere, `rating_text_disagreement` drives ~50-60% of English errors, code-switching confirmed non-factor (`docs/error_analysis.md`).

**Reproducibility**: seed=42 throughout; `experiments/registry.csv`; pinned `requirements.txt`; two independent adversarial-reviewer passes (`decisions.md` D8, D16) found zero fabrication/leakage across both audits.

**Deployment**: FastAPI backend + React/Vite frontend serving a separate full-FT GPU deployment checkpoint (val macro-F1=0.7999539, not interchangeable with the E4 research figures — `decisions.md` D17).

### RQs only partially answered (flag explicitly)

| RQ | Status |
|---|---|
| RQ1 | Answerable for Arabic (clean, human-annotated test set). For English, only answerable with the standing rating-derived-label caveat — not a clean accuracy claim until the pending manual-validation slice (§7 below) is annotated. |
| RQ2 | Answered, but the answer is "not statistically significant" (§6) — a real, reportable, but modest answer, not "transformers win" or "classical wins." |
| RQ3 | **Only partially answered.** The matched-pool comparison is explicitly confounded (dataset origin, label provenance, geography — `dataset_audit.md` §7). The one mitigation the project itself designed to produce a clean answer — the 766-row matched-protocol manually-annotated slice (`docs/annotation_guidelines.md`) — is **still unannotated**. This is the single most consequential open item in the entire project for RQ3's credibility. |
| RQ4 | Reasonably well answered for Phase 3A (systematic, two-rater, fixed-category error analysis exists). Not yet repeated for Phase 3B's full-FT predictions — no error analysis exists for the GPU runs at all (confirmed: no `error_cases_*` files reference Phase 3B run IDs). |

---

## 2. Phase 3A vs. Phase 3B — Separation Verified

Both tracks are physically separate in the repository (`results/predictions/` + `experiments/checkpoints/` for 3A; `results/phase3b_kaggle_gpu/` for 3B) and separate in every table (`model_comparison.csv`'s `LoRA_adapted_NOT_full_finetune` column; `master_final_results.csv`'s `Training_Setting`/`Result_Status` columns). Neither has overwritten the other — verified directly:

- `results/tables/model_comparison.csv` row for `E1_xlmr` (Phase 3A): macro_f1=0.623310, `LoRA_adapted_NOT_full_finetune`=True.
- `results/phase3b_kaggle_gpu/master_final_results.csv` row "XLM-R Full FT + Weighted / Standalone / Arabic": 0.740295. Both figures coexist; neither was deleted or silently merged.

**Data-identity verification, re-confirmed:** `docs/decisions.md` D17 states an MD5 hash comparison between `results/phase3b_kaggle_gpu/input_data_bundle_sent_to_kaggle/` and `data/processed/frozen_v1/` + `data/splits/frozen_v1/` found all 8 files byte-identical. I could not re-run the hash comparison myself in this audit pass (no destructive/compute actions were taken, consistent with the brief), so this is **evidence as documented, not independently re-executed in this session** — it was executed and logged at integration time (2026-10-26), by the same actor compiling this audit, which is a limitation worth naming: a fully independent third party has not re-run this hash check. Recommend re-running it once before manuscript submission as a 30-second sanity step, not because there is specific reason to doubt it, but because "I verified my own earlier verification from memory" is weaker than a fresh checksum in the same sitting.

**Non-causal framing — correctly enforced in the documentation.** `configs/training.yaml`'s `phase3b_gpu.non_causal_framing_requirement`, `known_limitations.md` #21, and `phase3b_report.md`'s opening section all state the same constraint in the same words: fine-tuning method, class-weighting, and max_seq_length changed simultaneously with hardware, so no score difference may be attributed to "the GPU." **This is the strongest scientifically defensible interpretation and the project has already converged on it correctly** — my only addition: the manuscript should name this as what it is, a **multi-factor bundled intervention**, and should NOT attempt post-hoc partial attribution language ("probably mostly the class weighting") without an ablation (see §12).

---

## 3. Master Audit Table

| Language | Model | Setting | Phase | Val/Test | Macro-F1 | Accuracy | Primary/Rerun | Predictions available? | Stat-test eligible? | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Arabic | TF-IDF+LogReg | Standalone | 3A | Test | 0.704756 | 0.785908 | — | Yes | Yes | `results/tables/model_comparison.csv` row 2 |
| Arabic | TF-IDF+SVM | Standalone | 3A | Test | 0.704820 | 0.796748 | — | Yes | Yes | same, row 1 |
| Arabic | XLM-R (LoRA) | Standalone | 3A | Test | 0.623310 | 0.794038 | — | Yes | Yes | same, row 3 |
| Arabic | MARBERT (LoRA) | Standalone | 3A | Test | 0.617712 | 0.810298 | — | Yes | Yes | same, row 4 |
| Arabic | MARBERT Full FT+Weighted | Standalone | 3B | Test | **0.785025** | n/a (not in this repo) | **Primary** | **No — lost** | Via rerun only | `master_final_results.csv` |
| Arabic | MARBERT Full FT+Weighted | Standalone | 3B | Test | 0.765263 | n/a | Reproducibility rerun | Yes | Yes | `E1_marbert_arabic_reproducibility_test_predictions.csv` (369 rows, verified) |
| Arabic | XLM-R Full FT+Weighted | Standalone | 3B | Test | **0.740295** | n/a | **Primary** | **No — lost** | Via rerun only | `master_final_results.csv` |
| Arabic | XLM-R Full FT+Weighted | Standalone | 3B | Test | 0.740126 | n/a | Reproducibility rerun | Yes | Yes | `E1_xlmr_arabic_reproducibility_test_predictions.csv` (369 rows, verified) |
| Arabic | XLM-R Multilingual | Combined | 3B | Test | 0.767865 | n/a | Primary (=E4) | Yes | Yes | `E4_multilingual_xlmr_arabic_test_predictions.csv` (369 rows, verified) |
| Arabic | XLM-R EN→AR zero-shot | Cross-lingual | 3B | Test | 0.679992 | n/a | Primary | Yes | Yes | `E5B_english_to_arabic_test_predictions.csv` (369 rows, verified) |
| Arabic | XLM-R (LoRA) AR-trained | Cross-lingual | 3A | Test | 0.541114 | 0.758808 | — | Yes | Yes | `model_comparison.csv` row 8 |
| English | TF-IDF+LogReg | Standalone | 3A | Test | 0.687062 | 0.760309 | — | Yes | Yes | `model_comparison.csv` row 5 |
| English | TF-IDF+SVM | Standalone | 3A | Test | 0.650639 | 0.744845 | — | Yes | Yes | row 6 |
| English | XLM-R (LoRA) | Standalone | 3A | Test | 0.611012 | 0.780928 | — | Yes | Yes | row 7 |
| English | XLM-R Full FT+Weighted | Standalone | 3B | Test | 0.727644 | n/a | Primary | Yes | Yes | `E2_xlmr_fullft_gpu_3ep_test_predictions.csv` (388 rows, verified) |
| English | XLM-R Multilingual | Combined | 3B | Test | 0.739722 | n/a | Primary (=E4) | Yes | Yes | `E4_multilingual_xlmr_english_test_predictions.csv` (388 rows, verified) |
| English | XLM-R AR→EN zero-shot | Cross-lingual | 3B | Test | 0.680415 | n/a | Primary | Yes | Yes | `E5A_arabic_to_english_test_predictions.csv` (388 rows, verified) |
| English | XLM-R (LoRA) EN-trained | Cross-lingual | 3A | Test | 0.545502 | 0.747423 | — | Yes | Yes | row 9 |
| Arabic (binary) | TF-IDF+LogReg | Jordan auxiliary | 3A | Test | 0.923332 (observed-classes-only) | 0.923333 | — | Yes | n=300, marginal | row 10 |
| CS (n=9) | MARBERT (LoRA) | Qualitative only | 3A | n/a | **not computed** | n/a | — | Yes | **No — explicitly excluded, correctly** | `error_analysis.md` §E6 |

**All "expected" values from the audit brief are confirmed present and correct, to 6 decimal places where given.** No discrepancies found between the brief's expected numbers and the actual repository artifacts.

**One correction to the audit brief's framing:** the brief lists "English→Arabic zero-shot: 0.679992" under *Arabic* primary results and "Arabic→English zero-shot: 0.680415" under *English* — this is correct as the brief states it (the zero-shot score is reported against the *target* language's test set), and the repository is internally consistent with this convention (`E5B_english_to_arabic_test_predictions.csv` evaluates on the Arabic test set, scoring 0.679992).

---

## 4. Primary vs. Reproducibility-Rerun Treatment — Assessment

**Is the treatment scientifically defensible? Yes, with one required disclosure improvement.**

What the repository does right:
- Primary figures (0.785025, 0.740295) are never silently replaced — confirmed in `master_final_results.csv`, `configs/models.yaml`, `phase3b_report.md`.
- The rerun's use is scoped correctly: *only* for paired statistical testing, *only* because row-level predictions for the primary runs don't exist. This is the only methodologically coherent choice available — you cannot run a paired test without paired predictions, and fabricating predictions to match a known aggregate score would be a serious integrity violation (correctly avoided).
- The gap between primary and rerun is small (0.785025 vs. 0.765263 = 1.98 points; 0.740295 vs. 0.740126 = 0.017 points) — small enough that the rerun is a reasonable stand-in for *approximate* significance testing, though not identical.

**What must change before a journal manuscript, not just before this audit:**
1. Every table/figure that reports a Holm-adjusted p-value touching "MARBERT" or "standalone XLM-R" on Arabic must carry an inline footnote: *"Significance computed on the reproducibility-rerun realization (macro-F1=X), not the primary reported score (macro-F1=Y), because the primary run's row-level predictions were not retained."* `known_limitations.md` #22 states this in prose; it has **not yet been propagated as an inline table footnote** in `results/phase3b_kaggle_gpu/master_final_results.csv` itself (only in the separate `README_PHASE3B.txt`). A reader who opens only the CSV would not see this caveat. **Fix before manuscript: add the caveat to the CSV/table that will actually be reproduced in the paper, not only to a README.**
2. The manuscript's methods section must state explicitly *why* the original predictions were lost (process failure during the Kaggle session — not specified anywhere in the repository beyond "lost," which is honest but thin). If a root cause is knowable (notebook overwritten, output not saved, session timeout), stating it strengthens credibility; if genuinely unknown, say "not recoverable" rather than leaving it unexplained.
3. A 1.98-point MARBERT gap (primary vs. rerun) on the *same* model/data/hyperparameters is itself a small data point about run-to-run variance under full fine-tuning — worth one sentence in the limitations section, since it's informative about the single-seed-training-variance question raised in §12.

---

## 5. Statistical Methodology Audit

**Implementation inspected directly:** `src/evaluation/metrics.py::paired_bootstrap_macro_f1_diff` (lines 66-103, Phase 3A). Phase 3B's bootstrap code is **not in this repository** — only its output CSVs (`arabic_paired_bootstrap_holm_results.csv`, `english_paired_bootstrap_holm_results.csv`) exist. This asymmetry matters: Phase 3A's statistical methodology is fully auditable from source; Phase 3B's is not, and must be requested/retrieved from whoever ran the Kaggle notebook before manuscript submission, or the methods section can only describe it secondhand (as README_PHASE3B.txt does).

**What the Phase 3A implementation actually does:**
1. Resample test-row **indices** with replacement (n_iterations times), applying the *same* resampled index set to both model A's and model B's predictions and the shared true labels — this correctly preserves pairing (not an unpaired/independent bootstrap).
2. Compute Δmacro-F1 = f1(A) − f1(B) on each resampled set, building an empirical distribution of 2,000 (Phase 3A) differences.
3. Two-sided p-value = `2 × min(P(Δ_boot ≤ 0), P(Δ_boot ≥ 0))` depending on the sign of the *observed* difference — i.e., a **percentile-bootstrap-based hypothesis test**, not a null-centered permutation test.

**Classification: ACCEPTABLE WITH CLARIFICATION — not a critical flaw, but not maximally rigorous either.**

This is a legitimate, widely-used method in the NLP statistical-testing literature — it matches the paired bootstrap procedure popularized by Berg-Kirkpatrick, Burkett & Klein (2012, "An Empirical Investigation of Statistical Significance in NLP," EMNLP) and is one of the methods surveyed favorably by Dror, Baumer, Shlomov & Reichart (2018, "The Hitchhiker's Guide to Testing Statistical Significance in NLP," ACL). It is **not**, however, a formal randomization/permutation test, and the brief's suspicion is technically correct on one specific point: a percentile-bootstrap CI constructed from the *observed* (non-null-shifted) resampling distribution is testing "does the sampling distribution of the observed statistic exclude zero," which is a close but not identical question to "what is the probability of this result under the null hypothesis of no difference" (true permutation tests directly simulate the null by exchanging labels). For the sample sizes here (n=369/388, moderate, not tiny) the two approaches are expected to agree in the great majority of cases, but can diverge for comparisons near the significance boundary — and several of this project's own comparisons (e.g., Phase 3A E1 MARBERT vs. SVM, adjusted p=0.09; Phase 3B English standalone vs. zero-shot, adjusted p=0.10) sit **exactly at that boundary**, which is precisely where the choice of test could matter.

**Multiple-comparison family definition — correctly scoped.** Verified directly in `scripts/evaluate.py` (lines 184-192): Holm correction is applied per `(experiment_id, language)` group, not pooled globally — e.g., Phase 3A's E1/Arabic 6 pairwise comparisons form one family, E2/English's 3 form another. Phase 3B mirrors this (Arabic 6-comparison family, English 3-comparison family, per the separate CSV files). This is a defensible, pre-specifiable family definition and should be stated explicitly as such in the methods section (name the rule: "family = all pairwise model comparisons within one experiment×language cell").

**CI construction**: percentile method (2.5/97.5), standard and acceptable; `bootstrap_macro_f1_ci` correctly declines to compute a CI below n=30 (sensible floor, though somewhat arbitrary — no citation given for why 30 specifically, a minor point).

**Recommendation for the manuscript (not urgent enough to block submission, but should precede camera-ready):**
- **SHOULD DO:** Re-run the handful of boundary-case comparisons (adjusted p in [0.03, 0.15]) with a formal paired permutation/randomization test (shuffle which model's prediction is assigned to each test example under the null, B=10,000) as a robustness cross-check. If the permutation test agrees with the bootstrap test's significant/non-significant calls, state this agreement in the methods section as evidence of robustness. If it disagrees on any boundary case, report both and let the reader see the sensitivity — do not silently pick whichever supports the stronger claim.
- **MUST DO:** State the test's exact mechanics (bootstrap-CI-based, not permutation) in the methods section, with the Berg-Kirkpatrick/Dror citations, so a statistically literate reviewer sees the choice was deliberate and precedented, not naive.
- Phase 3B's statistical code must be retrieved and either included in the repository or its exact mechanics confirmed to match Phase 3A's (same resampling unit, same p-value construction) before claiming the two phases' significance tests are comparable in rigor.

---

## 6. Verification of Stored Statistical Claims

All Arabic and English Holm-adjusted conclusions from the audit brief were checked directly against `results/phase3b_kaggle_gpu/arabic_paired_bootstrap_holm_results.csv` and `english_paired_bootstrap_holm_results.csv` (both files, full contents, read in this audit):

| Comparison | Adjusted p | Brief's expectation | Match? |
|---|---|---|---|
| AR: XLM-R-rerun vs MARBERT-rerun | 0.355 | not significant | ✓ |
| AR: XLM-R-rerun vs Multilingual | 0.101 | not significant | ✓ |
| AR: XLM-R-rerun vs EN→AR zero-shot | 0.033 | significant | ✓ |
| AR: MARBERT-rerun vs Multilingual | 0.906 | not significant | ✓ |
| AR: MARBERT-rerun vs zero-shot | 0.006 | significant | ✓ |
| AR: Multilingual vs zero-shot | <0.001 | significant | ✓ |
| EN: Standalone vs Multilingual | 0.508 | not significant | ✓ |
| EN: Standalone vs zero-shot | 0.100 | not significant | ✓ |
| EN: Multilingual vs zero-shot | 0.007 | significant | ✓ |

**All nine match exactly.** No numerical-superiority-to-statistical-superiority conversion was found anywhere in the documentation I reviewed (`phase3b_report.md`, `known_limitations.md` #23 both state the pattern correctly: only the "beats zero-shot" comparisons survive correction; no claim of "MARBERT beats XLM-R" or similar appears anywhere).

---

## 7. Dataset and Label Validity Audit

**Arabic origin**: Zenodo 17011574 (Saudi tourism, Google Maps, human-annotated κ=0.87) + Zenodo 22061934 (Jordanian restaurants, Google Maps, majority LLM-labeled, redirected to auxiliary use). **English origin**: UCSD/McAuley Google Local, Wyoming+Vermont, rating-derived.

**Matching procedure** (`experimental_dataset_protocol.md` §1): sentiment distribution matched exactly; domain restricted via a category-keyword proxy (tourist attraction/park/museum/historical); review length matched by quartile bin. **NOT matched, and disclosed as such**: geography (Saudi Arabia vs. two small US states) and star-rating distribution (Arabic has none to match against).

**Human vs. rating-derived labels**: cleanly separated by the `label_provenance_policy.md` three-way taxonomy; the binding rule against calling rating-derived or LLM labels "ground truth" is followed consistently everywhere I checked (`model_comparison.csv`'s `test_label_provenance` column explicitly tags English rows `rating_derived_NOT_human_verified`).

**Class imbalance**: Positive dominates (~61% of the Arabic pool); Neutral is the minority class throughout. Natural distributions preserved in val/test (never rebalanced — confirmed by the class-imbalance policy in `configs/training.yaml` and the achieved-not-forced split proportions documented in `decisions.md` D11).

**Duplicate handling / leakage prevention / group-level splitting**: deduplication by normalized-text hash performed before splitting; group-aware splitting by place (Arabic, 42 groups) and business (English, 896 groups) independently re-verified to have zero cross-split group overlap (`decisions.md` D16's adversarial-reviewer confirmation).

**Geographic/domain confound — the single largest validity threat to RQ1/RQ3, correctly identified by the project itself, not by me**: Saudi tourist attractions vs. Wyoming/Vermont general local businesses (parks/museums/historical sites as the closest proxy). This is explicitly named as unresolved in `dataset_audit.md` §7, `decisions.md` D13, and `known_limitations.md` #3/#15.

**English label noise — quantified, not just asserted**: the error analysis found `rating_text_disagreement` responsible for 15-19% of English model errors on its own, and ~50-60% combined with `mixed_sentiment` (`error_analysis.md` §E2). This is a genuine, measured finding, not a generic caveat — it is one of the stronger pieces of evidence in the entire project and should be foregrounded in the manuscript, not buried in limitations.

**Arabic label reliability**: generally strong (κ=0.87 inter-annotator agreement from the source dataset's own paper), but the project's own error analysis found 4 cases (out of 70-79 errors per model) where the reviewing agent's own reading contradicted the gold label (e.g., AR-TOUR-01145, sarcastic "organization less than one star 👍" labeled Positive/Neutral) — a small, disclosed crack, correctly not overstated.

**Comparability between Arabic and English — the core limitation for RQ1 claims**: **confounded by geography, sub-domain, era, label-generation process, and scale simultaneously** (`dataset_audit.md` §7's own words, which this audit independently endorses as accurate, not inflated). 

### What RQ1 can legitimately support
A within-language claim ("this pipeline achieves macro-F1=X on Arabic Google Maps tourism reviews under a human-annotated, resource/compute-constrained [3A] or fully-fine-tuned [3B] setting") is well-supported. A **cross-language** claim ("Arabic is harder/easier than English for this task") is **not** supportable from the matched pools alone — it would conflate language with domain, geography, annotation process, and era. The only data source designed to answer this cleanly (the 766-row matched-protocol manual-validation slice) remains unannotated. **This is the single most important blocking gap for any strong RQ1/RQ3 claim in the eventual manuscript** (see §12).

---

## 8. Error Analysis Audit

Inspected: `docs/error_analysis.md` in full, plus the underlying category-count tables it reports from.

| Claim | Evidence type | Supported? |
|---|---|---|
| "Neutral is the hardest class" | Direct, quantified (per-class F1 in `per_class_results.csv`: 0.167-0.531 range, consistently lowest of 3 classes across every model) | **Observed association, strongly supported.** Not a causal claim — correctly phrased as descriptive throughout the reviewed docs. |
| "Mixed sentiment contributes to errors" | Direct, quantified (35-79% of all categorized errors) | **Observed association, strongly supported.** The project correctly frames this as a task-design property (forcing one label onto genuinely split-sentiment text), not purely a model deficiency — this is the right causal caution. |
| "Rating-text disagreement contributes to English errors" | Direct, quantified (15-19% alone, ~50-60% combined with mixed_sentiment) | **Plausible explanation with strong circumstantial support**, correctly not overstated as proven causation (the error analysis shows *association* between the disagreement pattern and the model's error, which is the right level of claim — it does not and cannot prove the rating-derivation process *caused* each specific model error, only that it correlates heavily with where errors cluster). |
| "Label construction/noise contributes substantially" | Quantified for English (above); for Arabic, 4/70-79 cases — smaller, explicitly described as "small... not overturning the overall label-quality assessment" | **Correctly calibrated — strong claim for English, appropriately modest claim for Arabic.** No overreach found. |

**Causal-language check**: I read every paragraph of `error_analysis.md` specifically hunting for causal overreach and found none — every claim is phrased as "drives," "accounts for," "is dominated by," or "contributes to," never "causes" in a strict sense, and the one place a stronger claim could have been made (code-switching as a driver of the 2 code-switch-diagnostic mismatches) is explicitly walked back: *"No pattern suggests code-switching itself is what drove the two errors — the confound with short/sparse context cannot be ruled out with n=9."* This is exactly the right epistemic hygiene.

**Is the error analysis systematic enough for Q1?** Largely yes for Phase 3A (two independent raters, blind, fixed 13-category taxonomy given in advance, all 327 errors categorized — not a sample). **Gap**: no error analysis exists for Phase 3B's full-fine-tuning predictions at all. For a paper whose headline results will likely be the Phase 3B numbers (they're the strongest), having qualitative error analysis only for the weaker Phase 3A LoRA models is a real asymmetry a reviewer will notice. **Recommend (SHOULD DO, not MUST DO — see §12): run the same error-categorization protocol on at least the Phase 3B standalone-rerun predictions (which do have row-level data) before submission**, so RQ4 has matching evidence for the results the paper will foreground.

---

## 9. Code-Switching Audit

**Verified count: 9**, confirmed directly from `docs/codeswitch_audit.md` §"Final verified result" and cross-checked against `data/annotations/mixed_manual_audit.csv`'s `include_as_real_codeswitch=="yes"` rows (both give 9, with matching review IDs). This was derived via a two-rater blind audit (κ=0.853 overall, κ=0.809 binary) of all 109 heuristic candidates, with 6 disagreements individually arbitrated — a rigorous process for a small number, not a casual guess.

**Where should E6 appear in the manuscript?**

**Recommendation: a short exploratory subsection in the main paper (not supplementary, not removed), explicitly and repeatedly framed as qualitative.**

Reasoning: removing it entirely would hide a genuinely interesting, hard-won negative/null finding — that the Google-Maps-review domain, contrary to what the project initially hoped, contains almost no naturally-occurring code-switching (9 of 1,050,832 documents, ≈0.00086%), and that 84/109 heuristic "hits" turned out to be a platform display artifact (Google's own translation UI), not linguistic code-mixing. **This is itself a contribution** — it corrects a plausible but wrong assumption (that review platforms are a rich natural source of code-switched text) and gives future researchers a concrete reason to look elsewhere (e.g., social media, as EESA and SESA-CSD did) rather than repeating this project's initial approach. Relegating it to supplementary material would bury this finding where it's least likely to inform future work design. However, it must **never** be presented with a quantitative accuracy/F1 number as if it were a benchmark result — the 7/9-correct figure in `error_analysis.md` is explicitly framed as "qualitative, not statistical" and must stay that way; if a reviewer or co-author is tempted to write "the model achieved 78% accuracy on code-switched reviews," that sentence must be deleted, not softened.

---

## 10. Novelty and Contribution Audit

### Strong contributions
- **The negative/corrective code-switching finding** (§9): a concrete, quantified demonstration that the review domain is nearly devoid of naturally-occurring Arabic-English code-switching, overturning a plausible prior assumption and redirecting future data-collection strategy for this specific research question.
- **The rating-derived-label-noise quantification** (§7, §8): a concrete mechanism (`rating_text_disagreement`), not just a generic caveat, showing ~50-60% of English errors trace to label construction rather than model weakness — directly actionable for anyone else using rating-derived sentiment labels.
- **The resource-constrained-vs-full-fine-tuning comparison (Phase 3A vs. 3B)**, correctly and conservatively framed as a multi-factor configuration comparison, not a GPU-causality claim. This is methodologically mature handling of a comparison many papers would mishandle by overclaiming hardware causality.

### Moderate contributions
- MARBERT vs. multilingual XLM-R vs. zero-shot cross-lingual transfer comparison on a matched, documented, frozen Arabic dataset — solid, but the specific finding (nothing beats anything except zero-shot) is a fairly common pattern in cross-lingual transfer literature, not a surprising result in itself.
- The primary-vs-reproducibility-rerun handling (§4) — scientifically careful, genuinely useful as a case study in honest reporting, but it is a *process* contribution (how to handle lost artifacts honestly), not a *scientific* finding about sentiment analysis.
- Class-specific (Neutral) behavioral analysis — real and well-evidenced, but "Neutral is hard in 3-class sentiment" is a widely-replicated finding in the broader sentiment literature, so its novelty here is in the *specific, quantified, bilingual* demonstration, not the general phenomenon.

### Engineering contributions (valuable, but not the paper's scientific core)
- Reproducibility infrastructure (frozen splits, registry, two independent adversarial audits).
- Deployment demonstration (FastAPI + React frontend).
- The LoRA-substitution-under-OOM-constraint engineering story — genuinely interesting as methodology/infrastructure notes, but it is an **engineering constraint**, not a scientific finding, and should be scoped accordingly (see §15).

### Claims that are NOT sufficiently novel and must not be made
- "First Arabic-English code-switched sentiment study" — **false**, the project's own Phase 1 review already corrected this.
- "First Arabic Google Maps sentiment study" — **false**, AraMAMS and the tourism ABSA paper precede it.
- "Transformers outperform classical ML for this task" — **not statistically supported** (§5-6).
- "GPU training caused the improvement" — **explicitly rejected by the project's own framing rule** (§2).
- Any claim that the matched Arabic-English comparison measures a clean language effect — **confounded, pending the unannotated validation slice** (§7).

### What is the strongest publishable story of this paper?

**A controlled, resource-aware study of Arabic-English sentiment classification on a frozen, leak-free, matched (but honestly-disclosed-as-imperfectly-matched) Google Maps review corpus, reporting (a) the multilingual/cross-lingual transfer behavior of MARBERT and XLM-R under two training regimes (resource-constrained LoRA vs. full fine-tuning), with rigorous paired-bootstrap significance testing showing most apparent differences are not statistically significant except cross-lingual zero-shot transfer underperforming in-domain training; (b) a quantified demonstration that rating-derived labels and task-inherent "mixed sentiment" reviews — not model architecture — are the dominant error sources; and (c) a corrective empirical finding that genuine Arabic-English code-switching is nearly absent from this review domain, contradicting an initial design assumption.** This story is honest, defensible, and has at least three genuinely reportable findings (not just "we built a pipeline") — but it requires finishing the manual-validation slice to make its RQ3/cross-language claims clean rather than exploratory (see §12).

---

## 11. Reviewer #2 Attack

| # | Criticism | Severity | Repo evidence already addresses it? | Additional analysis required? | Disclose as limitation? | Recommended fix |
|---|---|---|---|---|---|---|
| 1 | "Arabic and English datasets are not comparable — different geography, domain, annotation process, era, scale." | **Major** | Yes, extensively (`dataset_audit.md` §7, `known_limitations.md` #3/#13/#15) — the project got there first. | Yes — finish the 766-row manual-validation slice (§12, MUST DO). | Yes, already drafted limitations text exists; strengthen with the validation-slice result once available. | Complete the pending annotation before submission, or explicitly downgrade all cross-language claims to "exploratory" in the manuscript (not just the docs). |
| 2 | "English labels are rating-derived, not real sentiment ground truth." | **Major** | Yes — quantified via error analysis (§7/§8), not just asserted. | No additional analysis strictly required; the quantification already exists. | Yes, already disclosed thoroughly. | Keep the `rating_text_disagreement` quantification prominent in the main results, not buried. |
| 3 | "Only 9 genuine code-switched examples — this undermines the project's own stated novelty angle." | **Major** | Yes, extensively and honestly disclosed (§9). | No — the project already concluded quantitative E6 is infeasible and correctly stopped trying. | Yes. | Reframe the paper's novelty claim away from "we evaluate code-switching" toward "we find and explain the near-absence of code-switching in this domain" (a defensible pivot, see §10). |
| 4 | "Phase 3A and Phase 3B are confounded (LoRA vs. full-FT, class weighting, seq length, hardware all changed at once) — you can't isolate what helped." | **Major** | Yes — the project pre-emptively disclaims causal GPU attribution everywhere (§2). | Yes — an ablation isolating one factor at a time would resolve this, but is explicitly a SHOULD/NICE-TO-HAVE, not a blocker, given the honest framing already in place (§12). | Yes, already well-disclosed. | State explicitly in the paper that this is a bundled-configuration comparison; consider one small ablation (e.g., LoRA + weighted loss on the same hardware) if time permits, as the single highest-value addition to resolve this cleanly. |
| 5 | "Two Phase 3B primary predictions were lost — how do we trust the reported numbers at all?" | **Major** | Partially — the rerun-substitution is disclosed in prose (§4) but not yet as an inline table footnote where the numbers themselves are reported. | No new analysis — a documentation fix. | Yes, but make it more prominent (§4 fix #1). | Add the caveat directly to `master_final_results.csv`/its paper-table equivalent, not only to a README. |
| 6 | "The bootstrap significance test is a heuristic, not a formal permutation test." | **Moderate** | Partially — the method is legitimate and precedented (§5) but the manuscript hasn't yet cited the precedent or acknowledged the bootstrap-vs-permutation distinction. | Yes — SHOULD DO a permutation-test cross-check on boundary cases (§5, §12). | Yes, can be disclosed as "bootstrap-CI-based, following Berg-Kirkpatrick et al. 2012" with citation. | Add citations; cross-check boundary-case p-values with a permutation test before camera-ready. |
| 7 | "Test sets are small (n=369/388) — how much power do you really have?" | **Moderate** | Implicitly yes — bootstrap CIs exist and are reasonably wide; the project never claims more precision than the data supports. | No — this is a structural property of the dataset (`dataset_audit.md`'s own scarcity finding, #1), not fixable without new data collection. | Yes. | State test-set size and resulting CI widths explicitly in the methods/results; do not oversell precision. |
| 8 | "Transformer hyperparameters weren't tuned as carefully as the classical baselines (no class-weighting grid search for transformers)." | **Major** | Yes, extensively self-disclosed (`known_limitations.md` #20, Phase 3 report Q8) — this is one of the project's most intellectually honest findings. | Yes — a weighted-loss LoRA run would resolve the ambiguity (§12, SHOULD DO). | Yes, already disclosed clearly. | Run at least one class-weighted LoRA variant before claiming anything about "transformers vs. classical" in the final paper; otherwise frame RQ2's answer as explicitly conditional on this untested factor. |
| 9 | "Class imbalance (Positive-dominant, Neutral-minority) could be inflating apparent accuracy." | **Moderate** | Yes — macro-F1 (not accuracy) is the stated primary metric specifically to address this; per-class F1 is reported; natural distributions preserved in test. | No. | Yes, implicitly handled by metric choice; state explicitly why macro-F1 was chosen. | None needed beyond stating the rationale explicitly in methods. |
| 10 | "No external validation set / no out-of-domain test." | **Moderate** | Partially — HARD, SemEval ABSA, and others were explicitly reserved for exactly this purpose (`dataset_audit.md` §3/§4) but never actually run. | Yes — SHOULD DO, not MUST DO (§12). | Yes if not run. | Run at least one reserved external set (e.g., a small HARD subset) as an out-of-domain robustness check if time permits; otherwise disclose as future work, not a blocking gap. |
| 11 | "Single random seed (42) throughout — no variance estimate across training runs, only across bootstrap resamples of a fixed prediction set." | **Major** | No — not addressed anywhere I found. This is a genuine, currently-undisclosed gap. | Yes — ideally 3-5 seeds per transformer configuration (§12). | Yes, must be added as an explicit limitation if not run. | At minimum, add a sentence to `known_limitations.md` acknowledging single-seed training variance is unmeasured (distinct from the bootstrap resampling variance, which IS measured); if time permits, re-run the cheapest configuration (classical baselines, seconds each) across 3-5 seeds as a cheap partial mitigation. |
| 12 | "Novelty is thin — sentiment analysis + transformers is not new; code-switching barely features in the final story." | **Moderate** | Partially — §10 above already identifies the narrower, defensible novelty angle; the risk is a weak abstract overselling the code-switching angle that the data doesn't support at scale. | No new analysis — a framing/writing decision. | N/A — this is a writing risk, not a data gap. | Write the abstract around the three strong contributions in §10, not around "we study code-switching," which the data cannot support as a headline claim. |
| 13 | "Is the deployment/frontend relevant to a research contribution, or padding?" | **Minor** | See §15 below — addressed directly. | No. | Yes, scope explicitly. | Position deployment as a brief demonstration subsection, not a core contribution (§15). |
| 14 | "6/6 manual sanity-check examples is not evidence of anything statistically meaningful." | **Minor, but must be preempted** | The user's own framing already avoids calling this an accuracy estimate; however, **no repository file documents this check at all** — it exists only in the user's message to me, not in the repo. | No analysis — a documentation gap. | Yes. | Add a one-paragraph note (e.g., in `known_limitations.md` or a short `docs/deployment_verification.md`) explicitly stating this was a 6-example sanity check, not an evaluation, with the examples and outcomes listed, so the claim is traceable to a repository artifact rather than only a chat message. |

---

## 12. Q1-Level Experiment Gap Analysis

| Addition | Classification | Expected scientific value |
|---|---|---|
| Finish the 766-row matched-protocol manual-validation annotation | **MUST DO** | This is the *only* mechanism the project itself designed to make the central RQ3 cross-language claim non-confounded. Without it, every cross-language comparison in the paper must be labeled exploratory — a real ceiling on the paper's strongest possible claim. |
| Inline disclosure of the MARBERT/XLM-R primary-vs-rerun substitution in the actual results table (not just a README) | **MUST DO** | Prevents a reviewer from flagging apparent inconsistency between reported primary scores and the predictions backing the significance tests — cheap to fix, costly if caught by a reviewer instead. |
| Statistical methodology citation + permutation-test cross-check on boundary-case p-values | **SHOULD DO** | Strengthens an already-legitimate method against the specific, foreseeable "is this a real significance test" question (§5, §11#6); low cost, meaningfully de-risks a statistics-literate reviewer's critique. |
| Class-weighted-loss LoRA re-run (at least E1, the cheapest configuration) | **SHOULD DO** | Directly resolves the single largest open confound in the RQ2 "transformers vs. classical" story (§7/§8/§11#8) — currently the honest answer is "we don't know if the gap is architecture or untested class weighting," and this is answerable with one more LoRA run (~45-50 min based on the project's own observed per-run timing). |
| Multiple random seeds (3-5) for at least the cheapest configurations | **SHOULD DO** | Addresses §11#11 — distinguishes training-variance from the already-measured resampling-variance; classical baselines cost seconds per seed, making this cheap for at least a partial mitigation. |
| Error analysis repeated on Phase 3B (full-FT) predictions | **SHOULD DO** | Closes the asymmetry noted in §8 — the paper's likely headline numbers (Phase 3B) currently have no qualitative error analysis behind them at all. |
| LoRA vs. full-FT controlled ablation (same hardware, same class-weighting, same seq-length, only fine-tuning method varied) | **NICE TO HAVE** | Would cleanly answer "did LoRA or full-FT cause the Phase 3A→3B gap," but requires a GPU-capable or memory-adequate environment Phase 3A's own hardware constraint makes infeasible locally — genuinely valuable but not achievable without new compute access, so it cannot be a MUST DO. |
| Max-sequence-length ablation (64 vs. 128) | **NICE TO HAVE** | A real confound (§2) but lower expected payoff than the class-weighting ablation above, since most reviews are short (`methodology_plan.md`'s own word-count percentiles suggest 64 tokens covers the bulk of the distribution already). |
| External dataset validation (HARD, SemEval ABSA — already reserved for this purpose and never used) | **NICE TO HAVE** | Would strengthen generalization claims, but the project never promised this for the core RQs, and reviewer pressure here (§11#10) is moderate, not major. |
| Calibration metrics (e.g., Brier score, reliability diagrams) for the deployed model's confidence scores | **NICE TO HAVE** | Relevant mainly if the deployment/confidence-display aspect is emphasized in the paper (§15 recommends keeping that minimal); low priority if deployment stays a brief demonstration. |
| Additional transformer baselines (AraBERT, CAMeLBERT) | **NOT NECESSARY** | The project already has a documented, literature-grounded rationale for preferring MARBERT over AraBERT (`decisions.md` D6); adding more models without a specific RQ they'd answer would be the "model zoo" the project has explicitly and correctly avoided throughout. |
| LLM-prompting baselines (e.g., GPT-4/Claude zero-shot) | **NOT NECESSARY** | No RQ currently requires this; `research_gap.md` §4 flags it only as an open question for a *future* targeted search, not a gap in the current study's scope. Adding it now would be scope creep, not rigor. |
| Stronger classical baselines (e.g., fastText, gradient-boosted trees on TF-IDF) | **NOT NECESSARY** | TF-IDF+LogReg/SVM already answer RQ2 adequately; marginal additional classical variants would not change the paper's conclusions and risk diluting focus. |
| Domain-specific error analysis beyond what exists | **NOT NECESSARY** | The existing 13-category, two-rater, all-327-rows analysis is already systematic; further subdivision would have diminishing returns relative to the MUST/SHOULD items above. |

---

## 13. Literature Review Readiness

**Inspected:** `docs/research_raw/literature_review_raw.md` (full file, verified via direct source fetches per its own documented methodology, not search-summary-only) and `paper/references/` (empty except `.gitkeep` — **no formal reference-management file exists yet**, e.g. no `.bib` file).

| Area | Covered? | Assessment |
|---|---|---|
| Recent Arabic sentiment-analysis work | Yes | AHaSIS (RANLP 2025), DialectSentEval 2026 shared task, multiple 2023-2025 Saudi-dialect papers — current. |
| Multilingual sentiment literature | Partially | XLM-R, XLM-T, mBERT comparisons noted, but citations are generic ("comparisons exist") rather than a curated, specific multilingual-sentiment-benchmark bibliography — **needs a dedicated pass**. |
| Cross-lingual transfer literature | Thin | The literature review's §3 focuses on multilingual *benchmarks including* Arabic, not specifically on *cross-lingual zero-shot transfer* methodology/theory — this project's own E5 finding (transfer underperforms in-domain training) would benefit from grounding in the broader cross-lingual-transfer-gap literature (e.g., Pires et al., Conneau et al. on cross-lingual transfer mechanisms), which is **not yet searched**. |
| MARBERT/AraBERT/XLM-R foundational work | Yes, well-covered and independently verified | Original papers confirmed via direct ACL Anthology/arXiv fetch (Abdul-Mageed et al. 2021 for ARBERT/MARBERT; Antoun et al. 2020 for AraBERT; Conneau et al. 2020 for XLM-R) — publication-ready as-is. |
| Google review/location review sentiment work | Yes, and unusually rigorous | AraMAMS, the tourism ABSA paper, and several English-language Google Maps sentiment papers all independently verified via DOI resolution — a genuine strength of this project's Phase 1 work. |
| Statistical evaluation methodology literature | **Not covered at all** | No citation anywhere in the repository for the bootstrap/permutation-testing methodology being used (§5). This is a **required fresh search** before manuscript drafting — specifically Berg-Kirkpatrick et al. 2012 and Dror et al. 2018, at minimum, plus whatever the actual Holm-Bonferroni citation convention is in the target venue's house style. |

**Fresh literature search required before drafting, specifically for:**
1. Cross-lingual transfer-learning theory/mechanisms (to ground the E5 zero-shot finding).
2. NLP statistical significance testing methodology (to ground §5's methods section).
3. A supplementary Arabic-language-venue search pass (`known_limitations.md` #11's own flagged gap — not yet done).
4. Recent (2026) work potentially published *after* the original Phase 1 search date that could affect the novelty framing — the field moves fast and the Phase 1 search has an implicit cutoff.

---

## 14. Figures and Tables Plan

| # | Item | Purpose | Data source | Main paper or supplementary |
|---|---|---|---|---|
| 1 | Dataset/split summary table | Ground the reader in exact N's, label provenance, and split sizes before any result is shown | `experimental_dataset_protocol.md`, `final_dataset_statistics.csv` | Main |
| 2 | Experimental design diagram (Phase 3A/3B, E1-E5, data flow) | One visual replacing several paragraphs of "what ran and why" | `configs/experiments.yaml`, this audit's §1-2 | Main |
| 3 | Primary model comparison table (Phase 3A + 3B, both languages, with LoRA/rating-derived/primary-vs-rerun flags inline) | The paper's central results table | `model_comparison.csv` + `master_final_results.csv`, merged | Main |
| 4 | Confusion matrices (best model per language, both phases) | Visualize the Neutral-class collapse concretely | `results/figures/confusion_matrix_*.txt` (already generated) | Main (2 matrices) / rest in Supplementary |
| 5 | Class-level F1 comparison (bar chart, Negative/Neutral/Positive × model × phase) | Makes the Neutral-weakness finding visually unmissable — arguably the single most important chart in the paper | `per_class_results.csv` | Main |
| 6 | Cross-lingual transfer figure (in-domain vs. zero-shot, both directions, both phases) | Visualizes the one consistently-significant finding (§6) | `model_comparison.csv` + `phase3b` zero-shot rows | Main |
| 7 | Statistical effect-size/CI forest plot (all pairwise comparisons, both languages, with significance markers) | Replaces a dense p-value table with one scannable visual; directly supports the "numerical ≠ statistical superiority" message | `significance_tests.json` + Phase 3B Holm CSVs | Main |
| 8 | Error-category taxonomy figure (stacked bar, category × model × language) | Visualizes RQ4's answer | `error_analysis.md`'s category tables | Main |
| 9 | Phase 3A vs. 3B configuration-difference table (not a performance table — a *what-changed* table: LoRA/full-FT, weighting, seq-len, hardware) | Pre-empts the "GPU caused it" misreading before the reader even sees performance numbers | `configs/training.yaml` phase3b_gpu section | Main (place *before* the results table it contextualizes) |
| 10 | Reproducibility/provenance table (seeds, software versions, hardware, data hashes) | Standard Q1 reproducibility appendix content | `experiments/registry.csv`, `requirements.txt`, `configs/models.yaml` | Supplementary |
| 11 | Code-switch diagnostic case table (the 9 examples, qualitative) | Supports §9's exploratory subsection | `codeswitch_diagnostic_final.csv` | Main, but small and explicitly labeled qualitative — could also sit in Supplementary if space-constrained |
| 12 | Primary-vs-reproducibility-rerun comparison table (MARBERT, XLM-R-Arabic) | Supports §4's disclosure requirement directly | `master_final_results.csv` | Main (small table, high transparency value) |

**Avoid redundancy**: do not create both a confusion-matrix figure AND a separate per-class-F1 bar chart for every model — pick the strongest 2-3 confusion matrices (worst and best per-class collapse cases) for the main paper and move the rest to supplementary, since item #5 (the class-level F1 bar chart) already conveys the Neutral-collapse finding more efficiently across *all* models at once than a wall of confusion matrices would.

---

## 15. Deployment and Frontend Positioning

**Strongest defensible positioning: secondary system demonstration, briefly described in a short "Deployment Demonstration" subsection — not a core research contribution, and not relegated to a passing footnote either.**

Reasoning: the deployment model is a *separate* training run (full-FT, optimized for serving, val macro-F1=0.7999539 — aggregate across languages, not the per-language research test figures) explicitly documented as not interchangeable with the research results (`known_limitations.md` #24, `decisions.md` D17). It therefore cannot be presented as evidence *for* the paper's scientific claims. But building and verifying an end-to-end pipeline (model → API → UI, with CORS correctly scoped, error handling verified against a real connection-refused condition, and build/lint/type-checks passing) is genuine engineering work that demonstrates the research is *actionable*, which many Q1 applied-NLP papers do briefly showcase as a "proof the pipeline works end-to-end" paragraph with one architecture figure — this is standard practice in applied-AI/NLP venues and adds credibility without requiring the deployment to carry any evaluative weight.

**Do not report the 6/6 manual sanity-check examples as accuracy, as explicitly instructed — and go further: do not report it as a number at all.** State in prose only: *"The deployed pipeline was manually exercised end-to-end across all three classes in both languages to confirm the API returns well-formed predictions; this is a functional/integration check, not an accuracy evaluation."* Any numeric framing ("6/6", "100%") invites exactly the misreading the brief warns against, even with a disclaimer attached — disclaimers get dropped in citation and conference-talk slides; numbers without a denominator attached get repeated. Also recall this sanity check exists only in the user's message to me, not as a repository artifact (§11#14) — create the one-paragraph record before it's cited in a manuscript, for traceability.

---

## 16. Publication Ethics and Reproducibility

| Item | Status | Action needed |
|---|---|---|
| Dataset licensing | Zenodo 17011574 and 22061934: CC-BY-4.0, independently confirmed via API (`dataset_audit.md` §8). | None — resolved. |
| UCSD/McAuley license | **Unresolved** — no license file found anywhere (`known_limitations.md` #2). | **Must resolve or disclose explicitly in the data-availability statement before submission** — contacting the McAuley Lab was the project's own stated fallback (`decisions.md` D2) and has apparently not yet been attempted. |
| Dataset redistribution | The frozen splits (`data/processed/frozen_v1/`) are derivative of the above sources; redistribution rights inherit from each source's license. | State explicitly in the data-availability section which parts can be redistributed (the CC-BY-4.0 Arabic data, certainly) vs. which cannot pending the UCSD license question. |
| PII | No explicit PII audit found in the repository. Google Maps reviews can contain reviewer names/photos in the raw platform, though the processed datasets here appear to be text-only. | Add a one-sentence statement confirming no PII fields (names, exact locations beyond city-level, photos) were retained in the processed/frozen data — a quick grep-level check, not a deep audit, but currently absent from the documentation. |
| Google review data terms | Addressed for data *sourcing* (no uncontrolled scraping — `decisions.md` D5) but not explicitly for *redistribution* of Google-derived content in a public dataset release accompanying the paper. | Clarify whether the frozen dataset itself will be released, and under what terms, given it derives from Google Maps content via third-party intermediaries. |
| Human annotation disclosure | Clear and thorough — κ values, annotator counts, protocols documented throughout. | None needed. |
| LLM-assisted labels disclosed | Yes, explicitly and consistently (`label_provenance_policy.md`). | None needed. |
| Code availability | Yes — full pipeline in this repository. | Confirm the repository (or a camera-ready-appropriate subset) will actually be made public; state the license for the code itself (none currently declared at the repo root). |
| Model availability | Checkpoints exist locally (`experiments/checkpoints/`, `backend/model/`) but are gitignored (large binaries) — not currently positioned for public release. | Decide and state explicitly whether trained models will be released (e.g., via Hugging Face Hub) or only code+data; if models are Google-Maps-content-derived, factor the UCSD license question into this decision too. |
| Random seeds | seed=42 throughout, logged per run. | None needed, though see §12's multi-seed recommendation. |
| Software versions | Pinned in `requirements.txt` (`torch==2.12.0`, `transformers==4.57.6`, `peft==0.21.2`, etc.) for Phase 3A; **Phase 3B's exact package versions are not recorded anywhere in this repository** (only the GPU/hyperparameter protocol in `configs/training.yaml`). | **Must obtain and record Phase 3B's exact library versions** before a reproducibility statement can honestly cover both phases. |
| Hardware disclosure | Thorough for Phase 3A (RAM/CPU specifics in multiple docs); Phase 3B states "2×Tesla T4" but not more granular Kaggle environment details (CUDA version, driver, etc.). | Minor — add if readily available from the original Kaggle notebook's environment info. |
| Frozen splits | Yes, immutable, hash-verified. | None needed. |
| Experiment configuration | Thoroughly logged for Phase 3A (`experiments/registry.csv`); Phase 3B's configuration is documented in prose (`configs/training.yaml`) but has no equivalent machine-readable per-run registry. | Should add a Phase 3B registry entry (even retrospectively, from the known hyperparameters) for consistency. |
| Reproducibility limitations | Explicitly and honestly disclosed (Phase 3A's OOM-dependent non-determinism, documented in `phase3_report.md` Q19). | None needed — this is a model of how to disclose this kind of limitation. |

---

## 17. Recommended Paper Structure

1. **Introduction** — motivation, the narrow defensible gap (§1), the three RQs (with RQ3's confound caveat stated up front, not discovered mid-paper), explicit non-claims (no "first ever" language).
2. **Related Work** — Arabic sentiment (saturated — brief), English review sentiment (saturated — brief), Arabic transformer baselines (MARBERT/AraBERT/XLM-R — moderate detail, these are the models used), cross-lingual transfer (needs the fresh search from §13), Arabic-English code-switching sentiment (EESA/SwitchEmbed/SESA-CSD — the gap argument lives here), Google Maps/location review sentiment (AraMAMS, tourism ABSA — the domain-gap argument lives here).
3. **Dataset and Problem Formulation** — figure #1/#2 from §14; label provenance taxonomy; the matching procedure and its explicit limits (geography, domain); task definition (3-class, document-level).
4. **Methodology** — preprocessing, frozen split protocol (group-aware, hash-verified), models (classical + MARBERT/XLM-R under both LoRA and full-FT), the Phase 3A/3B configuration-difference table (#9 in §14) placed *here*, before any results.
5. **Experimental Setup** — exact hyperparameters for both phases, the statistical testing procedure (with citations per §13), the family-wise Holm correction definition stated explicitly.
6. **Results** — primary comparison table (#3), confusion matrices (#4), class-level F1 (#5) — RQ1/RQ2's quantitative answers, with every LoRA/rating-derived/primary-vs-rerun flag preserved inline.
7. **Statistical Analysis** — effect-size/CI forest plot (#7), the "numerical ≠ statistical significance" finding as its own clearly-flagged subsection (this project's most statistically mature finding deserves a dedicated space, not a buried paragraph).
8. **Cross-Lingual and Multilingual Analysis** — figure #6, directly answering the "does multilingual/cross-lingual transfer help" question with the one robustly significant pattern in the whole study.
9. **Error Analysis** — figure #8, the Neutral-collapse and rating-noise findings as the chapter's two headline results, explicit observed-association-not-causation framing throughout.
10. **Code-Switching Exploratory Analysis** — short, explicitly qualitative, framed as a corrective/redirective finding (§9/§10), table #11.
11. **Deployment Demonstration** — brief, 1 figure (architecture) + prose only, explicitly scoped as secondary per §15, no numeric "accuracy" framing of the sanity check.
12. **Discussion** — synthesize: what RQ3 can and cannot yet claim (pending the manual-validation slice), the Phase 3A/3B configuration-comparison takeaway, the code-switching redirect, practical implications for anyone building Arabic-English sentiment systems from review platforms.
13. **Limitations** — consolidate the 24 items already in `known_limitations.md`, prioritized (geography/domain confound, rating-derived labels, lost Phase 3B predictions, single-seed training, untested class-weighting-for-transformers, English-venue literature blind spot).
14. **Conclusion** — restated narrow contribution claims only (§10's "strong contributions" list), explicit no-guarantee-of-generalization statement, concrete future-work pointers (finish the validation slice; class-weighted LoRA ablation; multi-seed runs).

This largely matches the brief's suggested structure; the one substantive change is **splitting "Results" from "Statistical Analysis" from "Cross-Lingual Analysis" into three distinct sections** rather than folding statistics into Results generically — given how much of this project's most defensible, least-overclaiming work is specifically *in* the statistical testing (§5-6), it deserves its own visible section rather than being a subsection a skimming reviewer might miss.

---

## 18. Candidate Journal Positioning

Based on the actual contribution profile (§10): this work fits best in venues scoped around **applied/empirical NLP for under-resourced or multilingual settings**, **language resources and evaluation**, or **multilingual/cross-lingual computing** — not a general "intelligent systems" or broad "applied AI" venue, where the specific linguistic/dataset contributions (label-provenance taxonomy, code-switching-domain finding, Arabic-English matched-corpus methodology) would read as too narrowly NLP-specific to be the strongest fit. The statistical-rigor and reproducibility-infrastructure angle (§4-6, §16) would also read well in a venue that explicitly values reproducibility documentation, which several NLP-adjacent journals now do.

I am **not** naming specific journal titles or quartiles — per the brief's own instruction, any such naming requires external verification of current indexing/quartile status that I cannot perform from this repository, and naming journals without that verification risks exactly the kind of unsupported claim this audit exists to prevent.

---

## 19. Final Publication Readiness Scores (0-10)

| Dimension | Score | Justification |
|---|---|---|
| Novelty | 5/10 | The headline angle (code-switched Google Maps reviews) turned out to be nearly unanswerable at scale (9 examples); the project correctly pivoted to a narrower, still-real set of contributions (§10), but the paper's novelty rests more on careful methodology and an honest corrective finding than on a bold new result. Respectable, not groundbreaking. |
| Dataset quality | 6/10 | The Arabic anchor (κ=0.87, exact domain match) is genuinely strong. The English matched pool is honestly caveated but structurally confounded on geography/domain, and its labels are rating-derived. The Jordan dataset's LLM-weak labels and the English pool's unresolved license are real, documented weaknesses, not oversights — scored for what exists, not for the honesty of its disclosure (which is excellent, see Reproducibility). |
| Methodological rigor | 8/10 | Frozen, hash-verified, group-aware, leak-free splits; two independent adversarial audits; explicit label-provenance taxonomy; correct non-causal framing of the Phase 3A/3B comparison. Docked for the untested class-weighting confound in the transformer-vs-classical comparison and the still-unannotated validation slice. |
| Statistical rigor | 7/10 | A legitimate, precedented paired-bootstrap test with correctly-scoped Holm-Bonferroni families (§5-6), and — unusually for a project at this stage — it already surfaces its own "numerical ≠ significant" finding rather than hiding it. Docked because it's a bootstrap-CI-based proxy rather than a formal permutation test, Phase 3B's statistical code isn't in the repository, and there's no multi-seed training-variance estimate. |
| Reproducibility | 8/10 | Exceptional documentation discipline (decision log, two adversarial audits, pinned Phase 3A dependencies, hash-verified data identity). Docked for Phase 3B's missing software-version record and its external, unauditable-from-this-repo statistical code. |
| Experimental completeness | 6/10 | E1-E3, E5 well-covered across both phases; E4 completed only on Phase 3B; E6 correctly scoped down to qualitative; E7/E8 honestly marked not-run. The core matrix is covered, but several "SHOULD DO" items (§12) remain open, and RQ3's clean answer is still pending. |
<br>
| Error analysis | 8/10 | Systematic, two-rater, fixed-taxonomy, all-rows-not-a-sample, explicitly avoids causal overreach. Docked only because it doesn't yet cover Phase 3B's predictions. |
| Writing/documentation readiness | 9/10 | Among the most thoroughly self-documented research repositories I have audited at this stage — every major decision has a dated, evidenced, risk-flagged log entry, and limitations are tracked cumulatively across four project phases rather than written once and forgotten. This is itself a notable strength worth mentioning in a reproducibility-focused cover letter. No manuscript prose exists yet, which is appropriate at this stage and not scored down for. |
| Practical/system contribution | 6/10 | A real, tested, working end-to-end deployment (backend verified, frontend built, CORS/error-handling genuinely exercised) — solid engineering, correctly scoped as secondary (§15) rather than inflated into a core contribution. |
| **Overall Q1 submission readiness** | **5/10** | Strong bones, real unresolved gaps. See verdict below. |

### Final Classification: **READY AFTER MAJOR FIXES**

Not "NOT READY" — the underlying work is honest, mostly rigorous, and has at least three genuinely reportable findings. Not "READY TO DRAFT MANUSCRIPT" or better — because the project's own best mitigation for its central confound (the manual-validation slice) is unfinished, two "MUST DO" documentation fixes exist (§4, §12), Phase 3B's statistical code and software versions are not in the repository, and the untested class-weighting confound currently prevents a clean answer to RQ2. These are fixable in a bounded amount of additional work (not a redesign), which is why this is "major fixes," not "not ready."

---

## 20. Required Final Output

### A. Executive Verdict

- The project's own documentation discipline (decision log, two independent adversarial audits, honest handling of lost predictions and non-significant results) is a genuine strength and should be highlighted, not hidden, in the manuscript's reproducibility statement.
- All numeric claims in the audit brief were independently verified against actual repository files — no discrepancies found anywhere.
- The central scientific risk is RQ3: the cross-language comparison remains confounded, and its only designed fix (the 766-row manual-validation slice) is unannotated.
- The classical-vs-transformer (RQ2) comparison is honestly non-significant after correction, and is further confounded by an untested class-weighting asymmetry that favors classical models by design, not by architecture.
- Phase 3A and Phase 3B are correctly kept separate and correctly never causally attributed to hardware — this is handled better than in many published papers that make exactly this mistake.
- Code-switching data is genuinely scarce (9/1,050,832) — this must be reframed as a corrective finding, not apologized for as a shortfall.
- Two "MUST DO" items are pure documentation fixes (inline rerun-disclosure, deployment sanity-check record) — cheap, should be done immediately regardless of what else happens.
- Phase 3B's statistical-test code and software versions are not in this repository and must be retrieved before the methods section can be written with full confidence.
- No fabrication, leakage, or falsified numbers were found anywhere in this audit.
- Overall: a solid, honestly-run study that is not yet ready to draft, principally because its best answer to its own central research question is still pending, not because of any flaw in what has been done so far.

### B. Critical Issues Before Manuscript

1. Finish (or formally abandon and reframe RQ3 around) the 766-row manual-validation annotation.
2. Add inline primary-vs-rerun disclosure to the actual results table, not only a README.
3. Retrieve Phase 3B's statistical-test source code and exact software/library versions.
4. Resolve or explicitly disclose-as-unresolved the UCSD/McAuley license question before any public data/model release.
5. Document the 6-example deployment sanity check as a repository artifact (currently exists only in chat).

### C. Recommended Additional Analyses (prioritized)

1. **MUST DO** — Complete the manual-validation slice annotation (§12).
2. **SHOULD DO** — Class-weighted LoRA re-run for E1 at minimum (resolves the RQ2 confound cheaply).
3. **SHOULD DO** — Permutation-test cross-check on boundary-case (p≈0.03-0.15) comparisons.
4. **SHOULD DO** — Error analysis repeated on Phase 3B predictions.
5. **SHOULD DO** — Multi-seed runs (3-5 seeds) at least for the classical baselines.
6. **NICE TO HAVE** — LoRA-vs-full-FT controlled ablation, external-dataset validation, max-length ablation.

### D. Claims We CAN Make

- "On a frozen, leak-free, human-annotated Arabic review test set, [best model] achieves macro-F1=X, with Y% [non]-significant difference from [other model] after Holm-Bonferroni correction."
- "Zero-shot cross-lingual transfer significantly underperforms in-domain/multilingual training in both directions (p<0.05 after correction)."
- "Neutral is consistently the hardest class to predict across every model and both languages, with per-class F1 gaps of 0.2-0.3+ between classical and transformer models."
- "Rating-derived sentiment labels introduce measurable, quantified noise (~50-60% of English model errors trace to rating-text disagreement), independent of model architecture."
- "Genuine Arabic-English code-switching is nearly absent (9 of 1,050,832 documents) in this Google Maps review domain, contradicting an initial assumption that motivated this study's design."
- "A LoRA-adapted, resource-constrained training configuration and a full-fine-tuning GPU configuration produce different results on the same frozen data, but the specific cause (fine-tuning method, class weighting, or sequence length) was not isolated via controlled ablation."
- "A working end-to-end Arabic-English sentiment classification pipeline was built and functionally verified (not benchmarked) via a FastAPI backend and web frontend."

### E. Claims We MUST NOT Make

- "First Arabic-English code-switched sentiment study" or any "first" framing for Arabic Google Maps sentiment work.
- "Transformers outperform classical ML" or vice versa, as a general claim (the difference is not statistically significant).
- "GPU training caused the performance improvement" — multiple factors changed simultaneously.
- "Arabic is harder/easier than English for sentiment classification" — the comparison is confounded by geography, domain, and label provenance.
- Any numeric accuracy framing of the 6-example deployment sanity check.
- Any citation of "ArEnSA" as a real dataset (flagged as unverifiable since Phase 1).
- Any claim of guaranteed publication, Q1 acceptance, or specific journal quartile.

### F. Recommended Paper Story

*This study presents a controlled, resource-aware investigation of Arabic-English sentiment classification on a frozen, hash-verified, leak-checked Google Maps review corpus, comparing classical baselines against MARBERT and XLM-RoBERTa under two training regimes — a resource-constrained LoRA-adapted setting and a fully fine-tuned GPU setting — with rigorous paired-bootstrap, Holm-corrected significance testing throughout. We find that apparent performance differences among strong models are largely not statistically significant, while cross-lingual zero-shot transfer reliably and significantly underperforms in-domain or multilingual training in both directions. Systematic, two-rater error analysis identifies task-inherent mixed-sentiment reviews and rating-derived label noise — not model architecture — as the dominant sources of classification error, with the latter accounting for roughly half of all English-language errors. Finally, in pursuing a code-switching-focused research angle, we find that genuine Arabic-English code-switching is nearly absent from this review domain (9 of over one million documents), a corrective empirical finding that redirects where future Arabic-English code-switched sentiment resources should actually be collected.*

*The paper's credibility rests less on a single bold result than on the discipline of its negative and null findings — what doesn't hold up (code-switching at scale, most model-vs-model comparisons, a clean cross-language causal claim) is reported as plainly as what does, and every confound the data cannot resolve is named rather than argued away.*

### G. Next Action

**Before drafting any manuscript text:** (1) make the explicit, bounded decision of whether to invest the time to complete the manual-validation annotation (the single highest-leverage remaining task) or to formally reframe RQ3 as permanently exploratory and write the paper around that constraint instead — this decision determines how section 3/discussion can be written and should be made first, before anything else; (2) in parallel, apply the two cheap documentation fixes (§B items 2 and 5); (3) retrieve Phase 3B's statistical code and software versions from wherever the Kaggle work was run; (4) only after those three things, decide which SHOULD-DO analyses (§C) are worth the remaining time budget before drafting begins.

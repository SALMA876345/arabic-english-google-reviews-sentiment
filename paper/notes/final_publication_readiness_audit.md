# Final Publication-Readiness Scientific Audit

**Role:** Highly critical reviewer for a strong NLP/applied-AI journal. **Goal:** find what could still cause rejection, not reassure.
**Scope:** Entire project through the Human-Gold evaluation phase (`results/human_gold_evaluation/`). No results modified; no new experiments run.
**Supersedes:** `paper/notes/publication_readiness_audit.md` (2026-10-26), which pre-dates the completed 3-annotator + adjudicator Human-Gold study and is now out of date on RQ3 (it correctly flagged the matched-protocol slice as "still unannotated" -- that gap is now closed, with new findings that change the recommended framing below). That file is left in place as a historical record, not deleted.

---

## 1. The central scientific story -- what should this paper actually claim to be?

**Verdict: (D) a combination, but not an equal-weighted one.** The evidence no longer supports leading with (A) Arabic-English model comparison or (B) multilingual modeling as the headline contribution. It strongly supports leading with **(C) evaluation-label reliability and its effect on model conclusions**, with (B) multilingual/cross-lingual modeling under resource constraints as a well-supported secondary thread, and (A) demoted to background/descriptive material only.

**Why not (A):** RQ3's own design doc (`known_limitations.md` #3) and this audit's own re-confirmation (Section 8 below) establish that any Arabic-vs-English *performance* comparison is confounded by geography, domain, source, and label-construction history. Human validation (the 3-annotator + adjudicator study) improves label *quality* on both sides but does not and cannot remove this confound. A paper centered on "Arabic vs. English" invites exactly the rejection this audit is designed to anticipate.

**Why not (B) alone:** Multilingual-vs-monolingual (E4) is a real, clean-ish comparison (Phase 3B at least holds max_seq_length/epochs/loss constant across standalone and multilingual runs), but the result itself is a null result in both labelings (no significant difference, Section 2/5 below) -- a legitimate but modest finding, not enough to anchor a paper alone.

**Why (C):** this is the strongest, cleanest, most novel finding in the whole project, and it did not exist in the pre-Human-Gold version of this work:
- A well-powered (757 reviews), well-documented (3 independent annotators, Fleiss' κ=0.650, blinded 4th-adjudicator resolution of all 179 disagreements) human-validation study.
- A striking, specific, reproducible empirical result: **82.9% of originally-Neutral-labeled reviews were revised away from Neutral under independent human adjudication** (89.3% Arabic, 77.1% English), while Positive/Negative labels were revised only 3.3%/11.1% of the time.
- A direct demonstration that this label unreliability **changes scientific conclusions**: 3 of 4 previously-significant model comparisons lose significance under Human-Gold re-evaluation, only 1 survives, and 1 previously non-significant comparison becomes significant [corrected 2026-10-27 from an earlier "2 of 4" miscount; verified against `results/human_gold_evaluation/statistical_tests_human_gold.csv`]; Phase 3B's apparent dominance over Phase 3A shrinks or reverses in Arabic (mean macro-F1 delta -0.146 vs. -0.040); mean Neutral-F1 across 16 models falls further (0.396->0.176).
- This contribution does **not** depend on resolving the Arabic/English confound, is self-contained, and is exactly the kind of "don't trust your eval labels" finding that NLP/applied-AI venues reward when it is this well-instrumented.

**Recommended framing:** *"How reliable are the evaluation labels behind reported sentiment-classification results, and how much does that reliability affect the scientific conclusions drawn from a bilingual (Arabic-English) review sentiment benchmark?"* -- with the Arabic-English multilingual experiments serving as the concrete testbed for that question, not as a destination claim in themselves.

---

## 2. Claim table

| # | Proposed claim | Supporting evidence | Statistical support | Limitations/confounds | Status |
|---|---|---|---|---|---|
| 1 | Neutral is the hardest class | Lowest per-class F1 under both original labels (mean 0.396) and Human-Gold (mean 0.176), across every one of 16 models, both languages | Descriptive (mean F1 across models); no formal test comparing Neutral-F1 vs. other classes with a CI; Human-Gold Neutral support is tiny (Arabic n=9, English n=33) | Severe class imbalance; annotation-boundary instability (82.9% revision rate) could itself partly explain the low observed F1 (noisy/rare class is intrinsically hard to score, independent of model quality) | **SAFE WITH QUALIFICATION** -- see Section 3 for exact wording |
| 2 | Multilingual training (E4) is competitive with monolingual training | Phase 3B: E4 vs. standalone not significant in either language, both before and after Human-Gold | Paired permutation test, Holm-corrected, n=369/388 | Only 2 comparisons total (1 per language); "competitive" = "not significantly different," not "equivalent" -- absence of significance is not evidence of equivalence at this n | **SAFE WITH QUALIFICATION** |
| 3 | Zero-shot cross-lingual transfer underperforms in-language/multilingual training | True under original labels (3/4 significant comparisons); weakens sharply under Human-Gold (1/4 remain significant) | Paired permutation test, Holm-corrected | Zero-shot is still numerically weakest/near-weakest in most rankings even where not significant -- a real but now much more modest effect | **SAFE WITH QUALIFICATION** (must state the pre/post-Human-Gold change explicitly, not just the original-label number) |
| 4 | Classical ML (TF-IDF) is competitive with or beats transformers | True numerically under original labels (not significant after correction); becomes *more* defensible under Human-Gold in Arabic (TF-IDF beats 2 of 3 Phase 3B transformers) | Paired permutation/bootstrap, Holm-corrected; non-significant in Phase 3A comparisons both before/after | Confounded by the untested transformer class-weighting gap (`known_limitations.md` #20) -- Phase 3A transformers never had class-weighted loss tried, so this is not a clean "classical > transformer" architecture claim | **SAFE WITH QUALIFICATION**, framed as "not significantly different / numerically competitive," never "beats" |
| 5 | LoRA underperforms full fine-tuning | True under original labels for every Phase 3A-vs-3B pair; **the gap shrinks or reverses under Human-Gold**, especially in Arabic, where several LoRA models now numerically outscore 2-3 Phase 3B full-FT models | No same-realization paired test exists across phases (different training configs + unmatched realizations) -- see Section 5/6 | Phase 3A and 3B differ in fine-tuning method, class weighting, and max_seq_length simultaneously; never isolated | **TOO STRONG as currently sometimes implied; SAFE only as "the LoRA-vs-full-FT gap observed under original labels is not fully explained by capacity alone -- it narrows substantially once labels are human-validated"** |
| 6 | Arabic sentiment classification is harder than English (or vice versa) | Not tested; explicitly disclaimed throughout this project | N/A -- RQ3 is observational/confounded by design | Geography, domain, source, label-construction history all differ simultaneously | **REMOVE** as a direct claim; **SAFE** only as "the two language sub-corpora are not performance-comparable due to compounding confounds" (a methods-section statement, not a results claim) |
| 7 | Label-quality (rating-derived vs. human-annotated) materially affects reported model performance | Mean macro-F1 drop of -0.101 (Phase 3B) vs. -0.025 (Phase 3A) when re-scored against Human-Gold; concentrated in the Neutral class | Descriptive, backed by the full before/after metrics table (16 models) | Not a controlled ablation across phases; the *size* of the effect differs by training track for reasons not isolated (could be fine-tuning method, could be degree of fit to the noisy label, could be both) | **SAFE WITH QUALIFICATION** -- this is the strongest claim in the paper; state the number, do not speculate on the mechanism beyond what Section 3's per-class breakdown shows |
| 8 | Human annotation reliability was high / human annotators agreed well | Fleiss' κ=0.650 (757 reviews, 3 raters), 76.4% unanimous | Standard inter-rater statistic, computed and independently reproduced | κ=0.650 is "substantial," not "near-perfect," by Landis & Koch bands; the *mixed-sentiment* secondary flag was unreliable (κ=0.269) and was correctly dropped from downstream use | **SAFE**, provided "substantial agreement" language is used, not "high" or "near-perfect" |
| 9 | Model rankings changed materially after Human-Gold re-evaluation | Documented reordering, especially Arabic (GPU models fall from top-3 to mid/bottom) | Descriptive + the 2-of-4 significance reversals above | Some reordered comparisons mix primary and rerun realizations (Section 6) -- the ranking-change claim itself is robust, but any specific pairwise reordering involving a rerun model must say so | **SAFE WITH QUALIFICATION** -- always name which realization (primary/rerun) is being discussed |
| 10 | Rating-derived labels (English) are measurably less reliable than the single-pass Arabic human annotation | English disagreement-with-Human-Gold rate (18.8%) is slightly higher than Arabic's (16.0%); both are dominated by the same Neutral-revision pattern | Descriptive only, small language gap (16.0% vs 18.8%), not tested for significance | The "single-pass Arabic human annotation" that served as the *original* label is itself a single annotator's work from an earlier phase, of unknown individual reliability -- it was never itself validated the way Human-Gold now is | **SAFE WITH QUALIFICATION** -- the gap between languages is small and undramatic; do not oversell it |
| 11 | Code-switching is empirically rare in this corpus (9/1,050,832 ≈ 0.00086%) | Exhaustive manual 2-rater audit of all 109 heuristic-flagged candidates, κ=0.809 (binary) | Strong inter-rater reliability on the audit itself; but n=9 final count has no CI/test of its own (a count, not a rate estimated from a sample) | The audit covers only documents the heuristic flagged in the first place -- a different/looser heuristic could in principle catch cases this one missed (though the audit's root-cause finding suggests the opposite risk, over-counting, is more likely) | **SAFE** as a dataset-audit finding; **REMOVE** any version of this claim that implies anything about model *performance* on code-switched text (n=9 cannot support that) |

---

## 3. The Neutral finding -- careful audit

**Empirical observation (defensible, state exactly this):** "Across all 16 evaluated model/dataset combinations, Neutral obtained the lowest per-class F1 of the three sentiment classes, both when scored against the original evaluation labels (mean F1=0.396) and, more sharply, when re-scored against the human-adjudicated Human-Gold reference set (mean F1=0.176)."

**Interpretation (defensible with explicit hedging):** "This pattern is consistent with Neutral being the class where sentiment judgment is genuinely least stable -- it is also the class with by far the highest rate of label revision under independent human adjudication (82.9% of originally-Neutral reviews), and the class for which the original three annotators' own agreement was weakest within the annotation study itself."

**What must NOT be claimed (causal explanation):** Do not write that models "struggle with Neutral because Neutral sentiment is inherently ambiguous" or "because Neutral is a harder linguistic phenomenon" as a settled fact. The data support an *association* between (a) low annotator/adjudicator agreement on Neutral and (b) low model F1 on Neutral -- not a demonstrated causal mechanism. It is equally consistent with the explanation that Neutral's low F1 is substantially a *measurement* artifact of class rarity and boundary instability, not a *modeling* failure at all.

**On the small-n concern specifically:** Arabic Human-Gold Neutral support is n=9. Any Arabic-specific Neutral-F1 number (e.g. `E1_marbert_lora`: Neutral F1=0.000 on Arabic) is based on so few examples that a single misclassification swings it by ~11 percentage points -- **this number must be reported with its support count attached every time it is cited**, and should not be used alone to rank models. The English Human-Gold Neutral support (n=33) is more usable but still small by conventional standards for a per-class F1.

**Recommended manuscript wording:**
> "Neutral was the lowest-performing class for every evaluated model, under both the original evaluation labels and the human-adjudicated reference set (mean per-class F1 0.40 and 0.18 respectively; Arabic Neutral support n=9, English n=33). This finding should be read alongside the annotation study's own results: Neutral was also the class most frequently revised during independent human adjudication (82.9% of originally-Neutral-labeled reviews were reassigned to Positive or Negative). We interpret this as evidence that Neutral sentiment is difficult to pin down reliably by annotators and models alike in this domain, rather than evidence of a specific modeling deficiency; we do not have a controlled design that isolates *why* Neutral is unstable (e.g., genuine linguistic ambiguity vs. annotation-guideline boundary placement vs. class rarity)."

---

## 4. Human-Gold methodology audit

**Strengths:**
- Three independent annotators, documented blinding (no cross-visibility, no rating/original-label/model exposure), Fleiss' κ, Krippendorff's α, and pairwise Cohen's κ all computed and independently reproduced against the user-supplied preliminary figures (exact match).
- A pre-registered adjudication protocol (`ADJUDICATION_PROTOCOL.md`) that explicitly rejects automatic majority-vote-as-gold, justified by the independently low mixed-sentiment κ (0.269) -- this is good practice and should be cited as such.
- The 4th adjudicator was blinded to annotator identity, vote counts, majority outcome, original/rating-derived label, rating, and model prediction -- verified programmatically (column-set assertions + full-text forbidden-term scan), not just asserted.
- Full provenance chain: SHA-256 hashes at every handoff point (raw annotator files, adjudication export, merged file, final Human-Gold file), re-verified multiple times across this conversation.
- Three-way distinction (original annotator labels / majority vote / adjudicated label) preserved as separate columns throughout, never collapsed.

**Weaknesses (must be disclosed in the manuscript, not hidden):**
- **Single adjudicator.** All 179 disagreement cases were resolved by one person. There is no second adjudicator and no adjudicator-vs-adjudicator reliability statistic. If that one adjudicator has an idiosyncratic bias (e.g., toward resolving ambiguous cases as Negative), it propagates into 23.6% of the entire Human-Gold set uncontested. This is the single largest methodological weakness of the Human-Gold construction.
- **The adjudicator agreed with the pre-existing 2/3 majority only 62.7% of the time** (and only 26.5% of the time when the majority was specifically Neutral) -- this is informative (it is the whole point of not defaulting to majority vote) but also means the adjudicator is doing a lot of independent "overruling," which increases the stakes of weakness #1.
- The original annotators' Fleiss' κ=0.650 is "substantial" but not "almost perfect" (Landis & Koch); some residual unreliability is baked into even the 578 "unanimous" rows' *boundary* cases that happened to land on 3/3 agreement by chance at a 0.65-κ base rate -- this is a standard limitation of any annotation study and should be named, not treated as if unanimous=flawless.
- No formal check of adjudicator *consistency* (e.g., no repeated/duplicate cases re-shown to the same adjudicator to measure self-agreement).

**Naming recommendation:** Prefer **"human-adjudicated reference set"** (or "Human-Gold reference set," explicitly defined at first use with the disclaimer already present in `README.md`) over bare **"Human-Gold"** or any phrase implying infallibility. "Human-Gold" alone, used repeatedly without qualification in a manuscript, reads to a reviewer as an overclaim of ground-truth status; "human-adjudicated reference set" is accurate, conservative, and still allows "Human-Gold" as a defined shorthand after the first full statement, e.g.: *"...a human-adjudicated reference set (hereafter 'Human-Gold', following [convention]; not claimed to be an infallible ground truth -- see Limitations)."*

---

## 5. Statistical analysis audit

- **Pairing is genuine.** `04_statistical_tests.py` merges each model pair's saved predictions by `review_id` before extracting arrays, with an explicit assertion that both models' Human-Gold truth columns agree post-merge -- this correctly guards against silent misalignment from differing row orders in the source prediction files (a real risk that was checked, not assumed).
- **The permutation test is appropriate for Macro-F1.** Swapping which model's prediction occupies "slot A" vs. "slot B" per row under the null of exchangeability, holding the true label fixed, is a standard generalization of the paired sign-flip permutation test to a non-additive multiclass statistic (Macro-F1 cannot be meaningfully permuted at the per-row level the way an additive loss could, so the row-level "whose prediction is this" swap is the correct granularity). Add-one-smoothed p-value formula is standard and correctly implemented.
- **The bootstrap CI implementation is a resampling CI, not a permutation test**, and this phase's own documentation (`README_PROVENANCE.md`) correctly refuses to call it one -- this is the single specific methodological correction the current project instructions asked for, and it was applied.
- **Seeds and iteration counts are adequate and recorded**: seed=42 throughout, 10,000 iterations for both the bootstrap CI and the permutation test (up from 2,000 in the original Phase 3A/3B significance testing -- an improvement, should be noted as such, not silently treated as if it were always 10,000).
- **Holm families are scientifically justified** and mirror the pre-Human-Gold pairing structure exactly (Phase3A_Arabic_E1, Phase3A_English_E2, Phase3B_Arabic, Phase3B_English) -- correct, because it keeps Phase 3A and Phase 3B as separate correction families (consistent with the project's standing rule never to merge the two tracks) and allows a clean before/after read on the *same* comparisons.
- **No inappropriate realization-mixing was found in the significance tests themselves**: every pairwise comparison in `statistical_tests_human_gold.csv` is within a single phase/track, and the rerun-vs-primary distinction for the two lost Arabic MARBERT/XLM-R primaries is preserved (`realization` column, `RERUN_REALIZATION_not_primary` label) -- verified by direct inspection, not just by description.

**What should be rerun or removed:** Nothing in the implemented statistical tests needs to be rerun; the method is sound. **One thing should be added, not removed**, before manuscript submission: a direct statement in the methods section (not just the code comments) that the bootstrap-heuristic p-value and the permutation p-value are reported side by side deliberately, and that the permutation p-value is the one that should be treated as the primary significance result, with the bootstrap figure retained only for the CI and for continuity with the pre-Human-Gold Phase 3A/3B methodology.

---

## 6. Model-ranking claims audit

- **Directly comparable rankings (same realization on both sides of history):** Phase 3A's 4 Arabic models and 3 English models (all are each model's one-and-only realization, LoRA laptop); Phase 3B's `E4_multilingual`, `E5A/E5B` zero-shot, and `E2_xlmr_fullft` (English standalone, which never lost its primary) -- these rankings, before and after Human-Gold, are a clean apples-to-apples comparison.
- **Rankings involving a rerun realization:** any ranking position occupied by `E1_xlmr_fullft` or `E1_marbert_fullft` (both reruns, Arabic) must be reported as "the rerun realization ranked Nth," never silently as "XLM-R/MARBERT ranked Nth" without the qualifier -- the original primary MARBERT (0.785025) and XLM-R (0.740295) scores are higher than their reruns (0.765263, 0.740126) under original labels, and **no Human-Gold figure exists for the lost primaries at all** -- it is unknown, and must stay stated as unknown, whether the primary realizations would rank the same way under Human-Gold that their reruns do. This is a real gap in the ranking story, not a cosmetic one.
- **Rankings that should not be emphasized:** any single-position ranking swap driven by a sub-0.01 macro-F1 margin (e.g. English top-2 swapping by 0.006) should be described as "statistically indistinguishable, numerically reordered," not narrated as a finding in its own right.
- **Is ranking instability itself a defensible result?** Yes -- and this is arguably the paper's best figure/table candidate: showing the *same* models, *same* test rows, two different evaluation-label sources, and a materially different leaderboard (especially Arabic) is a clean, reviewer-legible demonstration of the central (C)-framing contribution from Section 1. This should be presented explicitly as "ranking instability under label-reliability change" as a *result*, not buried as an incidental observation.

---

## 7. Phase 3A vs. Phase 3B interpretation audit

**Verified: no causal GPU attribution exists anywhere in the current documentation** (`configs/training.yaml`'s `non_causal_framing_requirement`, `known_limitations.md` #21, `decisions.md` D17, and this audit's own Section 1/6 above all state the bundle-of-changes framing consistently). This is already correct and should be preserved verbatim into the manuscript.

**Exact safe language (reuse, do not rephrase into something causal):**
> "Phase 3A (laptop) and Phase 3B (Kaggle GPU) differ in fine-tuning method (LoRA vs. full fine-tuning), class-weighting (unweighted vs. weighted loss), maximum sequence length (64 vs. 128 tokens), and hardware, all changed simultaneously. Any score difference between the two tracks reflects this bundled configuration change and must not be attributed to any single factor, including hardware."

**All Phase 3A-vs-3B comparisons should remain descriptive-only in the manuscript** -- no inferential statistic should be computed comparing a Phase 3A run directly against a Phase 3B run (the current project correctly does not do this; the statistical tests in `results/human_gold_evaluation/` keep the two tracks in separate families, per Section 5 above). This should be stated as an explicit methods-section rule, not left implicit.

**One addition recommended:** the manuscript should name the specific, now-quantified consequence of this bundling that the Human-Gold phase surfaced -- Phase 3B's larger apparent gains over Phase 3A shrink disproportionately under Human-Gold (Arabic mean delta -0.146 vs. -0.040) -- and should state plainly that this pattern is *consistent with* Phase 3B's bundled configuration (e.g., weighted loss, longer sequences) having fit the noisier original labels (especially the inflated Neutral class) more closely, without asserting that this is the confirmed mechanism, since the ablation to isolate it was never run.

---

## 8. RQ3 / Arabic-English comparison audit

**Recommendation: RQ3 should become descriptive only; it should not be removed outright, because the confound analysis and the human-validation study are themselves a legitimate, reportable contribution, just not a "which language is harder" contribution.**

Reasoning: the Human-Gold study improves *label quality* symmetrically in both languages (both got the identical 3-annotator + blind-adjudicator protocol), but it does nothing to equalize geography (Saudi tourism sites vs. US Wyoming/Vermont attractions), domain match, collection era, or the upstream difference in how the *original* labels were constructed (single-pass human annotation for Arabic vs. rating-derived heuristic for English) -- all pre-existing, independently documented confounds (`known_limitations.md` #3, #15; `decisions.md` D13). A reviewer will immediately ask "did you control for domain/geography?" and the honest answer remains no.

**What RQ3 can now legitimately claim (reframed):** "We find that human-validated reference labels change the measured Arabic/English performance picture for several models, particularly in Arabic, where the original labels appear to have been less reliable for the Neutral class specifically. We do not interpret this as evidence that Arabic sentiment classification is intrinsically harder than English; the two sub-corpora differ in geography, domain, and original label-construction method, any of which could independently explain the differential sensitivity to relabeling."

**What RQ3 must not claim:** any sentence of the shape "Arabic is harder/easier than English" or "the Arabic model generalizes worse/better than the English model," full stop, with or without a hedge bolted on afterward. Hedges do not fix a structurally confounded comparison; they only disclose it.

---

## 9. Code-switching claim audit

**Strongest defensible contribution: a measurement-methodology finding, not a sentiment-modeling finding.** The real, reportable result is: a naive script-mixing heuristic flagged 109 candidate documents, but exhaustive two-rater blind manual audit (κ=0.809 binary) found that **77.1% of those candidates were a Google Maps UI display artifact** (a translation shown alongside its original, not organic code-switching), leaving only 9 genuine code-switched reviews (≈0.00086% of the corpus). This is a legitimate, citable dataset-audit/methodology contribution: it demonstrates that a common, cheap code-switch-detection heuristic can be dominated by platform display artifacts rather than genuine bilingual production, in this domain.

**What must not be claimed:** any accuracy, F1, or other performance number computed on the 9 genuine examples as if it were a model-evaluation result. n=9 supports no train/test split, no confidence interval, no significance test, and the project's own documentation already says this correctly (`codeswitch_audit.md`: "far too small for any statistically meaningful standalone model comparison... NOT feasible as a quantitative experiment"). This audit confirms that framing is correct and must be preserved unchanged into the manuscript -- the 9 examples belong only in a qualitative case-study subsection or appendix, illustrating phenomena, never in a results table with a metric column.

---

## 10. Reproducibility audit

| Item | Status |
|---|---|
| Python version | **MISSING.** No `.python-version`, `runtime.txt`, or explicit statement of the Python version used for Phase 3A/3B anywhere in the repo. |
| PyTorch version | Pinned for Phase 3A/local (`torch==2.12.0`, CPU build, in `requirements.txt`). **MISSING for Phase 3B** (Kaggle notebook environment version never recorded). |
| Transformers version | Pinned for Phase 3A/local (`transformers==4.57.6`). **MISSING for Phase 3B.** |
| scikit-learn / NumPy / Pandas | Pinned (`requirements.txt`; also independently confirmed live in this audit: pandas 2.2.3, numpy 2.4.4, sklearn 1.7.2, scipy 1.17.1). |
| CUDA environment | Hardware named ("2x Tesla T4 GPUs (Kaggle)," `configs/training.yaml`) but **no CUDA/driver/cuDNN version recorded.** |
| Hardware | Phase 3A: "8.3GB RAM, CPU-only" (`decisions.md` D14) -- no CPU model named. Phase 3B: GPU model named, no further detail. |
| Random seeds | **Present and thorough**: seed=42 pervasive (training, bootstrap, permutation); annotation seeds 1001/2002/3003; adjudication seed 9009 -- all distinct and documented. |
| Model identifiers | **Present**: HF model IDs in `configs/models.yaml` (`UBC-NLP/MARBERT`, `FacebookAI/xlm-roberta-base`). |
| Dataset versions | Zenodo record IDs given (17011574, 22061934) functioning as de facto stable identifiers; UCSD/McAuley named as "2021 release" but **no explicit URL/DOI recorded in the docs reviewed**. |
| Dataset URLs/DOIs | **Partially missing** -- Zenodo IDs are DOI-resolvable in principle (10.5281/zenodo.XXXXXXX) but the manuscript-ready DOI strings were not found written out anywhere; UCSD/McAuley has no DOI/URL on file. |
| Split IDs/hashes | **Present**: `data/splits/frozen_v1/manifest.json`, MD5 cross-check against the Kaggle input bundle documented in `decisions.md` D17. |
| Human-Gold hash | **Present and repeatedly re-verified**: SHA-256 `7b53ca621d2...be53fd`, checked at the start of every downstream script. |
| Prediction artifacts | **Present**: all referenced in `results/predictions/` and `results/phase3b_kaggle_gpu/`, verified for exact ID coverage in this and the prior phase. |
| Training configuration | **Present**: `configs/training.yaml`, `configs/models.yaml`, `configs/experiments.yaml`. |
| Evaluation / statistical scripts | **Present**: `scripts/evaluate.py`, `src/evaluation/metrics.py`, and the full `results/human_gold_evaluation/0{1-6}_*.py` suite. |

**Action required before submission:** record the exact Python/PyTorch/Transformers/CUDA versions used in the Kaggle Phase 3B notebook (if the notebook or its output log still exists, extract from there; if not, this must be disclosed as an unrecorded-environment limitation, not silently left blank), and write out the full resolvable DOI/URL for every dataset (Zenodo DOIs, and the specific UCSD/McAuley page/version used) in one place (recommend a new `docs/data_availability.md`).

---

## 11. Licensing and release audit

**Status, re-confirmed, unchanged from `known_limitations.md` #2 and #7 and `decisions.md` D2: the UCSD/McAuley Google Local Review Dataset has no confirmed license.** This audit does not invent one. Distinguishing the five release scenarios explicitly:

| Activity | Status |
|---|---|
| Using the UCSD/McAuley data for internal research (training/evaluating models, as done here) | Generally accepted practice for academic datasets shared this way, consistent with the McAuley Lab's own stated public stance ("cite our papers, use at your own judgment") -- **acceptable to continue**, not a release action. |
| Redistributing raw UCSD/McAuley review text (e.g., in a public repo, a paper appendix, or a released dataset file) | **Not authorized.** No license permits redistribution; this must not be done. |
| Releasing derived review_ids / split membership lists for the English portion | Lower risk than raw text but still references the underlying dataset's structure; **recommend treating as not authorized for public release either**, absent explicit permission, since it could allow reconstruction of the original record mapping. |
| Releasing Human-Gold annotations (sentiment labels) keyed to English review_ids, without the review text itself | Labels alone (no text) are the project's own original annotation work, not McAuley Lab content -- but publishing them keyed to review_ids that map back to McAuley's unlicensed text is a gray area; **recommend NOT releasing this publicly either without permission**, since it would let a third party trivially re-join labels to the original (unlicensed-for-redistribution) text if they also hold a copy of the source dataset. |
| Releasing model artifacts/checkpoints trained on this data | A derivative work; `decisions.md` D2's own fallback already anticipated this ("restrict any model/derivative trained on this data to internal, non-published research use only" if license escalation fails) -- **this fallback has never been invoked because the escalation itself was never attempted.** |

**The Arabic-side data (Zenodo 17011574, CC-BY-4.0 confirmed; Zenodo 22061934) has a confirmed open license** and raises no equivalent concern -- the gap is specifically and only the English primary source.

**Recommended conservative release strategy for camera-ready/public release:**
1. Release all code, configs, and scripts (no dataset dependency issue).
2. Release the Arabic-side data derivatives freely (CC-BY-4.0-compatible).
3. **Do not release** English raw review text, English review_ids, or Human-Gold labels keyed to English review_ids, until the McAuley Lab is actually contacted and a response (or confirmed non-response after a documented attempt) is on record. This escalation was recommended in Phase 1 (`decisions.md` D2) and **has still not been performed** -- it should be done before, not after, submission, since "license status unresolved" is a reviewable, fixable gap and a reviewer may ask directly.
4. If release is required before the escalation resolves, fall back to releasing only aggregate statistics and model performance numbers for the English side, not any row-level artifact.

---

## 12. Deployment claims audit

The FastAPI/React deployment (`backend/`, `frontend/`) was built and smoke-tested (`decisions.md` D17, D18): 8 automated API tests pass, and ad-hoc manual testing confirmed functional Arabic/English/code-switched inference, valid probability outputs, and correct error handling -- this is consistently described in the existing documentation as **functional verification**, not **accuracy evidence**, and this audit found no place in the repository where the smoke-test results are mischaracterized as a performance claim. (The user's framing of "the six manually tested examples" refers to this ad-hoc testing; the exact count is not pinned to "six" anywhere in the written record -- the documented facts are "8 automated tests + an unspecified small number of hand-typed ad-hoc examples," and the manuscript should use that accurate description rather than a specific count that isn't actually recorded.)

**One real finding from the smoke testing must not be downplayed**: a hand-typed clearly-positive Arabic sentence was predicted Negative at 0.58 confidence during manual testing (`decisions.md` D17) -- this is a genuine, disclosed weak-reliability signal for the deployed checkpoint specifically (not the Phase 3B research E4 result, which is a different checkpoint/aggregation -- already correctly distinguished in the docs).

**Where deployment belongs:** **supplementary material / a short demonstration section, not the main scientific contribution.** The deployed model is a separate training pass from every reported research figure (`decisions.md` D17 states this explicitly and must continue to), so it cannot support any claim in the Results section. It is reasonable to mention briefly in an implementation/availability section ("a demonstration API and UI were built to allow interactive inspection of model behavior; this is an engineering artifact for demonstration purposes and is not evidence of model performance") -- never cited alongside Macro-F1/accuracy figures in the same table or paragraph.

---

## 13. Missing experiments -- classification

| Candidate experiment | Classification | Reasoning |
|---|---|---|
| Second human adjudicator (inter-adjudicator reliability) | **HIGH VALUE** | Directly addresses the single largest Human-Gold methodology weakness (Section 4) -- a second blind adjudicator on a subsample of the 179 disagreement cases would let the paper report adjudicator-level agreement, closing the most obvious reviewer question about the reference set's own reliability. Not critical (the current single-adjudicator design is defensible and disclosed), but it is the highest-leverage addition available. |
| Class-weighted LoRA (Phase 3A, matching Phase 3B's weighted loss) | **HIGH VALUE** | Directly resolves the standing confound in `known_limitations.md` #20 (classical-vs-transformer and LoRA-vs-full-FT comparisons are currently entangled with an untested class-weighting difference). This is a cheap, well-scoped ablation (same LoRA setup, one changed hyperparameter) that would materially strengthen claims 4 and 5 in the claim table. |
| Multi-seed reruns (variance estimation across training seeds) | **OPTIONAL** | Would strengthen confidence in point estimates, but the paired bootstrap/permutation tests already quantify sampling uncertainty in the *test-set* evaluation; multi-seed would add *training* variance, a different and real but lower-priority source of uncertainty given the sprint's time/compute constraints. |
| Additional transformer architectures (e.g. CAMeLBERT, AraBERT) | **NOT JUSTIFIED** | The project already explicitly considered and declined this (`decisions.md` D6) with a stated rationale; adding architectures now would not resolve any identified scientific weakness, only inflate the experiment count. |
| Additional datasets / external validation set | **OPTIONAL**, bordering **NOT JUSTIFIED** for this submission | Would help generalizability claims but is a substantial new-data-collection effort; the current scope (two review-domain corpora, clearly scoped) is defensible as-is provided generalization is not overclaimed. |
| More annotation (expanding Human-Gold beyond 757, or re-annotating the 578 "unanimous" rows with a 4th rater for a true gold-standard floor) | **OPTIONAL** | Would be nice (a true inter-coder reliability floor on the "easy" unanimous rows) but the unanimous rows are, by construction, the 3/3-agreement cases -- lowest marginal value of any additional annotation effort relative to cost. |
| Calibration analysis (confidence/probability calibration of model outputs) | **OPTIONAL** | Not currently claimed anywhere in the paper's intended contributions; only relevant if the deployment's confidence scores are going to be discussed quantitatively, which this audit recommends against (Section 12). |
| Statistical robustness checks beyond what exists (e.g., a sensitivity analysis removing the single adjudicator's most-disagreed-with cases) | **HIGH VALUE** | Cheap to run post-hoc on existing data (no new annotation needed) -- would directly quantify how much the Section 1/Section 6 "ranking instability" finding depends on the specific 60 majority-overruled cases, strengthening the paper's central claim's robustness. |

**Nothing above is classified CRITICAL.** The paper is scientifically complete enough to write up without any additional experiment; the HIGH VALUE items would strengthen it but their absence does not make the existing findings indefensible, provided the qualifications in Section 2's claim table are applied.

---

## 14. Manuscript readiness score

| Dimension | Score /10 | Why |
|---|---|---|
| Dataset rigor | 7 | Frozen, group-aware, hash-verified splits; real, documented confounds (geography, domain, label-source) correctly disclosed rather than hidden. Deduction: one primary dataset's license is still unresolved after being flagged in Phase 1. |
| Annotation rigor | 7 | Genuinely strong 3-annotator + blind-4th-adjudicator design with full provenance; deduction for the single-adjudicator weakness (Section 4) and the never-re-tested mixed-sentiment flag. |
| Experimental rigor | 6 | Two legitimate, honestly-separated training tracks (3A/3B); real compute-constraint failures (E4 Phase 3A OOM) disclosed rather than hidden. Deductions: untested class-weighting confound in Phase 3A transformers (#20), two lost primary prediction files, E4-Phase3A never completed. |
| Statistical rigor | 8 | Genuinely paired tests, correct permutation-test design for Macro-F1, Holm correction applied per justified family, 10,000 iterations, deterministic seeds, old bootstrap-heuristic correctly relabeled rather than misrepresented as a permutation test. Deduction only for the inherent low power at n=369/388 (not a flaw in execution, a fact about the sample size). |
| Reproducibility | 6 | Strong on seeds/hashes/splits/model IDs; real gaps on Python/PyTorch/Transformers/CUDA version pinning for the Kaggle (Phase 3B) environment, and on explicit dataset DOI/URL strings. |
| Novelty/contribution clarity | 6 | The *originally* intended novelty (code-switching × review domain) collapsed to n=9 and cannot carry the paper; the Human-Gold label-reliability finding is a genuinely novel and clean replacement contribution, but the manuscript has not yet been reframed around it (that reframing is this audit's main recommendation, not yet executed). |
| Claim discipline | 7 | The project's own running documentation (`known_limitations.md`, `decisions.md`) has consistently and voluntarily hedged claims throughout every phase -- a real strength. Deduction for a few claims (LoRA-vs-full-FT, classical-vs-transformer) that have been stated with s somewhat stronger framing in places than the evidence supports (Section 2, claims 4-5), now correctable. |
| **Overall publication readiness** | **6.5** | A methodologically honest, well-documented project with one major reframing still needed (lead with label-reliability, not code-switching or Arabic/English comparison) and several concrete, scoped fixes (Section 15) rather than a fundamental redesign. **No claim or guarantee of Q1 acceptance is made or implied by this score.** |

---

## 15. Final decision

## **B. READY AFTER MINOR FIXES**

(Not A: the central framing has not yet been updated to lead with the Human-Gold label-reliability finding, and several claims need the exact qualifying language from Section 2/3/7/8 applied before being written into a manuscript -- these are documentation/framing fixes, not new science. Not C or D: no experiment is missing that the paper cannot be written without, per Section 13.)

### CRITICAL issues

1. **The project's central framing still implicitly centers Arabic-English comparison / multilingual modeling rather than the label-reliability finding.** -- *Corrective action:* before drafting the manuscript, write a one-paragraph "contribution statement" using the Section 1 framing, and check every planned section/table against it; demote any RQ3 "Arabic vs. English" framing to the confound-disclosure language in Section 8.
2. **UCSD/McAuley license escalation was identified as necessary in Phase 1 (`decisions.md` D2) and has still never been attempted.** -- *Corrective action:* contact the McAuley Lab (or document a dated, specific attempt and non-response) before submission; until this is done, commit explicitly to the conservative release plan in Section 11 and say so in the paper's data-availability statement.
3. **Two Arabic Phase 3B primary runs' row-level predictions are permanently lost, and no Human-Gold figure exists for them at all (only their reruns).** -- *Corrective action:* state this explicitly and specifically wherever Arabic MARBERT/XLM-R standalone results are cited in the manuscript (both original-label and Human-Gold tables), using the `RERUN_REALIZATION_not_primary` qualifier verbatim or an equivalent footnote; do not let a reader infer the Human-Gold MARBERT/XLM-R-standalone figures are about the same model realization as the headline 0.785025/0.740295 primary scores.

### HIGH-PRIORITY issues

4. **Single-adjudicator Human-Gold construction has no second-adjudicator reliability check.** -- *Corrective action:* either run the HIGH VALUE second-adjudicator sub-sample experiment (Section 13) before submission, or add an explicit Limitations paragraph quantifying this gap (Section 4's exact wording) if time does not permit a new annotation round.
5. **Phase 3A transformer class-weighting was never tested, confounding claims 4 and 5 in the claim table.** -- *Corrective action:* either run the class-weighted-LoRA HIGH VALUE experiment (cheap, scoped), or explicitly soften claims 4/5 to the exact qualified wording given in the claim table and restate the confound in the manuscript's limitations section.
6. **Phase 3B (Kaggle) software/CUDA environment versions were never recorded.** -- *Corrective action:* recover from Kaggle notebook metadata/output logs if still available; otherwise, add an explicit "environment version not recorded" disclosure rather than omitting the topic.
7. **Dataset DOIs/URLs are not written out in one canonical place.** -- *Corrective action:* create `docs/data_availability.md` with resolvable DOI/URL strings for every dataset (Zenodo 17011574, Zenodo 22061934, UCSD/McAuley) before manuscript submission.

### MINOR issues

8. **"Human-Gold" used as a bare term risks reading as an infallibility claim.** -- *Corrective action:* first-use definition as "human-adjudicated reference set (Human-Gold)" per Section 4, consistently thereafter.
9. **"Six manually tested deployment examples" is not an exact figure recorded anywhere.** -- *Corrective action:* describe the deployment smoke testing using the actually-recorded facts (8 automated tests + ad-hoc manual spot checks), not an unverified specific count.
10. **The prior `publication_readiness_audit.md` is now stale on RQ3's status** (it describes the matched-protocol slice as "still unannotated"). -- *Corrective action:* this file (the current audit) supersedes it; add one line at the top of the old file pointing to this one, rather than deleting project history.

---

## Final summary (as requested)

**1. Recommended central paper contribution:** evaluation-label reliability in bilingual (Arabic-English) review sentiment classification, and its demonstrated effect on model rankings and significance conclusions -- using the multilingual/zero-shot/classical-vs-transformer experiments as the testbed, not as the destination claim.

**2. Recommended research questions:**
- RQ1 (reframed): How reliable are commonly-used sentiment evaluation labels (rating-derived; single-pass human annotation) relative to a multi-annotator, blind-adjudicated reference set, in this domain?
- RQ2: Does model ranking / statistical-significance structure change when evaluation moves from the original labels to the human-adjudicated reference set?
- RQ3 (reframed, descriptive): What does the original-label-vs-Human-Gold disagreement structure look like across two independently-sourced language sub-corpora, without claiming a causal language-difficulty comparison?
- RQ4 (retained, modest scope): Is multilingual joint training competitive with monolingual training under these same labels?
- RQ5 (retained, explicitly qualitative/diagnostic): What does the corpus's code-switching audit reveal about the reliability of common code-switch-detection heuristics in review text?

**3. Claims we may safely make:** all claims in the claim table marked SAFE or SAFE WITH QUALIFICATION, using exactly the qualifying language specified next to each; the Neutral-class finding using the Section 3 wording; the ranking-instability finding as a first-class result (Section 6); the code-switch-heuristic-false-positive finding (Section 9) as a methodology contribution.

**4. Claims we must not make:** any Arabic-vs-English difficulty/performance claim (direct or hedge-then-claim-anyway); any performance/accuracy claim derived from the 9 code-switch examples; any claim that Human-Gold is ground truth/infallible; any claim attributing Phase 3A-vs-3B score differences to GPU hardware specifically; any claim that silently treats a rerun realization as identical to its lost primary.

**5. Is any additional experiment actually required?** No experiment is CRITICAL (Section 13); the paper can be written now. The two HIGH VALUE items most worth the remaining time, in priority order, are (a) a second blind adjudicator on a disagreement subsample, and (b) a class-weighted LoRA rerun for Phase 3A -- both directly close named confounds rather than adding breadth for its own sake.

**6. Exact files/documentation to fix before manuscript writing:**
- Add a contribution-statement note reflecting Section 1's reframing (new short file or a header added to `paper/notes/`).
- `docs/decisions.md`: add a new entry recording either the McAuley Lab contact attempt or the decision to proceed under the conservative release plan (Section 11) with a stated reason.
- New `docs/data_availability.md`: resolvable DOIs/URLs for all three datasets, plus the final release-scope statement from Section 11.
- `docs/known_limitations.md`: add a Phase-4/Human-Gold addendum covering the single-adjudicator limitation (Section 4) and the Section 2 claim-table qualifications, parallel in style to the existing phase addenda.
- `paper/notes/publication_readiness_audit.md`: add a one-line pointer at the top to this file as the current/superseding audit.
- Any manuscript draft text touching claims 4/5/9 in the claim table (classical-vs-transformer, LoRA-vs-full-FT, "six examples") must use the exact qualified wording given above, not the stronger informal framing used in earlier chat/status summaries during this project.

**No manuscript text was written. This is the audit only, as instructed.**

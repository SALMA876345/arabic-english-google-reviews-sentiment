# RQ3 Manual-Validation Slice — Completion Plan

**Status: planning/templates only. No review has been annotated. No original research data or results were modified to produce this plan.** This directory supplements, and in one place corrects, `docs/annotation_guidelines.md` and `data/annotations/`.

---

## 1. Where the evidence lives (full repository search)

| File | Relevance |
|---|---|
| `docs/annotation_guidelines.md` | The protocol document — purpose, label definitions, process. **Contains stale numbers (809/800/400+400) — see §2 correction below.** |
| `data/annotations/validation_slice_candidate_ids.csv` | The actual 766 candidate IDs (confirmed by direct inspection, not the guideline doc's prose). |
| `data/annotations/annotation_template_pending.csv` | The actual 766-row template with text, blank label columns. |
| `docs/experimental_dataset_protocol.md` §6 | States the slice is "pending," cross-references the guidelines doc. |
| `docs/decisions.md` D11 | **The real origin of the 766/757 figures** — explains the candidate set was *re-derived* from the group-aware test split, superseding an earlier (now-deleted) script that produced the 809/800 numbers still sitting in the guidelines doc's prose. |
| `docs/label_provenance_policy.md` | Defines human_annotated / rating_derived / llm_weak_label — the taxonomy this slice exists to let us escape, for evaluation purposes. |
| `docs/dataset_audit.md` §7 | The original statement of the confound this slice targets. |
| `docs/known_limitations.md` #3, #19 | Restates the confound as an open limitation at the dataset and Phase-3-results level respectively. |
| `src/preprocessing/freeze_splits.py` | **The actual generating code** — confirms exactly how candidates were selected (see §2). |
| `paper/notes/publication_readiness_audit.md` §1, §7, §12 | The audit that flagged this as the project's top-priority open item. |
| `data/processed/frozen_v1/arabic_tourism_frozen.csv`, `english_matched_frozen.csv` | Source of the 757 main-slice rows' text/labels (they ARE the frozen test split). |
| `data/processed/arabic_jordan_v2.csv`, `english_ucsd_v2.csv` | Source of the 9 code-switch diagnostic rows. |
| `docs/codeswitch_audit.md` | The project's own precedent for exactly this kind of double-blind-annotation + arbitration design (κ=0.853/0.809 reported there) — the design in this directory mirrors it deliberately. |

No reference to "766" by that literal number exists anywhere in the prose docs — it is only recoverable by actually counting the candidate files. This itself is worth noting: **the headline number used throughout later work (including the publication audit) was never written down as a design target; it is an emergent count from the group-aware split, confirmed here by direct inspection.**

## 2. Reconstructing the original design — confirmed facts vs. unrecoverable details

**Confirmed from `src/preprocessing/freeze_splits.py` (the actual generating code) and direct inspection of the output files:**

- **Why 766 rows, not a round number**: the "main_stratified" portion (757 rows) is not a freshly-drawn stratified sample — it is **literally the frozen TEST split** of the Arabic tourism pool (369 rows) and the English matched pool (388 rows), assigned by group-aware place/business splitting targeting train/val/test fractions of 79%/10%/11%. The count 757 = 369 + 388 is a *consequence* of that split, not a chosen target. The remaining 9 rows are the verified genuine code-switch set from `docs/codeswitch_audit.md`, added as a separate addendum.
- **How sampled**: for the 757, no separate sampling occurred — whichever rows landed in "test" during group-aware splitting (by place name for Arabic, by `gmap_id` business ID for English) became the candidates. For the 9, all verified genuine code-switch examples were included (no sampling — it is the full set, since there were only 9).
- **Arabic vs. English split**: 369 Arabic (7 more in the code-switch addendum) + 388 English (2 more in the addendum) = 766 total. Confirmed by direct count of `data/annotations/validation_slice_candidate_ids.csv`.
- **Stratification**: intended to approximate each pool's natural sentiment distribution (not force an exact match) — group-integrity (no split business/place) was prioritized over hitting exact proportions, per `decisions.md` D11's own stated tradeoff.
- **Classes represented**: all three (Positive/Neutral/Negative) in both languages — see §3 below for exact counts; this is directly confirmed, not inferred.
- **Train/val/test membership**: the 757 main-slice rows ARE the frozen TEST split for both primary pools (confirmed — `freeze_splits.py` builds the candidate list directly from `ar_split[ar_split["split"]=="test"]` and the English equivalent). They are not drawn from train or val. The 9 code-switch rows are NOT part of either primary pool's train/val/test at all — 7 come from the Jordan auxiliary dataset (never in the frozen splits) and 2 from the full English corpus (reserved for the separate E8 scale experiment, also never in the frozen splits).
- **Intent**: confirmed directly from `docs/annotation_guidelines.md`'s own "Purpose" section — to apply one consistent annotation protocol, by the same annotator(s), across both languages, specifically to separate the label-provenance confound from a true language effect. This targets the **label-construction/annotation-process** confound specifically, not geography, domain, or dataset-origin (those are separately and explicitly named as NOT addressed by this slice — see §6).
- **Current label on each row**: recovered directly — see §3. For the 757: 100% of Arabic rows carry `human_annotated` labels (from the source dataset's original authors, not this project's new annotation); 100% of English rows carry `rating_derived` labels. For the 9: 7 Arabic-side rows carry `llm_weak_label`, 2 English-side rows carry `rating_derived`.
- **What human annotation was supposed to add**: a *new*, single-protocol, blinded (no rating/prior label shown), ideally same-annotator(s)-across-languages label, replacing (for evaluation purposes only — never for retroactively "correcting" the existing frozen pool's training labels) the existing label as the primary evaluation ground truth for this specific slice.
- **Whether any rows have already been annotated**: **No.** Confirmed directly: `annotation_template_pending.csv`'s `annotator_label` column is 100% blank (0 non-empty values out of 766, checked programmatically). This audit does not change that.

**One correction to the written record, not an inference:** `docs/annotation_guidelines.md`'s "Candidate subset" section still describes **809 total / 800 main (400 Arabic + 400 English) / stratified sentiment proportions "61.3/21.3/17.5" for both languages** — this describes an earlier design, implemented in a script `decisions.md` D11 confirms was superseded and deleted (`build_validation_slice.py`). The files that actually exist on disk reflect the later, group-aware redesign: **766 total / 757 main (369 Arabic + 388 English)**. This document was evidently never updated after the redesign. **This is a real, fixable documentation inconsistency, flagged here rather than silently corrected in the original file** (out of scope for this task per the instructions — see "next action" below for the recommended fix).

## 3. Audit of the actual 766 rows (exact counts, computed directly — not estimated)

### Main stratified slice (757 rows = the frozen test split)

| | Arabic (n=369) | English (n=388) |
|---|---|---|
| Positive | 238 (64.5%) | 221 (56.9%) |
| Negative | 75 (20.3%) | 106 (27.3%) |
| Neutral | 56 (15.2%) | 61 (15.7%) |
| Label source | 100% human_annotated | 100% rating_derived |
| Word count: median / mean / max | 15 / 18.1 / 64 | 18 / 30.1 / 335 |
| Rating distribution | n/a (no star ratings in this source) | 1★:66, 2★:40, 3★:61, 4★:43, 5★:178 |

**Finding not previously documented anywhere I could locate: the Arabic and English candidate subsets' sentiment distributions are *not* identical to each other**, even though the parent pools were constructed to match exactly (both 61.4% Positive / 21.2% Negative / 17.4% Neutral at the pool level, per `docs/experimental_dataset_protocol.md` §1). The divergence (64.5/20.3/15.2 vs. 56.9/27.3/15.7) is a side effect of group-aware test-split assignment not being able to hit exact proportions with only 42 Arabic place-groups (already acknowledged in `decisions.md` D11 at the split level, but not previously quantified specifically for this candidate slice). **This means the validation slice itself is a close-but-imperfect match on class balance between languages — report this explicitly if the slice is used for any language-balance-sensitive analysis.**

Word-count disparity is substantial and persists into this slice specifically: English's right tail (max 335) is over 5× Arabic's (max 64) even within just these 757 rows — consistent with, not an artifact unique to, the broader pool-level disparity already documented in `results/tables/arabic_vs_matched_english_comparability.md`.

### Code-switch diagnostic addendum (9 rows)

7 Arabic-side (all `llm_weak_label`, from the Jordan auxiliary dataset — **not** human-annotated, **not** part of either frozen pool) + 2 English-side (both `rating_derived`, from the full English corpus reserved for E8 — **not** part of the matched subset). These 9 are correctly kept conceptually separate from the 757 in every project document I found; this audit preserves that separation.

### Data-quality checks (whole 766)

- Missing text: **0**. Empty text: **0**.
- Duplicate `review_id`: **0**.
- Duplicate normalized text (case/whitespace-insensitive) within the 766: **0**.
- Existing `annotator_label` values in the pending template: **0 non-blank** (confirms nothing has been annotated).

**No data-quality blockers exist.** This slice is clean and ready for annotation exactly as designed.

## 4. Recommended annotation protocol (minimum sufficient, not elaborate)

Per-review fields, in order of importance:

1. **`sentiment_label`** (Positive/Neutral/Negative) — the core field, required. Required to answer RQ3 at all.
2. **`confidence`** (high/medium/low) — already specified in `docs/annotation_guidelines.md`; keep as-is. Cheap, directly useful for weighting/filtering analysis.
3. **`mixed_sentiment_flag`** (yes/no) — **new, recommended addition, not in the current template.** Justification: `docs/error_analysis.md` found `mixed_sentiment` is the single largest error category in the entire project (35-79% of errors depending on model/language). The current Neutral-class definition in `annotation_guidelines.md` *bundles* genuinely-mixed, purely-factual, and genuinely-ambiguous reviews into one label. Without this flag, a post-hoc analyst cannot tell *which* of those three phenomena is driving any given Neutral assignment in the new gold data — exactly the ambiguity that currently makes "Neutral is the hardest class" hard to explain mechanistically. This single boolean directly feeds RQ4 as well as RQ3/RQ2's interpretation, at near-zero added annotator burden.
4. **`notes`** (free text, optional) — already specified; keep as-is, valuable for RQ4 seeding exactly as the existing guidelines state.

**Explicitly NOT recommended as a new annotator-facing field** (to keep the task focused, per the brief's own instruction):
- **Rating-text disagreement flag** — do not ask annotators to produce this. It is fully **derivable automatically** after annotation by comparing `sentiment_label` to the existing rating-derived label for English rows (no information is lost by computing it post-hoc, and it removes an annotation-time decision that would otherwise require showing the annotator the rating — directly contradicting the blinding requirement).
- **Language verification as a dedicated structured field** — given the source pools are already language-segregated by construction and genuine code-switching is already known (from `codeswitch_audit.md`) to be exceedingly rare in this domain (9 of 1,050,832 documents), a dedicated mandatory field would mostly record "yes, as expected" at near-zero marginal value. Ask annotators to note it in free-text `notes` only if they actually encounter something unexpected — covered by the existing "flag anything difficult" instruction, no new field needed.

## 5. Annotation quality design

- **Number of annotators: 2, double-annotating the full 757-row main slice** (not a partial-overlap subsample). Justification: the main slice is the headline evaluation set for RQ3; a partial-overlap design would only let a κ be computed on part of the data, weakening exactly the claim this slice exists to support. The workload is realistic for full double annotation (§9). The 9 code-switch rows are included in both annotators' sheets too (negligible marginal cost) since they are already explicitly qualitative-only and do not need the same statistical rigor.
- **Bilingual, same annotator(s) across both languages — this is not optional, it is the design's entire point.** `docs/annotation_guidelines.md`'s own stated purpose is "one consistent annotation protocol, **by the same annotator(s)**, across both languages" specifically to remove annotator-identity as a confound. Using separate monolingual annotators per language would silently reintroduce exactly the kind of inter-annotator-identity confound this slice exists to eliminate. Both annotators must be comfortable reading both Arabic and English well enough to judge sentiment confidently in each.
- **Blinding**: no star rating, no prior label, no dataset/source indicator shown — already implemented in `annotator_1_blinded.csv`/`annotator_2_blinded.csv` (§8). Order randomized (seed=42, same order for both annotators — this does not bias independence, it only matters that each annotator doesn't see the *other's* answers) rather than grouped by language or sentiment, per the existing guidelines.
- **Independence**: two **separate files** handed to each annotator (not one shared sheet with two columns), mirroring this project's own established precedent for exactly this kind of task (`docs/codeswitch_audit.md`'s "Reviewer B had no access to Reviewer A's labels"). File-level separation is the only way to actually guarantee this at the artifact level (a shared-sheet approach relies on social/process discipline, not the file structure itself).
- **Disagreement handling / adjudication**: for every row where the two annotators' `sentiment_label` differs, a third pass (the lead researcher, or another available person not involved in the first two passes) reads the review directly and makes a final, documented `adjudicated_label` with reasoning in `adjudicator_notes` — **exactly** the pattern already proven in `docs/codeswitch_audit.md` (κ=0.853/0.809, 6 disagreements individually arbitrated with recorded reasoning). `build_adjudication_sheet.py` (§8) automates generating the list of rows needing this pass; it never fills in a label itself.
- **IAA metric**: Cohen's κ (unweighted), primary — consistent with this project's existing convention (κ=0.87 source dataset, κ=0.853/0.809 code-switch audit). A linear-weighted κ may be reported as a secondary, optional statistic (adjacent-category disagreements are less severe than opposite-category ones) but should never replace the unweighted figure other project artifacts already use.
- **Neutral definition**: use the existing verbatim definition in `docs/annotation_guidelines.md` without change — it is sound. The new `mixed_sentiment_flag` (§4) supplements it by making the heterogeneous Neutral bucket analyzable, rather than replacing or redefining it.
- **Mixed sentiment handling**: captured by the new boolean flag (§4), not folded into a 4th label category — keeping the label scheme at exactly 3 classes preserves direct comparability with every existing model result in this project, which were all trained/evaluated on a strict 3-class scheme.

## 6. What completing this slice can and cannot do for RQ3

**This is the single most important finding of this audit pass, stated as plainly as possible: completing the 766 annotations would NOT create a fully controlled cross-language experiment. It would remove exactly one confound — label-construction process and annotator identity — while several others remain structurally baked into which reviews exist in each pool.**

| Confound | Can this slice reduce it? | Why / why not |
|---|---|---|
| Label-generation process (human-annotated-by-original-authors vs. rating-derived) | **Yes — this is the slice's entire purpose.** | Both languages get a new label from the same protocol, same annotator(s), same blinding. |
| Annotator-identity / "what counts as Neutral" differing by who labeled it | **Yes, conditional on using the same bilingual annotator(s) for both languages (§5).** | If violated (different people per language), this confound re-enters by the back door. |
| Geography (Saudi Arabia vs. Wyoming/Vermont) | **No.** | Re-labeling the same reviews does not change where they were written. This is a property of which reviews exist in each pool, not how they're labeled. |
| Sub-domain (Saudi tourist attractions vs. US tourist-attraction-proxy businesses) | **No.** | Same reasoning — the underlying businesses don't change. |
| Source platform/era/collection methodology (2025 Zenodo deposit vs. 2021 UCSD scrape) | **No.** | Structural property of the source datasets, unaffected by new labels. |
| Review-length distribution (English's much longer right tail, confirmed again in this specific slice, §3) | **No.** | A re-label does not shorten or lengthen the underlying reviews. |
| Within-slice sentiment-balance mismatch between languages (§3's new finding) | **Partially** — can be reported/stratified around in analysis, but not eliminated without discarding rows (not recommended — would shrink an already-small sample). | A known, quantifiable imperfection in this specific realization of the slice. |

**The exact scientific claim that becomes defensible after completion:**

> *"Using a single blinded annotation protocol applied by the same bilingual annotator(s) to matched Arabic and English review samples, [result]. This isolates the effect of label-construction process from any residual cross-language performance difference; it does not isolate language from the geographic, domain, and platform differences that remain between the two underlying review pools."*

**What must NOT be claimed, even after full completion:** "this experiment shows Arabic is harder/easier than English for sentiment classification" as an unqualified, generalizable claim. The matched-protocol slice upgrades the *evaluation label quality*; it does not upgrade the *sampling frame* to a controlled cross-language design. This is precisely the distinction `paper/notes/publication_readiness_audit.md` §6-7 draws, and this plan is built to deliver exactly what that audit identified as achievable — no more, no less.

## 7. Statistical analysis plan

See `statistical_analysis_plan.md` in this directory for the full, pre-specified plan (re-scoring existing model predictions against new labels; per-language label-distribution comparison; Cohen's κ; rating-vs-human and human-vs-original-human disagreement analyses, kept analytically distinct; bootstrap CIs; the paired-vs-unpaired significance-testing distinction, which is easy to get wrong here and is spelled out explicitly; and an explicit statement of what any resulting p-value can and cannot support, cross-referencing §6 above).

## 8. Practical completion workflow and artifacts prepared in this directory

| File | Purpose | Labels filled? |
|---|---|---|
| `master_reference_DO_NOT_SHOW_ANNOTATORS.csv` | Full 766-row reference copy with `original_label`, `original_label_source`, `rating`, `slice_type` — for post-annotation diagnostic analysis only. **Never shown to annotators.** | N/A (contains only pre-existing labels, not new annotation) |
| `annotator_1_blinded.csv`, `annotator_2_blinded.csv` | The actual annotation-facing sheets — `review_id`, `language`, `text` only, same randomized order (seed=42), blank `sentiment_label`/`confidence`/`mixed_sentiment_flag`/`notes` columns. Two **separate files** for true independence. | **No — confirmed 0 non-blank values in every label column, checked programmatically.** |
| `annotator_instructions.md` | Standalone, handoff-ready instructions consolidating `docs/annotation_guidelines.md`'s definitions plus the new mixed-sentiment-flag instruction. | N/A |
| `build_adjudication_sheet.py` | Script that will merge the two annotators' sheets, compute κ, and generate the disagreement list for adjudication — **written and ready, but will refuse to run until both annotator sheets contain real labels** (checked at the top of the script). | N/A — not executed |
| `statistical_analysis_plan.md` | The full post-annotation analysis plan (§7 above, expanded). | N/A |

**Workflow, in order:**
1. Recruit/confirm 2 bilingual annotators (same two people for both languages — §5).
2. Hand each annotator their own `annotator_N_blinded.csv` + `annotator_instructions.md`. Do not give either annotator access to the other's file or to `master_reference_DO_NOT_SHOW_ANNOTATORS.csv`.
3. Annotators fill in `sentiment_label`, `confidence`, `mixed_sentiment_flag`, and `notes` for all 766 rows in their own file, independently.
4. Once both files are complete, run `python paper/annotation/build_adjudication_sheet.py` — produces `agreement_report.md` (κ) and `disagreement_for_adjudication.csv`.
5. A third person (adjudicator) reads every row in `disagreement_for_adjudication.csv` and fills in `adjudicated_label` + `adjudicator_notes`.
6. Merge: final gold label = annotator agreement where they agree, `adjudicated_label` where they don't. This becomes the new evaluation ground truth for the 757-row test slice (per `docs/annotation_guidelines.md`'s own stated disposition) and a qualitative supplement for the 9-row code-switch addendum.
7. Execute `statistical_analysis_plan.md`.
8. **Separately recommended, out of this directory's scope**: fix `docs/annotation_guidelines.md`'s stale 809/800/400+400 figures to match the actual 766/757/369+388 numbers confirmed here, so future readers of that file aren't misled the way this audit's own search initially was.

## 9. Workload estimate

- 757 main-slice reviews, median length 15-18 words (fast to read), with a long tail of longer English reviews (up to 335 words).
- Estimated time per review, blended across the length distribution: **~30-40 seconds** (read + decide + confidence + occasional note), with longer English outliers taking 1-2 minutes each.
- Per annotator, full 757-row pass: **≈ 6-9 hours** (757 × ~35s ≈ 7.4 hours, plus the 9 code-switch rows, negligible). Realistically spread across 3-4 working sessions, not one sitting.
- Two annotators, full double annotation: **≈ 12-18 person-hours** total for the first pass.
- Adjudication: assuming a κ in the 0.6-0.8 range (typical for 3-class sentiment with a well-specified guideline, consistent with this project's own code-switch audit at κ=0.809-0.853 for a binary-leaning decision), expect roughly **15-25% disagreement** ≈ 115-190 rows, at ~1-2 minutes each ≈ **2-6 additional hours** for one adjudicator.
- **Total realistic estimate: ~15-25 person-hours** across the full workflow (first-pass double annotation + adjudication). This is a **feasible, boundable** amount of work for a small research team or even a single dedicated researcher recruiting one additional annotator — not an unreasonable ask.
- **Recommendation: complete the full 757-row main slice, not a reduced subsample.** A smaller subsample (e.g., ~150-200/language) would roughly halve the workload but would produce visibly wider confidence intervals on an already carefully-designed, already-small sample, and the full set was already deliberately sized to exactly match the frozen test splits — shrinking it further would re-introduce a sampling decision this project has otherwise been careful to avoid making casually. Given the estimated cost is modest relative to everything else already completed in this project (Phases 1 through 3B), completing the full designed sample is the better use of the same ballpark of effort.

## 10. Final Recommendation

### COMPLETE THE 766 ANNOTATIONS

**Justification:**
- The candidate data is clean (§3 — zero missing/duplicate/blocking issues found).
- The protocol is sound and needs only two small, well-justified refinements (the `mixed_sentiment_flag` addition, and explicit enforcement of same-bilingual-annotator(s)-across-languages) rather than a redesign.
- The estimated workload (~15-25 person-hours) is genuinely feasible, not a theoretical ideal — this project has already invested far more effort than that into Phases 1-3B.
- Completing it provides the only designed mechanism to upgrade RQ3's claim from fully exploratory to "label-provenance-confound-controlled, with remaining confounds explicitly named" (§6) — a real, meaningful, and honestly-scoped improvement, not a false promise of full causal cleanliness.
- A redesign is not warranted: nothing about the sampling, the data quality, or the core protocol is broken — only refinements are needed.
- Reframing RQ3 as permanently exploratory would be the right call only if the annotation genuinely could not be resourced — but the workload estimate shows it can be, making that option a lower-value fallback rather than the best available choice.

### Exact next action

1. **Decide who the two bilingual annotators will be** (this is the one external dependency nothing in this repository can resolve) — confirm before anything else proceeds.
2. Apply the one outstanding content fix noted in §4/§5 to the blinded sheets if desired (they currently already include the recommended `mixed_sentiment_flag` column — no further file changes are needed on that front).
3. Hand off `annotator_1_blinded.csv` + `annotator_instructions.md` to annotator 1, and `annotator_2_blinded.csv` + `annotator_instructions.md` to annotator 2, separately.
4. Once both are filled, run `build_adjudication_sheet.py` and proceed through the workflow in §8.
5. Separately, fix `docs/annotation_guidelines.md`'s stale candidate-subset numbers (809/800/400+400 → 766/757/369+388) so the written record matches reality.

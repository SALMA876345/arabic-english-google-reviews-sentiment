# Full RQ3 Human-Validation Annotation Package

**Status: package prepared, zero annotations collected.** This is the full 757-review, three-annotator round, following on from the 20-review pilot in `paper/annotation/pilot/` (preserved, untouched, separate exercise).

## For the three annotators

1. Read `ANNOTATOR_INSTRUCTIONS.md` first — it is standalone and identical for all three of you.
2. **Annotator 1**: open `annotator_1_interface.html` directly in a web browser (double-click the file, or right-click → Open With → your browser). No installation, no internet connection, and no server needed.
3. **Annotator 2**: open `annotator_2_interface.html` the same way.
4. **Annotator 3**: open `annotator_3_interface.html` the same way.
5. Work through all 757 reviews using the Sentiment / Confidence / Mixed buttons and the optional notes box. The page shows your progress (e.g. "245 / 757") and a completed/remaining count at all times.
6. Your progress saves automatically after every single review, in your browser's local storage, tied to that specific HTML file. **Do not rename or move the HTML file while annotating** — if you do, your saved progress stays with the original filename/location, not the new one. Closing the tab, closing the browser, or restarting your computer is safe; reopening the same file resumes exactly where you stopped.
7. When all 757 reviews are done, the page will tell you clearly ("All 757 reviews completed"). Click **Export Results** — this downloads a CSV file (e.g. `annotator_1_COMPLETE_2026-...-....csv`) to your browser's default downloads location.
8. Send that exported CSV back. Please don't open and re-save it in Excel first (Excel can silently change encoding/formatting) — send the file exactly as downloaded.

**If you export before finishing**, the downloaded filename will say `INCOMPLETE_<N>remaining` instead of `COMPLETE` — this is allowed (useful as a backup), but only a file marked `COMPLETE` should be treated as your final submission.

## For the researcher, once all three completed files are back

1. Rename (or save) the three exported files as exactly: `annotator_1_completed.csv`, `annotator_2_completed.csv`, `annotator_3_completed.csv`, in this directory.
2. Run `python paper/annotation/full/compute_agreement.py` — produces `agreement_report.json` (3-rater exact/unanimous/majority agreement, Fleiss' kappa, Krippendorff's alpha, pairwise Cohen's kappa, per-language and per-class breakdowns, mixed-flag agreement, confidence distributions, pairwise confusion matrices). This script refuses to run if any completed file is missing or still blank.
3. Run `python paper/annotation/full/build_adjudication_sheet.py` — produces `classification_all_757.csv` (every row, all three raw annotations preserved, plus the computed `agreement_type` and `majority_label`) and `adjudication_template.csv` (only the non-unanimous rows, ready for a human adjudicator to fill in `adjudicated_label` + `adjudicator_notes`). This script also refuses to run against incomplete files.
4. A human adjudicator resolves every row in `adjudication_template.csv` by reading the review text directly — never by this script, never automatically from the majority vote.
5. The final gold label per row = the unanimous label where one exists, else the human-adjudicated label — these remain two distinctly-tracked columns throughout (`majority_label` vs. `adjudicated_label`), never silently merged into one "the label" column without preserving which path produced it.

## Files in this directory

| File | What it is |
|---|---|
| `human_validation_757_master.csv` | Canonical master (review_id, language, text, word_count, original_label, label_source, rating, source_group_id) — **research-side only, never shown to annotators.** |
| `build_master.py` | Script that built the master directly from the frozen test splits, with full verification. |
| `annotator_{1,2,3}_blinded.csv` | The three annotator-facing sheets (blank), before any interface wrapping. |
| `build_blinded_sheets.py` | Script that built the three blinded sheets with distinct seeds (1001/2002/3003). |
| `annotator_{1,2,3}_interface.html` | The actual offline annotation tools — one per annotator, each embedding that annotator's own review order. |
| `build_interfaces.py` | Script that generated the three HTML files from the blinded sheets. |
| `ANNOTATOR_INSTRUCTIONS.md` | Standalone instructions, identical for all three annotators. |
| `compute_agreement.py` | 3-rater agreement analysis — **prepared, not run** (refuses to run without real completed files). |
| `build_adjudication_sheet.py` | Classification + adjudication-template generator — **prepared, not run** (refuses to run without real, fully-completed files). |
| `ANNOTATION_PROVENANCE.md` | Full provenance record: source files, hashes, seeds, verification results, generation date. |

## Scope boundary

This package only prepares and (once returned) analyzes the human annotations. It does not retrain any model, does not modify the frozen train/val/test splits, and does not change any Phase 3A or Phase 3B result. See `paper/notes/FINAL_SCIENTIFIC_FRAMING.md` and `paper/MANUSCRIPT_DRAFT.md` §9.4/§10.3 for exactly what this annotation round can and cannot resolve about RQ3's cross-language confound (the original pointer target, `paper/annotation/README.md`, was the superseded 2-annotator planning doc and has been moved to `archive/annotation_planning_v1_superseded/`).

## Status: COMPLETE -- human-adjudicated reference set ("Human-Gold") constructed (2026-10-27)

**Terminology note:** this reference set is referred to as "Human-Gold" throughout the code and filenames (`human_gold_757.csv`) for brevity and reproducibility continuity, but in any publication-facing text it should be introduced as the **human-adjudicated reference set** and only abbreviated to "Human-Gold" after that first, explicit, non-infallibility-implying definition. It is not claimed to be an infallible ground truth -- see Limitations below.

Three independent bilingual annotators each labeled all 757 reviews independently (sentiment, confidence, and an exploratory mixed-sentiment flag) -- **2,271 primary sentiment annotations in total (3 x 757)** -- each blinded to the review's rating, original/rating-derived label, model prediction, and the other two annotators' choices. Agreement was computed (`compute_agreement.py`): **578/757 (76.4%) unanimous 3/3**, **Fleiss' kappa = 0.6499** and **Krippendorff's alpha (nominal) = 0.6500** for sentiment (both indicate "substantial," not "near-perfect," agreement by conventional Landis & Koch bands), and kappa = 0.269 for the mixed-sentiment flag (too low to trust -- treated as exploratory only, never re-collected downstream). Pairwise Cohen's kappa ranged 0.628-0.700 across the three annotator pairs (`agreement_outputs/overall_agreement_sentiment.json`).

The 179 non-unanimous reviews (161 with a 2/3 majority, 18 three-way splits) were resolved by a **fourth, independent human adjudicator** (`paper/annotation/full/adjudication/`), blinded to all three original annotators' choices, the majority vote outcome, the agreement type, the rating, the original/rating-derived label, and any model prediction -- shown only the review text and the same sentiment-decision rule given to the original annotators. The adjudicator was never asked about mixed sentiment (exploratory, not re-collected). This blind-adjudication design was chosen specifically so the low mixed-flag kappa could not be papered over by defaulting to an automatic majority vote; see `ADJUDICATION_PROTOCOL.md` for the pre-registered reasoning.

**Human-Gold construction rule** (`build_human_gold.py`, output `human_gold_757.csv`):
- 578 unanimous rows -> `human_gold_sentiment` = the unanimous label, `human_gold_source` = `unanimous_3of3`.
- 179 non-unanimous rows -> `human_gold_sentiment` = the blind fourth adjudicator's independent decision, `human_gold_source` = `independent_adjudication`. **The 2/3 majority vote is never substituted for the adjudicator's decision.**

**Reference-set limitations (state explicitly in any publication-facing use of this data):**
- **Single-adjudicator limitation:** all 179 disagreement cases (23.6% of the full 757-review reference set) were resolved by **one** adjudicator. There is no second adjudicator and no adjudicator-vs-adjudicator reliability statistic for this set. If that adjudicator has any idiosyncratic bias, it propagates uncontested into nearly a quarter of the reference set. This is the largest known methodological weakness of the Human-Gold construction (see `paper/notes/final_publication_readiness_audit.md` §4 and §13 for the proposed, not-yet-run, second-adjudicator strengthening study).
- The original annotators' Fleiss' kappa (0.6499) indicates substantial, not near-perfect, agreement -- some residual unreliability is inherent even in the 578 "unanimous" rows' boundary cases.
- The mixed-sentiment flag was measured (kappa=0.269) and found too unreliable to use; it is not part of the reference set at all.
- This reference set is not claimed to be infallible ground truth. "Disagreement with Human-Gold" is an operational definition, not a claim that the reference set is always correct.

This is referred to throughout the project as the **Human-Gold reference set**, not as infallible ground truth -- every row carries `human_gold_source` and `agreement_type` so provenance stays auditable. Original/rating-derived labels are deliberately kept out of `human_gold_757.csv`; they live only in `human_validation_757_master.csv` and `adjudication/classification_all_757.csv` as separate comparison artifacts, so Human-Gold provenance stays clean.

`human_gold_757.csv` is now **FROZEN**: 757 rows, 369 Arabic / 388 English, review_id set verified identical to the frozen Arabic+English test splits, zero train/val leakage, review text verified byte-identical to the frozen master. See `ANNOTATION_PROVENANCE.md` for hashes and full verification output. It must not be modified in any later phase -- read it, never rewrite it.

Comparison against original/rating-derived labels, model evaluation against Human-Gold, and any resulting statistics are a **separate, not-yet-performed phase**, pending explicit approval.

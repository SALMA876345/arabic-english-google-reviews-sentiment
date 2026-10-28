# Adjudication Protocol — Full 757-Review, 3-Annotator Round

**Status: protocol defined BEFORE adjudication begins. Zero adjudicated labels exist yet.** This document specifies how disagreement cases will be resolved; it is written now, before anyone reads `adjudication/master_adjudication_sheet.csv`'s disagreement rows, so the resolution rule is pre-registered rather than invented after seeing the data.

## Scope

Of 757 reviews, three independent annotators produced sentiment labels that were:
- **Unanimous (3/3) on 578 reviews (76.4%)** — no adjudication needed. The unanimous label stands as-is.
- **Majority (2/3) on 161 reviews (21.3%)** — one annotator differed from the other two.
- **Three-way disagreement on 18 reviews (2.4%)** — all three annotators gave different labels.

**Total requiring adjudication: 179 reviews** (161 + 18), in `adjudication/master_adjudication_sheet.csv`.

## Core rules

1. **Unanimous (3/3) cases require no adjudication.** The unanimous label is used as-is for those 578 reviews.
2. **Every non-unanimous case (majority or three-way) enters adjudication** — no case is silently dropped or auto-resolved.
3. **The three original annotator decisions can never be changed.** `completed_raw/annotator_{1,2,3}_completed.csv` are locked, hashed, and permanent. Adjudication produces a new, separate `adjudicated_sentiment` value; it does not edit, overwrite, or annotate over any annotator's original file.
4. **The adjudicated label is stored in its own column**, never merged into or confused with any individual annotator's column or with `majority_label`. Three distinct concepts, three distinct columns, permanently: `annotator_N_sentiment` (what each person said), `majority_label` (what 2-or-more agreed on, when that exists — blank for true 3-way splits), `adjudicated_sentiment` (the adjudicator's final call, made after reading the text).
5. **Majority vote is NOT adjudication.** `majority_label` is recorded as a reference column precisely so it is visible and auditable, but it is explicitly not treated as the automatic final answer — see "Why not just use majority vote" below.
6. **Adjudication is performed using only the review text and the original annotation guidelines** (`ANNOTATOR_INSTRUCTIONS.md`). No star rating, no original/rating-derived dataset label, and no model prediction may be shown or consulted during adjudication — same blinding standard as the original three annotation rounds.
7. **Whether a case was originally 2/3 or 3-way is preserved** in the `agreement_type` column and must never be dropped from the record, even after a final decision is reached — a 3-way disagreement that got adjudicated to "Positive" is scientifically different from a 2/3-majority case that got adjudicated the same way, and the manuscript needs to be able to say so.
8. **A concise reason is recorded for every adjudicated decision** (`adjudication_reason`) — not a formality, but the mechanism that makes the adjudicated label auditable by someone other than the adjudicator later.

## Why not just use majority vote?

A reviewer familiar with 3-rater designs will ask this directly: with three annotators, why not simply take the 2/3 majority as the gold label and only hand-adjudicate the 18 true three-way splits?

This project does **not** adopt automatic majority voting, for a specific, stated reason: `docs/error_analysis.md`'s prior model-error analysis (Phase 3A) found that `mixed_sentiment` is the single largest error category in this corpus (35–79% of model errors depending on model/language), and this round's own `mixed_sentiment_flag` agreement is markedly weaker than sentiment agreement (overall Fleiss' κ=0.269 vs. 0.650 for sentiment — see `agreement_outputs/`). Put together, this means a 2/3 majority on a genuinely mixed-sentiment review is not necessarily "two people got it right and one got it wrong" — it can just as easily be "two people resolved a genuinely ambiguous case the same way by chance or by a shared minor bias, while the third's reading was equally defensible." A majority count cannot distinguish these two situations; reading the text can. Given this project already explicitly rejected automatic majority-voting-as-gold in its own task instructions, and the mixed-sentiment finding independently supports that caution, every non-unanimous case is adjudicated by human reading, not by vote count.

## Recommended procedure (most defensible given three original annotators)

1. **One adjudicator** (someone not required to be one of the three original annotators, though it may be; consistent with this project's own precedent in `docs/codeswitch_audit.md`, where the lead researcher adjudicated disagreements after the two-rater pass) reads the review text directly, without seeing which annotator gave which label in advance if practically possible — the sheet as prepared does show all three labels side by side for efficiency, so this is a **recommended practice, not an enforced blind**, and should be noted as such in the manuscript's methods section.
2. The adjudicator considers the three original labels and the three `mixed_sentiment_flag` values as *context*, not as a vote to ratify, and decides the sentiment using exactly the same label definitions given to the original annotators (`ANNOTATOR_INSTRUCTIONS.md`): net overall impression, Positive/Neutral/Negative only.
3. For **majority (2/3) cases**: the adjudicator may end up agreeing with the majority — that is a legitimate, common outcome, not a default to be assumed. The `adjudication_reason` must say why, briefly (e.g., "majority correct — review is clearly positive despite one complaint" vs. "majority appears to have missed the genuinely mixed balance here; siding with the minority annotator's reading").
4. For **three-way disagreement (18 cases)**: there is no majority to lean on at all; the adjudicator's reading is the sole basis for the final label. These 18 cases should receive comparatively more careful documentation in `adjudication_reason`, since they represent the corpus's most genuinely contested reviews.
5. **If a second adjudicator is available**, independently adjudicating a subsample of the 179 (e.g., the 18 three-way cases plus a random sample of the 161 majority cases) and reporting adjudicator-adjudicator agreement would further strengthen the manuscript's reproducibility claims — this is a **recommended enhancement, not a requirement**, and should be decided based on available resourcing, not treated as blocking.
6. The final gold label per review, once this process completes = the unanimous label (578 reviews, untouched) **or** the adjudicated label (179 reviews) — these two sources remain distinguishable in the final merged file by an explicit `label_source` flag (`unanimous_3of3` vs. `adjudicated`), not collapsed into a single undifferentiated "gold" column.

## What this protocol explicitly does not decide yet

This document defines *how* adjudication will proceed. It does not itself adjudicate anything, does not estimate how long adjudication will take, and does not compare the resulting gold labels against model predictions or against the original rating-derived/dataset labels — those are later, separate steps, explicitly out of scope until the human annotation stage you are reading this at has been reviewed and approved.

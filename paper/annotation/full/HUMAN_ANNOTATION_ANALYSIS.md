# Human Annotation Analysis — Full 757-Review, 3-Annotator Round

**Status:** Raw annotation complete and locked. Agreement analysis complete. Adjudication protocol defined. **Adjudication itself has not been performed** — 179 of 757 reviews (23.6%) still lack a final gold label. No human-gold labels have been compared against model predictions, original dataset labels, or ratings. No manuscript claims are made here beyond what this specific analysis supports.

## 1. Annotation design

- **757 reviews** (369 Arabic, 388 English), drawn exactly from the frozen primary test splits (`data/splits/frozen_v1/arabic_tourism_test_ids.json`, `english_matched_test_ids.json`) — not resampled, not rebalanced, not selected by rating. The 9 verified genuine code-switch reviews (`docs/codeswitch_audit.md`) are explicitly excluded from this set and remain a separate qualitative E6 exercise.
- **3 independent bilingual annotators**, each annotating all 757 reviews — 2,271 total independent judgments.
- **Blinding:** no rating, no original/rating-derived label, no model prediction, and no other annotator's answer was visible to any annotator during annotation (verified structurally — the annotator-facing interfaces embedded only `review_id`, `language`, `text`).
- **Independence:** each annotator used a separate HTML interface and a separate localStorage-backed progress file; `ANNOTATOR_INSTRUCTIONS.md` explicitly instructed no discussion of individual reviews, no viewing of another annotator's answers, and no use of any LLM to decide sentiment.
- **Randomization:** each annotator saw the 757 reviews in a distinct deterministic order (seeds 1001 / 2002 / 3003 — `ANNOTATION_PROVENANCE.md`), so no shared presentation-order or fatigue effect could affect all three identically.
- **Decision rule:** net overall impression (Positive/Neutral/Negative), with `mixed_sentiment_flag` tracked as an explicitly separate, secondary yes/no variable — never a fourth label, never merged into the primary sentiment column.

## 2. Primary sentiment agreement — overall

| Measure | Value |
|---|---|
| N | 757 |
| Unanimous (3/3) | 578 (76.4%) |
| Majority (2/3) | 161 (21.3%) |
| Three-way disagreement | 18 (2.4%) |
| At least 2/3 agreement | 739 (97.6%) |
| Fleiss' κ | 0.650 |
| Krippendorff's α (nominal) | 0.650 |

Pairwise:

| Pair | Raw agreement | Cohen's κ |
|---|---|---|
| Annotator 1 vs. 2 | 86.5% | 0.700 |
| Annotator 1 vs. 3 | 81.9% | 0.629 |
| Annotator 2 vs. 3 | 81.9% | 0.628 |

By conventional interpretation scales for κ (e.g., Landis & Koch), these values sit in the **substantial** agreement range (0.6–0.8), not the **almost perfect** range (>0.8) — a defensible, respectable level of agreement for 3-class sentiment on real-world review text, but one that leaves meaningful room for genuine disagreement, which is exactly what the 23.6% non-unanimous rate reflects.

## 3. By-language results

| | Arabic (N=369) | English (N=388) |
|---|---|---|
| Unanimous (3/3) | 300 (81.3%) | 278 (71.6%) |
| Majority (2/3) | 58 (15.7%) | 103 (26.5%) |
| Three-way disagreement | 11 (3.0%) | 7 (1.8%) |
| Fleiss' κ | 0.671 | 0.628 |
| Krippendorff's α | 0.671 | 0.629 |

**This difference is not interpreted as evidence that Arabic is inherently easier than English for human annotators, and must not be cited as such.** Arabic and English in this corpus differ simultaneously in source platform, geography, sub-domain, review-length distribution, and original label-generation process (`docs/dataset_audit.md` §7, `paper/notes/publication_readiness_audit.md` §7) — any agreement-rate difference is consistent with any combination of these factors, annotator-specific familiarity, or genuine linguistic difficulty, and this analysis cannot and does not separate them.

## 4. Disagreement structure — which class-pairs drive non-unanimous cases

| Pair | Overall | Arabic | English |
|---|---|---|---|
| Positive vs. Neutral | 80 | 29 | 51 |
| Neutral vs. Negative | 53 | 18 | 35 |
| Positive vs. Negative | 28 | 11 | 17 |
| Three-way (all classes) | 18 | 11 | 7 |

**Positive-vs-Neutral is the single largest disagreement driver in both languages**, followed by Neutral-vs-Negative. Positive-vs-Negative — the starkest possible disagreement — is comparatively rare (28 of 179 non-unanimous cases, 15.6%). **This pattern is consistent with, though does not by itself prove, the prior model-level finding that Neutral is the hardest class to predict** (`docs/error_analysis.md`): if human annotators themselves disagree about the Positive/Neutral and Neutral/Negative boundaries at a much higher rate than the Positive/Negative boundary, a classifier's difficulty with Neutral is at least partly inherited from genuine ambiguity in the underlying construct, not solely a model weakness. This is an observed association between two independent analyses (human disagreement structure and model error structure), not a controlled test of why either occurs.

## 5. Mixed-sentiment flag — secondary variable, reliability notably lower than primary sentiment

| Measure | Overall | Arabic | English |
|---|---|---|---|
| Fleiss' κ | **0.269** | 0.341 | 0.197 |
| Unanimous (3/3) rate | 61.6% | 64.5% | 58.8% |

Pairwise κ: Annotator 1 vs. 2 = 0.436, Annotator 1 vs. 3 = 0.184, Annotator 2 vs. 3 = 0.242.

Mixed=yes frequency per annotator: Annotator 1 = 291 (38.4% of 757), Annotator 2 = 137 (18.1%), Annotator 3 = 87 (11.5%).

**This agreement level is substantially weaker than primary sentiment (κ=0.269 vs. 0.650) and falls in the "fair" range by conventional interpretation scales, not "substantial."** This is reported transparently rather than minimized: the three annotators applied the `mixed_sentiment_flag` concept quite differently in practice — Annotator 1's flagging rate (38.4%) is more than triple Annotator 3's (11.5%), a difference in criterion/threshold, not merely in which specific reviews each flagged. **This project does not claim the mixed-sentiment flag is a reliable measurement as currently instructed and executed.** Any use of this variable in the eventual manuscript must carry this reliability caveat explicitly; it should be treated as a lower-confidence, exploratory signal rather than a validated construct on the same footing as the primary sentiment label.

## 6. Confidence — treated strictly as metadata, not ground truth, not converted to a label

Confidence distributions differ substantially by annotator (Annotator 1: 76.5% high / 21.8% medium / 1.7% low; Annotator 2: 96.7% high / 2.8% medium / 0.5% low; Annotator 3: 55.7% high / 19.6% medium / 24.7% low) — these are **annotator-specific response-scale tendencies**, not a shared, calibrated measure of item difficulty, and are not interpreted as such.

Within each annotator, low/medium confidence is associated with a higher rate of landing in a non-unanimous (2/3 or 3-way) row than in a unanimous row — e.g., Annotator 1's "high" confidence rate is 84.6% on unanimous rows vs. 50.3% on non-unanimous rows; Annotator 3's is 68.3% vs. 15.1%. This directional pattern holds for all three annotators and is consistent with confidence tracking genuine item difficulty to some degree, but given the annotators' very different baseline confidence distributions, this is reported as a within-annotator association only, not as evidence that confidence is comparable or poolable across annotators.

## 7. Cases requiring adjudication

**179 of 757 reviews (23.6%)** require adjudication: **161 majority (2/3) cases** and **18 three-way disagreement cases**. Full breakdown by class-pair is in §4. See `ADJUDICATION_PROTOCOL.md` for the pre-registered resolution procedure and `adjudication/master_adjudication_sheet.csv` for the prepared (currently blank) adjudication sheet.

## 8. Limitations

- **Mixed-sentiment-flag reliability is low** (§5) — any manuscript use of this variable must carry that caveat prominently, not in a footnote.
- **Confidence is annotator-specific metadata**, not a calibrated or poolable measure (§6) — it must not be converted into a sentiment label or treated as a proxy for case difficulty across annotators.
- **Arabic/English agreement-rate differences are confounded** by the same dataset-origin factors already documented since Phase 2.5 and must not be read as a language-difficulty finding (§3).
- **Human annotation is not infallible.** A κ of 0.650 (substantial, not perfect) and a 23.6% non-unanimous rate are themselves evidence that even careful, blinded, independent human judgment does not converge on a single "true" answer for a meaningful fraction of real-world reviews — this is a property of the task (genuinely ambiguous sentiment in real text), not a flaw unique to these three annotators.
- **179 reviews currently have no final gold label.** Any analysis, table, or claim that requires a complete gold-labeled 757-row set cannot yet be produced.
- **No claim of guaranteed publication or Q1 acceptance** is made or implied by any result in this document.

## 9. Exact files and scripts used

| File | Role |
|---|---|
| `completed_raw/annotator_{1,2,3}_completed.csv` | Locked, hashed, immutable raw annotations (SHA-256 recorded in `ANNOTATION_PROVENANCE.md`) |
| `verify_completed_integrity.py` | Pre-analysis integrity gate — all checks passed before any statistic below was computed |
| `compute_agreement.py` | Produces every statistic in §2–6 |
| `agreement_outputs/*.json`, `*.csv` | Machine-readable outputs (overall, by-language, disagreement structure, mixed-flag, confidence, pairwise/summary CSVs) |
| `build_adjudication_sheet.py` | Produces the 179-row adjudication sheet and the full 757-row permanent audit record |
| `adjudication/master_adjudication_sheet.csv` | The 179 cases awaiting adjudication (all adjudication fields blank) |
| `adjudication/classification_all_757.csv` | Full 757-row record, all three raw annotations preserved per row, permanently |
| `ADJUDICATION_PROTOCOL.md` | Pre-registered resolution procedure |

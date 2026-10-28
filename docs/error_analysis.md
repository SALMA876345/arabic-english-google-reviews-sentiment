# Error Analysis (Phase 3)

Systematic review of every misclassification from the strongest baseline and strongest transformer on E1 (Arabic) and E2 (English), by two independent agent passes reading each error's actual text against a fixed category list (no cherry-picking — all 327 error rows across the 4 files were categorized). Full row-level data: `results/error_analysis/error_cases_*.csv`. Categories were never invented post-hoc to fit a narrative — the fixed list was given to the reviewer in advance, with `uncertain`/`no_clear_pattern` available whenever a case didn't fit.

## E1 — Arabic (strongest baseline: TF-IDF+LogReg, val F1=0.749; strongest transformer: MARBERT/LoRA, val F1=0.582)

| Category | LogReg (79 errors) | MARBERT (70 errors) |
|---|---|---|
| mixed_sentiment | 47 (59%) | 55 (79%) |
| negation | 8 (10%) | 2 (3%) |
| implicit_sentiment | 6 (8%) | 5 (7%) |
| short_ambiguous | 5 (6%) | 0 |
| named_entities | 4 (5%) | 2 (3%) |
| label_noise_suspected | 4 (5%) | 4 (6%) |
| dialect | 2 (3%) | 0 |
| sarcasm / emoji / code_switching | 0 | 1 / 0 / 0 |
| other (spelling, no_clear_pattern, uncertain) | 3 | 1 |

**Finding:** `mixed_sentiment` (hedge reviews — "place is nice BUT X complaint," usually gold-labeled Neutral) is the dominant error driver for both models, and even more so for MARBERT (79% vs. 59%) — MARBERT's errors have concentrated almost entirely into this one genuinely-hard category, while the classical baseline still fails on things a contextual model handles better: negation (10% vs. 3%) and dialect (3% vs. 0%). This is consistent with the per-class results (MARBERT's Neutral F1 is the weakest class for both models) and suggests MARBERT has partially solved the baseline's lexical-confusion failures but not the inherently ambiguous 3-way-label cases.

**Code-switching was not a meaningful error driver.** Every error row in both files has `script_mix=arabic_only`. Manual scan found only two embedded English tokens total ("vip", "outlines") and one Arabizi loanword ("بيرفكت"/perfect) — all `named_entity_or_brand`/`arabizi` per `codeswitch_audit.md`'s own criteria, not genuine code-switching. This corroborates the project's dataset-level finding (9 genuine code-switch examples out of 1,050,832 documents) at the error-analysis level too.

**Suspected label noise (4 cases, both models agree with the reviewing agent's own reading over the gold label):** AR-TOUR-01139, AR-TOUR-01140, AR-TOUR-01145, AR-TOUR-01166 — e.g. AR-TOUR-01145 explicitly says "organization less than one star" (sarcastic 👍) but is gold-labeled Neutral/Positive. This is a small, real crack in the "human-annotated = ground truth" assumption even for the highest-quality dataset in the project — worth noting, not overturning the overall label-quality assessment.

## E2 — English (strongest baseline: TF-IDF+LogReg, val F1=0.677; only transformer: XLM-R/LoRA, val F1=0.639)

| Category | LogReg (93 errors) | XLM-R (85 errors) |
|---|---|---|
| mixed_sentiment | 33 (35%) | 37 (44%) |
| rating_text_disagreement | 14 (15%) | 16 (19%) |
| negation | 12 (13%) | 5 (6%) |
| implicit_sentiment | 11 (12%) | 7 (8%) |
| short_ambiguous | 7 (8%) | 8 (9%) |
| sarcasm | 4 (4%) | 5 (6%) |
| label_noise_suspected | 3 (3%) | 3 (4%) |
| no_clear_pattern | 6 (6%) | 1 (1%) |
| other (spelling, emoji, uncertain) | 3 | 3 |

**Finding, and the most consequential one in this report:** `rating_text_disagreement` (the review's star rating conflicts with what the text actually says) accounts for 15–19% of errors on its own, and combined with `mixed_sentiment` (where the rating is defensible but a single label is inherently lossy), **roughly 50–60% of all English errors trace back to the rating-derivation labeling mechanism itself, not genuine model weakness.** Concretely: 5-star reviews that are lists of complaints, apologetic 1-star reviews, and 3-star "Neutral" labels attached to unambiguously glowing or clearly negative text, all appear repeatedly. This is direct, row-level evidence for the caveat already carried since Phase 1 (`label_provenance_policy.md`): rating-derived labels are not a reliable substitute for human sentiment annotation, and E2's measured macro-F1 ceiling is likely depressed by label noise more than by model weakness.

**Label noise beyond the rating mechanism (not just tone mismatch):** EN-WY-0233353 ("Me and Sarge caught a nice jack terrier today!", 1-star), EN-WY-0113930 ("Free love powwow", 2-star), EN-WY-0699202 ("It was big and impressive. I can say I seen one time", 2-star) — text with no discernible connection to a negative rating at all, suggesting either a data error or an off-topic/irrelevant review slipping through. EN-WY-0114112 (a garbled Google-translation from Russian) was marked `uncertain` — a translation-pipeline anomaly, not an ordinary disagreement.

**Baseline vs. transformer divergence:** the classical baseline shows a larger `negation`+`implicit_sentiment` share (25% combined) than XLM-R (14% combined), mirroring the Arabic finding — a contextual model handles negation/implicit cues somewhat better, but both are about equally vulnerable to genuinely mixed-sentiment and rating-noise-driven errors, which dominate regardless of model family.

## Cross-cutting conclusions for RQ4

1. **Mixed/hedge sentiment is the single largest error source in both languages and both model families** — this is a property of the labeling scheme (forcing one of 3 labels onto reviews with genuinely split sentiment) more than a model deficiency, and should be named explicitly as a task-design limitation in the manuscript, not just a model weakness.
2. **Rating-derived labels are measurably noisier than human-annotated ones** — the English error analysis found a concrete, quantified mechanism (`rating_text_disagreement`) that doesn't exist in the Arabic human-annotated data at anywhere near the same rate, directly supporting `label_provenance_policy.md`'s separation of rating-derived from human-annotated ground truth.
3. **Code-switching is confirmed, again, to be a non-factor in this corpus's errors** — consistent with `codeswitch_audit.md`'s dataset-level finding.
4. **A small amount of label noise exists even in the human-annotated Arabic data** (4 cases out of 70-79 errors per model) — real, but far smaller in scale than the rating-derived noise found in English, consistent with human annotation being more reliable but not perfect.
5. **Negation and implicit sentiment are handled somewhat better by transformers than by TF-IDF+LogReg in both languages** — one of the few places a transformer's contextual representation shows a clear qualitative advantage, even though it doesn't translate into a higher aggregate macro-F1 under the LoRA/CPU constraints of this phase (see `paper/notes/phase3_report.md`).

## E6 — Qualitative diagnostic on the 9 verified genuine code-switch examples

Per `codeswitch_audit.md`, n=9 is far too small for any quantitative metric — no accuracy/F1 rate is reported here, only individual case outcomes. MARBERT (E1 LoRA adapter) was run on all 9; XLM-R inference could not be completed (3 repeated OOM failures loading the larger base model on this memory-constrained machine — same root cause as `decisions.md` D15's E4 failures, not a special code-switching-related issue). Full data: `results/error_analysis/codeswitch_diagnostic_final.csv`.

| review_id | embedded term | source label (NOT gold) | MARBERT prediction | confidence | match |
|---|---|---|---|---|---|
| AR-JOR-01270 | "packaging" | Negative (llm_weak) | Positive | 0.43 | ✗ |
| AR-JOR-04350 | "call center" | Negative (llm_weak) | Negative | 0.66 | ✓ |
| AR-JOR-04600 | "Hire more people like..." (new content) | Positive (llm_weak) | Positive | 0.91 | ✓ |
| AR-JOR-06216 | "Five star" | Positive (llm_weak) | Positive | 0.94 | ✓ |
| AR-JOR-07320 | "play area" | Positive (llm_weak) | Positive | 0.94 | ✓ |
| AR-JOR-07449 | "staff" | Positive (llm_weak) | Positive | 0.93 | ✓ |
| AR-JOR-07691 | "list" | Negative (llm_weak) | Neutral | 0.38 | ✗ |
| EN-VT-0213840 | "takeaway" | Negative (rating_derived) | Negative | 0.53 | ✓ |
| EN-VT-0613379 | discourse-level EN→AR switch | Positive (rating_derived) | Positive | 0.94 | ✓ |

**Observations (qualitative, not statistical):** 7/9 predictions matched the source label, but both mismatches (AR-JOR-01270, AR-JOR-07691) were also the two lowest-confidence predictions (0.43, 0.38 — near the 3-class random baseline of 0.33), suggesting the model itself was uncertain on these rather than confidently wrong. Both mismatches also happen to be the two shortest, single-embedded-word cases ("packaging", "list") with otherwise terse Arabic context — consistent with the `short_ambiguous` error category identified in the main E1 error analysis above, rather than a code-switching-specific failure mode. The three highest-confidence correct predictions (0.91-0.94) are exactly the cases with richer surrounding Arabic context. **No pattern suggests code-switching itself is what drove the two errors** — the confound with short/sparse context cannot be ruled out with n=9, and this must not be overstated into a general claim about code-switching robustness.

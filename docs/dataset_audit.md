# Dataset Audit

**Status:** Three scout agents (Arabic / English / code-switching) independently searched Hugging Face, Kaggle, Zenodo, Mendeley Data, GitHub, and academic repositories; a fourth agent (Data Quality & Methodology Auditor) independently re-verified the most decision-critical claims (license text via Zenodo API, HARD's size discrepancy via the canonical GitHub README, EESA's accessibility via two additional search passes) and scored every serious candidate on a 12-dimension rubric.
**Full detail:** raw scout notes in [`research_raw/arabic_datasets_raw.md`](research_raw/arabic_datasets_raw.md), [`research_raw/english_datasets_raw.md`](research_raw/english_datasets_raw.md), [`research_raw/codeswitch_datasets_raw.md`](research_raw/codeswitch_datasets_raw.md); full scoring tables and red-flag matrix in [`research_raw/quality_audit_raw.md`](research_raw/quality_audit_raw.md); machine-readable inventory of all 34 candidates in [`../data/dataset_inventory.csv`](../data/dataset_inventory.csv).

## 1. Scoring rubric (12 dimensions, 0–5 each)

Domain Relevance · Arabic Quality · English Quality · Code-Switch Coverage · Dataset Size · Label Reliability · Class Balance · Provenance · Licensing Clarity · Reproducibility · Research Novelty Value · Comparability Across Languages. A dimension inapplicable to a given dataset (e.g. English Quality for an Arabic-only set) is excluded from that dataset's average rather than scored 0. Full per-dimension justification for every top-tier candidate is in `quality_audit_raw.md` §2.

## 2. Top-scoring candidates

| Dataset | Domain | Overall score | Verdict |
|---|---|---|---|
| Arabic Google Maps Tourism (Zenodo 17011574 / MDPI *Data* 2025) | Tourism attractions, Saudi Arabia | **3.6** | **USE (anchor)** |
| Jordanian-Arabic Restaurant (Zenodo 22061934) | Restaurants, Jordan | **3.2** | **COMBINE (volume, with caveat)** |
| UCSD/McAuley Google Local Review Dataset | General local businesses, global/US-dominant | **2.9** | **COMBINE (conditional)** |
| HARD (Hotel Arabic-Reviews Dataset) | Hotels | 2.7 | RESERVE (external eval) |
| SemEval-14/16 Restaurant ABSA (English) | Restaurants | 2.7 | RESERVE (cross-check) |
| EESA (Egyptian-English code-switched YouTube sentiment) | YouTube comments | 2.7 (high novelty, zero accessibility) | RESERVE — likely unobtainable in sprint window |
| LABR, GLARE, ArSAS, Yelp Open Dataset | Various | 2.5 each | RESERVE / supplementary only |

## 3. Arabic candidates — final recommendation

**Primary: COMBINE Zenodo 17011574 + Zenodo 22061934.**

- **Zenodo 17011574** (Arabic Google Maps Tourism, Saudi Arabia) is the only dataset in the *entire* pool (Arabic or English) that is simultaneously exact-domain-match, genuinely human-annotated by 2 annotators with reported inter-annotator agreement (Cohen's κ = 0.87), and under a license now independently confirmed as **CC-BY-4.0** (resolved via the Zenodo API's machine-readable metadata; a CC0 reference on the page is a stale description-text error, not a competing grant). Caveats: only 3,543 reviews, and labels are **aspect-level** (6 aspects), not a single document-level label — using the "overall experience" aspect as the document-level label is a defensible but explicit methodological choice that must be stated, not assumed.
- **Zenodo 22061934** (Jordanian-Arabic Restaurant, Google Maps) adds volume (8,671 reviews) and is also Google-Maps-sourced and CC-BY-4.0, but the **majority of its sentiment labels are LLM-generated** (Claude Sonnet / GPT-5), validated against only a 75–300-review human gold subset. This must be documented as **weak supervision**, not manual ground truth, everywhere it is used, and that human gold subset should be reserved as a validation slice rather than folded into training.

**Reserve-for-external-evaluation:** HARD (binary-only; license unresolved — no license file found in the GitHub repo or HF dataset card after direct inspection), ArSAS (high label quality but wrong domain — Twitter), LABR/GLARE (wrong domain, large-scale only).

**Reject:** OCLAR (severe imbalance, non-standard rating-3-as-positive handling, unknown license), ar_res_reviews (internally contradictory provenance — page states both "qaym.com" and "Twitter" as source), mteb/HotelReviewSentimentClassification (HARD repackaging — see leakage note §5), AURA-Sentiment and SaudiGovSent (off-domain, no neutral class / unconfirmed accessibility), two low-provenance Kaggle sets (JS-rendered pages prevented verification), SS2030 (Twitter).

## 4. English candidates — final recommendation

**Primary: UCSD/McAuley Google Local Review Dataset, conditional on two unresolved items being addressed before any use beyond this sprint.**

This is the strongest domain match for an English counterpart to the Arabic Google Maps data — the actual platform, essentially unlimited scale, freely downloadable with no access gate (state-level CSV subsets exist for sprint-scale extraction). Two genuine, unresolved gaps:
1. **No sentiment labels exist** — only star ratings. A star→3-class conversion rule must be designed and validated against a small hand-labeled gold sample before being trusted (see methodology plan §3).
2. **No confirmed license.** Direct inspection found no license declaration. This is a real usability constraint, not a formality — it should be escalated (e.g. contacting the McAuley Lab) before any public release of a model or derived dataset trained on it, and this constraint must be stated plainly in the paper's data-availability section.

**Reserve-for-external-evaluation:** Yelp Open Dataset and its five identified repackagings (academic/non-commercial restriction — this applies to *every* Yelp-derived row regardless of re-hosting site, since none of the mirrors independently restate or lift the restriction), TripAdvisor (two Kaggle mirrors disagree on size — 20,491 vs. 6,444 — not reconciled; CC BY-NC 4.0 on the HF/argilla version), SemEval Restaurant ABSA (best English label quality in the pool; useful as an aspect-level cross-check against the Arabic ABSA set), Google Play App Reviews (clean, documented 3-class rule, but app-store not location domain — useful as a structural stand-in only).

**Reject:** Amazon Polarity/Full and `amazon_reviews_multi` (withdrawn/defunct), the Zenodo "AI-generated Google Reviews" set (fully LLM-synthetic text — wrong distribution for a real-world sentiment study; reserve at most for robustness stress-testing, never core training), a brand-new unvetted Yelp Restaurant Zenodo deposit.

## 5. Code-switching — no off-the-shelf dataset exists; strategy revised accordingly

No genuine, accessible Arabic-English code-switched **review-sentiment** dataset was found or could be independently obtained:
- **EESA** (Sherif & Sabty 2024) has the right label scheme (3-class) but wrong domain (YouTube comments) and — confirmed via two additional independent search passes by the auditor, not just the scout's initial pass — **no public download path anywhere** (no GitHub/Kaggle/Zenodo/HF listing). Treat as evidence that the gap exists, not as usable data; pursuing it would require direct author contact with unpredictable turnaround, which the 4-day sprint cannot absorb.
- **SESA-CSD** (Alghamdi et al. 2026) likewise has no confirmed public release path at the time of this audit.
- **Mixat** (Emirati-English podcast speech) has genuine confirmed code-switching (36% of utterances by Code-Mixing Index) but zero sentiment labels and is speech, not text.
- **TUNIZI** and other Arabizi corpora are Tunisian/French-leaning, not Gulf/English.

**Revised strategy (recommended, concurred independently by both the scout and the auditor):** treat code-switching as an **analysis lens applied to the project's own collected Google Maps review data**, not an externally imported labeled resource. Classify each review by a Code-Mixing Index / script-identification heuristic (using Mixat's CMI methodology as a calibration reference) into pure-Arabic / pure-English / Arabizi / genuinely-mixed, then report model performance stratified by that classification. EESA remains cited as literature evidence of the gap (see `research_gap.md`), not listed as project data.

## 6. Leakage and duplication risks (cross-cutting, applies regardless of which datasets are finalized)

Treat the following as **single underlying corpora wearing multiple hosting costumes** — never use two rows from the same family as independent train/test sources without deduplication by review ID or text hash:
- **Yelp family** (5 identified repackagings: Open Dataset, Review Full, Polarity, a Kaggle mirror, a Zenodo deposit)
- **HARD / mteb HotelReviewSentimentClassification** (2 rows, same source corpus)
- **TripAdvisor** (2 Kaggle/HF mirrors with disagreeing sizes)
- **UCSD/McAuley full dump vs. its Kaggle "California" mirror** (same source, re-hosted)

## 7. Is combining the best Arabic and English datasets into one unified study scientifically defensible?

**Yes for building a working system and for an honestly-caveated exploratory comparison. No for a clean causal "Arabic is harder/easier than English" claim**, because the finalists differ simultaneously in label-generating process (human-annotated vs. majority-LLM-annotated vs. self-derived-from-ratings), sub-domain (tourism vs. restaurants vs. general business), era/region, and scale (thousands vs. effectively millions). Any cross-language performance gap found could be fully explained by these confounds rather than a true language-difficulty effect.

**Required mitigation, adopted as a project commitment (see `decisions.md`):** report results stratified by dataset origin, not only by language; build one small, matched-protocol human-annotated validation slice (same annotators, same guidelines, Cohen's κ reported) across self-collected Arabic, English, and code-switched reviews early in Phase 2 — this becomes the only clean cross-language comparison point in the study, with everything else explicitly labeled exploratory/confounded by dataset origin in the limitations section.

## 8. Licensing summary (do not proceed past this sprint without resolving the starred items)

| Dataset | License | Commercial use | Status |
|---|---|---|---|
| Zenodo 17011574 | CC-BY-4.0 (independently confirmed via API) | Yes, with attribution | Resolved |
| Zenodo 22061934 | CC-BY-4.0 | Yes, with attribution | Resolved |
| UCSD/McAuley Google Local | **Unknown — no license found** | Unknown | **Unresolved — escalate before any release** ★ |
| HARD | **Unknown — no license file in repo or HF card** | Unknown | **Unresolved** ★ |
| Yelp family (all 5 rows) | Academic/non-commercial, no redistribution (Yelp's own ToS, inherited by every re-host) | **No** | Resolved (restrictive) |
| TripAdvisor (HF/argilla) | CC BY-NC 4.0 | No | Resolved (restrictive) |

## 9. Final dataset strategy

Primary training/evaluation pool: Zenodo 17011574 (Arabic anchor) + Zenodo 22061934 (Arabic volume, weak-label caveat) + UCSD/McAuley Google Local (English anchor, pending license resolution and validated star→3-class rule). Code-switching handled as a self-collected analysis lens, not an external dataset. All other candidates reserved for external/robustness evaluation only, per §3–5 above.

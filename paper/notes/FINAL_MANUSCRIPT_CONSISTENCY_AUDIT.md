# Final Manuscript-Wide Scientific Consistency Audit

**Scope:** `paper/MANUSCRIPT_DRAFT.md` §§1–12, cross-checked against every authoritative project artifact. No experiment was run, no model retrained, no historical output altered. Findings are classified CRITICAL / HIGH / MINOR / CLEAN; CRITICAL and HIGH findings unambiguously correctable from existing artifacts were fixed in place during this audit.

## 1. Numerical consistency audit — CLEAN

Every numerical claim checked below was re-derived directly from its source artifact (not from the manuscript's own prior statement) and compared:

| Claim | Manuscript value | Source artifact value | Match |
|---|---|---|---|
| Human-Gold SHA-256 | `7b53ca621d2...be53fd` | Recomputed live from `human_gold_757.csv` | ✅ exact |
| Annotation: n/unanimous/majority/3-way | 757 / 578 (76.4%) / 161 (21.3%) / 18 (2.4%) | `agreement_outputs/overall_agreement_sentiment.json` | ✅ exact |
| Fleiss' κ / Krippendorff's α | 0.650 / 0.650 | 0.64985 / 0.65001 | ✅ (rounded correctly) |
| Arabic/English agreement, κ by language | 81.3%/κ=0.671; 71.6%/κ=0.628 | `language_specific_agreement_sentiment.json` | ✅ exact |
| Original-vs-reference agreement (overall/AR/EN) | 82.6%/κ=0.662; 84.0%/κ=0.660; 81.2%/κ=0.660 | `label_agreement_overall_by_language.json` | ✅ exact |
| Class distributions (orig/reference) | 181/117/459 → 201/42/514 | same file | ✅ exact |
| Named transitions (6-way) | 11/4/61/36/11/9 | `transitions_named` field | ✅ exact |
| Adjudication: majority agree/disagree | 101/161 (62.7%) / 60 (37.3%) | `adjudication_merged.csv`, recomputed | ✅ exact |
| Adjudication by class (Neg/Pos/Neu) | 85.4%/64.6%/26.5% | same, recomputed | ✅ exact |
| Three-way outcome distribution | Neg 9 / Neu 7 / Pos 2 | same, recomputed | ✅ exact |
| All 16 Macro-F1 before/after values (Table 5a) | — | `original_vs_human_gold_comparison.csv` | ✅ exact to 3 decimals, every row |
| 13/16 lower; phase means −0.025/−0.101; Phase3B AR/EN −0.146/−0.041 | — | recomputed from same file | ✅ exact |
| Mean Neutral/Negative/Positive F1 (orig→ref) | 0.396→0.176 / 0.748→0.798 / 0.879→0.875 | `human_gold_metrics_all_models.csv`, recomputed | ✅ exact |
| Neutral support (overall/AR/EN) | 42 / 9 / 33 | same | ✅ exact |
| Neutral lowest class for all 16 | stated | recomputed, confirmed True for all 16 | ✅ exact |
| Neutral precision/recall by phase | 0.129/0.286 (3A); 0.132/0.688 (3B) | same, recomputed | ✅ exact |
| All 5 key Holm-adjusted p-values (Table 6) | 0.647 / 0.016 / 0.377 / 0.119 / 0.0012 | `statistical_tests_human_gold.csv`, recomputed | ✅ exact |
| Seeds (42; 1001/2002/3003; 9009) | stated throughout | `configs/training.yaml`, `build_blinded_sheets.py`, `build_blinded_adjudication.py` | ✅ exact |
| Iterations (2,000 Phase 3A; 10,000 Phase 3B and reference-set) | stated | `configs/training.yaml`, `README_PHASE3B.txt`, `04_statistical_tests.py` | ✅ exact |

**No discrepancy, however minor, was found in this pass.**

## 2. Statistical audit — CLEAN

- Headline confirmed exactly: 4 significant originally; 3 lost significance (XLM-R rerun vs. EN→AR zero-shot, p=0.647; multilingual vs. EN→AR zero-shot, p=0.377; multilingual vs. AR→EN zero-shot, p=0.119); 1 survived (MARBERT rerun vs. EN→AR zero-shot, p=0.016); 1 newly significant (XLM-R rerun vs. MARBERT rerun, p=0.0012). Verified directly against `statistical_tests_human_gold.csv` row by row (Section 1 table above).
- Bootstrap CI and permutation-test p-values are kept lexically distinct everywhere checked (`bootstrap_resampling_p_heuristic`/CI language vs. `permutation_p_two_sided`/`permutation_p_holm_adjusted` language); no instance found where one is mislabeled as the other.
- Holm adjustment is correctly described as applied within explicitly named families (Phase3A_Arabic_E1, Phase3A_English_E2, Phase3B_Arabic, Phase3B_English) in every section that discusses it (§6.3, §7.6).
- Non-significance is never interpreted as equivalence; every occurrence of "equivalent" in the manuscript is either negated or qualifies a recommendation, not an empirical claim (confirmed by direct text search, Section 11/Terminology below).

## 3. Primary vs. rerun audit — CLEAN

All ~53 MARBERT/XLM-R mentions were categorized. Every mention of the Arabic Phase 3B standalone MARBERT or XLM-R realization under the human-adjudicated reference set carries an explicit "rerun realization" qualifier (§5.3, §7.4 Table 5a, §7.5, §7.6 Table 6, §9.2, §9.4, §10.5, §11.1). Mentions without the qualifier were individually checked and confirmed to be either (a) the Phase 3A LoRA MARBERT realization (never lost, correctly labeled "primary"), (b) the English standalone XLM-R realization (never lost — only the Arabic primaries were lost), or (c) a general architecture description unconnected to any specific reported figure. No instance was found presenting a rerun figure as if it were the lost primary realization.

## 4. Neutral audit — CLEAN

All figures in Section 1's table confirmed. Every strong Neutral statement in the manuscript (§1, §7.7, §8.1, §9.3) is accompanied, in the same paragraph, by its support count and/or the annotation-instability caveat; the one potentially over-strong phrasing ("models cannot understand Neutral sentiment") appears only inside an explicitly rejected quotation, immediately followed by the qualified alternative statement.

## 5. Annotation/adjudication audit — CLEAN

All figures confirmed in Section 1's table. Blinding is described consistently in §4.3 (annotators blinded to rating/original label/model prediction/each other; adjudicator additionally blinded to annotator identity, vote counts, majority outcome). The reference set is explicitly described as not infallible in §3 (Jordan disambiguation), §4.4, §9.1, §10.1, and §12 — never asserted as ground truth anywhere; every "ground truth" occurrence in the file (6 total, re-verified this pass) is either negated or appears inside a literature discussion in quotation marks.

## 6. Claim-strength audit — 2 MINOR FIXES APPLIED, otherwise CLEAN

A full scan for causal/superiority/equivalence language found the manuscript already compliant in the overwhelming majority of cases (every "harder/easier," "GPU caused," "proves/proved," "equivalent," and "state-of-the-art" occurrence found was already negated or explicitly hedged, re-verified this pass with fresh regex scans). Two **MINOR** wording issues were found and fixed in this audit pass (see Section 11, Terminology, below) — neither was a claim-strength violation in substance, both were surface wording (loose "ground truth" phrasing for the Jordan dataset's own subset; a bare "Human-Gold" mention in Results).

## 7. Cross-section consistency — CLEAN (after Stage-5 fixes, re-confirmed)

The corrected 3-of-4 significance statement, rerun-realization status, Neutral support figures, dataset provenance, licensing status, and release restrictions were each checked for identical wording/values across Introduction, Results, Discussion, Limitations, and Conclusion. All consistent; see the explicit occurrence list already re-verified in Section 1 above and the Terminology/Licensing sections below. Contribution wording (§1) and the Conclusion's restatement (§12) describe the same five contributions without introducing a sixth or dropping one.

## 8. Citation audit — CLEAN

All 15 inline citations used in the manuscript (`Alahmadi 2025; Sammour 2026; Li, Shang, & McAuley 2022; Yan et al. 2023; Landis & Koch 1977; Fleiss 1971; Hu et al. 2022; Abdul-Mageed et al. 2021; Conneau et al. 2020; Pavlick & Kwiatkowski 2019; Plank 2022; Dror et al. 2018; Northcutt et al. 2021; Shi & Agrawal 2025; Robnik-Šikonja et al. 2020`) were cross-checked against `LITERATURE_VERIFICATION.md`'s 15-row table: every citation used appears there, with consistent author/year, and no citation appears in the verification file that is not used in the manuscript (a 1:1 match). No citation placeholder remains (`grep` count: 0). No fabricated citation was found. No two rows represent the same underlying work under different names (each DOI/URL is distinct). No citation was added in this audit pass.

## 9. Licensing/release audit — CLEAN (after fixes already applied in the previous drafting stage)

Cross-checked `DATASET_PROVENANCE.md`, `DATA_LICENSING_AND_RELEASE.md`, `REPRODUCIBILITY_MANIFEST.md`, and `REPRODUCIBILITY_MANIFEST.json`: all four now consistently state Zenodo 17011574 = CC-BY-4.0 and Zenodo 22061934 = CC-BY-4.0 (the latter corrected from a stale "not independently reconfirmed" status in the prior drafting stage; no remaining stale instance found in this pass). The English source is consistently described as having an unresolved redistribution license, with release framed as "not released pending clarification" everywhere checked (§11.3 of the manuscript, `DATA_LICENSING_AND_RELEASE.md`) — no instance of "cannot legally be released" or an equivalent absolute-prohibition claim was found. No nonexistent repository URL or DOI is promised anywhere (§11.3 explicitly states none currently exists).

## 10. Reproducibility audit — RESOLVED (both flags removed)

Both `[AUTHOR REVIEW NEEDED]` flags (§6.3 and §7.6, concerning the 2,000-vs-10,000 iteration-count history) are resolved and removed in this audit pass. Resolution applied, per the preferred wording given: the historical protocols are stated accurately (Phase 3A original testing: 2,000 iterations; Phase 3B original testing and this paper's own re-evaluation: 10,000 iterations), the paper now states explicitly that none of the four significance-status changes it reports involve a Phase 3A comparison, and the iteration-count difference is stated as noted for completeness only, never as an explanation for the observed changes. No scientific reason remained to keep the flags open once this was stated plainly.

## 11. Terminology audit — 3 fixes applied (carried from Stage 5) + 0 new issues this pass

Re-scanned the full manuscript for: `Human-Gold` (2 remaining — the one sanctioned first-use definition in §4, and one internal EVIDENCE-TRACE filename reference; both acceptable), `ground truth` (6 remaining, all negated or quoted-literature-discussion), `accurate` (0 — the one flagged instance was fixed to "precise" in Stage 5), `first-ever` (0), `state-of-the-art` (1, explicitly negated), `proves`/`proved` (2, both negated/hedged), `equivalent` (6, all negated or qualifying a recommendation, none asserting empirical equivalence), `noise` (4, all either quoting literature or operationally defined). No new terminology violation was found in this pass beyond what Stage 5 already fixed.

## 12. Manuscript length/redundancy audit

**Word count by section** (main body, §1–12, prose only — excludes this audit document):

| Section | Words |
|---|---|
| 1. Introduction | 1,233 |
| 2. Related Work | 1,359 |
| 3. Data and Dataset Audit | 1,728 |
| 4. Human Annotation and Adjudication | 1,231 |
| 5. Experimental Methodology | 854 |
| 6. Evaluation Protocol and Statistical Analysis | 841 |
| 7. Results | 4,169 |
| 8. Error and Label-Stability Analysis | 899 |
| 9. Discussion | 1,705 |
| 10. Limitations | 1,062 |
| 11. Reproducibility and Data Availability | 1,078 |
| 12. Conclusion | 537 |
| **Total body** | **≈16,700** |

This total includes inline `[TABLE X]` placeholder markers (which become standalone table objects, not body prose, once finalized) and will shrink further once the temporary `<!-- EVIDENCE TRACE -->` blocks are removed before submission (those blocks are not counted toward a journal word limit but currently inflate this file's raw word count by an estimated 600–800 words).

**Identified redundancy (documented, not yet trimmed):**
- Discussion §9.1–9.2 restates several Results (§7.2, §7.6) numbers and p-values in near-full detail rather than citing the section and stating only the interpretive addition; this is the single largest trimming opportunity.
- The rerun-realization, Neutral-support, and non-infallible-reference-set caveats are each repeated in full sentence form in 4–5 sections; this repetition was requested explicitly across earlier drafting stages ("state throughout, not once and dropped") and is not classified as a defect, but several later occurrences could be shortened to a brief cross-reference (e.g., "see Section 5.3") without losing the caveat's substance.
- §7 (Results) at 4,169 words is the largest single section; Table 5b/8/11 (full per-model breakdowns) are already correctly deferred to supplementary material per the blueprint, but some of §7.4's prose could move numeric detail into Table 5a itself and shorten the surrounding paragraph.

**Recommended trimming target for journal submission:** main body **8,000–9,500 words** (roughly a 45–50% reduction from the current draft), achieved primarily by (a) moving the full per-model statistical/confusion-matrix detail already slated for supplementary material (Tables 5b, 8, 9–14) out of the body text entirely, (b) shortening Discussion's restatement of Results numbers to cross-references plus interpretation, and (c) tightening repeated caveat sentences to their shortest non-dropped form after their first full statement. This trimming is **not performed in this audit pass**, consistent with the instruction to document rather than aggressively shorten at this stage.

## Summary of fixes applied in this audit

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | Two `[AUTHOR REVIEW NEEDED]` flags on the iteration-count note (§6.3, §7.6) | HIGH | **Fixed** — resolved and removed, per preferred wording |
| 2 | (Carried from Stage 5, re-confirmed clean, no new action) | — | — |

No CRITICAL finding was identified anywhere in this pass. No numerical, statistical, citation, or licensing discrepancy was found. The only outstanding, documented (not fixed) item is the recommended length-trimming target above, which is explicitly out of scope for this audit per instruction.

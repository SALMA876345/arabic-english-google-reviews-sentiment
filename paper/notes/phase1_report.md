# Phase 1 Final Report

**Project:** Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews
**Date:** 2026-10-24
**Status:** Phase 1 complete (literature/dataset verification + experimental design only; no training performed). Reviewed by an independent adversarial agent pass — zero blocking issues, five wording fixes applied (see `docs/decisions.md` D8).

## A. Best dataset strategy
Combine two Google-Maps-sourced Zenodo releases for Arabic (one small/human-annotated anchor, one larger/LLM-weak-labeled volume set) with the UCSD/McAuley Google Local Review Dataset for English (huge scale, rating-derived labels, license unresolved). Treat code-switching not as an imported dataset but as a stratification lens applied to self-collected data in Phase 2, since no accessible genuine Arabic-English code-switched review-sentiment dataset exists. Full detail: `docs/dataset_audit.md`.

## B. Best Arabic dataset candidate
**Zenodo 17011574** — "Arabic Google Maps Reviews Dataset for Tourism in Saudi Arabia" (MDPI *Data* 2025). 3,543 reviews, genuinely human-annotated (2 annotators, Cohen's κ=0.87), CC-BY-4.0 (license conflict on the page independently resolved). Highest-scoring dataset in the entire pool (3.6/5). Paired with **Zenodo 22061934** (Jordanian-Arabic restaurant reviews, 8,671 reviews, majority LLM-generated labels) for volume.

## C. Best English dataset candidate
**UCSD/McAuley Google Local Review Dataset** — ~666M reviews, genuine Google Maps platform match, freely downloadable. No native sentiment labels (must derive from star ratings, validated against a gold subset) and no confirmed license (a real, unresolved legal gap — escalation required; fallback to SemEval Restaurant ABSA if unresolved).

## D. Best genuine code-switch candidate
**None usable.** EESA (Sherif & Sabty 2024) has the right label scheme but is YouTube-domain and confirmed to have no public download path after two independent verification passes. SESA-CSD (Alghamdi et al. 2026) has the same accessibility problem. Both are cited as literature evidence of the gap, not used as project data.

## E. Is combining datasets scientifically defensible?
**Yes for building a working system and an honestly-caveated exploratory study. No for a clean causal "Arabic vs. English" claim** — the finalists differ simultaneously in label-generating process, sub-domain, era, and scale, so language effects are confounded with dataset-origin effects. Mitigation: report results stratified by dataset origin, and build one small matched-protocol human-annotated validation slice as the only clean comparison point. Full analysis: `docs/dataset_audit.md` §7.

## F. Recommended final sentiment label scheme
3-class, document-level: Positive / Neutral / Negative. Every dataset's label provenance is tracked and reported using one of three distinct terms — human-annotated ground truth, rating-derived sentiment labels, or weak/LLM-generated labels — never conflated. Aspect-level labels (Zenodo 17011574) are aggregated to document-level via a documented, validated rule, not assumed.

## G. Confirmed or revised research gap
Confirmed, narrowed: no identified prior work performs sentiment classification on Arabic-English **code-switched Google Maps/location-business reviews**. Both components of this gap (code-switched Arabic-English sentiment in general, and Arabic Google Maps review sentiment in general) individually have recent prior work (2023–2026) — the intersection does not. Novelty claim is explicitly provisional on (1) successful Phase 2 code-switched data collection and (2) a literature blind spot in English-indexed search venues not yet checked against Arabic-language sources. Full detail: `docs/research_gap.md`.

## H. Confirmed or revised research questions
RQ1, RQ2, RQ4 confirmed as originally scoped. **RQ3 revised**: reframed to explicitly ask how much of any observed Arabic/English/code-switched performance difference is attributable to language versus dataset-origin/label-source confounds, answerable cleanly only via the matched-protocol validation slice (not yet built). Full wording: `docs/methodology_plan.md` §1.

## I. Main risks
1. Structural scarcity of large, human-annotated, document-level Arabic review data (not fixable by more searching).
2. UCSD/McAuley's license is genuinely unconfirmed — a real legal gap requiring escalation before any public release.
3. The matched-protocol validation slice that would make RQ3 scientifically clean does not exist yet and depends on unresolved Phase 2 collection feasibility (Places API access or an equivalent ToS-compliant path).
4. Code-switched (Group D) sample volume in the eventual corpus is unknown and may be small.
5. The novelty claim's literature search has an English-venue blind spot not yet checked against Arabic-language sources.

## J. Exact next step
Awaiting your approval to begin **Phase 2**: (1) download and license-escalate the three primary datasets, (2) build the preprocessing/language-ID/CMI pipeline, (3) attempt Places-API-based (or equivalent ToS-compliant) collection of a small matched-protocol bilingual validation slice, (4) implement — but not yet run final evaluation on — the baseline and transformer training scripts per `docs/methodology_plan.md`. No model training begins until you confirm.

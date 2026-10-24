# Data Quality & Methodology Audit — Phase 1

**Project:** Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews (3-class: Positive/Neutral/Negative)
**Role:** Data Quality & Methodology Auditor (independent critical review of three scout reports)
**Date:** 2026-10-24
**Inputs audited:** `arabic_datasets_raw.md` (14 candidates), `english_datasets_raw.md` (13 candidates), `codeswitch_datasets_raw.md` (code-switching landscape)
**Companion deliverable:** `data/dataset_inventory.csv` (34 rows, one per serious candidate)

This audit does not restate the scout findings. It (a) resolves or confirms-as-unresolved the specific inconsistencies flagged in the task, (b) applies a documented 12-dimension scoring rubric to every serious candidate, (c) flags cross-cutting risks, (d) gives a USE/COMBINE/REJECT/RESERVE-FOR-EXTERNAL-EVALUATION verdict per candidate, and (e) assesses whether combining the best Arabic and English datasets into one study is scientifically defensible.

---

## 1. Resolution of flagged inconsistencies (independent verification performed in this audit)

### 1.1 Zenodo 17011574 (Arabic Google Maps Tourism dataset) — license conflict: RESOLVED

Checked the record's machine-readable metadata directly via the Zenodo API (`zenodo.org/api/records/17011574`), which is the authoritative source for a record's governing license (as opposed to free-text description fields, which can be stale or miscopied). The API's `license` field returns **`cc-by-4.0`**. A separate fetch of the human-facing page corroborated this: the page's "Rights" section explicitly displays "Creative Commons Attribution 4.0 International," while the CC0 mention appears only in free-text description copy — i.e., the CC0 reference is a documentation inconsistency on the page itself, not a competing license grant.

**Verdict: CC-BY-4.0 is the governing license.** Attribution is required for any use (including commercial). The scout was right to flag the inconsistency; it is resolvable and should not be treated as an open legal question going forward — but future redistributions of this dataset should correct the description text to avoid perpetuating the CC0 confusion.

### 1.2 HARD size discrepancy (93,700 / 105,698 / 373,750 / 490,587) — PARTIALLY RESOLVED

Direct fetch of the canonical GitHub README confirms two numbers in the authors' own hands: **93,700** reviews (balanced version, 46,850 positive / 46,850 negative) and **373,750** reviews (unbalanced/"clean" version). A separate search surfaced **490,587** as the figure stated in the original Springer paper's own abstract/description — this most plausibly represents the **raw scraped corpus before cleaning**, with 373,750 being the cleaned/deduplicated "unbalanced" release and 93,700 the final balanced release derived from it. Under that reading, three of the four numbers form a coherent pipeline (raw → cleaned → balanced), not a contradiction.

**The fourth figure, 105,698, remains unresolved** — it appears only in a secondary GitHub project description, with no traceable link back to an official HARD release stage. Treat it as a likely miscitation of a different subset (possibly a train/test split size from a downstream paper) and **do not use it** without finding its source. The license question could NOT be resolved: direct inspection of both the GitHub README and the HF dataset card confirms **no license file or declaration anywhere** — this is a genuine, unresolved gap, not scout imprecision.

### 1.3 EESA public availability — CONFIRMED STILL UNRESOLVED (not an artifact of scout limitations)

Ran two additional independent search passes (general web search for "EESA dataset download/github/zenodo," and an attempt to fetch a 2026 ABJADNLP paper that cites EESA, which failed due to PDF extraction issues) specifically to try to find a download path the scout may have missed. **No public GitHub, Kaggle, Zenodo, or Hugging Face listing was found.** The dataset is cited as a benchmark by at least one 2026 paper (SwitchEmbed), confirming it is obtainable by some researchers, but no open-access link exists in any indexed source as of this audit. **This should be treated as confirmed-unavailable for this project's timeline, not merely "unverified."** If the team wants to pursue it, the only path is direct author contact (Sherif & Sabty, likely German University in Cairo) — budget for this to fail within a 4-day sprint, since author-request turnaround is unpredictable. Cite EESA as evidence of the gap; do not plan around it as usable data.

### 1.4 Other quick checks performed
- **Yelp Polarity construction-rule discrepancy** (1,2=neg/3,4=pos vs. the standard 1,2=neg/4,5=pos-drop-3): **not resolved** — would require pulling the actual HF loading script, which was out of scope for the 1-2 search budget. Flagged as an open risk in the inventory; do not trust either stated rule without checking the script directly before using this dataset.
- **TripAdvisor Kaggle mirror size disagreement** (20,491 vs. 6,444): not independently reconciled; treated as an open integrity flag, consistent with the scout's finding.

---

## 2. Scoring rubric (12 dimensions, 0–5 each)

| # | Dimension | What a 5 looks like | What a 0 looks like |
|---|---|---|---|
| 1 | Domain Relevance (DR) | Exact match: Google-Maps-style location/business reviews | Totally different domain (e.g., NLI, e-commerce) |
| 2 | Arabic Quality (AQ) | Real, well-documented Arabic text, dialect-aware | No Arabic present, or undocumented/unverifiable quality |
| 3 | English Quality (EQ) | Real, clean, well-documented English review text | No English present, or undocumented quality |
| 4 | Code-Switch Coverage (CSc) | Confirmed, quantified, genuine intra-sentence Arabic-English mixing | No code-switching, or claimed but unverified |
| 5 | Dataset Size (SZ) | Large enough for robust 3-class fine-tuning (tens of thousands+) | Unusably small or size itself unverified |
| 6 | Label Reliability (LR) | Genuine multi-annotator human sentiment labels w/ agreement reported | No labels, or fully synthetic/unverifiable labels |
| 7 | Class Balance (CB) | Documented, reasonably balanced 3-class distribution | Severely skewed or totally unknown distribution |
| 8 | Provenance (PR) | Peer-reviewed, well-documented collection methodology | No paper, contradictory/vague sourcing description |
| 9 | Licensing Clarity (LC) | Explicit, permissive, verified license | No license info, or confirmed hard restriction |
| 10 | Reproducibility (RP) | One-click open download, maintained tooling | Gated, request-only, or confirmed dead/unavailable |
| 11 | Research Novelty Value (NV) | Fills a genuine gap in this exact project's niche | Redundant with better-known resources, adds nothing new |
| 12 | Comparability Across Languages (CL) | Structurally/methodologically poolable with a counterpart dataset in the other language | Structurally incompatible with any cross-language pairing |

Dimension not applicable to a given dataset (e.g., English Quality for an Arabic-only dataset) is excluded from that dataset's average rather than scored as 0, so overall scores remain comparable across monolingual and bilingual candidates. Full per-dimension scores for all 34 candidates are in the working notes below; only the shortlist candidates get full narrative justification (scoring all 34 line-by-line in prose would bury the signal — the CSV's `overall_score` column carries the computed result for every row).

### 2.1 Top-tier scores (≥2.5/5) — full justification

| Dataset | DR | AQ | EQ | CSc | SZ | LR | CB | PR | LC | RP | NV | CL | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Arabic Google Maps Tourism (Zenodo 17011574) | 5 | 5 | n/a | 0 | 1 | 5 | 3 | 5 | 4 | 4 | 5 | 3 | **3.6** |
| Jordanian-Arabic Restaurant (Zenodo 22061934) | 5 | 4 | n/a | 0 | 4 | 2 | 2 | 3 | 4 | 4 | 4 | 3 | **3.2** |
| UCSD/McAuley Google Local | 5 | n/a | 3 | 0 | 5 | 1 | 2 | 3 | 1 | 4 | 4 | 4 | **2.9** |
| HARD | 3 | 4 | n/a | 0 | 5 | 1 | 4 | 3 | 1 | 5 | 2 | 2 | **2.7** |
| SemEval-14/16 Restaurant ABSA | 3 | n/a | 4 | 0 | 0 | 5 | 2 | 5 | 2 | 3 | 3 | 3 | **2.7** |
| EESA | 2 | 3 | 3 | 5 | 1 | 4 | 2 | 3 | 0 | 0 | 5 | 4 | **2.7** |
| LABR | 1 | 3 | n/a | 0 | 5 | 1 | 3 | 4 | 2 | 5 | 1 | 2 | **2.5** |
| GLARE | 2 | 3 | n/a | 0 | 5 | 0 | 2 | 4 | 4 | 4 | 2 | 2 | **2.5** |
| ArSAS | 0 | 4 | n/a | 0 | 3 | 5 | 3 | 4 | 2 | 3 | 2 | 2 | **2.5** |
| Yelp Open Dataset | 4 | n/a | 3 | 0 | 5 | 1 | 2 | 4 | 0 | 3 | 2 | 3 | **2.5** |

**Why the Zenodo 17011574 tourism dataset wins decisively on quality despite being the smallest serious candidate:** it is the only dataset in the entire pool — Arabic or English — with (a) the exact target domain, (b) genuinely human-annotated labels with a reported, strong inter-annotator agreement statistic (Kappa 0.87), and (c) a now-resolved, permissive license. Every other high scorer wins on scale or provenance but loses heavily on label reliability (rating-derived), domain match, or license clarity. This is the clearest signal in the whole audit: **label-quality and domain-match are the scarce resources here, not raw volume.**

**Why EESA scores respectably (2.7) despite being functionally unusable right now:** its *potential* value (NV=5, CL=4 — matching label scheme) is real, but it is dragged down by LC=0 and RP=0 because access is unresolved even after independent verification. A dataset that cannot be obtained cannot be relied upon, regardless of how well it would fit on paper — this is why it is recommended RESERVE, not COMBINE.

---

## 3. Red-flag matrix for top candidates (shortlist only)

| Dataset | Duplicate risk | Train/test leakage risk | Synthetic/LLM label risk | Weak provenance | Label noise | Rating/text disagreement risk | Class imbalance severity | Domain mismatch | Contamination risk if combined |
|---|---|---|---|---|---|---|---|---|---|
| Zenodo 17011574 (Tourism) | Low | Low (standalone, small) | None (human-annotated) | Low | Low (Kappa 0.87) | Low | Unknown (counts not published) — **moderate** | None (exact match) | Low — distinct source from everything else |
| Zenodo 22061934 (Jordanian restaurant) | Low | Low (standalone) | **High** — majority of labels LLM-generated | Moderate (no peer review confirmed) | **High** for the non-gold-validated majority | Moderate (LLM may mis-parse mixed-sentiment reviews) | Unknown — unquantified | None (exact match) | Low standalone, but combining its LLM-labeled majority with human-labeled data in the same training pool risks silently degrading overall label quality |
| HARD | **High** vs. mteb/HotelReviewSentimentClassification (same source) | **High** if HARD + mteb subset both used | None (rating-derived, not LLM) | Moderate (size figures needed reconciliation; license absent) | Moderate (mixed praise+complaint reviews noted by authors) | Moderate-High (binary collapse of 1-5 stars hides real ambivalence) | Low in balanced version; severe in raw/unbalanced | Moderate (hotel-only, not general places) | **High** — any other HARD-derived repackaging (mteb, future Kaggle mirrors) must be deduplicated by review ID/text hash before pooling |
| UCSD/McAuley Google Local | Low internally; **moderate** vs. Kaggle "California" mirror (same source, re-hosted) | Moderate if both the full dump and the Kaggle mirror are used | None | Low-moderate (two cited papers, but no dataset-specific paper/DOI) | High if self-derived rating→sentiment rule is applied naively (no validation step) | **High** — this is the central open risk: no validated conversion rule exists, and review text/rating disagreement is a well-known phenomenon (e.g., sarcastic 5-star reviews, apologetic 1-star reviews) | Unknown (not measured) | None (exact platform match) | Low alone; high if pooled with the Kaggle CA mirror without dedup |
| Yelp Open Dataset + derivatives (Review Full / Polarity / Kaggle / Zenodo repackagings) | **High across all five Yelp-derived rows** — same underlying corpus repackaged five different ways | **High** — several of these are literal subsets/resamples of the same source; using two in train vs. test is a direct leak | None (rating-derived) | Moderate (official source well documented; derivatives vary) | Low-moderate | Moderate (same sarcasm/ambivalence risk as any star-derived set) | Varies — official set unknown, benchmark cuts balanced by construction | Moderate (business reviews, but US/Canada-only regional/cultural skew vs. Gulf-region Arabic reviews) | **Very high** — treat all five Yelp-family rows as ONE dataset for any train/test split purpose, never as five independent sources |
| EESA | Low (standalone) | N/A (not currently obtainable) | None claimed (human-annotated per paper) | Moderate (peer-reviewed paper, but protocol not independently verified) | Unknown | Unknown | Unknown | Moderate (YouTube, not reviews) | N/A until access is secured |

**Cross-cutting pattern:** the single largest systemic risk in this space is **duplicate/leakage risk among same-origin repackagings** — Yelp (5 rows), HARD/mteb (2 rows), and TripAdvisor (2 rows) each represent one underlying corpus wearing multiple hosting costumes. Any pipeline that treats these as independent "different datasets" for augmentation purposes will silently leak test examples into training.

---

## 4. Recommendations per dataset (summary — full reasoning for every row is in `data/dataset_inventory.csv`, column `recommended_use`)

**Arabic — COMBINE (primary):** Zenodo 17011574 (Tourism, anchor/gold validation set) + Zenodo 22061934 (Jordanian restaurant, bulk training volume, LLM-label caveat prominently documented).
**Arabic — RESERVE-FOR-EXTERNAL-EVALUATION:** HARD (binary-only, license unresolved), ArSAS (wrong domain but high label quality), LABR/GLARE (wrong domain, future scale-up only).
**Arabic — REJECT:** OCLAR, ar_res_reviews, mteb/HotelReviewSentimentClassification, AURA-Sentiment, SaudiGovSent, the two low-provenance Kaggle sets, SS2030.

**English — COMBINE (primary):** UCSD/McAuley Google Local, conditional on (a) explicitly documenting and validating the star→3-class conversion rule against a small hand-labeled gold subset, and (b) resolving the license question before any use beyond coursework.
**English — RESERVE-FOR-EXTERNAL-EVALUATION:** Yelp Open Dataset and its family (non-commercial-only, document the restriction prominently), TripAdvisor (both versions, pending mirror reconciliation / non-commercial use), SemEval ABSA (best label quality in English pool, useful as an aspect-level cross-check against the Zenodo 17011574 Arabic ABSA set), Google Play App Reviews (3-class structural stand-in).
**English — REJECT:** Amazon Polarity/Full, amazon_reviews_multi (defunct), AI-generated Google Reviews (synthetic — reserve only for robustness testing, never core training), Yelp Restaurant Zenodo deposit (unvetted, brand-new).

**Code-switching:** no USE or COMBINE candidate exists. EESA is RESERVE-FOR-EXTERNAL-EVALUATION *only if* access is secured (treat as unlikely within a 4-day sprint). Mixat, ArzEn, CSCS are RESERVE as linguistic reference tools (CMI calibration), never as sentiment data (none have sentiment labels). Adouane's Algerian corpus and TUNIZI are REJECT as data (wrong L2 language) but RESERVE as annotation-methodology templates. CS-SNLI and ArE-CSTD are REJECT for sentiment use (no sentiment layer, synthetic text) and RESERVE at most for CS-aware pretraining augmentation.

**Recommended primary strategy for code-switching (concurring with the scout's own recommendation, independently verified as sound):** treat code-switching as an **analysis lens applied to the project's own scraped Google Maps review data**, not as an externally sourced labeled dataset. Classify each self-collected review by a Code-Mixing Index or script/language-ID heuristic (using Mixat's CMI methodology as the calibration reference), then report model performance stratified by that classification. This is more defensible than importing an off-domain, access-uncertain external corpus, and it turns the absence of a ready-made dataset into a legitimate methodological contribution rather than a gap to apologize for.

---

## 5. Is combining the best Arabic and English datasets into one unified study scientifically defensible?

**Short answer: defensible for building a working system and for engineering-level benchmarking; NOT defensible for drawing a clean causal "Arabic vs. English" comparison without explicit caveats and mitigation.**

### 5.1 The core problem: dataset effects are confounded with language effects

The best Arabic candidates (Zenodo 17011574: human-annotated, tourism, 2025, 3,543 reviews; Zenodo 22061934: LLM-annotated, restaurant, 2026, 8,671 reviews) and the best English candidate (UCSD/McAuley: self-derived labels, general local business, 2021, effectively unlimited size) differ from each other along **every axis simultaneously**:

- **Label source:** genuine human annotation (Arabic tourism) vs. majority-LLM annotation (Arabic restaurant) vs. self-derived rating conversion (English). These are three different label-generating processes, not one.
- **Sub-domain:** tourism attractions vs. restaurants vs. general local businesses (mixed categories).
- **Collection era and region:** 2025 Saudi tourism vs. 2026 Jordanian restaurants vs. 2021 US-dominant local businesses.
- **Scale:** thousands vs. functionally millions — any model trained on the pooled set will be dominated by whichever language's data is larger, which is itself an artifact of dataset availability, not a property of the languages.

If a resulting paper reports "the model performs worse on Arabic than English," that finding could just as validly be explained by: the Arabic data being 100-1000x smaller, the Arabic labels being partly LLM-generated vs. the English labels being rating-derived (a different noise profile, not necessarily worse or better), or the sub-domain mix differing (tourism/restaurant vs. general business). **None of these confounds can be separated from a true language-difficulty effect using the datasets as currently found.** This is a real internal-validity threat, not a cosmetic one.

### 5.2 Label-scheme compatibility

On the positive side, the label schemes are reconcilable with effort:
- Zenodo 17011574 is aspect-level 3-class; it can be converted to document-level by using the "Overall Experience" aspect alone, or by aggregating across aspects — but this is itself a methodological choice that must be documented and validated, not treated as free.
- UCSD/McAuley has no labels at all; a 1-2/3/4-5 star-to-3-class rule must be invented and should be validated against a small human-labeled gold sample (ironically, the Zenodo 17011574 annotation protocol — 2 annotators, Kappa reporting — is a good template for building that validation slice).
- The Jordanian restaurant dataset's LLM-generated labels are at least nominally on the same 3-class scheme, but their error profile is unknown and likely systematically different from both the human-annotated Arabic set and the rating-derived English set.

So the three candidate pools can be *forced* onto a common 3-class document-level scheme, but each requires a different, non-trivial adaptation step, and each adaptation step introduces its own label-noise profile. A reader comparing results across languages is implicitly also comparing across these three different noise profiles.

### 5.3 Recommended mitigations if the team proceeds with combination

1. **Report results stratified by dataset origin, not only by language.** This makes the confound visible instead of hiding it inside an aggregate "Arabic" vs. "English" number.
2. **Build one small, truly matched human-annotated slice.** Apply the exact same annotation protocol (2 annotators, same guidelines, Kappa reported) to a small sample of both the project's own scraped Arabic and English Google Maps reviews. This slice — even if only a few hundred examples per language — becomes the only truly clean comparison point in the study; everything else should be labeled "exploratory / confounded by dataset origin" in the paper's limitations section.
3. **Document and validate every label-derivation rule** (rating→3-class for English, aspect-aggregation for the Arabic ABSA set, LLM-label spot-checking for the Jordanian set) against a human-labeled reference subset before trusting it, following exactly the pattern the scouts already flagged as missing.
4. **Deduplicate aggressively before pooling** any same-origin repackagings (Yelp family, HARD/mteb, TripAdvisor mirrors) to avoid train/test leakage, per Section 3 above.
5. **Favor the project's own freshly scraped Google Maps reviews (Arabic + English + mixed) as the primary evaluation set**, using all external datasets strictly as supplementary training signal or as out-of-domain robustness checks — this sidesteps most of the domain/era/label-source confounds because at least the *domain and collection methodology* are held constant across languages, even if volume still differs.

### 5.4 Verdict

Combination is **scientifically usable** for engineering purposes (building a functioning bilingual sentiment classifier) and for an honestly-caveated exploratory comparison, but it is **not defensible as a clean causal claim** about inherent cross-language difficulty without the matched-slice mitigation in 5.3.2. The team should commit to self-collecting a small matched-protocol bilingual validation set early — it is the single highest-leverage action available to make the eventual cross-language comparison in the paper defensible rather than confounded.

---

## 6. Most serious unresolved risks (not fixable by more desk research within this sprint)

1. **No large, human-annotated, document-level, review-domain Arabic dataset exists at scale.** The best candidate (Zenodo 17011574) is genuinely high-quality but tiny (3,543) and aspect-level; the only sizeable alternative (Zenodo 22061934, 8,671) is majority LLM-labeled. This is a structural data-scarcity problem, not a research-pass oversight.
2. **No formally confirmed license exists for the best-fit English dataset (UCSD/McAuley).** This is a real legal gap for anything beyond coursework-scale academic use and should be escalated (e.g., email the lab) before any public release of a model or derivative dataset trained on it.
3. **EESA's inaccessibility is now confirmed, not merely suspected**, closing off the one dataset that would have let the project cite a genuine, scheme-matched Arabic-English code-switched sentiment benchmark. The project should proceed on the assumption that no external CS-sentiment dataset will become available in time, and build its code-switching contribution entirely from self-collected data (Section 4).

Everything else audited (Yelp-family redistribution restrictions, HARD's license gap, the various Kaggle provenance gaps) is a known, bounded, documentable risk rather than an open unknown — those just need to be stated plainly in the paper's data section, not resolved.

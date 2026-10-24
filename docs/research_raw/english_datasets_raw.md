# English Sentiment Dataset Scouting — Raw Findings

**Project:** Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews
**Phase:** 1 — Dataset discovery/audit (no modeling, no decision made yet)
**Scout:** English dataset candidates
**Date compiled:** 2026-10-24
**Method:** Web search (Google Dataset Search style queries) across Hugging Face Datasets, Kaggle, Zenodo, Mendeley Data, UCI, GitHub, and institutional pages. All fields verified via search snippets / fetched pages where noted; anything not directly verifiable is marked `unknown`.

> Caution: this is a raw, unfiltered research log. Numbers and claims below come from dataset cards, Kaggle pages, Zenodo records and search-engine summaries of those pages — they have NOT been independently re-derived (e.g., no file was downloaded and counted). Treat all counts as "as stated by source," not ground truth. A proper Phase 2 audit should re-verify the top picks by actually downloading a sample.

---

## 1. UCSD / McAuley Lab — Google Local Review Dataset (2021)

- **Name / URL:** Google Local review data — https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/ (also mirrored at https://jiachengli1995.github.io/google/index.html and listed on https://cseweb.ucsd.edu/~jmcauley/datasets.html)
- **Associated paper(s):**
  - Li, J. et al., "UCTopic: Unsupervised Contrastive Learning for Phrase Representations and Topic Mining," ACL 2022.
  - Yan, A. et al., "Personalized Showcases: Generating Multi-Modal Explanations for Recommendations," SIGIR 2023.
  - DOI: unknown (no DOI found for the dataset itself; cite the two papers per site instructions).
- **Sample count:** ~666.3 million reviews, 113.6 million unique users, 4.96 million businesses, covering all 50 US states + DC, through September 2021.
- **Label scheme:** No sentiment labels. Only 1–5 star rating + free text. Sentiment would need to be derived (e.g., 1–2=neg, 3=neutral, 4–5=pos, or similar rule chosen by us).
- **Label source:** N/A (no sentiment label present at all) — would be 100% rating-derived if we construct one.
- **Domain:** Google Maps / Google Local reviews — real businesses, real users. This is the closest domain match to the Arabic Google Maps review data in this project.
- **Text quality notes:** unknown from search alone — no public spam/duplicate-rate statistics found. Dataset includes user images and business owner responses alongside review text, which is a good sign of authenticity but also means heavy cleaning will likely be needed (HTML artifacts, non-English text mixed in, possible bot/spam reviews — not documented, must be audited directly).
- **License:** Not explicitly published as a formal license (no CC/MIT/etc. tag found). The McAuley Lab's general stance across its datasets (Amazon, Goodreads, etc.) is "collected for academic/research use; cite our papers; don't redistribute." No explicit commercial-use grant or prohibition could be found in search results — this is a **real gap**, flagged as unknown/ambiguous rather than assumed permissive.
- **Accessibility:** Freely downloadable without an access request form — direct links to compressed JSON files per state, hosted at `datarepo.eng.ucsd.edu`. Smaller subsets offered (10-core, ratings-only CSV) explicitly for class-project-scale use, which is convenient for a 4-day sprint.
- **Class balance:** N/A — not labeled for sentiment; star-rating distribution not found in search results (would need direct inspection).
- **Also seen as partial Kaggle mirror:** "California - Google Local Data" by user `mexwell` — https://www.kaggle.com/datasets/mexwell/california-google-local-data — ~44 million reviews for ~500k CA businesses, license listed on Kaggle as "Other (specified in description)" (i.e., inherits the ambiguous UCSD terms, not a standard Kaggle license). Useful as an easier single-file entry point if the full McAuley download pipeline is too slow for the sprint.
- **Related/adjacent:** UCI ML Repository entry "Amazon Product and Google Locations Reviews" (https://archive.ics.uci.edu/dataset/1276/amazon+product+and+google+locations+reviews) — a preprocessed, combined Amazon + Google Local dataset, ~3.06M instances, framed by UCI for "regression / time-series" tasks rather than text sentiment. Whether raw review text is retained in this preprocessed version is **unknown** — needs direct inspection before relying on it; do not assume text is present.

---

## 2. Yelp Open Dataset (official Yelp release)

- **Name / URL:** Yelp Open Dataset — https://business.yelp.com/data/ (terms: e.g., https://s3-media0.fl.yelpcdn.com/assets/srv0/engineering_pages/f64cb2d3efcc/assets/vendor/Dataset_User_Agreement.pdf, last updated July 7, 2023)
- **Associated paper:** No single canonical paper; originated from the "Yelp Dataset Challenge." Used in many derivative papers (see below).
- **Sample count:** Multi-million reviews across several US/Canada metro areas (exact current count not pinned down in search; historically several million reviews, hundreds of thousands of businesses). Treat as `unknown, order of magnitude millions` until the actual JSON is inspected.
- **Label scheme:** 1–5 star rating + review text; no native sentiment label.
- **Label source:** N/A — would be rating-derived if used for sentiment.
- **Domain:** Yelp business reviews (restaurants, services, shops) — business/location-adjacent, same character as Google Maps reviews, good domain match.
- **Text quality notes:** unknown precisely, but widely used in academic NLP so generally considered clean enough; real risk is regional skew (US/Canada metros only) and Yelp-specific review culture possibly differing from Google Maps review style.
- **License:** **Academic-use only, explicitly non-commercial.** Terms of Use state the license is "solely for academic use" and explicitly prohibit commercial use, redistribution/sublicensing, and public redistribution of the data or derivative works without Yelp's written consent. This is a hard legal constraint, not just etiquette.
- **Accessibility:** Freely downloadable after agreeing to the terms (no payment, but a click-through academic-use agreement is required — i.e., "gated" in the sense of requiring acceptance of restrictive terms, not freely redistributable).
- **Class balance:** unknown (would need direct inspection of the star-rating histogram).
- **Red flag:** Any derivative dataset built from Yelp Open Dataset (see #3, #4, #6 below) technically still carries Yelp's non-commercial/no-redistribution restriction upstream, even when re-hosted on Kaggle/HF/Zenodo without restating that restriction. This is a license-provenance risk across several "derived" candidates below.

---

## 3. Yelp Review Full (`Yelp/yelp_review_full` on Hugging Face)

- **Name / URL:** https://huggingface.co/datasets/Yelp/yelp_review_full
- **Associated paper:** Zhang, X., Zhao, J., & LeCun, Y., "Character-level Convolutional Networks for Text Classification," NeurIPS 2015 (the original Yelp-5 benchmark construction).
- **Sample count:** 650,000 training / 50,000 test (stated in multiple benchmark descriptions of "Yelp-5").
- **Label scheme:** 5-class — raw star rating 1–5 used directly as the label (not collapsed to 3-class).
- **Label source:** Star-rating-derived (rating = label, no sentiment relabeling, no human sentiment annotation).
- **Domain:** Yelp business reviews — same domain-match benefits/risks as #2.
- **Text quality notes:** unknown beyond "widely used benchmark," no duplicate/spam stats found.
- **License:** Inherits Yelp's academic-only restriction (see #2) — the HF card itself doesn't override Yelp's original Dataset Terms of Use.
- **Accessibility:** Freely downloadable directly via HF `datasets` library, no request form — but see license caveat above (easy ≠ unrestricted).
- **Class balance:** Roughly even by construction (benchmark papers typically balance classes).

---

## 4. Yelp Polarity (`fancyzhx/yelp_polarity` on Hugging Face)

- **Name / URL:** https://huggingface.co/datasets/fancyzhx/yelp_polarity
- **Associated paper:** Same Zhang/Zhao/LeCun NeurIPS 2015 paper as #3 ("Yelp-2" binary benchmark).
- **Sample count:** 560,000 training / 38,000 test reviews (per HF dataset card description).
- **Label scheme:** Binary — negative vs. positive. **Note on construction rule:** search summaries were inconsistent — one description says "stars 1,2 = negative; 3,4 = positive" while the standard/original Zhang et al. construction is "1,2 = negative; 4,5 = positive, with 3-star reviews dropped." This inconsistency itself is a flag — **the exact rule needs to be re-verified directly from the dataset card before any use**, do not trust either summary blindly.
- **Label source:** Star-rating-derived, not sentiment-annotated.
- **Domain:** Yelp reviews, same as #2/#3.
- **Text quality notes:** unknown.
- **License:** Inherits Yelp academic-only restriction (see #2 red flag).
- **Accessibility:** Freely downloadable via HF, no gate — but same license caveat as above.
- **Class balance:** Stated as balanced (≈280,000/280,000 train, ≈19,000/19,000 test per one description) — **not 3-class**, would need a neutral class sourced elsewhere or dropped from the project's 3-class design entirely.

---

## 5. "Yelp Reviews Sentiment Dataset" (Kaggle, user `thedevastator`)

- **Name / URL:** https://www.kaggle.com/datasets/thedevastator/yelp-reviews-sentiment-dataset
- **Associated paper:** None found — appears to be a Kaggle-user repackaging, not tied to a publication.
- **Sample count:** 7,000 labeled training reviews + 3,000 **unlabeled** test reviews (per Kaggle page description).
- **Label scheme:** Binary (0 = negative, 1 = positive). Not 3-class.
- **Label source:** Not stated precisely on the page — likely rating-derived from underlying Yelp data, but the page doesn't document the exact conversion rule. Must be recorded as `unknown / unverified`, not assumed.
- **Domain:** Yelp reviews.
- **Text quality notes:** Small scale (7K/3K) relative to other Yelp derivatives; no documented cleaning or dedup process.
- **License:** CC0 1.0 Universal (public domain dedication) as listed on the Kaggle page — **if genuinely CC0, this is the most license-permissive Yelp-derived candidate found**, though it inherits the same upstream Yelp-ToS provenance question flagged in #2 (a Kaggle contributor relabeling it CC0 doesn't necessarily extinguish Yelp's original restriction — legal ambiguity, not resolved by this research pass).
- **Accessibility:** Freely downloadable, no gate.
- **Class balance:** unknown exact split; binary only.

---

## 6. "Yelp Restaurant Reviews Sentiment Dataset" (Zenodo, record 18723813)

- **Name / URL:** https://zenodo.org/records/18723813
- **Associated paper:** unknown / not identified in search (appears to be a standalone Zenodo data deposit, published 2026-02-21, very recent).
- **Sample count:** 14,351 individual restaurant review records.
- **Label scheme:** **3-class — Positive / Neutral / Negative — exactly matching this project's target scheme.** This is the only candidate found with that exact pre-built 3-class label.
- **Label source:** Described as a "pre-labelled sentiment variable" — the Zenodo description does not state whether this was human-annotated or rating-derived. Given it's built "collected from the official Yelp Open Dataset" and includes both review-star-rating and a separate sentiment label, it is **plausibly rating-derived**, but this is **not confirmed** — flag as unknown pending direct inspection of the file and any accompanying methodology notes.
- **Domain:** Yelp restaurant/food-service reviews specifically (narrower than general Yelp).
- **Text quality notes:** unknown; dataset is very recent (Feb 2026) with no citing papers yet found, meaning zero independent validation/track record — a credibility/quality-vetting red flag distinct from the license question.
- **License:** unknown (Zenodo deposit license not confirmed in search) — AND, because it is explicitly derived from the Yelp Open Dataset, it likely inherits Yelp's academic-only, no-redistribution restriction (see #2) regardless of whatever license tag the Zenodo record itself displays. This needs direct verification before use.
- **Accessibility:** Freely downloadable as a 3.7MB ZIP, no gate.
- **Class balance:** unknown (not stated in search results).

---

## 7. TripAdvisor Hotel Reviews (Kaggle — multiple mirrors, e.g. `andrewmvd`, `thedevastator`)

- **Name / URL:**
  - https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews
  - https://www.kaggle.com/datasets/thedevastator/tripadvisor-hotel-reviews
- **Associated paper:** Alam, M. H., Ryu, W.-J., & Lee, S., "Joint multi-grain topic sentiment: modeling semantic aspects for online reviews," Information Sciences, 2016 (the `andrewmvd` mirror cites this as the data's origin).
- **Sample count:** 20,491 unique reviews (andrewmvd mirror); the `thedevastator` mirror states 6,444 ratings — i.e., **the two Kaggle mirrors disagree on size**, suggesting they may be different subsets/versions, not identical copies. Needs reconciliation before use.
- **Label scheme:** 1–5 star rating, raw text. No separate sentiment label out of the box (would need derivation/collapsing to 3-class).
- **Label source:** N/A natively; rating-derived if we build one.
- **Domain:** Hotel reviews — a plausible location/business domain match, though narrower than general Google Maps reviews (hotels only, not restaurants/shops/services generally).
- **Text quality notes:** unknown; no documented spam/dedup stats found.
- **License:** unknown/unspecified consistently across mirrors — Kaggle license fields not confirmed in search results for either mirror; must check directly on the dataset page before relying on it.
- **Accessibility:** Freely downloadable, no gate.
- **Class balance:** unknown (star-rating histogram not found).

---

## 8. `argilla/tripadvisor-hotel-reviews` (Hugging Face)

- **Name / URL:** https://huggingface.co/datasets/argilla/tripadvisor-hotel-reviews
- **Associated paper:** Same underlying data as #7 (Alam et al. 2016), repackaged in Argilla's annotation-tool format.
- **Sample count:** 20,491 training examples (31.8 MB).
- **Label scheme:** 1–5 star rating field present; dataset also carries Argilla annotation scaffolding fields (prediction, prediction_agent, annotation, explanation, etc.) — but these look like **empty/template Argilla fields for an annotation project**, not evidence of a completed human sentiment-annotation pass. Should not be described as "human-annotated sentiment" without verifying the annotation fields are actually populated.
- **Label source:** Same as #7 — rating is the only confirmed label; any sentiment label would still need deriving unless the Argilla annotation fields are confirmed populated (unverified).
- **Domain:** Hotel reviews, same as #7.
- **Text quality notes:** unknown.
- **License:** **CC BY-NC 4.0** — explicitly non-commercial. Clear and documented (unlike #7's Kaggle mirrors), which makes this version more legally transparent even though it adds a commercial-use restriction.
- **Accessibility:** Freely downloadable via HF, no gate.
- **Class balance:** unknown.

---

## 9. Google Play Store App Reviews — Sentiment Dataset (Kaggle, `farhaouimouhamed`)

- **Name / URL:** https://www.kaggle.com/datasets/farhaouimouhamed/sentiment-analysis-datasetgoogle-play-app-reviews
- **Associated paper:** None found — appears to be a Kaggle-user-built scrape, not tied to a publication.
- **Sample count:** 16,092 reviews, extracted via the Google Play scraper API.
- **Label scheme:** 3-class — Negative / Neutral / Positive — **matches this project's target scheme**, with a stated conversion rule: ratings 1–2 → negative, 3 → neutral, 4–5 → positive.
- **Label source:** **Star-rating-derived per an explicitly stated rule** (not human-annotated sentiment) — this is one of the more precisely documented conversion rules found in this search pass.
- **Domain:** Google Play Store app reviews. This is "Google" branded and has consumer-service review character, but it is **app-store reviews, not location/business Google Maps reviews** — a real domain gap from the project's target (Arabic Google Maps reviews), though closer than movie/Twitter data.
- **Text quality notes:** unknown; app reviews are typically shorter and noisier (emoji-heavy, very short "good app" style text) than Google Maps business reviews — a known general characteristic of this domain, not confirmed specifically for this file.
- **License:** unknown/unspecified in search results — needs direct check on the Kaggle page.
- **Accessibility:** Freely downloadable, no gate.
- **Class balance:** unknown exact counts per class.

---

## 10. Amazon Reviews Polarity / Amazon Review Full (Zhang et al. 2015; e.g. `fancyzhx/amazon_polarity` on Hugging Face)

- **Name / URL:** https://huggingface.co/datasets/fancyzhx/amazon_polarity
- **Associated paper:** Zhang, X., Zhao, J., & LeCun, Y., NeurIPS 2015 (same paper family as Yelp-2/Yelp-5).
- **Sample count:** Binary version ("Amazon-2"): 3,600,000 train / 400,000 test. 5-class version ("Amazon-5"): 3,000,000 train / 650,000 test.
- **Label scheme:** Binary (pos/neg, 3-star reviews dropped) or 5-class (raw star rating).
- **Label source:** Star-rating-derived, not sentiment-annotated.
- **Domain:** **Amazon product reviews — not location/business reviews.** This is the "generic e-commerce" domain the task explicitly said to de-prioritize unless nothing better exists. Listed here for completeness/benchmarking value, not as a front-running candidate.
- **Text quality notes:** Well-known benchmark; large scale but documented as including very short/low-information reviews in places (common critique of Amazon review benchmarks in NLP literature, not re-verified here specifically for this release).
- **License:** Treated as an open academic benchmark; no commercial-use grant confirmed, no explicit prohibition found either — unknown precisely, likely research-use convention similar to other McAuley/Zhang-family releases.
- **Accessibility:** Freely downloadable via HF, no gate.
- **Class balance:** Balanced by construction (benchmark papers).

---

## 11. SemEval-2014 Task 4 / SemEval-2016 Task 5 — Restaurant Reviews (Aspect-Based Sentiment Analysis)

- **Name / URL:** https://alt.qcri.org/semeval2016/task5/ (official task page); mirrors exist on Kaggle (e.g. https://www.kaggle.com/datasets/charitarth/semeval-2014-task-4-aspectbasedsentimentanalysis) and Hugging Face (e.g. `NEUDM/semeval-2016`).
- **Associated paper:** Pontiki, M. et al., "SemEval-2014 Task 4: Aspect Based Sentiment Analysis," SemEval 2014; Pontiki, M. et al., "SemEval-2016 Task 5: Aspect Based Sentiment Analysis," SemEval 2016.
- **Sample count:** SemEval-2014 restaurant subset: "over 3K English sentences" (from Ganu et al. 2009 restaurant reviews). SemEval-2016: 5,801 sentences across restaurants + laptops combined (restaurant-only count not isolated in search).
- **Label scheme:** Aspect-level, not document-level: each aspect category (Food, Service, Price, Ambience, Anecdotes/Misc for 2014; Food/Service/Ambience/Drinks/Location/Restaurant for 2016) gets its own polarity — **4 labels in 2014 (Positive, Negative, Conflict, Neutral)**, this is a genuinely finer-grained, differently-shaped task than this project's whole-review 3-class target.
- **Label source:** **Human-annotated** — this is one of the only candidates in this list with a credible claim to true manual sentiment annotation (fine-grained, by task organizers/annotators), not rating-derived.
- **Domain:** Restaurant reviews — good domain match in spirit, but sentence/aspect-level granularity is a structural mismatch with a document-level 3-class review classification task; would require nontrivial reformatting (e.g., aggregating aspect polarities to a single document label) to reuse here.
- **Text quality notes:** Small, curated, high-quality (human-annotated academic benchmark) — opposite profile from the large noisy web-scraped candidates above.
- **License:** unknown precisely — SemEval task data historically distributed under task-specific research-use terms via the task organizers' site; some unofficial redistributions exist on Kaggle/HF whose own license compliance with the original terms is not verified here.
- **Accessibility:** Appears freely accessible via the task page and unofficial mirrors; no payment gate found, though the "official" channel may require signing up for the SemEval task archive rather than a one-click download — not fully confirmed.
- **Class balance:** unknown exact counts; "Conflict" class is typically a small minority in these benchmarks (general ABSA literature knowledge, not re-verified for this specific release).

---

## 12. `amazon_reviews_multi` (Hugging Face) — EXCLUDED, documented for completeness

- **Name / URL:** https://huggingface.co/datasets/defunct-datasets/amazon_reviews_multi
- **Status:** **Defunct.** Amazon withdrew distribution rights; the dataset is no longer officially available ("Amazon has decided to stop distributing the multilingual reviews dataset"). Unofficial re-hosts exist (e.g. `mteb/amazon_reviews_multi`, community copies) of uncertain provenance/legality.
- **Languages:** Originally English, Japanese, German, French, Chinese, Spanish — **no Arabic**, so even when it was live it offered no built-in Arabic counterpart for this bilingual project.
- **Why excluded:** Dead upstream license status (withdrawn by the rights holder) plus no Arabic coverage makes this unsuitable regardless of its past quality. Not recommended even as a fallback.

---

## 13. "AI-generated Google Reviews" (Zenodo, record 18162470) — EXCLUDED, documented for completeness

- **Name / URL:** https://zenodo.org/records/18162470
- **Associated paper:** "Ghostwriters of the Marketplace: A Corpus of Machine-Generated Reviews for Google Services and Businesses," accepted at ICWSM 2026 (by Karla Schäfer).
- **Sample count:** ~78,000 reviews generated by 6 LLMs (plus a smaller external set from 3 additional LLMs), using 50 prompts, 3 writing styles, 117 tones, and 3 target ratings (positive/negative/neutral).
- **Label source:** **Fully synthetic — these are LLM-generated reviews, not real user reviews**, with ratings assigned by prompt design rather than by real reviewers or human annotators.
- **Domain:** Framed as "Google services and businesses" reviews, but entirely machine-generated text, explicitly built as a detector-training/benchmarking corpus for AI-generated-text detection, not as a sentiment-analysis training set.
- **Why excluded (for Phase 1 purposes):** Using synthetic LLM text as primary training/eval data for a real-world sentiment classifier risks distributional mismatch with genuine human review language (the actual target domain here) and could bias a model toward LLM writing patterns rather than real reviewer sentiment expression. Could conceivably be considered later for robustness/adversarial testing, but it is explicitly out of scope for building/evaluating the core sentiment model in this sprint.
- **License:** "Released for research purposes only" per the record description — further restricts any non-research use even if it were otherwise suitable.

---

## Summary table (quick reference — see sections above for full detail and caveats)

| # | Dataset | Domain | Size (as stated) | Label scheme | Label source | License | Gated? |
|---|---|---|---|---|---|---|---|
| 1 | UCSD Google Local (2021) | Google Maps/local | ~666M reviews | none (stars only) | n/a / would be rating-derived | unclear/unstated | No |
| 2 | Yelp Open Dataset | Yelp business | millions (unknown exact) | none (stars only) | n/a / would be rating-derived | academic-only, no commercial/redistribution | Click-through terms |
| 3 | Yelp Review Full (HF) | Yelp business | 650K/50K | 5-class (star=label) | rating-derived | inherits Yelp academic-only | No |
| 4 | Yelp Polarity (HF) | Yelp business | 560K/38K | binary | rating-derived (exact rule unverified/inconsistent) | inherits Yelp academic-only | No |
| 5 | Yelp Sentiment (Kaggle, thedevastator) | Yelp business | 7K/3K (test unlabeled) | binary | unknown, likely rating-derived | CC0 (stated) but provenance ambiguous | No |
| 6 | Yelp Restaurant Sentiment (Zenodo) | Yelp restaurants | 14,351 | 3-class (Pos/Neu/Neg) | unknown, likely rating-derived | unknown, likely inherits Yelp terms | No |
| 7 | TripAdvisor Hotel Reviews (Kaggle) | Hotels | 20,491 or 6,444 (mirrors disagree) | none (stars only) | n/a / would be rating-derived | unknown | No |
| 8 | TripAdvisor (argilla, HF) | Hotels | 20,491 | none confirmed (stars + empty annotation scaffold) | n/a | CC BY-NC 4.0 | No |
| 9 | Google Play App Reviews Sentiment (Kaggle) | App store | 16,092 | 3-class (Neg/Neu/Pos) | rating-derived, stated rule (1-2/3/4-5) | unknown | No |
| 10 | Amazon Polarity/Full (HF) | E-commerce products | up to 3.6M | binary or 5-class | rating-derived | unknown, likely research-convention | No |
| 11 | SemEval-14/16 Restaurant ABSA | Restaurants | ~1K-3K sentences | 4-class, aspect-level | **human-annotated** | unknown, task-specific terms | Possibly (archive signup) |
| 12 | amazon_reviews_multi | E-commerce, multilingual (no Arabic) | n/a | n/a | n/a | defunct/withdrawn | Excluded |
| 13 | AI-generated Google Reviews (Zenodo) | Google services (synthetic) | ~78K | 3-class by prompt design | **synthetic, not real reviews** | research-only | Excluded |

---

## Open questions flagged for Phase 2 (if a candidate advances)

1. **UCSD Google Local license** — no formal license text found; must email j9li@eng.ucsd.edu or re-check the download page directly before any use beyond pure academic coursework citation.
2. **Yelp-derivative provenance** — every Yelp-based derivative (#3–#6) should be checked for whether it actually honors or violates Yelp's original no-redistribution academic-only clause; using Yelp-derived data for anything beyond non-commercial coursework is legally murky regardless of what license tag a reposted copy carries.
3. **Yelp Polarity construction rule discrepancy** (#4) — "1,2=neg / 3,4=pos" vs. the standard "1,2=neg / 4,5=pos, drop 3" must be resolved by inspecting the actual HF loading script before trusting any class-balance claim.
4. **TripAdvisor Kaggle mirrors disagree on size** (20,491 vs. 6,444) — these may not be the same dataset; do not assume interchangeability.
5. **Zenodo Yelp Restaurant Sentiment dataset** (#6) is brand-new (Feb 2026) with zero citing literature found — quality/correctness of its pre-built 3-class labels is unverified; would need a manual spot-check of at least ~50 rows before trusting the label column.
6. No candidate found in this pass offers genuinely **human-annotated** document-level 3-class sentiment on real Google-Maps-style business reviews at meaningful scale. The closest things to human annotation are the SemEval ABSA sets (#11), which are aspect-level, not document-level, and small.

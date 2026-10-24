# Arabic Sentiment Dataset Scouting — Raw Findings (Phase 1)

Project: Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews (3-class: Positive/Neutral/Negative)
Scope: Arabic-side dataset candidates. Phase 1 discovery/audit only — NO decision made yet.
Compiled: 2026-10-24
Method: Web search (Hugging Face, Kaggle, Zenodo, GitHub, journal/arXiv pages) + direct page fetches. All fields not directly verifiable are marked "unknown" — do not treat as confirmed.

IMPORTANT GENERAL CAVEAT: Several candidates below have sentiment labels **derived from star ratings**, not human-annotated sentiment. This is explicitly flagged per entry. Star-derived binary labels (pos/neg only, rating 3 discarded) are NOT equivalent to validated 3-class (pos/neutral/neg) sentiment and would need extra work/validation before use in a 3-class scheme.

---

## 1. Jordanian-Arabic Restaurant Review Dataset

- **URL:** https://zenodo.org/records/22061934
- **Associated paper:** No standalone published paper identified at time of search; appears to be a standalone Zenodo release with an annotation protocol/validation package (not yet verified as peer-reviewed). Title on Zenodo: "Jordanian-Arabic Restaurant Review Dataset with Annotation Protocol and Validation Materials."
- **Sample count:** 8,671 restaurant reviews
- **Label scheme:** Sentiment (positive/negative/neutral implied — exact label set and per-class counts not confirmed from the page), plus Aspect categories, plus a 10-category Theme taxonomy (sources of satisfaction/dissatisfaction). Per-class counts: unknown.
- **LABEL SOURCE:** Hybrid — described as "applied using Claude Sonnet 4.6, with GPT-5 used as an independent annotator during protocol validation," with human annotators providing reference/gold-standard annotations for validation (gold subsets of 75 and 300 reviews with inter-annotator agreement, confusion matrices, precision/recall/F1 reported). **This is primarily LLM-generated annotation validated against a small human-annotated gold set — NOT full human annotation of the whole corpus.** This is an important caveat for label trustworthiness/provenance.
- **Dialect coverage:** Jordanian Arabic (dialectal), not MSA. Determined by data source (Jordan-based restaurants on Google Maps) rather than a dedicated dialect-ID process.
- **Text quality:** Not explicitly discoverable beyond protocol/validation materials; no explicit mention of duplicates/spam.
- **License:** CC-BY-4.0
- **Accessibility:** Freely downloadable (CSV 1.7MB, XLSX 602KB) + protocol docs and validation scripts.
- **Domain:** Restaurant reviews, sourced directly from **Google Maps** — strong domain match for this project.
- **Red flag:** LLM-annotated (not fully human-annotated) sentiment; needs independent verification of label quality before trusting at scale. Also unverified whether this has gone through peer review.

---

## 2. OCLAR (Opinion Corpus for Lebanese Arabic Reviews)

- **URL:** https://huggingface.co/datasets/community-datasets/oclar
- **Associated paper:** Al Omari, Al-Hajj, Hammami, Sabra (2019), "Sentiment Classifier: Logistic Regression for Arabic Services Reviews in Lebanon." Venue/DOI: not confirmed (found via Semantic Scholar reference only); authors affiliated with Lebanese University and Jouf University.
- **Sample count:** 3,916 reviews total
- **Label scheme & counts:** Binary — Positive (ratings 3–5): 3,465; Negative (ratings 1–2): 451. Heavily imbalanced (~89% positive).
- **LABEL SOURCE:** **Star-rating derived**, not manually annotated for sentiment. Conversion rule: ratings 3–5 → positive, ratings 1–2 → negative (note: rating 3, often "neutral," is folded into positive here — a methodological choice worth scrutinizing for a 3-class task).
- **Dialect coverage:** Lebanese Arabic (ar-LB), determined by source (reviewers in Lebanon), not by linguistic dialect-ID.
- **Text quality:** Not discoverable from the page; no duplicate/spam analysis found.
- **License:** Unknown (listed as "unknown" on HF page).
- **Accessibility:** Freely downloadable from Hugging Face.
- **Domain:** Services reviews — hotels, restaurants, hospitals, shops — collected from **Google Reviews and Zomato**. Good domain match.
- **Red flags:** Small size, severe class imbalance, star-derived (not manual) labels, unknown license, and the rating-3-as-positive convention is non-standard for 3-class sentiment.

---

## 3. HARD (Hotel Arabic-Reviews Dataset)

- **URL (HF):** https://huggingface.co/datasets/Elnagara/hard
- **URL (GitHub, canonical):** https://github.com/elnagara/HARD-Arabic-Dataset
- **Associated paper:** Elnagar, A., Khalifa, Y.S., Einea, A. (2018). "Hotel Arabic-Reviews Dataset Construction for Sentiment Analysis Applications." Springer (book chapter), DOI via https://link.springer.com/chapter/10.1007/978-3-319-67056-0_3
- **Sample count:** Conflicting figures across sources — GitHub README states balanced version = 93,700 reviews (46,850 pos / 46,850 neg); unbalanced/"clean" version = 373,750 reviews. Other secondary sources cite 490,587 or 105,698 for different cuts. **Exact canonical number should be re-verified directly from the repo's data files before use — do not trust a single secondary citation.**
- **Label scheme:** Binary only — Positive (ratings 4 & 5), Negative (ratings 1 & 2). **Neutral (rating 3) reviews are explicitly excluded entirely** ("No neutral reviews are included" per README).
- **LABEL SOURCE:** **Star-rating derived**, not manually annotated for sentiment.
- **Dialect coverage:** Mix of Modern Standard Arabic (MSA) and Dialectal Arabic (DA); not separately tagged per-review — determined post-hoc via general description, not per-item dialect labels.
- **Text quality:** Review length ranges ~5–3,370 characters; mix of formal/informal Arabic; some reviews contain both praise and complaints in one text (potential labeling-noise source for a 3-class scheme). Unbalanced version described as "clean" (quality-filtered) by the authors, but specifics of filtering not detailed in what was retrieved.
- **License:** Unknown — no license file/declaration found in HF card or GitHub README.
- **Accessibility:** Freely downloadable (GitHub, HF — Parquet ~13.6MB on HF).
- **Domain:** Hotel reviews, Booking.com (collected June/July 2016). Strong review-domain match, though hotel-specific rather than general location/business.
- **Red flag:** No neutral class at all — would require either discarding the "neutral" requirement for any HARD-based training data, or pulling in rating-3 reviews separately (untested, no ground truth for those). License unknown — must clarify before any downstream/commercial use. Widely used/well-cited benchmark, so strong community validation.

---

## 4. mteb/HotelReviewSentimentClassification

- **URL:** https://huggingface.co/datasets/mteb/HotelReviewSentimentClassification
- **Associated paper:** Derived/repackaged from HARD (Elnagar, Khalifa, Einea 2018) for the MTEB/MMTEB benchmark suite (MTEB 2022, MMTEB 2025).
- **Sample count:** Small MTEB-benchmark subset — 2,048 train samples; ~2,040 total rows (not the full HARD corpus).
- **Label scheme & counts:** Appears to be 4 classes (labeled 0,1,3,4 in the viewer) — counts: class 4: 512; class 3: 512; class 1: 745; class 0: 279. The exact semantic mapping (e.g., which class = negative/neutral/positive) is **not confirmed** from the card; likely a re-binned/re-sampled cut of HARD's rating scale, but this needs direct verification before use.
- **LABEL SOURCE:** Same as HARD — star-rating derived, not manual sentiment annotation.
- **Dialect coverage:** Same as HARD (MSA + dialects), unverified per-item.
- **License:** Unknown.
- **Accessibility:** Freely downloadable via Hugging Face/MTEB tooling.
- **Domain:** Hotel reviews (Booking.com), same underlying source as HARD.
- **Red flag:** This is a benchmark-sized subset, not a full dataset for training — likely too small for standalone project use, and the class-label mapping is unclear. Treat as a secondary/reference artifact pointing back to HARD, not an independent first choice.

---

## 5. ar_res_reviews (ArRestReviews)

- **URL:** https://huggingface.co/datasets/hadyelsahar/ar_res_reviews
- **Associated paper:** Hady ElSahar, Samhaa R. El-Beltagy (2015), "Building Large Arabic Multi-domain Resources for Sentiment Analysis," Springer (CICLing 2015 or similar — exact venue not independently confirmed in this pass). Part of the "Large Arabic Sentiment Analysis Resources" project.
- **Sample count:** 8,364 restaurant reviews
- **Label scheme & counts:** Binary — polarity field of 1 (positive) / -1 (negative). Exact per-class counts not stated on the card.
- **LABEL SOURCE:** **Unclear/unverified.** The HF dataset card has multiple "[More Information Needed]" placeholders for curation rationale and annotation process — cannot confirm human annotation vs. rating-derived. Do not assume manual annotation.
- **Dialect coverage:** Described as MSA-leaning; sourced from qaym.com (a restaurant review site), not Google/Yelp-style maps reviews. Dialect determination method: unknown.
- **Text quality:** Unknown — not documented.
- **License:** Unknown.
- **Accessibility:** Freely downloadable via Hugging Face.
- **Domain:** Restaurant reviews (qaym.com). Note: the dataset card oddly also references "From Twitter" in its collection description, which is inconsistent/confusing provenance — worth flagging as a provenance red flag.
- **Red flag:** Poorly documented provenance (conflicting "qaym.com" vs. "from Twitter" language), unverified annotation method, unknown license. Use with caution; would need to inspect raw data/original paper directly before trusting.

---

## 6. LABR (Large-scale Arabic Book Reviews Dataset)

- **URL (GitHub, canonical):** https://github.com/mohamedadaly/LABR
- **URL (HF mirror):** https://huggingface.co/datasets/mohamedadaly/labr
- **Associated paper:** Aly, M. & Atiya, A. (2013), "LABR: A Large Scale Arabic Book Reviews Dataset," ACL 2013 (Sofia, Bulgaria). arXiv: 1411.6718 (extended version titled "LABR: A Large Scale Arabic Sentiment Analysis Benchmark").
- **Sample count:** 63,257 reviews from 16,486 users covering 2,131 books.
- **Label scheme:** Two task formulations — (a) 2-class: Positive (ratings 4–5) vs. Negative (ratings 1–2), rating 3 excluded; (b) 5-class: direct 1–5 rating scale. Comes with pre-built balanced/unbalanced train/test splits for both.
- **LABEL SOURCE:** **Star-rating derived** (Goodreads 1–5 star ratings), not manual sentiment annotation.
- **Dialect coverage:** Not specified; book reviews on Goodreads are typically closer to MSA, but no explicit dialect tagging/analysis is provided.
- **Text quality:** Not detailed in README; described only as "cleaned up" reviews in a TSV file.
- **License:** Not specified in the README retrieved; generally cited as freely available for research.
- **Accessibility:** Freely downloadable (GitHub + HF), with a maintained Python interface (`labr.py`) and reproducible experiment scripts — strong usability/tooling support.
- **Domain:** Book reviews (Goodreads) — **not** location/business-review domain; a well-known generic benchmark.
- **Red flag:** Domain mismatch (books, not places/services) despite being one of the largest and most cited Arabic sentiment datasets. Star-derived, binary-or-5-class only (no native 3-class neutral-inclusive scheme without re-binning, and rating 3 is simply dropped in the 2-class setup).

---

## 7. GLARE (Google Apps Arabic Reviews Dataset)

- **URL:** https://huggingface.co/datasets/Fatima-Gh/GLARE
- **Associated paper:** AlGhamdi, Mohammed, Al-Khalifa, Alowisheq (Dec 2024), "GLARE: Google Apps Arabic Reviews Dataset," arXiv:2412.15259.
- **Sample count:** ~76 million reviews from 9,980 Android apps (Google Play Store, Saudi store). Very large.
- **Label scheme:** Raw star ratings (1–5) attached per review; no pre-built sentiment class labels — would need to be derived.
- **LABEL SOURCE:** **Star-rating only** — no sentiment annotation, human or otherwise, provided out of the box. Any 3-class sentiment use requires the project team to define and apply its own conversion rule.
- **Dialect coverage:** MSA + Saudi dialect (inferred solely from "Saudi Play Store" collection scope, not actual per-review dialect identification).
- **Text quality:** Dataset includes engineered quality indicators (tokenization, word counts, non-Arabic-character/noise detection, digit presence) — relatively well-instrumented for quality filtering.
- **License:** CC BY 4.0.
- **Accessibility:** Freely downloadable (Google Drive, Zenodo, Hugging Face); large total size (~21.9GB reviews + ancillary files).
- **Domain:** App reviews (Google Play), not location/business reviews — tangential domain match (it is "Google" platform reviews but of apps, not places).
- **Red flag:** Domain mismatch (apps, not places/businesses); massive scale may be overkill/costly for a 4-day sprint; no provided sentiment labels at all (raw ratings only), so this is a "raw text + ratings" resource, not a ready-made sentiment dataset.

---

## 8. AURA-Sentiment

- **URL:** https://huggingface.co/datasets/irfan-ahmad/AURA-Sentiment
- **Associated paper:** Aljeezani, Othman, et al., "Arabic App Reviews: Analysis and Classification," ACM TALLIP (to appear / in press) — DOI via https://dl.acm.org/doi/full/10.1145/3708987
- **Sample count:** 29,700 samples (described as "balanced between positive and negative")
- **Label scheme & counts:** Binary — positive/negative. Exact per-class counts not stated on the card beyond "balanced."
- **LABEL SOURCE:** **Unknown/unverified** — the HF card does not state whether labels are human-annotated or star-rating derived. Given the domain (app reviews) and the "balanced" framing, a rating-based origin is plausible but NOT confirmed — do not assume either way without checking the underlying paper directly.
- **Dialect coverage:** MSA and apparent Gulf-dialect content observed anecdotally in samples; no formal dialect-ID methodology documented.
- **Text quality:** Natural, informal user-generated text typical of app reviews (informal language, spelling variation, emoji) — no duplicate/spam analysis found.
- **License:** MIT (with attribution required).
- **Accessibility:** Freely downloadable (Hugging Face, Parquet format).
- **Domain:** App reviews (iOS/Android, multiple categories) — not location/business-review domain.
- **Red flag:** Label-source ambiguity (unknown whether human or rating-derived) is a significant provenance gap; domain mismatch (apps, not places).

---

## 9. Arabic Google Maps Reviews Dataset for Tourism in Saudi Arabia (ABSA)

- **URL (data):** https://zenodo.org/records/17011574
- **Associated paper:** "Multi-Aspect Sentiment Classification of Arabic Tourism Reviews Using BERT and Classical Machine Learning," published in MDPI *Data*, 2025, Vol 10(11), Article 168. DOI: 10.3390/data10110168. (Also indexed: https://www.mdpi.com/2306-5729/10/11/168)
- **Sample count:** 3,543 Arabic Google Maps reviews of tourist attractions (parks, historical sites, museums, recreational facilities) across Saudi Arabia.
- **Label scheme:** **Aspect-level only** — three-way polarity (positive/neutral/negative) assigned separately per aspect across six aspects: Price, Overall Experience, Facilities, Staff & Service, Environment, Cleanliness. Per-class counts not stated in what was retrieved. **No single document-level overall-sentiment label is provided** — this is an aspect-based sentiment analysis (ABSA) resource, not a plain document-level 3-class sentiment dataset, so it would need aggregation/adaptation (e.g., averaging aspect labels or using the "Overall Experience" aspect alone as a proxy) to fit a document-level 3-class task.
- **LABEL SOURCE:** **Manually annotated** by two trained human annotators, with inter-annotator agreement reported as Cohen's Kappa = 0.87 (substantial/high agreement) — this is one of the few candidates with clearly documented, genuine human annotation.
- **Dialect coverage:** Not specifically analyzed; general "Arabic" (likely mixed MSA/Saudi dialect) given Saudi tourist-review origin.
- **Text quality:** Not detailed beyond the annotation protocol; no explicit duplicate/spam check found.
- **License:** Listed inconsistently across pages — Zenodo record shows CC0 1.0 Universal in one spot and CC-BY-4.0 referenced elsewhere. **This conflict should be resolved by checking the Zenodo record directly before relying on a specific license.**
- **Accessibility:** Freely downloadable (Excel .xlsx, ~380KB).
- **Domain:** Tourism/location reviews from **Google Maps** — excellent domain match, directly analogous to the target project (Arabic Google Maps reviews).
- **Red flags:** Small sample size (3,543) relative to other candidates; aspect-level-only labels (no ready document-level sentiment target) requiring adaptation; license statement inconsistency needs resolving. Strongest candidate on label-quality and domain-match grounds despite small size.

---

## 10. SaudiGovSent

- **URL:** https://doi.org/10.3390/info17050402 (also https://www.mdpi.com/2078-2489/17/5/402)
- **Associated paper:** Alshammari, T., "SaudiGovSent: A Large-Scale Arabic Dataset and Benchmark for Sentiment Analysis in Mobile Government Applications," MDPI *Information*, 2026 (per search result dated), Vol 17(5), Article 402.
- **Sample count:** 84,000 reviews (final, balanced), drawn from reviews of five Saudi m-Government apps (Absher Business, Tawakkalna, Sehhaty, Nusuk, Najiz).
- **Label scheme & counts:** Binary — positive/negative, balanced 42,000/42,000 after processing. Raw/unprocessed data noted as 79.9% positive vs. 20.1% negative before balancing (range 78.0%–88.1% positive per-app).
- **LABEL SOURCE:** **Star-rating derived.** Conversion rule: ratings 4–5 → positive, ratings 1–2 → negative; rating 3 systematically **excluded** (not treated as neutral, simply discarded).
- **Dialect coverage:** Not analyzed/documented; general Saudi-context Arabic (MSA + dialect) inferred from source population, not verified linguistically.
- **Text quality:** Not detailed in what was retrieved.
- **License:** Unknown/not retrieved — MDPI articles are typically open-access (journal-level), but the dataset's own license/download terms were not independently confirmed; dataset availability statement not verified in this pass.
- **Accessibility:** Unclear whether the dataset itself (not just the paper) is downloadable — not confirmed; may require contacting the author.
- **Domain:** Government mobile-app reviews — not location/business-review domain, and not freely confirmed accessible.
- **Red flag:** Domain mismatch (gov apps, not places/businesses); no neutral class; accessibility of the actual data file unconfirmed (may be gated/request-only) — needs direct verification before considering further.

---

## 11. Arabic Egypt Customer Reviews (Kaggle)

- **URL:** https://www.kaggle.com/datasets/mohamedramadan2040/arabic-customer-reviews
- **Associated paper:** None identified — appears to be an independently curated Kaggle dataset without an accompanying academic publication.
- **Sample count:** 39,004 unique reviews (per secondary search snippet; not independently verified against the actual Kaggle data files since the page is JS-rendered and could not be fully fetched).
- **Label scheme & counts:** Reported as ~60% positive, ~35% negative, ~5% "other" — the meaning of "other" (neutral? mixed? unlabeled?) is **unclear and unverified**.
- **LABEL SOURCE:** **Unknown/unverified** — could not determine from available snippets whether labels are human-annotated or rating-derived.
- **Dialect coverage:** Implied Egyptian Arabic from the title, but not confirmed via any documented dialect-ID process.
- **Text quality:** Unknown.
- **License:** Reported as Apache 2.0 per search snippet (unverified directly from Kaggle page due to fetch limitation).
- **Accessibility:** Freely downloadable from Kaggle (assuming license claim holds).
- **Domain:** General "customer reviews... from various companies" — unclear if these are location/business reviews (e.g., Google-Maps-style) or e-commerce/product reviews. Provenance of "various companies" is vague.
- **Red flag:** Low provenance confidence overall — no paper, vague source description, unverified label methodology, and the "other" 5% category is unexplained. Could not be fully verified due to Kaggle's JS-rendered page; would require manual inspection of the actual CSV before use.

---

## 12. 330K Arabic Sentiment Reviews Dataset (Kaggle)

- **URL:** https://www.kaggle.com/datasets/abdallaellaithy/330k-arabic-sentiment-reviews
- **Associated paper:** None identified.
- **Sample count:** 330,000 reviews (per listing title/snippet).
- **Label scheme:** Binary — 1 (positive) / 0 (negative), per initial search snippet. Per-class counts: unknown.
- **LABEL SOURCE:** Unknown/unverified — could not confirm human annotation vs. rating-derived from available snippets; page is JS-rendered and could not be fully fetched for verification.
- **Dialect coverage:** Unknown.
- **Text quality:** Unknown.
- **License:** Unknown (not retrieved).
- **Accessibility:** Presumed freely downloadable via Kaggle, but terms not confirmed.
- **Domain:** Described loosely as "Arabic product reviews" in one secondary snippet — likely e-commerce, not location/business reviews; needs verification.
- **Red flag:** Essentially no verifiable provenance beyond size and a rough binary scheme. Large size is attractive but unusable responsibly without direct inspection of the source/methodology. Treat as a low-confidence/placeholder candidate only.

---

## 13. SS2030 (Arabic Short-Text Dataset for Sentiment Analysis of Tourism and Leisure Events / Saudi social-events tweets)

- **URL:** https://www.kaggle.com/datasets/snalyami3/arabic-sentiment-analysis-dataset-ss2030-dataset
- **Associated paper:** Referenced in search as "Arabic Short-Text Dataset for Sentiment Analysis of Tourism and Leisure Events" (ResearchGate listing found; full citation/venue not independently confirmed in this pass).
- **Sample count:** 4,009 tweets total — training split 3,207 (1,812 positive / 1,395 negative), test split 802 (453 positive / 349 negative).
- **Label scheme:** Binary — positive/negative only.
- **LABEL SOURCE:** **Manually labeled** by polarity (per search snippet) — appears to be genuine human annotation, though the exact annotation protocol/number of annotators/agreement was not independently verified.
- **Dialect coverage:** Saudi Arabic (tweets about Saudi Vision 2030 social reforms — women driving, cinemas reopening, stadium access, etc.), collected Oct–Nov 2018 via Twitter API.
- **Text quality:** Typical short-text tweet characteristics; no explicit spam/duplicate analysis found.
- **License:** Unknown.
- **Accessibility:** Freely downloadable via Kaggle (assumed; not independently fetched/verified).
- **Domain:** **Twitter/social-media commentary on political-social events — NOT review domain.** Small, topic-narrow, binary-only.
- **Red flag:** Domain mismatch (tweets about policy events, not business/location reviews), small size, binary-only (no neutral), narrow/dated topical scope (2018 Saudi social reforms) likely to introduce topic-specific bias unhelpful for a general review-sentiment task. Recommend exclusion.

---

## 14. ArSAS (Arabic Speech-Act and Sentiment Corpus of Tweets) — included as a strong generic benchmark for comparison

- **URL:** http://www.lrec-conf.org/workshops/lrec2018/W30/pdf/22_W30.pdf (LREC 2018 workshop paper)
- **Associated paper:** "ArSAS: An Arabic Speech-Act and Sentiment Corpus of Tweets," LREC 2018 (OSACT workshop).
- **Sample count:** ~21,000 tweets.
- **Label scheme & counts:** 4-way sentiment: Positive (4,543), Negative (7,840), Neutral (7,279), Mixed (1,302). Also includes 6-way speech-act annotation (Assertion, Expression, Recommendation, Respect, Question, Misc) on the same tweets.
- **LABEL SOURCE:** **Manually annotated** — genuine human annotation for both sentiment and speech-act, a key strength.
- **Dialect coverage:** Mixed/general Arabic Twitter content, multiple topics; no granular per-tweet dialect tagging confirmed.
- **Text quality:** Typical tweet-length short text; no explicit duplicate/spam analysis found in this pass.
- **License:** Not confirmed in this pass (would need to check the distribution page/request terms).
- **Accessibility:** Commonly cited/used in Arabic NLP literature, suggesting it is accessible for research use, but exact access mechanism (direct download vs. request form) not independently confirmed here.
- **Domain:** **Twitter — not review domain.** Included only as a strong, well-cited, genuinely human-annotated, native 4-class (with usable neutral class) benchmark in case review-domain options prove too weak and a generic high-quality fallback is needed.
- **Red flag:** Domain mismatch (tweets, not reviews) — only relevant as a fallback/benchmark, not a primary candidate for this project's review-domain focus.

---

## Cross-cutting notes / things NOT yet verified that should be checked before any final selection

1. **License verification**: Most candidates list license as "unknown" on their hosting page (HARD, ar_res_reviews, OCLAR, several Kaggle sets). None of these should be treated as cleared for any specific downstream use (including commercial) until the original paper/repo is checked directly for explicit terms.
2. **Kaggle pages (#11, #12)** could not be fully rendered via automated fetch (JS-heavy pages) — the figures reported here come from search-engine snippets only, not direct page verification. These should be manually opened and inspected before being taken seriously as candidates.
3. **Star-rating-derived vs. manual-annotation conflation is the single biggest cross-cutting risk** in this space — of the 14 candidates, only #1 (partially, LLM+human-validated), #9, #13, and #14 show genuine (partial or full) human sentiment annotation; the rest are either star-derived or unverified/unknown.
4. **None of the Google-Maps-sourced, review-domain, human-annotated candidates are large** (#1: 8,671, hybrid LLM/human; #9: 3,543, fully human but aspect-level only). The large, well-documented, easily accessible datasets (HARD, LABR, GLARE) are either off-domain (apps/books) or lack neutral/manual labels.

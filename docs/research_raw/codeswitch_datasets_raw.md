# Code-Switching Dataset Scout — Raw Findings

**Phase:** 1 (dataset discovery/audit), 4-day sprint
**Project:** Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews (3-class: Pos/Neu/Neg)
**Question driving this scout:** Does genuine Arabic-English **code-switched** sentiment data exist and is it usable as a central novelty piece?
**Date compiled:** 2026-10-24
**Method:** Web search (Hugging Face, Kaggle, Zenodo, GitHub, ACL Anthology/LREC/WANLP/CALCS, arXiv, IEEE, Springer). PDF full-text extraction largely failed (binary/compressed streams); findings below rely on search-engine summaries, abstract pages, and HTML-fetchable pages — flagged where unverified.

---

## 0. Bottom line (expanded)

A real research subfield exists ("code-switched Arabic NLP"), and a recent survey (Nagoudi et al.-style, *A Survey of Code-switched Arabic NLP: Progress, Challenges and Future Directions*, arXiv:2501.13419 / COLING 2025) explicitly states that **sentiment analysis is one of the most under-resourced downstream tasks in this space — only ~6 papers/datasets in the entire literature address CSW sentiment**, and most of those are **Algerian/Tunisian Arabic-FRENCH**, not Arabic-English. For Arabic-**English** specifically, the only dataset found that is (a) genuinely intra-sentence code-switched AND (b) has actual sentiment class labels AND (c) is a "benchmark" with train/dev/test splits is **EESA** (Sherif & Sabty, 2024) — but it is YouTube-comment-domain, Egyptian-dialect-specific, and its public download/license status could not be confirmed from available documentation (no GitHub/Kaggle/Zenodo page surfaced in search; likely obtainable only by contacting the authors or via the SPECOM 2024 paper's supplementary materials). No dataset was found that is (1) Arabic-English code-switched, (2) sentiment-labeled, AND (3) in the Google-Maps/business-review domain. Everything review-domain found is monolingual Arabic (Category A).

---

## 1. Category B candidates — genuine intra-sentence/intra-word Arabic-English code-switching

### 1.1 EESA (Egyptian-English Sentiment Analysis benchmark) — ★ most relevant sentiment-labeled CS dataset found
- **Paper:** Sherif, A. & Sabty, C. (2024). "Sentiment analysis for Egyptian Arabic-English code-switched data using traditional neural models and advanced language models." *SPECOM 2024* (26th Int'l Conf. on Speech and Computer, Belgrade), Springer LNCS/LNAI, pp. 54–69.
- **Size:** ~4,100 Egyptian-English YouTube comments total; benchmark splits reported elsewhere (via SwitchEmbed 2026 paper) as 2,464 train / 818 dev / 818 test.
- **Domain:** YouTube comments (social-media, user-generated opinion text — the closest domain analog to reviews found in the CS-sentiment literature).
- **Dialect:** Egyptian Arabic + English.
- **Category:** **B — genuine code-switching** (this is the explicit subject of the paper; CS is not incidental).
- **Sentiment scheme:** 3-class — Positive / Negative / Neutral (matches this project's target scheme almost exactly).
- **Annotation:** Sentence/comment-level sentiment labels (not token-level CS tags as far as could be determined — need to verify in full paper).
- **Availability/License:** **UNVERIFIED.** No GitHub, Kaggle, Zenodo, or HuggingFace listing surfaced despite targeted searches ("EESA dataset download", "Sherif Sabty github/zenodo"). It is referenced as a benchmark by later papers (SwitchEmbed, 2026) that evaluate on it, implying it is obtainable by at least some researchers (possibly via direct author request or university repository), but a public open-access link could not be confirmed.
- **Action for team:** Try to obtain via (a) emailing authors (Ahmed Sherif / Caroline Sabty, GUC — German University in Cairo, likely), (b) checking the SPECOM 2024 proceedings page on SpringerLink for supplementary data links, (c) checking if later papers that cite it (SwitchEmbed 2026, arXiv/SciTePress) bundle a copy or link.

### 1.2 CS-SNLI (Code-Switched SNLI)
- **Paper:** Introduced within "SwitchEmbed: Representation Learning for Arabic-English Code-Switched Text" (SciTePress, 2026). https://www.scitepress.org/Papers/2026/151951/151951.pdf
- **Size:** 86,141 triplets → 258,423 code-switched sentences (translated/code-switched extension of SNLI).
- **Domain:** Natural Language Inference (premise/entailment/contradiction) — **not naturally occurring review/social text; it's a translated/synthesized CS corpus** derived from SNLI.
- **Dialect:** Egyptian Arabic-English.
- **Category:** **B — genuine code-switching, but synthetically generated** (CS points likely inserted via code-switching generation/translation pipeline rather than organically produced speech/text). Treat as training-signal resource, not an authentic-usage sentiment corpus.
- **Sentiment labels:** None directly — CS-SNLI is an NLI dataset. The paper's embeddings are *evaluated downstream* on sentiment analysis (improves F1 by 2.17 pts over mBERT, 2.27 over XLM-R) — this downstream sentiment eval almost certainly uses **EESA** (see 1.1) or a similar existing CS-sentiment benchmark, but the exact test set used could not be confirmed from the fetchable abstract/summary (PDF full text would not extract).
- **Availability:** Unconfirmed; presumably released alongside the 2026 SwitchEmbed paper (check SciTePress / author GitHub).

### 1.3 Mixat — Emirati-English code-switched speech corpus
- **Paper:** "Mixat: A Data Set of Bilingual Emirati-English Speech." SIGUL 2024 workshop @ LREC-COLING; arXiv:2405.02578; ACL Anthology 2024.sigul-1.26.
- **GitHub:** https://github.com/mbzuai-nlp/mixat (MBZUAI-NLP)
- **Size:** ~15 hours of speech, 5,316 utterances total, of which **1,947 utterances (36%) are genuinely code-switched**, average Code-Mixing Index (CMI) = 0.11; rest are monolingual Emirati Arabic or monolingual English.
- **Domain:** Two public podcasts ("The Direction" — conversational/multi-speaker; "Think With Hessa" — single narrator). Not review/business domain, but **UAE/Emirati dialect — directly relevant to this project's likely target market (Google Maps reviews in UAE/Gulf) if the project geo-scopes to UAE.**
- **Dialect:** Emirati (Khaleeji/Gulf) Arabic + English.
- **Category:** **B — confirmed genuine intra-sentence code-switching** (CMI metric explicitly reported; this is the most rigorously documented CS corpus found in terms of proving intra-sentence mixing rather than just claiming it).
- **Sentiment labels:** **None.** Only speech transcription (Arabic script + Latin script for CS points) in metadata.csv. No sentiment or opinion annotation layer exists.
- **License:** CC BY-NC-SA 4.0 (research use only, no commercial use).
- **Note:** Author recommends using an updated transcription release via a companion repo ("PolyWER") rather than this GitHub repo directly.
- **Relevance:** Excellent as a *linguistic reference/exemplar* of real Gulf Arabic-English CS and for building CS-detection heuristics (CMI thresholds, script-mixing patterns), but **cannot be reused as-is as a sentiment-labeled dataset** — speech domain, no sentiment layer, no review-domain content.

### 1.4 ArzEn Corpus (and ArzEn-ST)
- **Papers:** Hamed et al., "ArzEn: A Speech Corpus for Code-switched Egyptian Arabic-English," LREC 2020 (aclanthology.org/2020.lrec-1.523); extension "ArzEn-ST: A Three-way Speech Translation Corpus," WANLP 2022 (aclanthology.org/2022.wanlp-1.12), arXiv:2211.12000.
- **Site:** https://sites.google.com/view/arzen-corpus/home
- **Size:** 12 hours of speech, 6,216 sentences, 38 bilingual speakers (interviews).
- **Domain:** Spontaneous interview speech (university students/employees) — not review domain.
- **Dialect:** Egyptian Arabic + English.
- **Category:** **B — genuine code-switching** (classic, widely-cited foundational corpus for this language pair; designed explicitly to capture naturalistic CS).
- **Sentiment labels:** **None** — corpus is designed for ASR/speech-translation/linguistic analysis (POS, lemma, translation alignment), not sentiment.
- **Availability:** Obtainable via request from the ArzEn corpus site/authors; not an open self-serve download as far as could be determined.

### 1.5 CSCS — Cairo Student Code-Switch Corpus
- **Paper:** Balabel, Hamed, Abdennadher, Vu, Çetinoğlu. "Cairo Student Code-Switch (CSCS) Corpus: An Annotated Egyptian Arabic-English Corpus." LREC 2020 (aclanthology.org/2020.lrec-1.489).
- **Size:** 1,153 sentences (speech transcriptions).
- **Domain:** Student speech; tokenized, lemmatized, POS-tagged.
- **Category:** **B — genuine code-switching**, but small and linguistically rather than sentiment oriented.
- **Sentiment labels:** None (POS/lemma annotation only).
- **Availability:** "Publicly available... can be obtained from the authors" per secondary sources — not a direct download link.

### 1.6 Algerian Code-Switched Sentiment (Adouane et al., 2020) — NOT Arabic-English, French-dominant
- **Paper:** Adouane, Touileb, Bernardy. "Identifying Sentiments in Algerian Code-switched User-generated Comments." LREC 2020 (aclanthology.org/2020.lrec-1.328).
- **Size:** 36,120 YouTube comments.
- **Languages mixed:** MSA + Algerian Arabic + **French** + Berber (no English component confirmed).
- **Category:** **B — genuine code-switching, but Arabic-FRENCH (and Berber), not Arabic-English.** Listed here as the closest methodological analog (CS + sentiment + YouTube comments), and flagged by the 2025 survey as one of the only ~6 CSW-sentiment datasets in existence, underscoring how sparse Arabic-English CSW sentiment data is by comparison.
- **Sentiment scheme:** 4-class (POS/NEG/NEU/MIX).
- **Relevance:** Useful as a **methodology template** (how to annotate CS sentiment, what macro-F1 is achievable — CNN got 60.17% macro-F1, suggesting CS sentiment is intrinsically harder than monolingual) but not directly usable for an Arabic-English project.

### 1.7 Tunisian CS Sentiment (Jerbi et al., 2019)
- Found only via the survey's summary; "domain: social media; labels: sentiment present; methodology: RNN." Likely Tunisian Arabic-French, not English. **Category D (unverified)** pending full-text access — could not independently confirm language pair or size.

---

## 2. Category C — Arabizi (Latin-transliterated Arabic), separately noted as highly relevant to real review text

Arabizi is NOT script-mixing code-switching in the strict linguistic sense (it's a transliteration system, not two languages interleaved) — but in practice Arabizi text is frequently interspersed with genuine English words/phrases, so it is highly relevant to how real Arabic-English Google Maps reviews will actually look.

### 2.1 TUNIZI — Tunisian Arabizi Sentiment Dataset
- **Paper:** "TUNIZI: a Tunisian Arabizi sentiment analysis Dataset" (WANLP 2021 variant cited as 100k-comment version; an earlier/smaller release is ~3K sentences — sources conflict: some describe 100k comments, others describe a 3K balanced release — **treat size as unverified/needs confirmation**).
- **HF mirror:** https://huggingface.co/datasets/chaymafourati/tunizi
- **Domain:** Comments on movies, politics, sport, etc.
- **Dialect:** Tunisian.
- **Category:** **C (Arabizi) with confirmed token-level CS tagging.** Each word is explicitly labeled TUN (Tunisian Arabizi) or FOR (code-switched Foreign — French or English) — this is a genuine, documented **token-level language-ID annotation layer** proving intra-sentence mixing exists in the data, BUT the FOR tag merges French and English together (Tunisians' dominant L2 is French, not English), so the English-CS proportion specifically is likely small and not separately quantified.
- **Sentiment scheme:** Positive/Negative (binary, per most descriptions) — some sources say 3-class; needs direct verification.
- **Relevance:** Best available real-world demonstration that "Arabizi + sentiment + some foreign-language mixing" datasets exist and are annotated at token level — but it's the wrong dialect/L2-language combination (French-leaning, Tunisian) for an Arabic-English UAE/Gulf-oriented review project. Useful as a structural template for building a similar resource.

### 2.2 SenZi — Sentiment Lexicon for Arabizi
- **Paper:** "SenZi: A Sentiment Analysis Lexicon for the Latinised Arabic (Arabizi)" (Open University, oro.open.ac.uk/66829).
- **Content:** Lexicon (11.3K positive + 13.3K negative words) + a 3.4K-tweet Arabizi evaluation set with a language identifier component.
- **Category:** C (Arabizi). Lexicon-based, not a text corpus suitable for supervised deep learning directly; could seed a weak-labeling/rule-based baseline.
- **Dialect/L2:** Not confirmed which dialect/second-language mixing; likely broad/Levantine-leaning. Needs verification.

### 2.3 BAERT / LAD / SALAD
- **Content:** LAD = 7.7M-tweet Arabizi corpus (unlabeled, for pretraining a BERT-like LM called BAERT); SALAD = manually sentiment-annotated subset of LAD.
- **Category:** C (Arabizi); SALAD is sentiment-labeled.
- **Relevance:** Large-scale Arabizi pretraining resource; SALAD could be a genuine sentiment-labeled Arabizi dataset, but dialect coverage, exact SALAD size, and whether English-code-mixing is present within it were **not verified** (search summaries only; full paper not fetched). Flag as Category D pending verification — promising lead worth a direct follow-up read of the source paper.

### 2.4 Kaggle "Datasets for sentiment analysis of arabizi tweets" (mariajmraidy)
- URL: https://www.kaggle.com/datasets/mariajmraidy/datasets-for-sentiment-analysis-of-arabizi
- **Category: D — unverified.** WebFetch could not retrieve page content beyond the title; needs direct Kaggle account access to inspect. Likely a repackaging of TUNIZI/SenZi-type data.

### 2.5 Kaggle "Tunisian Arabizi Dialect Data – Sentiment Analysis" (waalbannyantudre)
- Likely another TUNIZI repackaging. **Category D — unverified**, not independently fetched.

---

## 3. Category A — monolingual pairs (NOT code-switching), but worth noting for domain relevance

### 3.1 Arabic Google Maps Reviews Dataset for Tourism in Saudi Arabia (closest domain match found)
- **Zenodo:** https://zenodo.org/records/17011574 (DOI 10.5281/zenodo.17011574)
- **Paper:** "Multi-Aspect Sentiment Classification of Arabic Tourism Reviews Using BERT and Classical Machine Learning," *Data* (MDPI) 2025, 10(11), 168. https://www.mdpi.com/2306-5729/10/11/168
- **Size:** 3,543 Arabic Google Maps reviews (Saudi tourist attractions: parks, historical sites, museums, recreational facilities).
- **Category: A — confirmed pure Arabic script, no English/CS text mentioned anywhere in documentation.**
- **Annotation:** 6 aspects (price, cleanliness, facilities, service, environment, overall experience) × 3-class sentiment (positive/neutral/negative); Cohen's Kappa 0.87 (2 annotators).
- **License:** CC BY 4.0. **Format:** .xlsx (city, place name, review text, aspect labels) + README.
- **Relevance:** **Extremely high domain match** (exact same source — Google Maps reviews — and exact same 3-class sentiment scheme as this project) but **zero code-switching** — pure monolingual Arabic. This is a strong candidate as (a) the Arabic half of a monolingual baseline, and (b) a template for annotation methodology (aspect scheme, Kappa reporting), even though it does not address the code-switching novelty claim at all.

### 3.2 ArSAS, ASTD, ArSentD-LEV, AraCust, etc. (Arabic-only Twitter sentiment corpora)
- All confirmed or strongly implied to be **monolingual Arabic** (various dialects) with no systematic English code-mixing documented. Any English tokens present would be incidental/rare loanwords, not a deliberate CS design feature — **Category A**, noted only as background/baseline resources, not pursued further here since other scout agents likely cover these directly.

---

## 4. Category D — leads that could not be verified (need follow-up if time allows)

| Name | What's claimed | Why unverified |
|---|---|---|
| ArE-CSTD (Ar-En Code-Switching Textual Dataset), Kaggle: sdaiancai/arabic-english-code-switching-textual-dataset, also on HF as SDAIANCAI/Ar-En-Code-Switching-Textual-Dataset | ~330K sentences, 3M tokens (1.6M Arabic + 1.3M English), covering MSA, Saudi, and Egyptian dialect splits; created by Saudi NCAI/SDAIA | **Synthetically generated using GPT-4**, not naturally occurring text — this is a critical caveat if used for evaluating "real-world" code-switching; also no sentiment annotation found. Large scale makes it interesting for CS-aware pretraining/fine-tuning, not for authentic sentiment eval. |
| Saudilang Code-Switch Corpus (SCC), Kaggle: sdaiancai/saudilang-code-switch-corpus-scc | ~5 hours, sourced from "Thmanyah" podcast, Arabic-English CS dialogue, built as an **out-of-domain test set** | Not fetched in detail; no sentiment layer apparent; podcast domain not review domain. |
| Arabic-English-Intra-Word-Code-Switching-Corpus, Kaggle: islamkaloop | Intra-word (sub-word level) CS annotation | Not explored in depth; token/intra-word granularity suggests linguistic (language-ID) rather than sentiment annotation. |
| A Code-Switched Arabic-English Sentiment Analysis Approach Based on Deep-Learning (Almasah, Ebrahim, Abdelaal; IEEE MI-UCC 2023; ieeexplore.org/document/10278363) | Custom dataset "collected from various online social networks" specifically because the authors found no existing CS Arabic-English sentiment dataset; CNN reached 83% accuracy, AutoKeras-optimized model reached 86% | IEEE page returned no fetchable abstract content (403/empty); dataset appears to be **private/not released** (standard for many small-lab Arabic NLP papers) — notable corroboration that **as of 2023, researchers found no existing dataset and had to build their own**, which independently supports this scout's overall "weak availability" conclusion. |
| MohamedRashad/arabic-english-code-switching (HF, 12.5k rows) | Audio+text, ASR-oriented, from YouTube | Speech/ASR domain, not sentiment; not pursued further. |
| MouradGad / years0 "multilingual-code-switching-bench" (HF) | Includes Arabizi/Franco-Arabic generation & translation tasks | Benchmark appears MT/generation oriented, not sentiment classification; not pursued further. |
| ArSyra/arsyra-content-mod (HF) | Content-moderation dataset with "2,215 code-switching records (9.3% of total)" | Content-moderation/safety labels, not sentiment polarity; but confirms code-switched Arabic-English text exists incidentally within a modern (likely 2024-25) Arabic safety dataset — a concrete example of "CS appearing incidentally inside a non-CS-purpose-built corpus," which is directly relevant to the "do other corpora incidentally contain CS text" question this scout was asked to flag. |
| SenZi/SALAD/BAERT details | See §2.2–2.3 | Full papers not fetched; sizes/dialects not independently confirmed. |
| Jerbi et al. 2019 Tunisian CS sentiment | See §1.7 | Only survey-summary level info found. |

---

## 5. Does any NON-code-switching-purpose-built corpus *incidentally* contain code-switched text?

Based on available evidence:
- **ArSyra content-moderation dataset (2024/25-era HF dataset)** explicitly reports that 9.3% of its records are code-switching records — strong, concrete evidence that modern large-scale Arabic social-media/safety corpora do incidentally capture real CS text, even when CS was not the design goal. This is a promising place to look for a "mine CS examples out of a larger corpus" strategy (see Recommendation below).
- Dialectal Arabic Twitter/YouTube sentiment corpora (ArSAS, ASTD, AraCust, Adouane's Algerian corpus) are collected from naturalistic social media, where loanwords/brand names/occasional English phrases are common; none of the sources reviewed quantify an "incidental CS rate," but given that Adouane et al.'s Algerian corpus needed a dedicated MIX/CS label specifically because it kept showing up unprompted in regular YouTube comments, it is reasonable to expect any sufficiently large raw Gulf/Levantine/Egyptian Arabic social-media or review corpus to contain a non-trivial minority of code-switched sentences — this just hasn't been systematically measured or released as a separate labeled set for Arabic-English specifically.
- No evidence was found of an existing Arabic-only OR English-only **review** corpus that has been audited/filtered for incidental CS content.

---

## 6. Summary table

| Name | Category | Sentiment labels? | Domain | Dialect | Size | Availability |
|---|---|---|---|---|---|---|
| EESA | B | Yes (3-class) | YouTube comments | Egyptian | ~4,100 (2464/818/818) | Unverified public link; contact authors |
| CS-SNLI | B (synthetic) | No (NLI only; used for downstream sentiment eval elsewhere) | NLI | Egyptian | 258,423 sentences | Unconfirmed |
| Mixat | B (confirmed via CMI) | No | Podcast speech | Emirati/Gulf | 5,316 utterances (36% CS) | GitHub, CC BY-NC-SA 4.0 |
| ArzEn / ArzEn-ST | B | No | Interview speech | Egyptian | 6,216 sentences | On request |
| CSCS | B | No | Student speech | Egyptian | 1,153 sentences | On request |
| Adouane Algerian CS | B (Arabic-French, not English) | Yes (4-class) | YouTube comments | Algerian/MSA/Berber/French | 36,120 comments | Via ACL paper / authors |
| TUNIZI | C (Arabizi, token-tagged) | Yes (binary/3-class, unconfirmed) | Social media comments | Tunisian | ~3K–100K (conflicting) | HF (chaymafourati/tunizi) |
| SenZi | C (Arabizi lexicon) | Lexicon, not corpus | Twitter | Unconfirmed | 24.6K lexicon words + 3.4K tweets | Paper/author request |
| SALAD/BAERT | C (Arabizi) | Yes (subset) | Twitter | Unconfirmed | 7.7M (LAD) / SALAD subset size unknown | Unverified |
| Arabic Google Maps Reviews (Saudi tourism) | A | Yes (3-class × 6 aspects) | **Google Maps reviews** | Saudi | 3,543 reviews | Zenodo, CC BY 4.0 |
| ArE-CSTD | D (synthetic, GPT-4 generated) | No | Generic/MT-style | MSA/Saudi/Egyptian | 330K sentences | Kaggle/HF (SDAIANCAI) |
| Almasah et al. 2023 custom CS sentiment dataset | B (claimed) | Yes | Social networks (unspecified) | Unspecified | Unspecified | Not released (presumed) |
| ArSyra content-mod | D (incidental CS) | No (safety labels) | Content moderation | Unspecified | 2,215 CS records / 9.3% of total | HF |

---

## 7. Recommended strategy for Phase 1 decision (for the main project team)

Given that no dataset combines all three required properties (Arabic-English, genuinely code-switched, sentiment-labeled, review-domain), the most defensible options, roughly in order of rigor-to-effort ratio:

1. **Treat code-switching as an *analysis lens*, not a separate labeled dataset.** Collect/scrape the project's own Google Maps reviews (Arabic + English + mixed), then post-hoc classify each review by script/language-mixing signature (pure Arabic, pure English, Arabizi, genuinely mixed-script) using a simple heuristic (e.g., Code-Mixing Index like Mixat uses, or langid per token). Report model performance broken out by this stratification — this turns "do we have code-switched sentiment data" into "we generated our own, from the exact target domain," which is actually a stronger contribution than reusing an off-domain CS corpus.
2. **Use EESA (if obtainable) as an external validation/robustness check**, not as training data — it's the only dataset found that matches the sentiment scheme and genuine-CS requirement, but domain mismatch (YouTube vs. reviews) means it should supplement, not replace, the project's own data.
3. **Use the Saudi Google-Maps-reviews dataset (Zenodo 17011574) as the monolingual-Arabic baseline/reference** for annotation scheme and as a sanity check on achievable aspect/sentiment agreement (they got Kappa 0.87 with 2 annotators on a near-identical task).
4. **Consider lightweight synthetic augmentation** following Hamed et al.'s lexical-replacement method (arXiv:2205.12649) to manufacture a small internal CS evaluation subset from existing monolingual Arabic/English review sentences — explicitly labeled as synthetic in any writeup, not presented as naturalistic data.
5. If the project is UAE-scoped, flag **Mixat** as the dialect-appropriate linguistic reference for what genuine Gulf-Arabic/English CS looks like (CMI ~0.11, 36% CS rate in natural bilingual podcast speech) — useful for setting realistic expectations about how much of the real review data will actually be code-switched versus just containing isolated loanwords.

---

## 8. Caveats on this research pass

- Most PDF full-text fetches failed (binary/FlateDecode streams not parsed by the fetch tool); conclusions rely heavily on search-engine-generated summaries of abstracts, which can be imprecise — **sizes, exact label schemes, and especially "is this genuinely intra-sentence CS" claims for several Category D entries should be re-verified by directly opening the HTML/abstract pages before citing in any formal deliverable.**
- No access was available to Kaggle/HF pages beyond page titles in several cases (JS-rendered content not fetched).
- Did not exhaustively check Zenodo/Mendeley Data search interfaces directly (relied on web search indexing); a direct Zenodo/Mendeley keyword search ("Arabic English code-switching sentiment") would be a good 15-minute follow-up if more time is available.

# Research Gap Verification

**Project:** Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews
**Status:** Phase 1 — literature verified by dedicated agent via live web search + direct source fetches (not search-summary only). Full raw notes with every reference, URL, and verification method: [`research_raw/literature_review_raw.md`](research_raw/literature_review_raw.md).
**Verification standard applied:** a claim is only used below if it was confirmed by fetching the actual source page/PDF/API (not just an AI search-summary snippet). Items that could not be confirmed this way are explicitly marked unverified and excluded from the gap argument.

## 1. What is already well-covered (do NOT claim as novel)

| Area | Status | Evidence |
|---|---|---|
| Arabic dialect sentiment (MSA, Gulf/Saudi, Levantine, Egyptian, Moroccan) | Saturated, active | AHaSIS (RANLP 2025), DialectSentEval 2026 (ArabicNLP) — multi-team shared tasks, 3-class, multi-dialect |
| English review-domain sentiment (Amazon/Yelp/e-commerce) with transformers | Saturated | Multiple 2022–2025 BERT/transformer papers, verified |
| Arabic transformer baselines (AraBERT, ARBERT/MARBERT, CAMeLBERT) and their benchmarking | Mature | Original papers verified (ACL/EACL/LREC), plus 2026 shared-task comparison confirming MARBERTv2 > AraBERT on dialectal sentiment |
| Multilingual/cross-lingual SA with Arabic as one of several benchmark languages | Reasonably covered | XLM-R, XLM-T, mBERT comparisons exist |
| Arabic Google Maps review mining | Exists, but narrow | AraMAMS (MDPI *Sustainability*, DOI 10.3390/su151612268) and the tourism ABSA paper (MDPI *Data*, DOI 10.3390/data10110168) — both are **aspect-based**, **monolingual dialectal Arabic**, **Saudi/Riyadh-centric** (restaurants, tourism, cafés) |
| **Arabic-English code-switched sentiment classification** | **Exists — not virgin territory** | Three verified papers, all within the last ~24 months: Sherif & Sabty 2024 (SPECOM, origin of the EESA benchmark, Egyptian-English YouTube comments); Rizkallah et al. 2026 (SwitchEmbed, DATA 2026, evaluates on EESA); Alghamdi, Rayson & Alotibi 2026 (SESA-CSD, AbjadNLP 2026, Saudi-English, unspecified social domain) |
| Code-switching detection/language-ID for Arabic-English (as opposed to sentiment) | Long-established | WANLP shared tasks since 2019+ |

**Important correction to the project brief's working assumption:** genuine Arabic-English code-switched sentiment classification is not unclaimed territory. Claiming "the first Arabic-English code-switched sentiment paper" would be **false** and must not appear in the eventual manuscript. The defensible gap is narrower (see §2).

## 2. Verified candidate gap (ranked)

1. **Strongest, confirmed defensible gap:** No identified paper performs sentiment classification on Arabic-English **code-switched Google Maps / location-business reviews**. The two existing CS-Arabic-English sentiment efforts are off-domain (EESA: YouTube comments; SESA-CSD: unspecified Saudi social text), and the existing Arabic Google Maps review work is monolingual-dialectal and aspect-based (AraMAMS, tourism ABSA). **The intersection — review domain × genuine code-switching × document-level 3-class sentiment — has no confirmed prior work.**
2. **Moderate, secondary contribution:** A single study spanning pure Arabic (multi-dialect), pure English, and organically code-switched Arabic-English Google Maps reviews under one consistent 3-class schema and annotation protocol does not appear to exist; prior work isolates one language condition at a time.
3. **Weaker, context-only framing:** A Gulf/UAE-specific instantiation (relevant given the research is being conducted from the UAE) is a narrower slice of gap #1, not an independent gap — present it as a specific instantiation, not a separate contribution.

**Compounding factor, not a separate gap:** neither EESA nor SESA-CSD's underlying data is confirmed publicly obtainable (see [`dataset_audit.md`](dataset_audit.md) and [`research_raw/quality_audit_raw.md`](research_raw/quality_audit_raw.md)). This means the project cannot simply adopt an existing CS-sentiment dataset even if it wanted to — code-switching must be treated as an **analysis lens on self-collected data** rather than an imported labeled resource. This is a methodological necessity, not a convenience choice, and should be framed that way in the paper.

## 3. Provisional novelty framing for the manuscript (contingent on Phase 2 execution — not yet locked in)

Recommended framing, to be used only once the Phase 2 steps it depends on are actually completed: *"To our knowledge, this is the first study to evaluate sentiment classification jointly across monolingual Arabic, monolingual English, and organically code-switched Arabic-English location/business reviews within the Google Maps review domain."*

**This framing is provisional, not confirmed, for two reasons flagged by the independent reviewer pass:** (1) it depends on the Group D (genuinely code-switched) data that does not exist yet — it requires the Phase 2 self-collection effort in `methodology_plan.md` §5, whose feasibility (Places API access, `decisions.md` D5) and yield (`known_limitations.md` #4) are both currently unresolved; if that collection fails or yields too little code-switched material, this framing cannot be used as written. (2) the underlying literature search (`research_raw/literature_review_raw.md`) covered English-indexed venues (ACL Anthology, arXiv, Springer, MDPI, ScienceDirect, SciTePress, ResearchGate, Google Scholar) only — see `known_limitations.md` #11 for the resulting blind spot. Re-confirm this framing at the start of manuscript writing, not now.

Do NOT use: any variant of "first Arabic-English code-switched sentiment paper" (false), "first Arabic Google Maps sentiment paper" (false — AraMAMS and the tourism ABSA paper precede it), or any claim of Q1/acceptance guarantee.

## 4. Areas of insufficient evidence (flagged, not resolved)

- Whether a document-level (non-aspect-based) Arabic Google Maps review dataset exists outside the Saudi/Riyadh restaurant-tourism cluster found — absence of evidence is not evidence of absence here.
- Whether "ArEnSA" is a real dataset — it surfaced only inside an AI search-summary, could not be independently confirmed, and must **not** be cited.
- Full-text content (beyond abstracts) of the Hamed et al. 2025 COLING CS-Arabic-NLP survey and the Shi & Agrawal 2025 NAACL-Findings Arabic SA survey — PDF extraction failed; a follow-up pass is recommended before camera-ready writing if deeper grounding is needed.
- Whether any paper has used LLM zero-shot prompting specifically for Arabic-English CS review sentiment (as distinct from fine-tuned encoders) — worth a targeted search if an LLM-prompting baseline arm is added later.

## 5. Research questions — validated against evidence

See [`methodology_plan.md`](methodology_plan.md) §1 for the final RQ wording and the evidence-based rationale for each revision.

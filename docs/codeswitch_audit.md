# Code-Switch Manual Audit (Phase 2.5)

## Process

A script heuristic (character-script-fraction based, see `methodology_plan.md` §4–5) flagged 109 documents out of 1,050,832 usable reviews as candidate "mixed Arabic-English" text. Because the candidate set was small enough to inspect exhaustively, every one of the 109 was manually classified rather than sampled.

**Two independent agent reviewers** read and classified all 109 rows blind (Reviewer B had no access to Reviewer A's labels). A third pass (the lead researcher) read the original text of every disagreement and made a final, documented arbitration call. Raw reviewer outputs: `research_raw/codeswitch_audit_reviewerA.csv`, `research_raw/codeswitch_audit_reviewerB.csv`. Final reconciled file: **`data/annotations/mixed_manual_audit.csv`** (columns: review_id, review_text, automatic_label, manual_category, include_as_real_codeswitch, agreement_status, notes).

## Operational code-switching criterion (applied strictly)

A document counts as `genuine_code_switch` **only if** Arabic and English (or Arabizi) are interleaved within the same sentence or the same short span of connected thought (e.g. an English word/phrase embedded inside an Arabic sentence, or a reviewer who starts a sentence in one language and continues the same narrative thread in the other, introducing new content rather than repeating themselves).

It is explicitly **NOT** code-switching if the document is:
- `bilingual_translation_pair` — a full passage in one language followed by its own translation into the other (most commonly Google Maps' own "(Translated by Google)/(Original)" display structure, but also user-authored self-translation)
- `named_entity_or_brand` — a single proper noun/brand name in the other script inside an otherwise monolingual review
- `incidental_english` — a stray word/interjection with no real bilingual sentence structure
- `arabizi` — Arabic written in Latin script without genuine English content mixed in
- `other` — keyboard noise, a different non-Arabic script misidentified by the heuristic (e.g. Persian/Farsi), non-semantic gibberish, or anything else that doesn't fit cleanly
- `uncertain` — genuinely ambiguous from the text alone

## Inter-rater reliability

| Measure | Value |
|---|---|
| Exact 7-category agreement | 103/109 = 94.5% |
| Cohen's κ (7-category) | 0.853 |
| Binary (genuine-code-switch yes/no) agreement | 106/109 = 97.2% |
| Cohen's κ (binary) | 0.809 |

Both figures indicate strong agreement (κ > 0.8), consistent with the annotation-quality bar used elsewhere in this project (cf. the κ=0.87 reported for Zenodo 17011574). Six disagreements were individually arbitrated by the lead researcher after re-reading the disputed text directly; reasoning for each is recorded in `data/annotations/mixed_manual_audit.csv`.

## What the heuristic actually caught (root-cause finding)

Manual inspection revealed the 109-candidate heuristic set was overwhelmingly **not** code-switching:

| Category | Count | % of 109 |
|---|---|---|
| bilingual_translation_pair | 84 | 77.1% |
| other (incl. misidentified Farsi/Hebrew, gibberish/keyboard noise) | 13 | 11.9% |
| **genuine_code_switch** | **9** | **8.3%** |
| named_entity_or_brand | 2 | 1.8% |
| incidental_english | 1 | 0.9% |

**Root cause of the false-positive rate:** the dominant pattern (84/109) is Google Maps' own UI convention of displaying a machine translation alongside the original text — a platform display artifact, not evidence of the reviewer code-switching. A secondary pattern (identified independently by both reviewers) is that the script-fraction heuristic conflates any Arabic-alphabet script with Arabic specifically, misclassifying several Persian/Farsi-English and at least one Hebrew/German-English document as "Arabic-English."

## Final verified result

**9 genuine Arabic-English code-switched reviews, out of 1,050,832 usable documents across the entire corpus (≈0.00086%).** IDs: AR-JOR-01270, AR-JOR-04350, AR-JOR-04600, AR-JOR-06216, AR-JOR-07320, AR-JOR-07449, AR-JOR-07691, EN-VT-0213840, EN-VT-0613379.

**This sample is far too small for any statistically meaningful standalone model comparison.** Nine examples cannot support a train/test split, a confidence interval, or a significance test. **E6 (real-world code-switch evaluation) is NOT feasible as a quantitative experiment with the data collected so far.** This confirms, with direct evidence rather than inference, the Phase 1/2 audit's concern that genuinely code-switched material would be rare in these sources (`known_limitations.md` #4).

**Recommended disposition:**
- These 9 examples are retained as a **qualitative diagnostic set only** — useful for illustrating code-switching phenomena in error analysis (RQ4) and for a short qualitative case-study subsection, never for a quantitative E6 metric.
- Any future attempt at a quantitative code-switch evaluation **requires dedicated new data collection** (e.g. Gulf-region social media or review platforms with higher natural code-mixing rates, per the literature review's note that EESA/SESA-CSD both drew from YouTube/social text rather than reviews) — not more mining of the current review-dataset sources, which have now been exhaustively checked for this phenomenon.
- Do not re-run the script heuristic at a looser threshold hoping for more hits without a corresponding manual re-audit — the false-positive mechanism (translation-pair UI structure) will dominate at any threshold applied to this corpus.

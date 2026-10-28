# Pilot Annotation — Decision Guide

Read this before opening `pilot_annotation_sheet.csv`. This is a 20-review pilot (10 Arabic, 10 English) to check the protocol is clear and comfortable to apply before the full 757-review round begins. You will see only the review text — no rating, no prior label, no other annotator's answers.

For each review, judge the **overall net impression**, not sentence-by-sentence.

- **Positive** — the overall impression is favorable, even if one detail is criticized. *("Parking was annoying but the food was amazing" → Positive.)*
- **Negative** — the overall impression is unfavorable, even if one detail is praised. *("Food was fine but the service was rude" → Negative.)*
- **Neutral** — no clear net lean either way: purely factual/descriptive text, or a review where positive and negative genuinely balance out.
- **Ambiguous / uncertain** — this is not a fourth label. If you genuinely cannot decide even after careful reading, pick your best-guess label from the three above, set `confidence` to **low**, and briefly say why in `notes` (e.g. "too short to tell," "unclear what it's referring to").
- **Mixed sentiment** — also not a separate label. If a review contains *both* clearly positive and clearly negative content — regardless of which way you leaned for the main label — set `mixed_sentiment_flag` to **yes**. A review can be confidently mixed (you're sure it's genuinely split) or one-sided; this flag is independent of your confidence level.

## What to fill in, per row

| Column | What goes here |
|---|---|
| `sentiment_label` | `Positive`, `Neutral`, or `Negative` |
| `confidence` | `high`, `medium`, or `low` |
| `mixed_sentiment_flag` | `yes` or `no` |
| `notes` | Optional — anything that made the call hard (sarcasm, negation, an unfamiliar word, a very short/vague review, mixed-language text, etc.) |

Work through the rows in the order given — don't skip around. There's no time limit, but a first-instinct call is more useful here than long deliberation; that's what `confidence` and `notes` are for.

This is only 20 reviews — if anything about these instructions feels unclear or awkward while you're doing them, that's exactly what this pilot is for. Say so when you hand it back, even if you still completed every row.

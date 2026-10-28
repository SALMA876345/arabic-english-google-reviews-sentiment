# Annotator Instructions — Matched-Protocol Validation Slice

You are labeling the **sentiment** of short location/business reviews. Some are in Arabic, some in English, some may contain a brief mix of both — read each one on its own.

**You will see only the review text.** No star rating, no prior label, and no information about which dataset a review came from is shown to you — this is intentional. Judge each review purely on what it says.

## Step 1: Assign a sentiment label

Choose exactly one:

- **Positive** — the reviewer's overall impression is favorable, even if they mention a specific complaint, as long as the net impression is positive. *("Parking was annoying but the food was amazing, would go again" → Positive.)*
- **Negative** — the reviewer's overall impression is unfavorable, even if they mention something positive, as long as the net impression is negative. *("Food was fine but service was so rude we're never going back" → Negative.)*
- **Neutral** — use this when the review is genuinely mixed with no clear net lean, is purely factual/descriptive with no evaluative sentiment, or is too short/vague for you to confidently call Positive or Negative.

Judge the review **as a whole**, not sentence-by-sentence. A review is not automatically Neutral just because it contains both praise and criticism — only use Neutral when there is genuinely no net lean either way.

## Step 2: Mark your confidence

- **High** — you're confident in the label.
- **Medium** — reasonably confident, but the review has some ambiguity.
- **Low** — you're genuinely unsure; this was a hard call.

## Step 3: Flag mixed sentiment (yes/no)

Separately from your label, mark **yes** if the review contains *both* clearly positive and clearly negative content (regardless of which way you ultimately leaned for the main label), and **no** otherwise. This is not the same as low confidence — a review can be confidently mixed (you're sure it's genuinely split) or confidently one-sided.

## Step 4: Notes (optional, but please use for anything unusual)

Briefly note anything that made a review hard to classify — sarcasm, negation that flips the meaning, an unfamiliar dialect word, a very short or vague review, an unclear reference, mixed-language text, or anything else. These notes feed directly into the project's error-analysis work, so plain, honest observations are more useful than none at all.

## General notes

- Work through the reviews in the order given — don't skip around or group by language/sentiment.
- There is no time limit, but try to make a first-instinct call rather than deliberating at length over borderline cases — that's exactly what the confidence and notes fields are for.
- You will not see what the other annotator wrote. Please don't discuss specific reviews with them until both of you have finished your full set.
- If a review is garbled, cut off, or clearly not a real review (e.g. test data, spam), label it the best you honestly can and say so in the notes — don't skip it.

Thank you — this is the single most important remaining piece of evidence for one of this project's central research questions.

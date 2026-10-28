# Adjudicator Instructions

You are resolving 179 reviews where three independent annotators did not all agree on the sentiment. You are seeing **only the review text** — no rating, no prior label, no information about how many annotators chose which label, and no identity of who chose what. This is deliberate: it keeps your decision independent and prevents anchoring on someone else's call (including a majority of two).

## What you are deciding

For each review, read the text and decide:

1. **Sentiment** — Positive, Neutral, or Negative, using the exact same rule given to the original annotators:
   - **Positive** — the overall impression is favorable, even with a minor criticism mentioned.
   - **Negative** — the overall impression is unfavorable, even with something positive mentioned.
   - **Neutral** — no clear positive or negative net lean: purely factual/descriptive, or genuinely balanced between positive and negative with no net direction.
   Judge the review **as a whole**, not sentence by sentence.

2. **Confidence** — High, Medium, or Low, reflecting how sure you are of your own call on this specific review, not any guess about why the original annotators disagreed.

3. **Reason** (optional, but please use it) — a short note on why you decided what you decided. This becomes the permanent documentation of how this case was resolved, so even a brief phrase ("mostly positive, one complaint doesn't change the net impression" / "genuinely balanced, no net lean") is valuable. You don't need to write one for every case if your reasoning is simple and the label is obvious to you, but use it whenever the decision required real judgment.

**You are not asked about mixed sentiment here.** That variable is being treated as exploratory for this project (the three original annotators did not agree on it reliably enough to trust it as-is), so it is intentionally left out of this stage.

## Why you're not shown more

You are not told how many of the three original annotators chose each label, who they were, what the review's star rating was, what any model predicted, or what the dataset's own original label was. This is not an oversight — showing you any of that would let it influence your judgment before you've formed your own independent read of the text, which defeats the purpose of having a separate adjudication step at all.

## Using the interface

- Click Sentiment, then Confidence (in either order). Add a reason if you want to. The interface automatically saves your answer and moves to the next case once both required selections are made.
- Use **Back** to revise the case you just answered — it only steps back one at a time.
- Your progress saves automatically after every decision, in your browser, on your machine. Closing or refreshing the page does not lose your work — reopening the same file resumes where you left off.
- When all 179 cases are done, the page will say so clearly. Click **Export Results** and send that file back exactly as downloaded.
- If you export before finishing, the filename will say `INCOMPLETE_<N>remaining` — fine as a backup, but only a file marked `COMPLETE` should be treated as your final submission.

Thank you — this closes out the last open piece of the human-validation round.

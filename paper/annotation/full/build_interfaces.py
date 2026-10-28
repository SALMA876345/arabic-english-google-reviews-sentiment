"""
Generates three self-contained, offline HTML annotation interfaces, one per
annotator, each embedding that annotator's own pre-shuffled 757-review order
(read from annotator_N_blinded.csv, produced by build_blinded_sheets.py --
run that script first).

Each HTML file is fully standalone: no server, no network calls, no external
JS/CSS dependencies. Progress is persisted in the browser's localStorage,
keyed by annotator ID, so closing/refreshing the browser never erases work.

Run from the repository root: python paper/annotation/full/build_interfaces.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper" / "annotation" / "full"

ANNOTATORS = ["annotator_1", "annotator_2", "annotator_3"]

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Sentiment Annotation -- __ANNOTATOR_LABEL__</title>
<style>
  :root {
    --bg: #f8fafc; --surface: #ffffff; --border: #e2e8f0; --text: #0f172a; --muted: #64748b;
    --accent: #2563eb; --positive: #16a34a; --neutral: #ca8a04; --negative: #dc2626;
  }
  * { box-sizing: border-box; }
  body { font-family: system-ui, "Segoe UI", Roboto, Tahoma, sans-serif; background: var(--bg);
         color: var(--text); margin: 0; padding: 0; }
  .wrap { max-width: 760px; margin: 0 auto; padding: 1.5rem; }
  header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; flex-wrap: wrap; gap: .5rem;}
  h1 { font-size: 1.1rem; margin: 0; }
  .progress-line { font-size: .85rem; color: var(--muted); }
  .progress-bar { height: 8px; background: var(--border); border-radius: 999px; overflow: hidden; margin-bottom: 1rem; }
  .progress-bar-fill { height: 100%; background: var(--accent); transition: width .2s ease; }
  .counts { display: flex; gap: 1rem; font-size: .85rem; color: var(--muted); margin-bottom: 1rem; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
  .lang-badge { display: inline-block; font-size: .7rem; text-transform: uppercase; letter-spacing: .05em;
                padding: .15rem .5rem; border-radius: 999px; background: var(--border); color: var(--muted); margin-bottom: .75rem; }
  .review-text { font-size: 1.15rem; line-height: 1.6; min-height: 4rem; margin-bottom: 1.5rem; white-space: pre-wrap; }
  .review-text[dir="rtl"] { text-align: right; }
  fieldset { border: none; margin: 0 0 1.25rem; padding: 0; }
  legend { font-size: .8rem; font-weight: 600; color: var(--muted); margin-bottom: .5rem; text-transform: uppercase; letter-spacing: .03em; }
  .btn-row { display: flex; gap: .5rem; flex-wrap: wrap; }
  .choice-btn { font: inherit; font-size: .95rem; padding: .55rem 1.1rem; border-radius: 8px; border: 1px solid var(--border);
                background: var(--bg); cursor: pointer; }
  .choice-btn.selected { border-color: var(--accent); background: var(--accent); color: #fff; font-weight: 600; }
  .choice-btn.selected.pos { background: var(--positive); border-color: var(--positive); }
  .choice-btn.selected.neu { background: var(--neutral); border-color: var(--neutral); }
  .choice-btn.selected.neg { background: var(--negative); border-color: var(--negative); }
  textarea { width: 100%; font: inherit; font-size: .9rem; padding: .6rem; border-radius: 8px; border: 1px solid var(--border);
             min-height: 3.5rem; resize: vertical; }
  .nav-row { display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; gap: .75rem; flex-wrap: wrap; }
  .btn { font: inherit; font-weight: 600; padding: .6rem 1.3rem; border-radius: 8px; border: 1px solid var(--border);
         background: var(--surface); cursor: pointer; }
  .btn:disabled { opacity: .5; cursor: not-allowed; }
  .btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
  .btn.export { background: #0f172a; color: #fff; border-color: #0f172a; }
  .status-banner { margin-top: 1rem; font-size: .85rem; padding: .6rem .9rem; border-radius: 8px; }
  .status-banner.complete { background: rgba(22,163,74,.1); color: var(--positive); border: 1px solid var(--positive); }
  .status-banner.incomplete { background: rgba(202,138,4,.1); color: var(--neutral); border: 1px solid var(--neutral); }
  footer { margin-top: 1.5rem; font-size: .75rem; color: var(--muted); text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Sentiment Annotation &mdash; __ANNOTATOR_LABEL__</h1>
    <span class="progress-line" id="progressLine">0 / __TOTAL__</span>
  </header>
  <div class="progress-bar"><div class="progress-bar-fill" id="progressFill" style="width:0%"></div></div>
  <div class="counts">
    <span id="completedCount">Completed: 0 / __TOTAL__</span>
    <span id="remainingCount">Remaining: __TOTAL__</span>
  </div>

  <div class="card">
    <span class="lang-badge" id="langBadge">language</span>
    <div class="review-text" id="reviewText" dir="ltr"></div>

    <fieldset>
      <legend>Sentiment (required)</legend>
      <div class="btn-row">
        <button class="choice-btn" data-group="sentiment" data-value="Positive" data-cls="pos">Positive</button>
        <button class="choice-btn" data-group="sentiment" data-value="Neutral" data-cls="neu">Neutral</button>
        <button class="choice-btn" data-group="sentiment" data-value="Negative" data-cls="neg">Negative</button>
      </div>
    </fieldset>

    <fieldset>
      <legend>Confidence (required)</legend>
      <div class="btn-row">
        <button class="choice-btn" data-group="confidence" data-value="high">High</button>
        <button class="choice-btn" data-group="confidence" data-value="medium">Medium</button>
        <button class="choice-btn" data-group="confidence" data-value="low">Low</button>
      </div>
    </fieldset>

    <fieldset>
      <legend>Mixed sentiment? (required)</legend>
      <div class="btn-row">
        <button class="choice-btn" data-group="mixed" data-value="yes">Yes</button>
        <button class="choice-btn" data-group="mixed" data-value="no">No</button>
      </div>
    </fieldset>

    <fieldset>
      <legend>Notes (optional)</legend>
      <textarea id="notesBox" placeholder="Anything that made this hard to classify..."></textarea>
    </fieldset>

    <div class="nav-row">
      <button class="btn" id="backBtn">&larr; Back</button>
      <button class="btn export" id="exportBtn">Export Results</button>
    </div>
    <div class="status-banner incomplete" id="statusBanner"></div>
  </div>
  <footer>review_id and presentation order are fixed per annotator and preserved on export. Progress saves automatically after every review.</footer>
</div>

<script>
const ANNOTATOR_ID = "__ANNOTATOR_ID__";
const STORAGE_KEY = "sentiment_annotation_" + ANNOTATOR_ID + "_v1";
const REVIEWS = __REVIEWS_JSON__;
const TOTAL = REVIEWS.length;

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) {
    try { return JSON.parse(raw); } catch (e) { /* fall through to fresh state */ }
  }
  return { currentIndex: 0, answers: {} };
}
function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();
let pending = { sentiment_label: "", confidence: "", mixed_sentiment_flag: "" };

function firstUnansweredIndex() {
  for (let i = 0; i < TOTAL; i++) {
    const r = REVIEWS[i];
    if (!state.answers[r.review_id]) return i;
  }
  return TOTAL - 1;
}

// On load, jump to the first unanswered review (resume behavior), but respect
// a manually-moved currentIndex if the saved state already points somewhere valid.
if (state.currentIndex === undefined || state.currentIndex >= TOTAL) {
  state.currentIndex = firstUnansweredIndex();
}

function completedCount() {
  return Object.keys(state.answers).filter(id => {
    const a = state.answers[id];
    return a && a.sentiment_label && a.confidence && a.mixed_sentiment_flag;
  }).length;
}

function render() {
  const idx = state.currentIndex;
  const review = REVIEWS[idx];
  const saved = state.answers[review.review_id] || {};
  pending = {
    sentiment_label: saved.sentiment_label || "",
    confidence: saved.confidence || "",
    mixed_sentiment_flag: saved.mixed_sentiment_flag || "",
  };

  document.getElementById("progressLine").textContent = (idx + 1) + " / " + TOTAL;
  document.getElementById("progressFill").style.width = (((idx + 1) / TOTAL) * 100) + "%";
  document.getElementById("langBadge").textContent = review.language;
  const textEl = document.getElementById("reviewText");
  textEl.textContent = review.text;
  textEl.setAttribute("dir", review.language === "arabic" ? "rtl" : "ltr");

  document.querySelectorAll(".choice-btn").forEach(btn => {
    const group = btn.dataset.group;
    const key = group === "sentiment" ? "sentiment_label" : (group === "mixed" ? "mixed_sentiment_flag" : "confidence");
    btn.classList.toggle("selected", pending[key] === btn.dataset.value);
  });

  document.getElementById("notesBox").value = saved.notes || "";
  document.getElementById("backBtn").disabled = (idx === 0);

  const done = completedCount();
  document.getElementById("completedCount").textContent = "Completed: " + done + " / " + TOTAL;
  document.getElementById("remainingCount").textContent = "Remaining: " + (TOTAL - done);
  const banner = document.getElementById("statusBanner");
  if (done >= TOTAL) {
    banner.textContent = "All " + TOTAL + " reviews completed. You may export your final results.";
    banner.className = "status-banner complete";
  } else {
    banner.textContent = (TOTAL - done) + " review(s) remaining -- export now only produces an INCOMPLETE file.";
    banner.className = "status-banner incomplete";
  }
}

function maybeAdvance() {
  if (pending.sentiment_label && pending.confidence && pending.mixed_sentiment_flag) {
    const review = REVIEWS[state.currentIndex];
    state.answers[review.review_id] = {
      sentiment_label: pending.sentiment_label,
      confidence: pending.confidence,
      mixed_sentiment_flag: pending.mixed_sentiment_flag,
      notes: document.getElementById("notesBox").value || "",
    };
    saveState();
    if (state.currentIndex < TOTAL - 1) {
      state.currentIndex += 1;
      saveState();
      render();
    } else {
      render(); // stay on last review, banner will show completion if done
    }
  }
}

document.querySelectorAll(".choice-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const group = btn.dataset.group;
    const key = group === "sentiment" ? "sentiment_label" : (group === "mixed" ? "mixed_sentiment_flag" : "confidence");
    pending[key] = btn.dataset.value;
    document.querySelectorAll('.choice-btn[data-group="' + group + '"]').forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    maybeAdvance();
  });
});

document.getElementById("notesBox").addEventListener("blur", () => {
  const review = REVIEWS[state.currentIndex];
  if (state.answers[review.review_id]) {
    state.answers[review.review_id].notes = document.getElementById("notesBox").value || "";
    saveState();
  }
});

document.getElementById("backBtn").addEventListener("click", () => {
  if (state.currentIndex > 0) {
    state.currentIndex -= 1;
    saveState();
    render();
  }
});

function csvEscape(val) {
  if (val === null || val === undefined) val = "";
  val = String(val);
  if (/[",\n]/.test(val)) {
    val = '"' + val.replace(/"/g, '""') + '"';
  }
  return val;
}

document.getElementById("exportBtn").addEventListener("click", () => {
  const done = completedCount();
  const complete = done >= TOTAL;
  const header = ["review_id", "language", "sentiment_label", "confidence", "mixed_sentiment_flag", "notes"];
  const lines = [header.join(",")];
  // Export in ORIGINAL master order (fixed canonical order), not this annotator's
  // display order, so review_id is the only merge key ever needed downstream.
  const byId = {};
  REVIEWS.forEach(r => { byId[r.review_id] = r; });
  const canonicalOrder = Object.keys(byId).sort();
  canonicalOrder.forEach(id => {
    const r = byId[id];
    const a = state.answers[id] || {};
    lines.push([
      csvEscape(r.review_id), csvEscape(r.language), csvEscape(a.sentiment_label || ""),
      csvEscape(a.confidence || ""), csvEscape(a.mixed_sentiment_flag || ""), csvEscape(a.notes || ""),
    ].join(","));
  });
  const csv = "﻿" + lines.join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const statusTag = complete ? "COMPLETE" : ("INCOMPLETE_" + (TOTAL - done) + "remaining");
  const ts = new Date().toISOString().replace(/[:.]/g, "-");
  a.href = url;
  a.download = ANNOTATOR_ID + "_" + statusTag + "_" + ts + ".csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});

render();
</script>
</body>
</html>
"""


def main():
    for name in ANNOTATORS:
        blinded = pd.read_csv(OUT / f"{name}_blinded.csv")
        assert len(blinded) == 757
        records = blinded[["review_id", "language", "text"]].to_dict(orient="records")
        reviews_json = json.dumps(records, ensure_ascii=False)

        label = name.replace("_", " ").title()
        html = (TEMPLATE
                .replace("__ANNOTATOR_ID__", name)
                .replace("__ANNOTATOR_LABEL__", label)
                .replace("__TOTAL__", str(len(records)))
                .replace("__REVIEWS_JSON__", reviews_json))

        out_path = OUT / f"{name}_interface.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"Wrote {out_path} ({len(records)} reviews embedded)")


if __name__ == "__main__":
    main()

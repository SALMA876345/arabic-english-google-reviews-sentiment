"""
Generates the standalone, offline HTML adjudication interface from
adjudication_blinded.csv (179 rows -- run build_blinded_adjudication.py first).

No server, no network calls. Only review_id, language, and text are embedded
-- no annotator labels, no majority_label, no agreement_type, no rating, no
original label, no model anything. Progress persists in localStorage.

Run: python paper/annotation/full/adjudication/build_adjudicator_interface.py
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Sentiment Adjudication</title>
<style>
  :root {
    --bg: #f8fafc; --surface: #ffffff; --border: #e2e8f0; --text: #0f172a; --muted: #64748b;
    --accent: #7c3aed; --positive: #16a34a; --neutral: #ca8a04; --negative: #dc2626;
  }
  * { box-sizing: border-box; }
  body { font-family: system-ui, "Segoe UI", Roboto, Tahoma, sans-serif; background: var(--bg);
         color: var(--text); margin: 0; padding: 0; }
  .wrap { max-width: 760px; margin: 0 auto; padding: 1.5rem; }
  header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; flex-wrap: wrap; gap: .5rem;}
  h1 { font-size: 1.1rem; margin: 0; }
  .subtitle { font-size: .8rem; color: var(--muted); margin-top: .2rem; }
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
    <div>
      <h1>Sentiment Adjudication</h1>
      <div class="subtitle">You are seeing only the review text. No rating, no prior label, no annotator count or identity is shown.</div>
    </div>
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
      <legend>Reason (optional, short)</legend>
      <textarea id="reasonBox" placeholder="Brief rationale for this decision..."></textarea>
    </fieldset>

    <div class="nav-row">
      <button class="btn" id="backBtn">&larr; Back</button>
      <button class="btn export" id="exportBtn">Export Results</button>
    </div>
    <div class="status-banner incomplete" id="statusBanner"></div>
  </div>
  <footer>review_id is preserved on export. Progress saves automatically after every decision.</footer>
</div>

<script>
const STORAGE_KEY = "sentiment_adjudication_v1";
const REVIEWS = __REVIEWS_JSON__;
const TOTAL = REVIEWS.length;

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) {
    try { return JSON.parse(raw); } catch (e) { /* fall through */ }
  }
  return { currentIndex: 0, answers: {} };
}
function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();
let pending = { adjudicated_sentiment: "", adjudication_confidence: "" };

function firstUnansweredIndex() {
  for (let i = 0; i < TOTAL; i++) {
    const r = REVIEWS[i];
    if (!state.answers[r.review_id]) return i;
  }
  return TOTAL - 1;
}

if (state.currentIndex === undefined || state.currentIndex >= TOTAL) {
  state.currentIndex = firstUnansweredIndex();
}

function completedCount() {
  return Object.keys(state.answers).filter(id => {
    const a = state.answers[id];
    return a && a.adjudicated_sentiment && a.adjudication_confidence;
  }).length;
}

function render() {
  const idx = state.currentIndex;
  const review = REVIEWS[idx];
  const saved = state.answers[review.review_id] || {};
  pending = {
    adjudicated_sentiment: saved.adjudicated_sentiment || "",
    adjudication_confidence: saved.adjudication_confidence || "",
  };

  document.getElementById("progressLine").textContent = (idx + 1) + " / " + TOTAL;
  document.getElementById("progressFill").style.width = (((idx + 1) / TOTAL) * 100) + "%";
  document.getElementById("langBadge").textContent = review.language;
  const textEl = document.getElementById("reviewText");
  textEl.textContent = review.text;
  textEl.setAttribute("dir", review.language === "arabic" ? "rtl" : "ltr");

  document.querySelectorAll(".choice-btn").forEach(btn => {
    const group = btn.dataset.group;
    const key = group === "sentiment" ? "adjudicated_sentiment" : "adjudication_confidence";
    btn.classList.toggle("selected", pending[key] === btn.dataset.value);
  });

  document.getElementById("reasonBox").value = saved.adjudication_reason || "";
  document.getElementById("backBtn").disabled = (idx === 0);

  const done = completedCount();
  document.getElementById("completedCount").textContent = "Completed: " + done + " / " + TOTAL;
  document.getElementById("remainingCount").textContent = "Remaining: " + (TOTAL - done);
  const banner = document.getElementById("statusBanner");
  if (done >= TOTAL) {
    banner.textContent = "All " + TOTAL + " cases adjudicated. You may export your final results.";
    banner.className = "status-banner complete";
  } else {
    banner.textContent = (TOTAL - done) + " case(s) remaining -- export now only produces an INCOMPLETE file.";
    banner.className = "status-banner incomplete";
  }
}

function maybeAdvance() {
  if (pending.adjudicated_sentiment && pending.adjudication_confidence) {
    const review = REVIEWS[state.currentIndex];
    state.answers[review.review_id] = {
      adjudicated_sentiment: pending.adjudicated_sentiment,
      adjudication_confidence: pending.adjudication_confidence,
      adjudication_reason: document.getElementById("reasonBox").value || "",
    };
    saveState();
    if (state.currentIndex < TOTAL - 1) {
      state.currentIndex += 1;
      saveState();
      render();
    } else {
      render();
    }
  }
}

document.querySelectorAll(".choice-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const group = btn.dataset.group;
    const key = group === "sentiment" ? "adjudicated_sentiment" : "adjudication_confidence";
    pending[key] = btn.dataset.value;
    document.querySelectorAll('.choice-btn[data-group="' + group + '"]').forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    maybeAdvance();
  });
});

document.getElementById("reasonBox").addEventListener("blur", () => {
  const review = REVIEWS[state.currentIndex];
  if (state.answers[review.review_id]) {
    state.answers[review.review_id].adjudication_reason = document.getElementById("reasonBox").value || "";
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
  const header = ["review_id", "language", "adjudicated_sentiment", "adjudication_confidence", "adjudication_reason"];
  const lines = [header.join(",")];
  const byId = {};
  REVIEWS.forEach(r => { byId[r.review_id] = r; });
  const canonicalOrder = Object.keys(byId).sort();
  canonicalOrder.forEach(id => {
    const r = byId[id];
    const a = state.answers[id] || {};
    lines.push([
      csvEscape(r.review_id), csvEscape(r.language), csvEscape(a.adjudicated_sentiment || ""),
      csvEscape(a.adjudication_confidence || ""), csvEscape(a.adjudication_reason || ""),
    ].join(","));
  });
  const csv = "﻿" + lines.join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const statusTag = complete ? "COMPLETE" : ("INCOMPLETE_" + (TOTAL - done) + "remaining");
  const ts = new Date().toISOString().replace(/[:.]/g, "-");
  a.href = url;
  a.download = "adjudication_" + statusTag + "_" + ts + ".csv";
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
    blinded = pd.read_csv(HERE / "adjudication_blinded.csv")
    assert len(blinded) == 179

    forbidden = {"annotator_1_sentiment", "annotator_2_sentiment", "annotator_3_sentiment",
                 "majority_label", "agreement_type", "rating", "original_label"}
    assert not (forbidden & set(blinded.columns)), "Hidden fields present in blinded.csv -- aborting."

    records = blinded[["review_id", "language", "text"]].to_dict(orient="records")
    reviews_json = json.dumps(records, ensure_ascii=False)

    html = TEMPLATE.replace("__TOTAL__", str(len(records))).replace("__REVIEWS_JSON__", reviews_json)

    out_path = HERE / "adjudicator_interface.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} ({len(records)} cases embedded, zero hidden fields)")


if __name__ == "__main__":
    main()

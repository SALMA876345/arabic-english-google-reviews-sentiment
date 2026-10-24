# Multilingual Sentiment Analysis of Arabic-English Google Maps Reviews

Research project (working title) studying 3-class (Positive/Neutral/Negative) sentiment classification across Arabic, English, and Arabic-English code-switched location/business reviews.

**Status: Phase 1 complete — dataset/literature verification and experimental design only. No model has been trained yet.**

## Phase 1 outputs

- [`docs/research_gap.md`](docs/research_gap.md) — verified literature findings and the confirmed research gap
- [`docs/dataset_audit.md`](docs/dataset_audit.md) — dataset discovery, scoring, and final selection rationale
- [`docs/methodology_plan.md`](docs/methodology_plan.md) — task definition, preprocessing, models, evaluation plan (design only)
- [`docs/decisions.md`](docs/decisions.md) — decision log with alternatives, evidence, rationale, risks
- [`docs/known_limitations.md`](docs/known_limitations.md) — structural limitations to carry into the eventual paper
- [`data/dataset_inventory.csv`](data/dataset_inventory.csv) — machine-readable audit of 34 candidate datasets
- [`docs/research_raw/`](docs/research_raw/) — full raw research-agent notes (literature, Arabic/English/code-switch dataset scouting, quality audit) preserved for provenance

## Repository structure

```
data/            raw/, processed/, annotations/, dataset_inventory.csv
src/             preprocessing/, language_detection/, baselines/, transformers/, evaluation/, utils/
experiments/     per-run config snapshots (Phase 2+)
results/         tables/, figures/, predictions/ (Phase 2+)
tests/
paper/           manuscript/, references/, notes/
docs/            research_gap.md, dataset_audit.md, methodology_plan.md, decisions.md, known_limitations.md, research_raw/
configs/
```

## Next step

Awaiting approval to proceed to Phase 2 (data preparation, matched-protocol validation slice, baseline implementation). See the Phase 1 report delivered in-conversation for the full A–J summary.

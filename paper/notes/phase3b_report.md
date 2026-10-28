# Phase 3B Report — Kaggle GPU Full Fine-Tuning Experiments

**Date integrated:** 2026-10-26
**Status:** Results received from external Kaggle GPU runs (2×Tesla T4), integrated and audited, not retrained. This is documentation of received results, not a new experimental run performed in this session.

## Relationship to Phase 3A

Phase 3A (`paper/notes/phase3_report.md`) ran on a CPU-only, 8.3GB-RAM laptop and used LoRA adapters because full fine-tuning OOM'd (`docs/decisions.md` D14). Phase 3B ran the same research questions with full fine-tuning on GPU. **Both tracks are preserved; neither replaces the other.** Phase 3A remains the project's documented resource-constrained baseline; Phase 3B is the adequately-resourced comparison. See `docs/decisions.md` D17 for the full integration record.

**Non-causal framing (binding):** Phase 3A and Phase 3B differ in fine-tuning method (LoRA vs. full), class-weighting (unweighted vs. weighted loss), and max_seq_length (64 vs. 128) simultaneously with hardware. Any score difference must be attributed to "the full-fine-tuning/weighted-loss/GPU configuration," never to "the GPU" alone.

**Data integrity:** independently re-verified by MD5 hash — the exact frozen train/val/test splits and review-ID manifests sent to Kaggle (`results/phase3b_kaggle_gpu/input_data_bundle_sent_to_kaggle/`) are byte-for-byte identical to `data/processed/frozen_v1/` and `data/splits/frozen_v1/`. Every prediction file's row count (369 Arabic / 388 English) matches the frozen test split sizes exactly. Phase 3B evaluated on the same frozen test set as Phase 3A, not a different one.

## Primary results (Test Macro-F1)

| Language | Model | Setting | Macro-F1 | Status |
|---|---|---|---|---|
| Arabic | MARBERT Full FT + Weighted Loss | Standalone | **0.785025** | Primary |
| Arabic | XLM-R Multilingual | Combined training | 0.767865 | Primary (= research E4 result) |
| Arabic | XLM-R Full FT + Weighted Loss | Standalone | 0.740295 | Primary |
| Arabic | TF-IDF + LogReg | Laptop classical baseline | 0.705000 | Phase 3A, for reference |
| Arabic | XLM-R English→Arabic | Zero-shot cross-lingual | 0.679992 | Primary |
| Arabic | XLM-R + LoRA | Laptop (Phase 3A) | 0.623300 | Phase 3A, for reference |
| English | XLM-R Multilingual | Combined training | **0.739722** | Primary (= research E4 result) |
| English | XLM-R Full FT + Weighted Loss | Standalone | 0.727644 | Primary |
| English | TF-IDF + LogReg | Laptop classical baseline | 0.687000 | Phase 3A, for reference |
| English | XLM-R Arabic→English | Zero-shot cross-lingual | 0.680415 | Primary |

Full table: `results/phase3b_kaggle_gpu/master_final_results.csv`.

## Reproducibility reruns (Arabic only) — preserved separately, not substituted

| Model | Primary | Rerun | Note |
|---|---|---|---|
| MARBERT Standalone | 0.785025 | 0.765263 | Original run's row-level predictions lost; paired significance tests use the rerun |
| XLM-R Standalone | 0.740295 | 0.740126 | Row-level predictions available for both; rerun used for consistency with MARBERT's significance tests |

**Both the primary and rerun figures are retained in every table** (`configs/models.yaml` `phase3b_transformers`, `master_final_results.csv`) — the rerun is a documented limitation (lost original predictions), not a replacement.

## Statistical testing (10,000 paired bootstrap samples, seed=42, Holm-Bonferroni correction)

**Arabic** (full table: `results/phase3b_kaggle_gpu/arabic_paired_bootstrap_holm_results.csv`):
- XLM-R-standalone-rerun vs. MARBERT-rerun: **not significant** (adjusted p=0.355)
- XLM-R-standalone-rerun vs. XLM-R-Multilingual: **not significant** (adjusted p=0.101)
- XLM-R-standalone-rerun > English→Arabic zero-shot: **significant** (adjusted p=0.033)
- MARBERT-rerun vs. XLM-R-Multilingual: **not significant** (adjusted p=0.906)
- MARBERT-rerun > English→Arabic zero-shot: **significant** (adjusted p=0.006)
- XLM-R-Multilingual > English→Arabic zero-shot: **significant** (adjusted p<0.001)

**English** (full table: `results/phase3b_kaggle_gpu/english_paired_bootstrap_holm_results.csv`):
- XLM-R-standalone vs. XLM-R-Multilingual: **not significant** (adjusted p=0.508)
- XLM-R-standalone vs. Arabic→English zero-shot: **not significant** (adjusted p=0.100)
- XLM-R-Multilingual > Arabic→English zero-shot: **significant** (adjusted p=0.007)

**Honest pattern:** the only comparisons that survive Holm-Bonferroni correction are each strong in-domain/multilingual model beating its own *zero-shot cross-lingual transfer* counterpart. None of the comparisons among the strong standalone/multilingual models themselves (MARBERT vs. XLM-R, standalone vs. multilingual) are statistically significant at these sample sizes. **Do not report "MARBERT beats XLM-R" or "multilingual beats standalone" as a supported finding — only "in-language/multilingual training beats zero-shot cross-lingual transfer" is statistically supported here.**

## Deployment model (separate from the research results above)

`backend/model/` — a full fine-tuning run on combined Arabic+English data, optimized for serving, with validation macro-F1=0.7999539 (aggregate across both languages, not a per-language test figure — not directly comparable to the 0.767865/0.739722 research numbers above). Integrated into a FastAPI backend (`backend/`) with `/health` and `/predict` endpoints; see the main `README.md` for usage. Ad-hoc manual testing found the deployment model notably more confident and accurate on English inputs than on Arabic inputs in casual spot checks — consistent with this project's documented Arabic/Neutral-class difficulty findings, logged as a reliability caveat in `known_limitations.md` #24, not resolved here (no retraining was performed, per the integration instructions).

## What this report does not do

Per the integration instructions, this is documentation of received Phase 3B results, not a rewritten final manuscript, abstract, or conclusion. The eventual paper's discussion section will need to address Phase 3A vs. 3B honestly, including the open question of which specific factor (fine-tuning method, class weighting, sequence length) drove the observed improvement — none were isolated as a controlled ablation in either phase.

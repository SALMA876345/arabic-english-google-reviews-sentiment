# Reproducibility Manifest

Recovered strictly from preserved artifacts already in this repository (pinned requirement files, saved model config metadata, training/eval configs, and this project's own documentation). Nothing below is guessed. Items that could not be recovered from any preserved artifact are marked **NOT RECOVERABLE FROM PRESERVED ARTIFACTS**, with the specific gap named. Machine-readable version: `REPRODUCIBILITY_MANIFEST.json`.

## Software versions

| Item | Phase 3A (laptop, LoRA) | Phase 3B (Kaggle GPU, full fine-tuning) | Source |
|---|---|---|---|
| Python | **NOT RECOVERABLE FROM PRESERVED ARTIFACTS** -- no `.python-version`, `runtime.txt`, or logged interpreter version found for either track | same | n/a |
| PyTorch | `2.12.0` (CPU build; "no CUDA available in the Phase 3 environment") | **NOT RECOVERABLE FROM PRESERVED ARTIFACTS** -- no Kaggle-side pin found. The local *serving* backend (`backend/requirements.txt`) separately pins `torch==2.12.0`, but this is the inference-serving environment, not the Kaggle training environment, and must not be conflated with it. | `requirements.txt` (Phase 3A); `backend/requirements.txt` (serving only) |
| Transformers (HF) | `4.57.6` | **Partially recoverable, with an important caveat:** `backend/model/config.json` (the deployment checkpoint, trained on Kaggle per `deployment_info.json`'s `best_checkpoint: "/kaggle/working/..."`) records `"transformers_version": "5.16.1"` at save time. This is strong indirect evidence for the Kaggle platform's library version *around the time the deployment pass ran*, but it is **not confirmed to be the identical notebook session** as the E1/E2/E4/E5 Phase 3B research training runs (the deployment model is documented as "a separate GPU training pass," `docs/decisions.md` D17). Treat as a plausible but unconfirmed value for the research runs specifically. | `requirements.txt` (3A); `backend/model/config.json` (deployment checkpoint save-time stamp) |
| accelerate | `1.15.0` | NOT RECOVERABLE | `requirements.txt` |
| peft (LoRA) | `0.21.2` | n/a (Phase 3B does not use LoRA) | `requirements.txt` |
| scikit-learn | `1.7.2` (confirmed live-importable in the current audit environment, matching the pin) | same pin used for all post-hoc metric computation, including Human-Gold re-evaluation | `requirements.txt` |
| NumPy | `2.4.4` | same (post-hoc computation only; Kaggle-side training NumPy version not recovered) | `requirements.txt` |
| Pandas | `2.2.3` | same (post-hoc only) | `requirements.txt` |
| scipy | `1.17.1` | same (post-hoc only) | `requirements.txt` |
| krippendorff | `0.9.0` | n/a | `requirements.txt` |
| statsmodels | `0.15.0` | n/a | `requirements.txt` |
| CUDA version / driver | n/a (CPU-only) | **NOT RECOVERABLE FROM PRESERVED ARTIFACTS** -- only the GPU model is recorded, not the CUDA/driver/cuDNN version | `configs/training.yaml` names hardware only |

## Hardware

| Track | Recorded hardware | Source |
|---|---|---|
| Phase 3A | "8.3GB RAM, CPU-only" laptop; specific CPU model **NOT RECOVERABLE FROM PRESERVED ARTIFACTS** | `docs/decisions.md` D14 |
| Phase 3B | "2x Tesla T4 GPUs (Kaggle)" | `configs/training.yaml` `phase3b_gpu.hardware` |

## Random seeds (fully recovered -- a genuine strength)

| Use | Seed(s) | Source |
|---|---|---|
| Model training (Phase 3A and 3B) | `42` (training seed, data seed) | `configs/training.yaml`, `backend/model/deployment_info.json` (`training_seed: 42`) |
| Phase 3A bootstrap significance testing | `42`, `n_iterations=2000` | `scripts/evaluate.py`, `src/evaluation/metrics.py` |
| Phase 3B original bootstrap significance testing | `42`, `n_iterations=10000` (per `README_PHASE3B.txt`) | **Implementation script itself is NOT present in this repository -- only its output CSVs (`arabic_paired_bootstrap_holm_results.csv`, `english_paired_bootstrap_holm_results.csv`) are preserved. This is a genuine reproducibility gap: the exact code that produced these numbers cannot be re-run from this repository.** |
| 3-annotator presentation order | `1001` / `2002` / `3003` (distinct per annotator) | `paper/annotation/full/build_blinded_sheets.py` |
| Adjudication presentation order | `9009` | `paper/annotation/full/adjudication/build_blinded_adjudication.py` |
| Human-Gold re-evaluation: bootstrap CI | `42`, `n_iterations=10000` | `results/human_gold_evaluation/04_statistical_tests.py` |
| Human-Gold re-evaluation: permutation/randomization test | `42`, `n_iterations=10000` | `results/human_gold_evaluation/04_statistical_tests.py` |

## Model identifiers

| Model | HF identifier | Source |
|---|---|---|
| MARBERT | `UBC-NLP/MARBERT` | `configs/models.yaml` |
| XLM-R | `FacebookAI/xlm-roberta-base` | `configs/models.yaml` |
| Deployment checkpoint | `FacebookAI/xlm-roberta-base` base, full fine-tuning, `max_length=128` | `backend/model/deployment_info.json` |

## Dataset versions / identifiers / hashes

Full table: `DATASET_PROVENANCE.md`. Summary: Zenodo 17011574 (CC-BY-4.0), Zenodo 22061934 (CC-BY-4.0, confirmed by live Zenodo record inspection, 2026 -- supersedes this document's earlier "not independently reconfirmed" status; see `paper/notes/LITERATURE_VERIFICATION.md`), UCSD/McAuley Google Local (no DOI found, 2021-collection-cutoff, no confirmed license -- see `DATA_LICENSING_AND_RELEASE.md`).

## Split identifiers / hashes

- `data/splits/frozen_v1/manifest.json` + per-pool `*_{train,val,test}_ids.json` files (Arabic tourism, English matched, Jordan auxiliary).
- MD5 byte-for-byte cross-check between `results/phase3b_kaggle_gpu/input_data_bundle_sent_to_kaggle/` and `data/processed/frozen_v1/` + `data/splits/frozen_v1/`, confirming Phase 3B trained on the identical frozen data (`docs/decisions.md` D17). This check was logged at integration time; not independently re-run during this audit pass (no destructive/recompute action was in scope).

## Human-Gold hash

- `paper/annotation/full/human_gold_757.csv` SHA-256: `7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd` -- verified at construction and re-verified at the start of every downstream script in `results/human_gold_evaluation/`.

## Training configuration files

- `configs/training.yaml` (Phase 3A `transformer_common`, Phase 3B `phase3b_gpu` sections)
- `configs/models.yaml` (model identifiers, LoRA config, `phase3b_transformers` results block)
- `configs/experiments.yaml` (experiment registry: E1-E8, E_jordan_binary_aux, statuses)

## Evaluation / statistical scripts

- `scripts/evaluate.py`, `src/evaluation/metrics.py` (Phase 3A metrics + original significance testing)
- `results/human_gold_evaluation/01_build_comparison_dataset.py` through `07_patch_rerun_labeling.py` (Human-Gold phase, this and the prior turn)
- **Missing:** the Phase 3B Kaggle-side script that produced `arabic_paired_bootstrap_holm_results.csv` / `english_paired_bootstrap_holm_results.csv` (see seeds table above) -- flagged as a genuine gap, not silently omitted.

## Summary of items that could NOT be recovered

1. Python interpreter version (either track).
2. PyTorch version actually used on Kaggle for Phase 3B training (only the local/serving pin is known).
3. CUDA/driver/cuDNN version on Kaggle.
4. Specific CPU model for the Phase 3A laptop.
5. The Phase 3B Kaggle-side significance-testing implementation script itself (outputs are preserved; code is not).
6. accelerate/peft/numpy/pandas/sklearn/scipy versions as actually used inside the Kaggle notebook (the pinned `requirements.txt` versions are confirmed only for the local Phase 3A environment and this project's own post-hoc Human-Gold computation, not for Kaggle-side training).

None of these were guessed or inferred beyond the explicitly-flagged partial recovery for Transformers version (item in the table above, sourced from the deployment checkpoint's own saved metadata, with its limitation stated).

# Data Licensing and Release Plan

**Status:** no license is invented or inferred here. Every statement below is either (a) a local-provenance fact already on file in this repository, or (b) a live verification performed during this phase (dated below), with the exact source quoted or summarized faithfully. Where a license cannot be confirmed, this document says so explicitly and recommends a conservative release posture instead of guessing.

## 1. Exact source/version of the English Google Local Reviews data used

**Local provenance (already on file, `docs/research_raw/english_datasets_raw.md`, `docs/dataset_audit.md`):** UCSD/McAuley Google Local Review Dataset, data collected through September 2021, US-only coverage. The specific subset actually used by this project is a domain-filtered, length-stratified, Wyoming + Vermont sample (`docs/decisions.md` D9, D13), not the full dump.

**Official source page:** https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/
**Mirrors referenced in local provenance:** https://jiachengli1995.github.io/google/index.html ; https://cseweb.ucsd.edu/~jmcauley/datasets.html

## 2. Live verification performed this phase (2026-10-27)

Both the primary page and the general datasets index page were fetched directly and inspected for license/terms-of-use text.

**Primary page (`.../googlelocal/`) -- verified content:**
- States the data was collected by Tianyang Zhang and Jiacheng Li (UCSD) and covers Google Maps review text, ratings, images, and business metadata, US-only, through September 2021.
- States an explicit **citation requirement**: two papers must be cited if the data is used ("UCTopic: Unsupervised Contrastive Learning for Phrase Representations and Topic Mining," ACL 2022; "Personalized Showcases: Generating Multi-Modal Explanations for Recommendations," SIGIR 2023).
- **Contains no license text, no terms-of-use document, and no explicit statement on commercial use, redistribution, modification rights, or academic-only restriction.** Only a contact email (j9li@eng.ucsd.edu) is given for inquiries.

**General datasets index page (`cseweb.ucsd.edu/~jmcauley/datasets.html`) -- verified content:**
- No blanket license or terms-of-use statement covering the listed datasets.
- The only universal instruction given is to cite the appropriate reference paper.

**Conclusion of live verification: consistent with, and confirms, the project's own Phase 1 finding (`known_limitations.md` #2, `decisions.md` D2) -- no explicit license exists for this dataset as sourced. This is not a documentation gap on this project's side; it is an actual absence of a license on the data provider's side.**

**One adjacent, non-applicable finding surfaced during this verification pass and recorded for completeness, not for use:** a web search located a *derivative* dataset ("Amazon Product and Google Locations Reviews," UCI ML Repository, donated 2026) released under CC BY 4.0. This is a different, preprocessed, third-party-derived dataset, not the one used in this project, and its license does not transfer to the original UCSD/McAuley source or to this project's derivative. It is noted here only so a future reader does not mistake it for a license on the actual source used. Per `docs/research_raw/english_datasets_raw.md`, it is also unconfirmed whether that derivative even retains raw review text -- it was never adopted by this project.

## 3. Escalation status

**Not yet performed.** `docs/decisions.md` D2 recommended contacting the McAuley Lab (j9li@eng.ucsd.edu or j9li@eng.ucsd.edu-equivalent contact) before any public release involving this data; this contact has still not been made as of this phase. This is logged as an open action item, not resolved by this document -- see the Release Plan below for how the project proceeds in the meantime.

## 4. Separated release categories

| Activity | Status | Basis |
|---|---|---|
| **Research use** (training/evaluating models internally, as done throughout this project) | **Acceptable to continue.** | Consistent with the McAuley Lab's own stated practice of making the data available for download with only a citation requirement; no restriction on research use was found. |
| **Redistribution of raw English review text** (publishing the review strings themselves, in a paper appendix, public repo, or released dataset file) | **NOT AUTHORIZED. Do not do this.** | No license grants redistribution rights; absence of a license is not permission. |
| **Redistribution of derived IDs/splits** (publishing which `review_id`s fall in train/val/test, or the English-side portion of `data/splits/frozen_v1/`) | **NOT AUTHORIZED for public release without further clarification.** | Lower risk than raw text, but still describes the structure of an unlicensed-for-redistribution source dataset closely enough that a holder of the original data could reconstruct the exact train/test partition; treated conservatively pending escalation. |
| **Redistribution of human annotations/Human-Gold labels keyed to English review_ids** | **NOT AUTHORIZED for public release without further clarification.** | The labels themselves are this project's own original work, but publishing them keyed to review_ids that resolve against McAuley's text would let any third party holding a copy of the source dataset trivially rejoin label+text, which has the same practical effect as redistributing annotated raw text. |
| **Redistribution of code** (preprocessing, training, evaluation, statistical scripts) | **Acceptable.** | No dependency on redistributing the dataset itself; code does not contain review text. |
| **Redistribution of model artifacts/checkpoints** trained on this data | **Treated as a derivative work; not authorized for public release pending escalation**, per the fallback already specified in `docs/decisions.md` D2. | A trained model is a derivative of the training data; the same license gap applies. |
| **Arabic-side data (Zenodo 17011574, CC-BY-4.0 confirmed via Zenodo API; Zenodo 22061934, CC-BY-4.0 confirmed via live Zenodo record inspection, 2026 — see `paper/notes/LITERATURE_VERIFICATION.md`)** | **No equivalent concern.** Confirmed open license; derivatives, splits, and (where otherwise permitted) raw text may be released under CC-BY-4.0 terms (attribution required). | `docs/decisions.md` D1; `paper/notes/LITERATURE_VERIFICATION.md`. |

## 5. Recommended conservative release plan

1. **Release freely:** all code (preprocessing/training/evaluation/statistical scripts), all configuration files, and the Arabic-side data derivatives (CC-BY-4.0-compatible, with attribution).
2. **Do not release:** English raw review text, English-side review_ids/splits, or Human-Gold/annotation labels keyed to English review_ids -- until the McAuley Lab is actually contacted and either (a) grants explicit redistribution permission, or (b) a documented, dated contact attempt with no response is on file, at which point the project should default to continued non-release of the English row-level artifacts rather than assuming permission from silence.
3. **If the paper must report English-side results before escalation resolves:** report only aggregate statistics, metrics, and model performance numbers for the English side (as the current manuscript framing already plans to do) -- never a row-level artifact (text, IDs, or labels).
4. **Model checkpoints:** keep the Phase 3A/3B research checkpoints and the deployment checkpoint (`backend/model/`) as internal/institutional artifacts only, not publicly released, until the licensing question resolves one way or the other.
5. **Action item to close before submission:** send the escalation email to the contact given on the official page (j9li@eng.ucsd.edu), and record the date sent and any response (or lack thereof) in `docs/decisions.md` as a new dated entry.

## 6. Source identifiers on file

| Dataset | Identifier |
|---|---|
| Saudi Arabic tourism (primary) | Zenodo record 17011574 (CC-BY-4.0, confirmed via Zenodo API per `docs/decisions.md` D1) |
| Jordan Arabic restaurant (auxiliary) | Zenodo record 22061934 |
| English Google Local Reviews | https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/ ; no DOI found on the official page; 2021-collection-cutoff release; mirrors: https://jiachengli1995.github.io/google/index.html, https://cseweb.ucsd.edu/~jmcauley/datasets.html |

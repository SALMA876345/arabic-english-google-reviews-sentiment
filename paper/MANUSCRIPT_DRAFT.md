# Manuscript Draft (Stage 1 + Stage 2 + Stage 3 + Stage 4 + Stage 5 + Stage 6 — Abstract through Conclusion)

**Status:** working draft. Abstract and Sections 1–12 are drafted (Stage 1: §3–6; Stage 2: §7 Results; Stage 3: §8–10; Stage 4: §1–2; Stage 5: §11–12; Stage 6: Abstract/Keywords, this pass), per `paper/MANUSCRIPT_BLUEPRINT.md`. Passed the Final Manuscript-Wide Scientific Consistency Audit (Grade A, `paper/notes/FINAL_MANUSCRIPT_CONSISTENCY_AUDIT.md`); scientific content is frozen. Every external citation below is verified in `paper/notes/LITERATURE_VERIFICATION.md`; none is used from citation-memory alone.

## Abstract

Evaluation of sentiment classifiers depends on the reliability of the labels used to measure them, yet many review-based sentiment datasets derive labels directly or indirectly from star ratings or a single annotation pass whose reliability is not independently measured. This paper examines how much this evaluation-reference construction affects the findings of a sentiment-classification study, in one bilingual setting. Using a frozen, matched test slice of 757 Arabic-English Google-Maps-style reviews (369 Arabic, 388 English), we constructed a human-adjudicated reference set: three independent bilingual annotators produced 2,271 primary annotations, and a blinded fourth adjudicator resolved all 179 reviews without three-way agreement, with no access to the original labels, ratings, or prior annotator decisions. This reference set is not treated as infallible. The original labels agreed with it on 82.6% of reviews (Cohen's kappa = 0.662); disagreement concentrated in the Neutral class, with 82.9% of originally Neutral-labeled reviews revised to Positive or Negative. Re-evaluating 16 previously trained model realizations against the reference set lowered Macro-F1 for 13 of them and reordered model rankings, substantially for the Arabic condition and modestly for English, without evidence that either language is inherently harder to classify. Of four pairwise comparisons significant under the original labels, three lost significance under the reference set, one survived, and one previously non-significant comparison became significant. These results indicate that evaluation-reference quality can materially affect performance estimates, model rankings, and statistical conclusions in sentiment-classification research, and should be treated as part of experimental design rather than a fixed assumption.

**Keywords:** sentiment analysis; evaluation-label reliability; annotation disagreement; human adjudication; multilingual NLP; Arabic NLP; cross-lingual evaluation; model evaluation

<!-- EVIDENCE TRACE: paper/notes/FINAL_MANUSCRIPT_CONSISTENCY_AUDIT.md §1-§2 (every number above independently re-verified against results/human_gold_evaluation/*, paper/annotation/full/agreement_outputs/*); paper/notes/ABSTRACT_ALTERNATIVES.md -->

---

## 1. Introduction

### Motivation

Sentiment-classification systems are typically evaluated against a fixed set of labels treated, at least implicitly, as a reliable reference against which model predictions are scored. In many practical review-mining settings, however, the labels used for this purpose are not the product of dedicated sentiment annotation: they are frequently derived from a numeric star rating, or from a single human pass whose own reliability is not independently measured. Prior work has shown that this kind of label does not always align with the sentiment expressed in the accompanying text, and more broadly that annotator disagreement in NLP tasks can reflect genuine, task-inherent variation rather than only noise to be averaged away (Pavlick & Kwiatkowski, 2019; Plank, 2022). Separately, work auditing test-set labels in widely used machine-learning benchmarks has found that label errors are not rare, and that correcting them can change which model a benchmark favors (Northcutt et al., 2021). Taken together, this literature motivates a direct question for sentiment classification specifically, rather than an assumption that any particular evaluation label is universally problematic: when an independently constructed, multi-annotator reference label is available, how much does it actually change what a sentiment-classification study concludes?

### Gap

Work comparing sentiment-classification architectures — classical, monolingual transformer, multilingual, and cross-lingual zero-shot — typically treats the evaluation label as fixed and reports performance differences, significance tests, and rankings conditioned on that label. Whether, and how much, those rankings and significance conclusions are *themselves* sensitive to how the evaluation reference was constructed is comparatively rarely measured directly within the same study, as opposed to being raised as a general caveat. This paper treats that sensitivity as the primary research question rather than a secondary caveat: **are model rankings and statistical model comparisons, in a concrete bilingual sentiment-classification setting, sensitive to the construction of the evaluation reference label, and if so, how much?** We do not assume in advance that the answer is "yes" in a way that generalizes beyond the setting studied here; the question is treated as empirical, to be answered from the specific evidence this study produces, not asserted as a predetermined universal conclusion.

### Study setting

We study three-class (Positive/Neutral/Negative) sentiment classification of Arabic and English Google-Maps-style location reviews, using a matched 757-review test slice (369 Arabic, 388 English) held out from two larger, independently sourced training pools. Four model families are evaluated: classical TF-IDF baselines, a language-specific transformer per language (MARBERT for Arabic, standalone XLM-R for each language), a multilingual XLM-R model trained jointly on both languages, and bidirectional zero-shot cross-lingual transfer. Two independent training configurations are used throughout and never merged: a resource-constrained laptop configuration using LoRA fine-tuning, and a GPU configuration using full fine-tuning. The original evaluation labels for this test slice are, by construction, not uniform in provenance: rating-derived for English, single-pass human-annotated for Arabic (Section 3). To examine how reliable these original labels are and what follows from that reliability, we conducted a dedicated human-validation study of the full 757-review slice: three independent bilingual annotators labeled every review, and a fourth, independently blinded adjudicator resolved every case without three-way agreement (Section 4). The result is a human-adjudicated reference set against which every existing model's saved predictions are re-evaluated, without retraining any model (Section 6–7).

### Key findings

Four headline findings, each reported with its necessary qualification, anchor this paper. First, the original evaluation labels and the human-adjudicated reference set agree on 82.6% of the 757 reviews (Cohen's κ = 0.662); the remaining disagreement is concentrated overwhelmingly in reviews originally labeled Neutral, 82.9% of which were revised to a different label under independent adjudication. Second, re-scoring 16 previously-trained model realizations against the reference set lowers Macro-F1 for 13 of them. Third, model rankings computed from the two label sources differ substantially for the Arabic evaluation condition and only modestly for the English condition. Fourth, of four model comparisons found statistically significant under the original labels, three no longer reach significance under the reference set, one survives, and one previously non-significant comparison becomes significant.

Each of these findings carries a standing qualification carried throughout this paper, not appended once and then dropped: the human-adjudicated reference set is not presented as an infallible ground truth (Section 4.4); any difference observed between the Arabic and English conditions is reported descriptively, since the two language sub-corpora differ simultaneously in geography, domain, and label-construction history, and is never read as evidence that one language is inherently harder to classify (Section 3.5, Section 9.4); and every Arabic MARBERT/XLM-R result reported under the human-adjudicated reference set uses a documented reproducibility-rerun realization, labeled as such, because the original primary runs' row-level predictions were lost before this study began (Section 5.3).

### Contributions

This paper makes the following contributions:

1. A 757-review, three-annotator human-validation study of a frozen bilingual sentiment test set, with a pre-registered, blinded fourth-adjudicator resolution procedure for all non-unanimous cases, reported with its own reliability statistics and disclosed limitations rather than treated as a settled reference.
2. A direct, quantified measurement of how much re-evaluating existing, unretrained sentiment models against this human-adjudicated reference set changes per-class performance, model rankings, and statistical-significance conclusions, relative to the originally reported evaluation.
3. A methodological demonstration, within this measurement, of keeping two distinct statistical procedures (a paired bootstrap resampling confidence interval and a genuine paired permutation test) explicitly separate, and of keeping primary and reproducibility-rerun model realizations explicitly distinguished throughout.
4. A secondary empirical contribution on multilingual and cross-lingual transfer: multilingual joint training is not significantly distinguishable from monolingual training in either language studied, under either evaluation reference, and several apparent zero-shot cross-lingual weaknesses found under the original labels do not survive re-evaluation against the reference set.
5. A dataset-measurement finding, independent of the sentiment-modeling results: a common script-mixing heuristic for detecting Arabic-English code-switching is shown, by exhaustive manual audit, to be dominated by a platform-specific display artifact rather than genuine bilingual text in this review domain.

None of these contributions is presented as a definitive, universally generalizing result, a state-of-the-art claim, or proof of any causal mechanism; each is scoped explicitly to the setting, sample, and design described in this paper.

### Research questions

This paper is organized around four research questions:

- **RQ1.** How reliable are the evaluation labels conventionally used for Arabic-English review sentiment classification — rating-derived heuristics for English, single-pass human annotation for Arabic — relative to a human-adjudicated reference set constructed from three independent bilingual annotators and a blinded fourth adjudicator?
- **RQ2.** To what extent does replacing the original evaluation labels with the human-adjudicated reference set change measured model performance (accuracy, Macro-F1, per-class F1) and the relative ranking of previously-trained sentiment models?
- **RQ3.** Does re-evaluating multilingual, language-specific, and cross-lingual zero-shot sentiment models against the human-adjudicated reference set change which pairwise performance differences are statistically significant?
- **RQ4.** How does model performance on the Neutral sentiment class behave under human-adjudicated labels, given Neutral's low support in the reference set and the high rate of label revision observed for originally-Neutral-labeled reviews — and what does this imply about the boundary between evaluation-label instability and genuine model weakness?

As throughout this paper, any Arabic-English comparison encountered while answering these questions is reported descriptively, not as evidence of inherent language difficulty (Section 3.5, Section 9.4).

<!-- EVIDENCE TRACE: paper/notes/FINAL_SCIENTIFIC_FRAMING.md; paper/MANUSCRIPT_BLUEPRINT.md (§3 Final Research Questions); results/human_gold_evaluation/label_agreement_overall_by_language.json; results/human_gold_evaluation/original_vs_human_gold_comparison.csv; results/human_gold_evaluation/statistical_tests_human_gold.csv; paper/notes/LITERATURE_VERIFICATION.md (rows 10, 11, 13: Pavlick & Kwiatkowski 2019, Plank 2022, Northcutt et al. 2021) -->

---

## 2. Related Work

### 2.1 Sentiment labels and annotation reliability

Human annotation of subjective phenomena such as sentiment does not always converge on a single answer even among careful annotators. Pavlick and Kwiatkowski (2019) show, for natural language inference, that disagreement among annotators on a substantial fraction of examples persists under repeated, high-redundancy annotation, and argue this reflects genuine variation in human judgment rather than only annotator error — a finding relevant to any task, including sentiment classification, where a label is meant to summarize a holistic, sometimes genuinely mixed, textual judgment. Plank (2022) extends this observation into a broader methodological argument: "ground truth" in NLP datasets is itself a constructed object, shaped by annotation guidelines, aggregation rules, and the number and selection of annotators, and should be treated as such in both dataset construction and model evaluation rather than as an unproblematic given. This paper's own framing — referring throughout to a "human-adjudicated reference set" rather than to "ground truth," and reporting that reference set's own construction choices and limitations explicitly (Section 4) — follows directly from this line of argument, applied to a setting (bilingual review sentiment) that this literature does not itself study.

A related and more domain-specific concern is the use of a numeric rating as a proxy for textual sentiment. Reviews on online platforms frequently pair a star rating with free text, and the mapping from rating to a sentiment label is a common, low-cost labeling shortcut; it is also a well-documented source of mismatch, since a review's star rating and its textual content do not always agree — for example, in cases of sarcasm, an apologetic low rating, or a rating dominated by one aspect of an otherwise mixed experience. This paper's English evaluation condition uses exactly this kind of rating-derived label as its original reference (Section 3.2), and the human-validation study reported here (Section 4, Section 7) provides a direct, measured account of how much that specific label-construction choice diverges from an independently constructed reference, for this dataset.

Beyond annotation-specific disagreement, label errors in already-released, widely used benchmark test sets have been shown to be common enough to matter: Northcutt et al. (2021) algorithmically and then manually identify label errors across ten standard machine-learning benchmarks (spanning vision, audio, and text) and show that correcting them changes which model is favored by the benchmark, in some cases reversing a reported ranking. This paper's central empirical question (RQ2, RQ3) is a direct extension of that concern into a setting — bilingual sentiment classification with two distinct original label-construction methods — that Northcutt et al. (2021) does not itself examine, and into a statistical-testing framework (Section 6.3) informed by the broader call for more careful significance testing in NLP specifically (Dror et al., 2018).

<!-- EVIDENCE TRACE: paper/notes/LITERATURE_VERIFICATION.md rows 10, 11, 12, 13; Section 3.2, Section 4, Section 7.2 of this manuscript -->

### 2.2 Arabic and multilingual sentiment analysis

Arabic sentiment analysis has moved, over the past several years, toward transformer-based approaches built on Arabic-specific pretraining; MARBERT (Abdul-Mageed et al., 2021) is one such model, pretrained on a large corpus of Arabic social-media text spanning both Modern Standard Arabic and dialectal variation, and is used in this paper as the Arabic-specialized encoder (Section 5.1). A recent survey of the field (Shi & Agrawal, 2025) characterizes contemporary Arabic sentiment analysis as having substantially adopted deep-learning and transformer methods, while identifying continued challenges around dialectal variation, limited annotated resources relative to English, and dataset quality — a characterization consistent with this project's own dataset audit (Section 3), which found only a narrow set of candidate Arabic review datasets at adequate scale and label quality, and none with an independently confirmed, large-scale, document-level sentiment annotation at the scale this study required (Section 3.1).

This paper's Arabic evaluation results are reported and discussed on their own terms, not as one side of an Arabic-versus-English competition. Where this paper's findings touch on both language conditions — most notably the differing degree of ranking instability under human-adjudicated re-evaluation (Section 7.5, Section 9.4) — they are presented as a property of this study's specific, confounded comparison, not as a contribution to, or a claim resolving, the question of whether Arabic sentiment analysis is inherently harder than English sentiment analysis in general.

<!-- EVIDENCE TRACE: paper/notes/LITERATURE_VERIFICATION.md rows 8, 14; docs/dataset_audit.md; docs/known_limitations.md #1 -->

### 2.3 Multilingual and cross-lingual transfer

XLM-R (Conneau et al., 2020) is a transformer encoder pretrained on filtered web text across 100 languages, shown in the original work to substantially outperform earlier multilingual encoders on cross-lingual benchmarks; this paper uses XLM-R as its multilingual and cross-lingual backbone throughout (Section 5.1), both for monolingual fine-tuning on each language separately, for joint multilingual training on both languages combined, and for zero-shot cross-lingual transfer (training on one language's data and evaluating, without further fine-tuning, on the other). Cross-lingual transfer of sentiment classifiers specifically — moving a model trained in one language to another without target-language supervision — has been studied as a way to extend sentiment analysis to languages or domains with less labeled data (Robnik-Šikonja et al., 2020). This paper's zero-shot condition (Section 5.1, Section 7.8) is a direct instance of this transfer setting, applied bidirectionally between Arabic and English; the literature on cross-lingual transfer motivates why this experimental condition is included in the study design, but the transfer mechanism itself is not this paper's object of study — the zero-shot condition functions here primarily as one of several model realizations whose evaluation-reference sensitivity (RQ3) is measured, alongside the monolingual and multilingual conditions.

<!-- EVIDENCE TRACE: paper/notes/LITERATURE_VERIFICATION.md rows 9, 15; Section 5.1 of this manuscript -->

### 2.4 Evaluation reliability and model comparison

A separate body of work addresses how NLP systems should be compared once trained, independent of how their evaluation labels were constructed. Dror et al. (2018) survey the (at the time) inconsistent use of statistical significance testing in ACL and TACL papers and propose a practical protocol for selecting and reporting significance tests for NLP system comparisons; this paper's own statistical protocol (Section 6.3) — paired comparisons restricted to models with valid row-level predictions on identical test rows, a genuine paired permutation test as the primary significance criterion, and Holm-Bonferroni correction within explicitly justified comparison families — is designed in that spirit, and is applied twice in this study: once to the original evaluation labels (reproducing the pre-existing significance results) and once to the human-adjudicated reference set (Section 7.6).

The specific question this paper asks — how much a change in the evaluation-reference label itself, rather than a change in model, training data, or statistical method, affects reported model comparisons — sits at the intersection of the annotation-reliability literature (Section 2.1) and the model-comparison literature just discussed, and is most directly anticipated by Northcutt et al. (2021)'s demonstration that correcting test-set label errors can change which model a benchmark favors. This paper differs from that work in domain (bilingual sentiment classification rather than general-purpose vision/audio/text benchmarks), in the mechanism studied (a full multi-annotator, blind-adjudicated re-annotation of the entire test slice, rather than algorithmic label-error detection followed by targeted correction), and in scope (one bilingual review-sentiment dataset, not a cross-benchmark survey). We are not aware of, and this paper's literature search (Section A, `paper/notes/LITERATURE_VERIFICATION.md`) did not surface, a study that applies this specific combination — independent multi-annotator re-annotation of a fixed bilingual sentiment test set, followed by a direct before/after comparison of performance estimates, model rankings, class-level conclusions, and paired statistical tests — to this domain; we state this as the outcome of the literature search actually conducted for this paper, not as a claim that no related work of this kind exists anywhere, since a literature search, however carefully conducted, cannot establish the latter.

In summary, this paper examines how independently human-adjudicating a fixed bilingual sentiment test set changes performance estimates, model rankings, class-level conclusions, and statistical comparisons for a set of previously-trained, unretrained models — a narrowly scoped question that builds directly on, without claiming to resolve, the broader literatures on annotation reliability, evaluation-label quality, and statistical model comparison surveyed above.

<!-- EVIDENCE TRACE: paper/notes/LITERATURE_VERIFICATION.md rows 10-13; Section 6.3, Section 7.6 of this manuscript -->

---

## 3. Data and Dataset Audit

This study draws on three independently sourced review corpora — two Arabic and one English — assembled from pre-existing public dataset releases rather than freshly collected for this project. The three corpora differ from one another in geography, platform-adjacent domain, collection era, and, critically, in how their sentiment labels were originally constructed. These differences are treated throughout this paper as standing confounds to be disclosed, not as incidental details to be elided; in particular, no comparison drawn between the Arabic and English corpora in this paper is intended, or should be read, as evidence about the inherent difficulty of one language relative to the other (see Section 9, Discussion).

### 3.1 Arabic datasets

**Primary Arabic pool (Saudi tourism reviews).** The primary Arabic corpus is drawn from Zenodo record 17011574 (Alahmadi, 2025), a collection of Saudi tourism-site reviews. The release is distributed under a CC-BY-4.0 license. Of 3,543 raw reviews, 3,525 were retained after removing 6 reviews with no derivable label and 12 duplicate entries. This dataset's sentiment labels are *human-annotated* at the point of original release, with an inter-annotator agreement figure (κ ≈ 0.87) reported in the dataset's own documentation; this figure was not independently re-verified by the present project and is reported here as the source's own claim, not as an independently confirmed statistic. This pool supplies the primary Arabic experimental condition (train/validation/test, Section 3.4).

**Auxiliary Arabic pool (Jordanian restaurant reviews).** A second Arabic corpus, Zenodo record 22061934 (Sammour, 2026), distributed under a CC-BY-4.0 license, consists of Jordanian-dialect restaurant reviews. Of 8,671 raw reviews, 8,664 were retained after removing 6 duplicates. Direct inspection confirmed this dataset is strictly binary at the label level: it contains zero Neutral-labeled reviews in either of its two label strata. Of the 8,664 usable reviews, 300 carry a label the dataset's own release designates as human-annotated ("gold"), reserved in this project exclusively as the evaluation reference for a separate, binary auxiliary experiment; the remaining 8,364 reviews carry labels assigned by a large language model (label provenance: `llm_weak_label`), used only for training augmentation and never for evaluation. This dataset does not contribute to the primary three-class Arabic experimental condition and is not pooled with it at any point. We note explicitly, to avoid a terminological collision later in this paper, that this corpus's own 300-review "human-gold" subset is unrelated to, and must not be confused with, the 757-review human-adjudicated reference set constructed by this project and described in Section 4.

### 3.2 English dataset

The primary English corpus is the Google Local Review Dataset released by the McAuley Lab at UC San Diego (data collection by Tianyang Zhang and Jiacheng Li, covering the United States through September 2021; official release page: `mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal`). The dataset's own release page specifies no formal license but requires citation of two companion papers if the data is used: "UCTopic: Unsupervised Contrastive Learning for Phrase Representations and Topic Mining" (Li, Shang, & McAuley, 2022) and "Personalized Showcases: Generating Multi-Modal Explanations for Recommendations" (Yan, He, Li, Zhang, & McAuley, 2023). This project worked from a Wyoming- and Vermont-restricted subset of the full release (selected as a practical, English-speaking, moderate-volume sample; the 2021 release has no Middle East/Gulf coverage, so true geographic matching to the Arabic corpora was not possible by construction). Of 1,993,624 raw lines, 1,170,942 remained after requiring non-null review text and a non-null rating, and 1,038,643 remained after deduplication (132,299 duplicate rows removed).

This dataset carries no native sentiment annotation. Sentiment labels for the English primary pool are therefore *rating-derived*: 1–2 star ratings are mapped to Negative, 3-star ratings to Neutral, and 4–5 star ratings to Positive. This label-construction method is explicitly distinguished throughout this paper from human annotation; it is a well-documented source of label noise (e.g., sarcastic high ratings, apologetic low ratings, and ratings that diverge from review-text sentiment), a phenomenon this paper's own human-validation findings (Section 4, Section 7) directly speak to for this specific corpus.

**Licensing status.** No license, terms-of-use document, or redistribution statement was found on the dataset's official release page or on the general datasets index page maintained by the same research group; this absence was independently re-verified by live inspection of both pages during this project (2026). Consequently, raw review text, review identifiers, and any annotation keyed to those identifiers from this dataset are not released as part of this project's data-availability plan (Section 11, to be finalized in a later drafting stage); aggregate statistics and model-performance figures computed on this data are reported, consistent with how the dataset's own stated terms (citation only, no explicit restriction on reporting results) are understood.

### 3.3 Dataset cleaning, deduplication, and the code-switching audit

All three corpora underwent deduplication and a non-null-field filter before any further processing (counts above). Beyond this general cleaning pass, a dedicated audit was conducted to identify genuinely code-switched (mixed Arabic-English) material across the combined usable corpus (12,189 usable Arabic documents + 1,038,643 usable English documents = 1,050,832 total).

A character-script-fraction heuristic flagged 109 candidate documents as containing a mixture of Arabic and Latin script. Because this candidate set was small enough to inspect exhaustively, all 109 (not a sample) were manually classified by two independent reviewers working blind to each other's labels, with a third-pass arbitration of the 6 cases on which the two reviewers disagreed. Inter-rater reliability on this manual audit itself was high (Cohen's κ = 0.809 for the binary genuine-code-switch-or-not judgment; 94.5% exact agreement across a finer 7-category scheme).

The audit's central finding is that the heuristic's candidate set was overwhelmingly **not** genuine code-switching. Of the 109 candidates, 84 (77.1%) were a structural artifact of the review platform's own user interface — a passage displayed alongside its own machine translation (the platform's "Translated by Google / Original" presentation), not a reviewer mixing languages within a single utterance. A further 13 (11.9%) were script-misidentification (most often Persian/Farsi or Hebrew text misread as Arabic by the character-fraction heuristic) or non-semantic noise; 2 (1.8%) were an isolated named entity or brand name in the other script within an otherwise monolingual review; 1 (0.9%) was an incidental interjection with no bilingual sentence structure. Only **9 of the 109 candidates (8.3%), and 9 of the full 1,050,832-document corpus (≈0.00086%), were confirmed as genuine Arabic-English code-switching** by the operational criterion applied (language mixing within the same sentence or connected span of thought, introducing new content rather than repeating it).

This sample size is explicitly insufficient to support any quantitative, model-performance-oriented evaluation: nine examples cannot populate a train/test split, support a confidence interval, or support a significance test. The 9 examples are retained in this project only as a qualitative illustrative set for error-analysis discussion (Section 8, not yet drafted); no accuracy, F1, or other performance statistic is computed on them anywhere in this paper. We report the audit's own finding — that a common, inexpensive code-switch-detection heuristic can be dominated by a platform display artifact rather than genuine bilingual production, in this review-platform domain — as a dataset-measurement-methodology result in its own right, independent of and not contingent on any sentiment-modeling claim.

### 3.4 Label provenance taxonomy

Three distinct label-provenance categories are used throughout this paper and are never conflated with one another:

- **Human-annotated**: assigned by a human rater at or near the point of original data collection (the Arabic tourism pool's original label; the Jordanian pool's 300-review gold evaluation subset).
- **Rating-derived**: algorithmically mapped from a numeric star rating, with no human sentiment judgment of the review text itself (the English primary pool's original label).
- **LLM-weak-labeled**: assigned by a large language model reading the review text, with no individual human confirmation (the Jordanian pool's 8,364-review training-augmentation subset).

A fourth category, the **human-adjudicated reference set** constructed specifically by this project from three independent annotators and a blinded fourth adjudicator, is described separately in Section 4 and is not a synonym for any of the three categories above; it supersedes the original evaluation labels only for the 757-review matched test slice described next, and is never described as an infallible ground truth.

### 3.5 Frozen train/validation/test design and the matched Arabic-English comparison slice

Group-aware splitting was applied independently to each primary pool — by tourist-site/place identifier for the Arabic pool, by business identifier for the English pool — so that no single place or business appears in more than one split. The resulting splits were frozen (immutable manifests, `data/splits/frozen_v1/`) before any model training began. The Arabic primary pool yields 2,786 training, 370 validation, and 369 test reviews; the English primary pool yields 2,785 training, 352 validation, and 388 test reviews.

The English primary pool was constructed as a matched comparison slice relative to the Arabic primary pool on two dimensions only: overall sentiment-class distribution (matched exactly by construction) and review-length distribution (matched approximately; quartile medians align closely, though the English subset retains a longer right tail). A domain proxy filter (reviews categorized under tourism, parks, museums, or historical sites) was applied to the English pool before sampling, to avoid comparing Saudi tourism-site reviews against an unrelated domain such as car dealerships or retail. Two dimensions were explicitly **not** matched and are disclosed as standing confounds: geography (Saudi Arabia vs. two U.S. states, Wyoming and Vermont) and star-rating distribution (the Arabic pool carries no star ratings at all, so no such matching was possible). Consequently, this paper treats the Arabic-English test slice as a matched-protocol comparison on sentiment distribution and approximate length only, not as a fully controlled cross-language experiment; any performance comparison drawn between the two language conditions in this paper is reported descriptively, not as evidence for an inherent language-difficulty effect (Section 9).

The 757-review union of the two primary test splits (369 Arabic, 388 English) is the fixed evaluation slice to which Section 4's human-annotation study, and all model re-evaluation reported in Sections 7–8, apply.

`[TABLE 1: Dataset composition and provenance — populated from the consolidated provenance record (project artifact: paper/notes/DATASET_PROVENANCE.md), covering source, DOI/identifier, raw/usable/retained counts, language, label-provenance category, task role, and license status for each of the three source datasets and the code-switch audit process.]`

<!-- EVIDENCE TRACE: docs/decisions.md (D1, D2, D3, D4, D9, D10, D12, D13); docs/known_limitations.md (#1-#9, #12, #14, #15, #19); docs/codeswitch_audit.md; docs/label_provenance_policy.md; docs/dataset_audit.md; docs/experimental_dataset_protocol.md; data/splits/frozen_v1/manifest.json; results/tables/phase2_corpus_stats.md; paper/notes/DATASET_PROVENANCE.md (updated this stage: Jordan dataset license corrected to confirmed CC-BY-4.0); paper/notes/DATA_LICENSING_AND_RELEASE.md (live verification of the UCSD/McAuley source page, performed 2026-10-27); paper/notes/LITERATURE_VERIFICATION.md (rows 1-4: Zenodo 17011574, Zenodo 22061934, UCTopic, Personalized Showcases) -->

---

## 4. Human Annotation and Adjudication

Because the English primary pool's original evaluation labels are rating-derived rather than human-judged, and the Arabic primary pool's original labels reflect a single-pass annotation process whose own reliability was never independently measured, this project conducted an independent human-validation study of the full 757-review matched test slice (369 Arabic, 388 English) to establish a separately-constructed reference set against which existing model predictions could be re-evaluated. We refer to this reference set throughout as the **human-adjudicated reference set**; where the shorter internal label "Human-Gold" appears elsewhere in this project's code and file names, it denotes the same object and is defined here, once, as a human-adjudicated reference, not as an infallible ground truth.

### 4.1 Annotation design

Three independent bilingual annotators (fluent in both Arabic and English) each annotated all 757 reviews, for a total of 2,271 primary sentiment-annotation decisions. Each annotator worked from a blinded presentation sheet containing only the review text and its language tag, with no access to the review's star rating, the original (rating-derived or single-pass-annotated) label, any model's prediction, or the identity or decisions of the other two annotators. Each annotator was shown the 757 reviews in an independently and deterministically randomized order, generated with a distinct seed per annotator (1001, 2002, and 3003 respectively), so that no two annotators saw the reviews in the same sequence and no annotator's order could be inferred from another's.

For each review, annotators recorded three fields: a three-class sentiment label (Positive / Neutral / Negative, defined by the same decision rule used for the original annotation process: Positive/Negative is assigned when the overall impression is favorable/unfavorable even if a minor contrasting remark is present; Neutral is assigned when there is no clear net lean, whether because the text is purely factual/descriptive or because it is genuinely balanced between positive and negative content with no net direction); a self-reported confidence level (High / Medium / Low); and a binary mixed-sentiment flag intended to capture whether the review contains a genuine mixture of positive and negative content. This third field is treated throughout this paper as *exploratory only* (Section 4.3) and is not used to construct the reference set.

### 4.2 Annotator agreement

Of the 757 reviews, 578 (76.4%) received the identical sentiment label from all three annotators (unanimous agreement); 161 (21.3%) received a 2-of-3 majority label with one dissenting annotator; and 18 (2.4%) produced a three-way split with no majority. At least a 2-of-3 majority was therefore achieved on 739 of 757 reviews (97.6%).

Overall three-rater agreement, computed with Fleiss' κ, was 0.650; Krippendorff's α (nominal level) was 0.650, closely consistent with the Fleiss' κ estimate. By the conventional interpretive bands of Landis and Koch (1977), this level of agreement is characterized as *substantial*, not *near-perfect* or *almost perfect*, and is reported as such throughout this paper. (The Fleiss' κ statistic itself follows Fleiss, 1971.) Pairwise raw agreement between annotators ranged from 81.9% to 86.5%, with corresponding pairwise Cohen's κ ranging from 0.628 to 0.700 across the three annotator pairs.

Agreement was also computed separately for the Arabic and English subsets of the 757-review slice (descriptive only; not an inferential comparison). Any difference observed between the two language subsets' agreement statistics is reported here as a property of this specific annotation round and must not be interpreted as evidence that sentiment is inherently more or less ambiguous in one language than the other — the two subsets differ in source, domain, and original label-construction method (Section 3), any of which could independently account for an observed agreement difference.

The mixed-sentiment flag's three-rater agreement (κ ≈ 0.269) was substantially lower than the sentiment label's agreement, falling well outside the range conventionally considered reliable. This variable is accordingly treated as exploratory throughout this paper: it informed the decision not to default to automatic majority-vote resolution for disagreement cases (Section 4.3), but it is not validated, not used to construct the reference set, and not re-collected at the adjudication stage.

`[TABLE 2: Three-annotator agreement statistics — project artifact: paper/annotation/full/agreement_outputs/overall_agreement_sentiment.json, plus the companion by-language and by-class breakdown files in the same directory.]`

### 4.3 Adjudication of non-unanimous cases

The 179 reviews without unanimous agreement (161 majority cases, 18 three-way cases) were not resolved by defaulting to the 2-of-3 majority label. This design choice was made, and pre-registered before adjudication began, specifically because the mixed-sentiment flag's low reliability (above) indicated that a bare majority vote on a genuinely contested review cannot be assumed to reflect "two correct annotators outvoting one incorrect annotator" — a 2-of-3 split may equally reflect a review that is legitimately difficult to place on a single net-sentiment axis.

Instead, all 179 non-unanimous reviews were independently resolved by a **fourth bilingual human adjudicator**, distinct from the three original annotators. The adjudicator was shown the 179 reviews in a deterministically randomized order generated with its own distinct seed (9009), unrelated to any of the three annotators' seeds. The adjudicator was blinded to all of the following: the three original annotators' individual sentiment decisions; the 2-of-3 majority label (where one existed); which of the three annotators selected which label; the number of annotators supporting each label; the review's original (rating-derived or single-pass human-annotated) label; the review's star rating, where applicable; and any model prediction. The adjudicator was shown only the review text, its language tag, and the same sentiment-decision rule given to the three original annotators (Section 4.1), and recorded a sentiment label, a confidence level (High / Medium / Low), and an optional free-text rationale. The adjudicator was not asked about mixed sentiment, consistent with that variable's exploratory-only status.

The 757-review human-adjudicated reference set was then constructed as follows: for the 578 unanimous reviews, the reference label is the unanimous label; for the 179 non-unanimous reviews, the reference label is the fourth adjudicator's independent decision. The 2-of-3 majority label is never substituted for the adjudicator's decision at any point in this construction, including for the 161 reviews where a majority existed — the adjudicator's independent judgment is used uniformly across all 179 non-unanimous cases.

### 4.4 Limitations of the human-adjudicated reference set

This reference set is not presented, and must not be read, as an infallible ground truth. Two limitations are disclosed explicitly. First, and most consequential, all 179 adjudicated cases — 23.6% of the full 757-review reference set — were resolved by a single adjudicator, with no second adjudicator and no measured adjudicator-vs-adjudicator reliability statistic; any idiosyncratic bias held by that one adjudicator propagates uncontested into nearly a quarter of the reference set. Second, the underlying three-annotator agreement that produced the 578 "unanimous" reference labels was itself only *substantial* (κ = 0.650), not near-perfect; some residual unreliability is inherent even among the reviews that happened to receive unanimous agreement. Both limitations are carried forward into this paper's Discussion and Limitations sections (not yet drafted) and are not resolved by this project at the current stage; a second-adjudicator reliability study on a subsample of the 179 disagreement cases has been identified as a valuable, but not required, future strengthening analysis and was not conducted for this paper.

`[TABLE 3: Adjudication outcome summary — project artifact: paper/annotation/full/adjudication/adjudication_merged.csv and results/human_gold_evaluation/01_build_comparison_dataset.py's outputs, covering case counts, adjudicator-vs-prior-majority agreement rate, and confidence distribution.]`

<!-- EVIDENCE TRACE: paper/annotation/full/README.md; paper/annotation/full/ADJUDICATION_PROTOCOL.md; paper/annotation/full/ADJUDICATOR_INSTRUCTIONS.md; paper/annotation/full/ANNOTATOR_INSTRUCTIONS.md; paper/annotation/full/build_blinded_sheets.py; paper/annotation/full/adjudication/build_blinded_adjudication.py; paper/annotation/full/adjudication/build_adjudicator_interface.py; paper/annotation/full/agreement_outputs/overall_agreement_sentiment.json; paper/annotation/full/adjudication/adjudication_merged.csv; paper/annotation/full/build_human_gold.py; paper/annotation/full/human_gold_757.csv (SHA-256 7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd); docs/known_limitations.md (#25); paper/notes/FINAL_SCIENTIFIC_FRAMING.md; paper/notes/LITERATURE_VERIFICATION.md (rows 5, 6: Landis & Koch 1977, Fleiss 1971) -->

---

## 5. Experimental Methodology

This section describes the models and training conditions whose predictions are evaluated in Sections 6–8. It is organized by experimental family, not by chronological project history.

### 5.1 Models

Four modeling families were used throughout: two classical baselines (TF-IDF features with logistic regression, and TF-IDF features with a support vector machine, each with class-weighting selected on validation data between an unweighted and a "balanced" setting); and two transformer architectures, MARBERT (Abdul-Mageed et al., 2021; checkpoint `UBC-NLP/MARBERT`), an Arabic-specialized pretrained encoder, and XLM-RoBERTa-base (Conneau et al., 2020; checkpoint `FacebookAI/xlm-roberta-base`), a multilingual pretrained encoder. MARBERT was applied to the Arabic condition only; XLM-R was applied to both the Arabic and English conditions individually, to a combined multilingual training condition, and to bidirectional zero-shot cross-lingual transfer (a model trained on one language's training split and evaluated, without any fine-tuning on the target language, on the other language's test split).

### 5.2 Two independently tracked training configurations

Model training was carried out under two separate configurations, referred to throughout this paper as Phase 3A and Phase 3B. These two configurations are reported side by side, never merged, and are never treated as directly interchangeable realizations of "the same model."

**Phase 3A** used Low-Rank Adaptation (LoRA) fine-tuning (Hu et al., 2022) rather than full fine-tuning, on CPU-only hardware with approximately 8.3 GB of total RAM. This configuration was adopted after a direct attempt at full fine-tuning exhausted available memory during the optimizer step; LoRA adapts approximately 0.3% of model parameters via low-rank matrices while leaving the base architecture unchanged, and was selected over alternatives (further batch-size reduction, a smaller unapproved architecture, or frozen-embedding feature extraction) as the smallest methodological deviation from standard fine-tuning available under the hardware constraint. Phase 3A used an unweighted cross-entropy loss, a maximum input sequence length of 64 tokens, a batch size of 4, 3 training epochs, the AdamW optimizer with learning rate 2×10⁻⁵, weight decay 0.01, a linear schedule with 10% warmup, and early stopping on validation Macro-F1 (patience 1), with training/data seed 42 throughout. The combined multilingual training condition under this configuration did not complete: three consecutive attempts at decreasing batch size each failed with an out-of-memory error, and this experiment is recorded as not run under Phase 3A, rather than approximated or omitted silently.

**Phase 3B** used full fine-tuning (100% of parameters trainable) on two Tesla T4 GPUs accessed via a cloud notebook platform (Kaggle), with a weighted cross-entropy loss (class weights, in contrast to Phase 3A's unweighted loss), a maximum input sequence length of 128 tokens, a batch size of 8 per GPU for training and 16 per GPU for evaluation, 3 training epochs, learning rate 2×10⁻⁵, weight decay 0.01, fp16 precision, and training/data seed 42. Under this configuration, the combined multilingual training condition completed successfully, using the same epoch count and sequence length as every other Phase 3B condition, so that the multilingual-vs-monolingual comparison within Phase 3B is not confounded by an unequal training budget in the way the (non-completed) Phase 3A attempt would have been.

Phase 3A and Phase 3B differ simultaneously in fine-tuning method (LoRA vs. full), loss class-weighting (unweighted vs. weighted), maximum sequence length (64 vs. 128 tokens), and compute environment (CPU-only laptop vs. multi-GPU cloud notebook). No single one of these factors was isolated by an ablation in this project. Accordingly, any performance difference observed between a Phase 3A and a Phase 3B realization of nominally the same model in this paper is reported as a difference between two bundled training configurations, and is never attributed to the GPU hardware specifically, nor to any other single factor in isolation.

### 5.3 Lost primary predictions and rerun realizations

Two Phase 3B Arabic models — standalone MARBERT and standalone XLM-R, each trained and evaluated once as the primary realization of that model under the Phase 3B configuration — subsequently had their row-level test-set predictions lost before this project's later re-evaluation phases began. The headline Macro-F1 figures from those primary runs (MARBERT 0.785025; XLM-R 0.740295) remain the primary reported results for those two conditions and are not altered anywhere in this paper. However, because the row-level predictions needed for paired statistical comparison and for re-evaluation against the human-adjudicated reference set (Section 6–8) no longer exist for these two primary runs, a documented reproducibility rerun of each model (MARBERT rerun Macro-F1 = 0.765263; XLM-R rerun Macro-F1 = 0.740126), trained under the identical Phase 3B configuration, is used in their place wherever row-level predictions are required. Every table, figure, and statistical result in this paper that uses either rerun is labeled explicitly as a rerun realization, distinct from the primary realization; the rerun is at no point presented, implicitly or explicitly, as though it were the original primary run's own predictions.

`[TABLE 4: Experimental conditions and configurations — project artifact: configs/training.yaml, configs/models.yaml, configs/experiments.yaml, covering model, language, training phase, fine-tuning method, key hyperparameters, and completion status for every experimental condition (E1, E2, E4, E5, and the classical baselines).]`

<!-- EVIDENCE TRACE: configs/training.yaml (transformer_common, phase3b_gpu sections); configs/models.yaml; configs/experiments.yaml; docs/decisions.md (D6, D14, D15, D16, D17); docs/known_limitations.md (#16-#23); results/phase3b_kaggle_gpu/README_PHASE3B.txt; results/phase3b_kaggle_gpu/master_final_results.csv; paper/notes/RERUN_LABELING_AUDIT.md; paper/notes/LITERATURE_VERIFICATION.md (rows 7, 8, 9: LoRA, MARBERT, XLM-R) -->

---

## 6. Evaluation Protocol and Statistical Analysis

### 6.1 Two evaluation references

Every model's predictions on the 757-review matched test slice are evaluated against two distinct label sources, kept separate throughout and never conflated: the **original evaluation labels** (the rating-derived labels for English, the single-pass annotated labels for Arabic, exactly as used for every result reported before the human-annotation study), and the **human-adjudicated reference set** described in Section 4. Comparing a model's performance under these two references is the central analytical device of this paper (Sections 7–8, not yet drafted); re-evaluation against the reference set changes no model's predictions, only the label each prediction is scored against.

### 6.2 Metrics

For every model/evaluation-reference combination, we report Accuracy, Macro-F1, Weighted-F1, and per-class Precision, Recall, and F1 for each of the three sentiment classes, together with the full 3×3 confusion matrix. **Macro-F1 is treated as the primary metric throughout this paper**, in preference to Accuracy or Weighted-F1, because the sentiment-class distribution is substantially imbalanced toward Positive in both the original labels and the human-adjudicated reference set (reference-set distribution: 514 Positive, 201 Negative, 42 Neutral, of 757); Accuracy and Weighted-F1 are reported alongside Macro-F1 but are not used as the basis for any ranking or significance claim in this paper, since both can be dominated by performance on the majority class in a way that obscures Neutral-class behavior, which is a specific focus of this paper's class-level analysis (Section 7).

### 6.3 Statistical comparison methodology

Paired model comparisons are computed only between models for which valid, complete, row-level predictions exist on the identical set of test reviews; before any comparison is computed, each candidate prediction file is verified to contain exactly the required review identifiers (no duplicates, no missing identifiers, no unexpected identifiers) and only valid sentiment-label values. Of the candidate model/configuration combinations considered for the human-adjudicated reference-set re-evaluation, all but two (the two lost Phase 3B Arabic primary runs, Section 5.3) satisfied this check; comparisons involving those two conditions use the corresponding rerun realization, labeled as such.

Two statistically distinct procedures are used and are not conflated with one another:

- A **paired bootstrap resampling confidence interval** for the difference in Macro-F1 between two models: test rows are resampled with replacement, the Macro-F1 difference is recomputed on each resample, and the 2.5th/97.5th percentiles of the resulting distribution form the 95% interval. An associated heuristic significance value (the proportion of resampled differences crossing zero relative to the observed difference's sign, doubled) is reported alongside the interval, but this value is described throughout this paper as a resampling-distribution heuristic, not as a permutation-test p-value, and is not used as the basis for a significance claim in this paper.
- A **paired permutation (randomization) test** for the same Macro-F1 difference: on each iteration, each test row's two predictions are independently reassigned between "model A" and "model B" with equal probability, holding the human-adjudicated (or original) true label fixed, and the Macro-F1 difference is recomputed under this reassignment to build a null distribution consistent with the hypothesis that the two models' predictions are exchangeable. The reported p-value is the add-one-smoothed proportion of null-distribution differences at least as extreme as the observed difference. This is the procedure whose result is treated as the primary significance determination in this paper.

Both procedures use 10,000 iterations and a fixed seed (42) for the human-adjudicated-reference-set re-evaluation reported in this paper. Earlier, original-label significance testing (reported for comparison in Section 7) used 2,000 iterations for the Phase 3A conditions and 10,000 iterations for the Phase 3B conditions, under the same seed convention. This paper's own re-evaluation standardizes on 10,000 iterations throughout, for both training tracks; the historical 2,000-iteration Phase 3A figures are reported as they were originally computed, not re-run, and are not among the four comparisons whose significance status this paper reports as changing (Section 7.6) — all four are Phase 3B comparisons, already computed at 10,000 iterations on both sides of the before/after comparison. The iteration-count difference is therefore noted here for completeness and must not be read as contributing to, or explaining, any significance-status change reported in this paper.

Within each evaluation reference, pairwise comparisons are grouped into four comparison families — Phase 3A Arabic, Phase 3A English, Phase 3B Arabic, Phase 3B English — matching the grouping used for the original-label significance tests, so that a before/after comparison of significance status is computed on a like-for-like family structure. Holm-Bonferroni correction for multiple comparisons is applied independently within each family, separately for the bootstrap-heuristic p-values and for the permutation-test p-values; Phase 3A and Phase 3B are never combined into a single correction family, consistent with their status as two distinct, non-merged training configurations (Section 5.2).

`[TABLE 5: Evaluation metrics and statistical test summary — project artifact: results/human_gold_evaluation/human_gold_metrics_all_models.csv, original_vs_human_gold_comparison.csv, and statistical_tests_human_gold.csv, covering per-model Accuracy/Macro-F1/Weighted-F1/per-class metrics under both evaluation references, and the full pairwise significance comparison with both bootstrap and permutation p-values, Holm-adjusted, with explicit realization (primary/rerun) tags throughout.]`

<!-- EVIDENCE TRACE: src/evaluation/metrics.py; scripts/evaluate.py; configs/training.yaml (bootstrap, significance_testing sections); results/human_gold_evaluation/01_build_comparison_dataset.py through 07_patch_rerun_labeling.py; results/human_gold_evaluation/README_PROVENANCE.md; results/human_gold_evaluation/statistical_tests_human_gold.csv/.json; results/tables/significance_tests.json; results/phase3b_kaggle_gpu/README_PHASE3B.txt; results/phase3b_kaggle_gpu/arabic_paired_bootstrap_holm_results.csv; results/phase3b_kaggle_gpu/english_paired_bootstrap_holm_results.csv; paper/notes/RERUN_LABELING_AUDIT.md; paper/notes/REPRODUCIBILITY_MANIFEST.md -->

---

## 7. Results

This section is organized around the paper's central argument rather than the chronological order in which experiments were run: it first establishes how reliable the original evaluation labels were (7.1–7.3), then reports what re-evaluating existing models against the human-adjudicated reference set does to the resulting scientific picture (7.4–7.8), before closing with a short, separately-scoped dataset-measurement finding (7.9).

### 7.1 Human annotation reliability

Three independent bilingual annotators each labeled all 757 reviews of the matched test slice (369 Arabic, 388 English), yielding 2,271 primary sentiment-annotation decisions. Of the 757 reviews, 578 (76.4%) received unanimous agreement across all three annotators; 161 (21.3%) received a 2-of-3 majority with one dissenting annotator; and 18 (2.4%) produced a three-way split. At least a 2-of-3 majority was reached on 739 of 757 reviews (97.6%).

Three-rater agreement on the sentiment label was Fleiss' κ = 0.650, with Krippendorff's α (nominal) = 0.650, a closely consistent estimate from an independent formula. Pairwise Cohen's κ across the three annotator pairs ranged from 0.628 to 0.700, with pairwise raw agreement ranging from 81.9% to 86.5%.

Agreement statistics computed separately for each language subset are reported descriptively: for the 369 Arabic reviews, 300 (81.3%) were unanimous and Fleiss' κ = 0.671; for the 388 English reviews, 278 (71.6%) were unanimous and Fleiss' κ = 0.628. **This difference is not evidence that Arabic sentiment is intrinsically easier to annotate than English sentiment, or vice versa.** The two language subsets differ simultaneously in source dataset, domain, and original label-construction history (Section 3), any of which could independently account for the observed agreement gap; no design in this study isolates language itself as the explanatory factor.

The mixed-sentiment flag collected alongside the sentiment label showed substantially lower three-rater agreement (κ ≈ 0.269), well below the sentiment label's own agreement and outside the range conventionally considered reliable. Consistent with Section 4.1, this variable is treated as exploratory only throughout this paper: it is not validated as a primary variable, is not used in the construction of the human-adjudicated reference set, and no finding in this paper rests on it.

`[TABLE 2: Three-annotator agreement statistics — populated. See content below.]`

**Table 2. Three-annotator agreement on the 757-review matched test slice.**

| Scope | N | Unanimous (3/3) | 2/3 majority | 3-way split | ≥2/3 agreement | Fleiss' κ | Krippendorff's α |
|---|---|---|---|---|---|---|---|
| Overall | 757 | 578 (76.4%) | 161 (21.3%) | 18 (2.4%) | 739 (97.6%) | 0.650 | 0.650 |
| Arabic | 369 | 300 (81.3%) | 58 (15.7%) | 11 (3.0%) | 358 (97.0%) | 0.671 | 0.671 |
| English | 388 | 278 (71.6%) | 103 (26.5%) | 7 (1.8%) | 381 (98.2%) | 0.628 | 0.629 |

*Pairwise Cohen's κ (overall): annotator 1–2 = 0.700, annotator 1–3 = 0.629, annotator 2–3 = 0.628. Mixed-sentiment flag (overall, exploratory only): κ ≈ 0.269.*

<!-- EVIDENCE TRACE: paper/annotation/full/agreement_outputs/overall_agreement_sentiment.json; paper/annotation/full/agreement_outputs/language_specific_agreement_sentiment.json; paper/annotation/full/agreement_outputs/mixed_sentiment_flag_agreement.json; paper/annotation/full/HUMAN_ANNOTATION_ANALYSIS.md -->

### 7.2 Original evaluation labels vs. the human-adjudicated reference set

Comparing the original evaluation labels (rating-derived for English; single-pass human-annotated for Arabic, Section 3) against the human-adjudicated reference set constructed in Section 4 shows agreement on 625 of 757 reviews overall (82.6%; Cohen's κ = 0.662). By language: Arabic agreement is 310/369 (84.0%; κ = 0.660); English agreement is 315/388 (81.2%; κ = 0.660).

We use the terms **label disagreement** and **label revision** throughout this subsection, not "annotation error," because a disagreement between the original label and the reference set does not by itself establish which label is incorrect; where the term "label noise" is used elsewhere in this paper, it is defined operationally as disagreement with the human-adjudicated reference set, not as a claim about the original label's objective validity.

The class distribution shifts substantially between the two label sources. Original labels: 181 Negative, 117 Neutral, 459 Positive. Human-adjudicated reference labels: 201 Negative, 42 Neutral, 514 Positive. The Neutral class shrinks from 117 to 42 — a reduction concentrated almost entirely in one direction: of the 117 reviews originally labeled Neutral, 97 (82.9%) were revised to a different label under the human-adjudicated reference set (Section 7.1's language-specific breakdown: 89.3% for Arabic, 77.1% for English). By contrast, originally Positive-labeled reviews were revised in only 3.3% of cases and originally Negative-labeled reviews in 11.1% of cases.

Among the six possible label transitions, two dominate: Neutral→Positive (61 reviews) and Neutral→Negative (36 reviews). All other transitions are comparatively uncommon (Positive→Neutral: 11; Positive→Negative: 4; Negative→Neutral: 11; Negative→Positive: 9).

`[TABLE 1: Original vs. human-adjudicated label agreement and transitions — populated. See content below.]`

**Table 1. Original-label vs. human-adjudicated reference-set agreement, class distribution, and transitions.**

| | Overall | Arabic | English |
|---|---|---|---|
| N | 757 | 369 | 388 |
| Agreement | 625 (82.6%) | 310 (84.0%) | 315 (81.2%) |
| Disagreement | 132 (17.4%) | 59 (16.0%) | 73 (18.8%) |
| Cohen's κ | 0.662 | 0.660 | 0.660 |
| Original class distribution (Neg/Neu/Pos) | 181 / 117 / 459 | — | — |
| Reference-set class distribution (Neg/Neu/Pos) | 201 / 42 / 514 | — | — |
| % of originally-Neutral reviews revised | 82.9% | 89.3% | 77.1% |

*Named transitions (overall): Positive→Neutral 11; Positive→Negative 4; Neutral→Positive 61; Neutral→Negative 36; Negative→Neutral 11; Negative→Positive 9.*

<!-- EVIDENCE TRACE: results/human_gold_evaluation/comparison_dataset_757.csv; results/human_gold_evaluation/label_agreement_overall_by_language.json; results/human_gold_evaluation/disagreement_rate_conditional.csv; results/human_gold_evaluation/full_transition_table_overall.csv, full_transition_table_arabic.csv, full_transition_table_english.csv -->

### 7.3 Adjudication outcomes and Neutral-boundary instability

Among the 161 reviews where the three original annotators produced a 2-of-3 majority, the independent fourth adjudicator agreed with that majority in 101 cases (62.7%) and disagreed in 60 (37.3%). This rate varied by the majority label itself: where the majority label was Negative, the adjudicator agreed in 41 of 48 cases (85.4%); where Positive, 51 of 79 (64.6%); where **Neutral, only 9 of 34 (26.5%)**. Among the 18 three-way-split reviews, where no majority existed to compare against, the adjudicator's own distribution of choices was 9 Negative, 7 Neutral, and 2 Positive.

We report this pattern as an observation about Neutral-boundary instability under independent re-reading, not as proof that the original majority vote was "wrong": a 2-of-3 majority and a single blinded adjudicator's independent judgment are two different decision processes, and disagreement between them does not establish which is correct. What this finding does support is that **majority-Neutral decisions from the three-annotator round were markedly less stable under an independent, blinded re-read than majority-Negative or majority-Positive decisions were** — a pattern consistent with, though not on its own sufficient to fully explain, the broader Neutral-class instability reported throughout this paper.

This finding carries one further, standing limitation: all 179 adjudication decisions (both the 161 majority cases discussed here and the 18 three-way cases) were made by a **single** fourth adjudicator. No second adjudicator was used, and adjudication reliability itself — unlike the three original annotators' reliability, which is directly measured in Section 7.1 — was not independently estimated. The 62.7%/37.3% agreement-with-majority split and the by-class breakdown above should be read as a description of what one adjudicator decided, not as a validated estimate of how any adjudicator would decide on re-test.

`[TABLE 3: Adjudication outcome summary — populated. See content below.]`

**Table 3. Adjudicator agreement with the prior 2-of-3 majority, and three-way-case outcomes.**

| Majority-case subset | N | Adjudicator agreed | Adjudicator disagreed |
|---|---|---|---|
| All majority cases | 161 | 101 (62.7%) | 60 (37.3%) |
| Majority label = Negative | 48 | 41 (85.4%) | 7 (14.6%) |
| Majority label = Positive | 79 | 51 (64.6%) | 28 (35.4%) |
| Majority label = Neutral | 34 | 9 (26.5%) | 25 (73.5%) |

| Three-way cases (no majority existed) | N = 18 |
|---|---|
| Adjudicator chose Negative | 9 |
| Adjudicator chose Neutral | 7 |
| Adjudicator chose Positive | 2 |

<!-- EVIDENCE TRACE: paper/annotation/full/adjudication/adjudication_merged.csv; paper/annotation/full/adjudication/analyze_adjudication.py (output reproduced above); docs/known_limitations.md (#25) -->

### 7.4 Effect of the human-adjudicated reference set on model performance

Of the 16 model/language realizations for which valid, complete row-level predictions exist (Section 5.3, Section 6.3), **13 show lower Macro-F1 under the human-adjudicated reference set than under the original evaluation labels**. The mean Macro-F1 change is −0.025 for the Phase 3A (laptop, LoRA) track and −0.101 for the Phase 3B (GPU, full fine-tuning) track; within Phase 3B, the Arabic subset shows a larger mean change (−0.146) than the English subset (−0.041).

Table 5 (below) reports the full set of before/after Macro-F1 values. Three realizations *improve* under the human-adjudicated reference set, and all three are Phase 3A (LoRA) realizations: the English-trained→Arabic-tested zero-shot model (+0.074), the standalone English XLM-R model (+0.012), and the Arabic-trained→English-tested zero-shot model (+0.017). No Phase 3B (full fine-tuning) realization improves.

Two interpretive constraints apply throughout this subsection and the rest of Section 7. First, **Phase 3A and Phase 3B are never compared to each other as if hardware, fine-tuning method, class weighting, and sequence length were a single isolated variable** (Section 5.2); the larger mean Macro-F1 drop observed for Phase 3B is reported as a property of that bundled configuration under the human-adjudicated reference set, not as evidence that full fine-tuning, GPU training, or weighted loss is individually inferior to its Phase 3A counterpart. Second, for the two Arabic conditions whose primary Phase 3B row-level predictions were lost (standalone MARBERT, standalone XLM-R), every before/after figure reported uses the **rerun realization** and is labeled as such; no comparison in this paper treats the rerun figure as if it were the lost primary run's own result, and no human-adjudicated-reference-set figure exists for the primary realizations of these two models at all.

`[TABLE 5a: Model Macro-F1, original-label vs. human-adjudicated reference, with realization tags — populated. See content below. (Per-class/precision/recall detail and the full 16-model confusion-matrix set are deferred to Table 5b, supplementary.)]`

**Table 5a. Model Macro-F1 under the original evaluation labels and the human-adjudicated reference set.**

*Arabic (n=369; human-adjudicated reference: 86 Negative, 9 Neutral, 274 Positive)*

| Model | Track | Realization | Macro-F1 (original) | Macro-F1 (reference set) | Δ |
|---|---|---|---|---|---|
| EN→AR zero-shot (LoRA) | 3A | primary | 0.541 | 0.615 | +0.074 |
| XLM-R (LoRA) | 3A | primary | 0.623 | 0.615 | −0.008 |
| MARBERT (LoRA) | 3A | primary | 0.618 | 0.601 | −0.017 |
| TF-IDF + LogReg | 3A | primary | 0.705 | 0.586 | −0.118 |
| TF-IDF + SVM | 3A | primary | 0.705 | 0.573 | −0.131 |
| MARBERT (full FT) | 3B | **rerun realization** | 0.765 | 0.626 | −0.140 |
| XLM-R multilingual (full FT) | 3B | primary | 0.768 | 0.595 | −0.173 |
| XLM-R standalone (full FT) | 3B | **rerun realization** | 0.740 | 0.582 | −0.158 |
| EN→AR zero-shot (full FT) | 3B | primary | 0.680 | 0.568 | −0.112 |

*English (n=388; human-adjudicated reference: 115 Negative, 33 Neutral, 240 Positive)*

| Model | Track | Realization | Macro-F1 (original) | Macro-F1 (reference set) | Δ |
|---|---|---|---|---|---|
| TF-IDF + LogReg | 3A | primary | 0.687 | 0.647 | −0.040 |
| TF-IDF + SVM | 3A | primary | 0.651 | 0.640 | −0.010 |
| XLM-R (LoRA) | 3A | primary | 0.611 | 0.623 | +0.012 |
| AR→EN zero-shot (LoRA) | 3A | primary | 0.546 | 0.562 | +0.017 |
| XLM-R standalone (full FT) | 3B | primary (no rerun needed) | 0.728 | 0.692 | −0.036 |
| XLM-R multilingual (full FT) | 3B | primary | 0.740 | 0.686 | −0.053 |
| AR→EN zero-shot (full FT) | 3B | primary | 0.680 | 0.648 | −0.033 |

<!-- EVIDENCE TRACE: results/human_gold_evaluation/original_vs_human_gold_comparison.csv; results/human_gold_evaluation/human_gold_metrics_all_models.csv; results/human_gold_evaluation/prediction_availability.csv (realization column); paper/notes/RERUN_LABELING_AUDIT.md -->

### 7.5 Model-ranking stability

Re-ordering the Arabic models by Macro-F1 under each label source shows a substantial change: under the original labels, the top three positions are held by Phase 3B full-fine-tuning realizations (multilingual XLM-R, MARBERT rerun, standalone XLM-R rerun, in that order), with the classical TF-IDF baselines and Phase 3A LoRA realizations occupying the lower half of the ranking. Under the human-adjudicated reference set, the MARBERT rerun realization remains at the top, but the next two positions are taken by Phase 3A LoRA realizations (the EN→AR zero-shot model and the standalone XLM-R LoRA model), while the multilingual XLM-R full-fine-tuning realization falls to fifth position and the Phase 3B zero-shot realization falls to last.

The English ranking is comparatively stable: the same two Phase 3B full-fine-tuning realizations (standalone XLM-R and multilingual XLM-R) occupy the top two positions under both label sources, and the rest of the ordering is unchanged. The two top positions do swap order, but by a small margin — a Macro-F1 separation of approximately 0.006 (standalone XLM-R 0.692 vs. multilingual XLM-R 0.686 under the human-adjudicated reference set) — and this reordering is not treated as a substantive finding in its own right (Section 7.6 addresses whether it, or any other pairwise difference, is statistically distinguishable).

This asymmetry between the two languages is reported descriptively, not as evidence that the Arabic evaluation is *intrinsically* less stable than the English evaluation: the Arabic ranking's upper positions include two rerun realizations whose primary counterparts' row-level predictions no longer exist (Section 7.4), so part of the observed Arabic instability may reflect the realization substitution itself rather than only the reference-label change; this confound cannot be fully separated with the predictions available to this study. The central claim this subsection supports is narrower and does not depend on resolving that confound: that **a model ranking computed under the original evaluation labels was sensitive to the choice of reference label**, at least for the Arabic condition, and this sensitivity is itself the finding, independent of which specific model ends up ranked first.

`[FIGURE 3 placeholder — see Section "Figures" below.]`

<!-- EVIDENCE TRACE: results/human_gold_evaluation/original_vs_human_gold_comparison.csv; results/human_gold_evaluation/prediction_availability.csv -->

### 7.6 Statistical-conclusion stability

Four pairwise model comparisons were found statistically significant (Holm-corrected, α=0.05) under the original evaluation labels in the Phase 3B significance testing: three in Arabic (standalone XLM-R rerun vs. EN→AR zero-shot; MARBERT rerun vs. EN→AR zero-shot; multilingual XLM-R vs. EN→AR zero-shot) and one in English (multilingual XLM-R vs. AR→EN zero-shot).

Re-running the equivalent comparisons against the human-adjudicated reference set, using a paired permutation/randomization test (10,000 iterations, seed 42, Holm-corrected within the same family structure; Section 6.3), produces a different pattern. Of the four originally-significant comparisons, **only one remains significant**: MARBERT rerun vs. EN→AR zero-shot (Holm-adjusted permutation p = 0.016). The other three no longer reach significance under the human-adjudicated reference set: standalone XLM-R rerun vs. EN→AR zero-shot (Holm-adjusted p = 0.647), multilingual XLM-R vs. EN→AR zero-shot (Holm-adjusted p = 0.377), and multilingual XLM-R vs. AR→EN zero-shot (Holm-adjusted p = 0.119). One additional comparison that was *not* significant under the original labels becomes significant under the human-adjudicated reference set: standalone XLM-R rerun vs. MARBERT rerun (Holm-adjusted permutation p = 0.0012), favoring MARBERT.

We report this as evidence of **statistical-conclusion sensitivity to the choice of reference label**, not as evidence that the underlying models became "equivalent" or that the human-adjudicated reference set "proved" the original findings wrong. Non-significance under either label source is not interpreted as evidence of true equivalence between any two models at this sample size (n=369 Arabic, n=388 English); it is reported only as "not statistically distinguishable under this test, at this correction level."

Two distinct statistics are reported throughout and must not be conflated: the paired bootstrap resampling 95% confidence interval (and its accompanying resampling-heuristic p-value, not treated as a significance criterion in this paper) and the paired permutation/randomization-test p-value (treated as the primary significance criterion). All Holm-adjusted significance statements in this subsection refer to the permutation-test p-value specifically.

`[TABLE 6: Statistical-comparison stability before vs. after — populated. See content below.]`

**Table 6. Pairwise statistical comparisons found significant (Holm-corrected, α=0.05) under the original evaluation labels, re-evaluated under the human-adjudicated reference set.**

| Comparison | Language | Significant under original labels? | Significant under reference set? (permutation test, Holm-adjusted) |
|---|---|---|---|
| XLM-R standalone (rerun) vs. EN→AR zero-shot | Arabic | Yes | **No** (p=0.647) |
| MARBERT (rerun) vs. EN→AR zero-shot | Arabic | Yes | **Yes** (p=0.016) |
| XLM-R multilingual vs. EN→AR zero-shot | Arabic | Yes | **No** (p=0.377) |
| XLM-R multilingual vs. AR→EN zero-shot | English | Yes | **No** (p=0.119) |
| XLM-R standalone (rerun) vs. MARBERT (rerun) | Arabic | No | **Yes** (p=0.0012) — newly significant |

*Full 18-comparison table (all families, both bootstrap and permutation statistics, raw and Holm-adjusted p-values): Table 11, supplementary.*

**Methodological note on iteration counts:** the original Phase 3A significance tests used 2,000 bootstrap iterations; the original Phase 3B significance tests and this paper's own human-adjudicated-reference re-evaluation both use 10,000 iterations (bootstrap and permutation alike), under the same seed (42). All four comparisons whose significance status this paper reports as changing are Phase 3B comparisons, computed at 10,000 iterations on both the original-label and reference-set side; none are Phase 3A comparisons. This difference in historical iteration count is therefore noted for completeness only and is not, on its own or in any other way, an explanation for the significance-status changes reported above.

<!-- EVIDENCE TRACE: results/human_gold_evaluation/statistical_tests_human_gold.csv (authoritative for all post-Human-Gold figures in this subsection); results/phase3b_kaggle_gpu/arabic_paired_bootstrap_holm_results.csv; results/phase3b_kaggle_gpu/english_paired_bootstrap_holm_results.csv (authoritative for original-label significance figures); results/tables/significance_tests.json (Phase 3A, not among the four comparisons discussed here); results/human_gold_evaluation/README_PROVENANCE.md -->

### 7.7 Neutral-class behavior

The human-adjudicated reference set contains 42 Neutral-labeled reviews of 757 (5.5%): 9 of 369 Arabic reviews (2.4%) and 33 of 388 English reviews (8.5%). Mean per-class F1 across all 16 evaluated model realizations falls from 0.396 (original labels) to 0.176 (human-adjudicated reference set) for the Neutral class specifically — a larger drop than for Negative (0.748→0.798, which rises) or Positive (0.879→0.875, essentially flat). **Neutral is the lowest-performing of the three classes for every one of the 16 evaluated model realizations under the human-adjudicated reference set**, verified individually against the per-model class-level output, not assumed from the mean alone.

Two findings must be read together here, not separately. First, models' measured performance on Neutral is markedly worse under the human-adjudicated reference set than under the original labels. Second, Neutral itself is the class with by far the highest rate of label revision in this study (82.9% of originally-Neutral reviews were revised, Section 7.2) and, independently, the class on which the original three annotators' own agreement was weakest within the annotation study (Section 7.1) and on which the fourth adjudicator most often overturned a prior majority (26.5% agreement with majority-Neutral decisions, Section 7.3). Given this, and given Neutral's small support — particularly the 9-review Arabic support, where a single misclassification changes the measured F1 by roughly 11 percentage points — we do not state that "models cannot understand Neutral sentiment" as a settled causal claim. We state instead: **Neutral remained the least stable and lowest-performing class in the evaluated setting, although its small support — particularly in Arabic — and substantial annotation-boundary instability limit stronger interpretation.** This paper's design does not separate genuine linguistic/sentiment ambiguity, class rarity, and annotation-guideline boundary placement as distinct causes of this pattern.

`[TABLE 4: Per-class F1 and support, focused on Neutral — populated. See content below.]`

**Table 4. Per-class F1 (original labels vs. human-adjudicated reference set), with Neutral support.**

| | Negative F1 (orig. → ref.) | Neutral F1 (orig. → ref.) | Positive F1 (orig. → ref.) | Neutral support (reference set) |
|---|---|---|---|---|
| Mean across all 16 model realizations | 0.748 → 0.798 | 0.396 → 0.176 | 0.879 → 0.875 | 42 / 757 overall |
| Arabic subset | — | — | — | 9 / 369 |
| English subset | — | — | — | 33 / 388 |

*Full per-model, per-class breakdown (16 models × 3 classes × 2 evaluation references): Table 8, supplementary (source: `human_gold_metrics_all_models.csv`).*

`[FIGURE 4 placeholder — see Section "Figures" below.]`

<!-- EVIDENCE TRACE: results/human_gold_evaluation/human_gold_metrics_all_models.csv; results/human_gold_evaluation/error_analysis_by_class_language.csv -->

### 7.8 Multilingual and zero-shot findings

Two secondary findings about the multilingual/cross-lingual experimental grid are reported here, subordinate to the label-reliability story above.

**Multilingual joint training.** The multilingual XLM-R realization was not significantly different (Holm-corrected permutation test) from the matched monolingual standalone realization in either language, under either label source (Arabic, original labels: multilingual vs. MARBERT rerun and vs. XLM-R rerun both non-significant in the original Phase 3B testing; Arabic, reference set: multilingual vs. MARBERT rerun Holm-adjusted p=0.163, multilingual vs. XLM-R rerun not among the four originally-significant pairs and remains non-significant under the reference set per Table 11; English, both label sources: multilingual vs. standalone XLM-R non-significant, Holm-adjusted p=0.778 under the reference set). We describe multilingual training as *not significantly distinguishable from* monolingual training under either evaluation, which is descriptively consistent with "competitive" — but non-significance at this sample size is not evidence of true equivalence, and is not reported as such.

**Zero-shot cross-lingual transfer.** Under the original evaluation labels, all four of this study's originally-significant findings (Section 7.6) involve a zero-shot comparison: zero-shot transfer was significantly weaker than every other Arabic model (3 comparisons) and significantly weaker than the multilingual model in English (1 comparison). Under the human-adjudicated reference set, this pattern weakens substantially: of those four zero-shot-involving significant findings, **three no longer reach significance** (standalone XLM-R rerun vs. EN→AR zero-shot; multilingual XLM-R vs. EN→AR zero-shot, Arabic; multilingual XLM-R vs. AR→EN zero-shot, English), and **one remains significant** (MARBERT rerun vs. EN→AR zero-shot, Holm-adjusted p=0.016). The precise summary is therefore: *most, but not all,* of zero-shot transfer's apparent statistically-supported weakness under the original labels does not survive re-evaluation against the human-adjudicated reference set, with one specific exception (MARBERT rerun remains significantly ahead of EN→AR zero-shot). Zero-shot realizations remain numerically the weakest or near-weakest in most rankings even where the statistical case no longer holds (Table 5a).

<!-- EVIDENCE TRACE: results/human_gold_evaluation/statistical_tests_human_gold.csv; results/phase3b_kaggle_gpu/arabic_paired_bootstrap_holm_results.csv; results/phase3b_kaggle_gpu/english_paired_bootstrap_holm_results.csv -->

### 7.9 Code-switching: a dataset-measurement finding, reported briefly

A character-script-fraction heuristic applied to the combined usable corpus (1,050,832 documents) flagged 109 candidate documents as containing mixed Arabic-English script. Exhaustive two-rater blind manual audit of all 109 candidates found that 84 (77.1%) were a platform display artifact — a passage shown alongside its own machine translation — rather than genuine code-switching; the remaining non-genuine candidates were script-misidentification, named entities, or incidental interjections. **Only 9 of the 109 candidates, and 9 of the full 1,050,832-document corpus, were confirmed genuine Arabic-English code-switching.**

This finding is reported here strictly as a dataset-measurement/audit observation: a common, low-cost code-switch-detection heuristic can be dominated by a platform-specific display artifact rather than genuine bilingual production, in this review-platform domain. **No quantitative model-performance evaluation is reported or implied for these 9 examples anywhere in this paper**; the sample size is explicitly insufficient to support a train/test split, a confidence interval, or a significance test, and the 9 examples are reserved only for qualitative illustration (Section 8, not yet drafted).

<!-- EVIDENCE TRACE: docs/codeswitch_audit.md -->

---

## Figures (placeholders and captions only — no graphics generated at this stage)

**Figure 1 (main).** *Purpose:* visualize where original-vs-reference-set label disagreement concentrates. *Data source:* `results/human_gold_evaluation/full_transition_table_overall.csv`. *Encoding:* alluvial/Sankey diagram, original class (left nodes) flowing to reference-set class (right nodes), flow width proportional to review count. *Draft caption:* "Disagreement between the original evaluation labels and the human-adjudicated reference set is concentrated almost entirely in originally-Neutral-labeled reviews (82.9% revised), while originally Positive- and Negative-labeled reviews are revised rarely (3.3% and 11.1% respectively)."

**Figure 2 (main).** *Purpose:* show the performance consequence of re-evaluation across all 16 model realizations at once. *Data source:* `results/human_gold_evaluation/original_vs_human_gold_comparison.csv`. *Encoding:* dumbbell/slope plot, one line per model realization from (Macro-F1, original labels) to (Macro-F1, human-adjudicated reference set), colored by training track (Phase 3A/3B) and marked where a realization is a rerun. *Draft caption:* "Macro-F1 decreases for 13 of 16 model realizations under human-adjudicated re-evaluation; the decrease is larger, on average, for the GPU full-fine-tuning track than for the laptop LoRA track. Rerun realizations are marked explicitly."

**Figure 3 (main).** *Purpose:* visualize ranking instability directly (Section 7.5). *Data source:* Table 5a. *Encoding:* bump/slopegraph, rank position under original labels (left) vs. under the reference set (right), one line per model, separate panels for Arabic and English, rerun realizations marked. *Draft caption:* "The Arabic model ranking reorders substantially under human-adjudicated evaluation; the English ranking is comparatively stable, with only the top two positions swapping by a small margin."

**Figure 4 (main).** *Purpose:* show Neutral's performance pattern with its support caveat visible in the figure itself, not only the caption (Section 7.7). *Data source:* `results/human_gold_evaluation/human_gold_metrics_all_models.csv`. *Encoding:* bar or forest plot, per-model Neutral F1 under both label sources, with the Neutral support count (n=9 Arabic / n=33 English) annotated directly beside each language's points on the plot itself. *Draft caption:* "Neutral F1 falls further under human-adjudicated evaluation for every model; Neutral support is small (annotated above) and must be read alongside the estimate, particularly for Arabic."

**Figure 5 (supplementary).** Adjudicator confidence distribution by case type and language. *Data source:* `paper/annotation/full/adjudication/adjudication_merged.csv`.

**Figure 6 (supplementary).** Confusion-matrix heatmaps for the most-discussed models (original labels vs. reference set, side by side). *Data source:* `results/human_gold_evaluation/confusion_matrix_*`.

**Figure 7 (supplementary).** Code-switch heuristic funnel: 109 candidates → 5 categories → 9 genuine. *Data source:* `docs/codeswitch_audit.md`.

---

## 8. Error and Label-Stability Analysis

This section examines model errors against the human-adjudicated reference set in more structural detail than Section 7.7's class-level summary, with particular attention to disentangling four distinct sources of apparent "disagreement" that are easy to conflate: (1) a model prediction that is simply wrong relative to a stable, trustworthy reference label; (2) instability in the reference label itself; (3) the mechanical effect of severe class imbalance on precision/recall/F1 arithmetic; and (4) genuine ambiguity in the underlying review text that no label scheme fully resolves. Not every model/reference disagreement reported in this section is treated as a model failure, and this section explicitly avoids that framing.

### 8.1 Neutral-related prediction errors: a precision problem, not only a recall problem

Breaking down each model's Neutral-class behavior into precision and recall (rather than F1 alone) reveals a specific, previously underspecified pattern. Under the human-adjudicated reference set, mean Neutral recall is substantially higher for the Phase 3B (full fine-tuning) track (0.688) than for the Phase 3A (LoRA) track (0.286), while mean Neutral precision is low and closely comparable across both tracks (0.132 vs. 0.129). In concrete terms: Phase 3B models predict Neutral considerably more often, correctly catching more of the (now rare) true-Neutral cases, but at the cost of a large number of false-Neutral predictions on reviews the reference set places in Positive or Negative — for example, the Arabic multilingual XLM-R realization predicts Neutral on 99 of 369 test reviews where the reference label is not Neutral, against only 9 true-Neutral reviews in the same set. Phase 3A LoRA models predict Neutral far less often overall and therefore accumulate fewer false-Neutral predictions in absolute terms, but still show low precision when they do predict it.

We read this pattern as evidence that the Phase 3B configuration's apparent original-label performance advantage (Section 7.4) was achieved partly by a classifier behavior — predicting Neutral comparatively often — that becomes a liability once evaluated against a reference set in which Neutral is much rarer than in the original labels (42 vs. 117 of 757; Section 7.2). This is reported as a plausible contributing mechanism, consistent with the observed precision/recall split, not as a demonstrated causal explanation; no ablation in this study isolates class-weighting, sequence length, or fine-tuning method as the specific driver of this behavior difference between the two tracks.

### 8.2 Model error vs. reference-label instability: two illustrative, non-cherry-picked cases

Using this project's pre-registered deterministic example-selection rule (for each model and each true-class/predicted-class error cell, the first review by ascending review-identifier is selected; applied identically everywhere, not chosen for favorability), two cases illustrate the distinction this section draws:

- **Review AR-TOUR-01100** (Arabic; human-adjudicated reference label: Positive; predicted Neutral by the multilingual XLM-R, Phase 3B realization). This review was among the 179 cases requiring adjudication in Section 4; the adjudicator's recorded rationale was that the review "explicitly states the place is nice and they didn't regret visiting, despite many closed booths and lack of authentic Gulf representation" — a case with genuine mixed content (an explicit positive statement alongside specific criticism) that a human adjudicator resolved toward Positive on balance, but which a model collapsing mixed-sentiment signal toward Neutral is not thereby simply "wrong" in an uncomplicated sense; this is an example where the model's error and the review's own mixed character are difficult to fully separate.
- **Review EN-VT-0026623** (English; human-adjudicated reference label: Positive; predicted Neutral by the standalone XLM-R full-fine-tuning realization). The review text — "Basically the only hardware store in town. It's nice to support this business over driving 30 minutes to a big box retailer. They will deliver building supplies." — is largely factual/descriptive with one brief positive clause. This is a plausible example of genuine dataset-level ambiguity at the Positive/Neutral boundary (category 4 above) rather than a clear-cut model error: a reasonable reader could place this review on either side of that boundary.

These two examples are reported as illustrations of categories (1)/(2) and (4) respectively, not as a representative sample of error frequency or type; no claim is made that the project's errors are "mostly" of one kind or another beyond the quantitative breakdown in Section 7.7, Section 8.1, and `error_analysis_by_class_language.csv`.

### 8.3 Attribution discipline

Consistent with this section's opening framing, four considerations are kept explicitly separate when interpreting any individual disagreement surfaced by this analysis: whether the disagreement reflects a model making a wrong prediction relative to a reference label that the human-adjudication study's own reliability statistics (Section 4, Section 7.1) support treating as comparatively stable (e.g., a majority-Negative or majority-Positive-derived label, which the adjudicator overturned only 14.6%/35.4% of the time, Section 7.3); a disagreement arising from reference-label instability itself, most concentrated in Neutral; the mechanical consequence of Neutral's small support (42 of 757, 9 of 369 for Arabic) on any single-model, single-class F1 estimate; or a case of genuine textual ambiguity that no single three-class scheme cleanly resolves. This paper does not attempt to assign every one of the hundreds of individual model/reference disagreements in the full error-analysis table to exactly one of these four categories; the two worked examples above illustrate that the categories are not always mutually exclusive for a given review.

`[TABLE 7: Neutral-class precision/recall breakdown by model and track — populated conceptually above (Section 8.1); full per-model table deferred to supplementary Table 8.]`

<!-- EVIDENCE TRACE: results/human_gold_evaluation/human_gold_metrics_all_models.csv (Neutral_precision, Neutral_recall columns); results/human_gold_evaluation/error_analysis_by_class_language.csv; results/human_gold_evaluation/qualitative_error_examples.csv; paper/annotation/full/adjudication/adjudication_merged.csv (AR-TOUR-01100 adjudication rationale) -->

---

## 9. Discussion

### 9.1 Evaluation-label reliability matters for model conclusions

**Observation.** The original evaluation labels and the human-adjudicated reference set agree on 625 of 757 reviews (82.6%; Cohen's κ = 0.662); the remaining 132 reviews (17.4%) are label revisions, overwhelmingly concentrated in originally-Neutral-labeled reviews (Section 7.2). Re-evaluating the same, unretrained model predictions against this reference set changes measured per-class performance (Section 7.4, 7.7), model rankings (Section 7.5), and statistical-significance conclusions (Section 7.6).

**Interpretation.** Within this specific study — one bilingual review-sentiment benchmark, three annotators, one blinded adjudicator, 757 reviews — the construction of the evaluation reference materially affected the conclusions drawn from an otherwise unchanged set of trained models. The central message this paper supports is narrow and evidence-bound: *in this setting*, evaluation-reference construction was not a neutral bookkeeping detail but an active ingredient in the scientific conclusions obtained.

**Limitation.** This magnitude of effect — an 17.4% relabeling rate, a 3-of-4 flip in significance status — is not generalized to sentiment datasets in general, to other domains, or to other annotation designs in this paper. No claim is made about how typical or atypical this magnitude is relative to other NLP evaluation settings without a comparative study this paper does not conduct.

<!-- EVIDENCE TRACE: results/human_gold_evaluation/label_agreement_overall_by_language.json; results/human_gold_evaluation/original_vs_human_gold_comparison.csv; results/human_gold_evaluation/statistical_tests_human_gold.csv -->

### 9.2 Statistical conclusions were reference-sensitive

**Observation.** Four pairwise model comparisons were significant (Holm-corrected) under the original evaluation labels. Under the human-adjudicated reference set: three no longer reach significance (standalone XLM-R rerun vs. EN→AR zero-shot; multilingual XLM-R vs. EN→AR zero-shot; multilingual XLM-R vs. AR→EN zero-shot); one survives (MARBERT rerun vs. EN→AR zero-shot); and one comparison not significant under the original labels becomes significant under the reference set (standalone XLM-R rerun vs. MARBERT rerun, favoring MARBERT) (Section 7.6).

**Interpretation.** A statistical conclusion about which model is superior can depend on how the evaluation reference label was constructed, holding the models, their predictions, and the test rows themselves entirely fixed. This is the central mechanism by which label-construction choices propagate into reported scientific conclusions in this domain. It should **not** be read as meaning the original statistical tests were "wrong": those tests correctly answered the question "are these models' predictions significantly different when scored against the original evaluation labels," which is a well-posed question with a well-computed answer. The human-adjudicated re-evaluation answers a related but distinct question — "…when scored against an independently constructed, multi-annotator reference label" — and the two questions can have different answers without either test being in error.

**Limitation.** Non-significance, under either label source, is not interpreted anywhere in this paper as evidence that two models perform equivalently; it is reported only as "not statistically distinguishable under this test, at this sample size and correction level." The reverse inference — that a surviving or newly-significant finding (MARBERT rerun's two significant comparisons) proves MARBERT is the best model in an absolute sense — is also not drawn; it is reported only as the specific pairwise comparisons that reach significance under the stated test.

<!-- EVIDENCE TRACE: results/human_gold_evaluation/statistical_tests_human_gold.csv; results/phase3b_kaggle_gpu/arabic_paired_bootstrap_holm_results.csv; results/phase3b_kaggle_gpu/english_paired_bootstrap_holm_results.csv -->

### 9.3 Neutral as both a modeling and an annotation challenge

**Observation.** Neutral support falls from 117 (original labels) to 42 (human-adjudicated reference set; 9 Arabic, 33 English); 82.9% of originally-Neutral reviews were revised to a different label (Section 7.2). Among the three original annotators, Neutral-related disagreement (reflected in the overall κ=0.650 sentiment statistic, and more specifically in which reviews ended up non-unanimous) and, at adjudication, majority-Neutral decisions were overturned far more often — the adjudicator agreed with only 26.5% of majority-Neutral decisions (73.5% overturned) — than majority-Negative (85.4% agreement, 14.6% overturned) or majority-Positive (64.6% agreement, 35.4% overturned) decisions (Section 7.3). Mean Neutral F1 across all 16 model realizations falls from 0.396 to 0.176 under the human-adjudicated reference set, and Neutral is the lowest-performing class for every single one of the 16 realizations (Section 7.7); the precision/recall decomposition in Section 8.1 shows this is driven substantially by low precision (frequent false-Neutral predictions, especially for the Phase 3B track) rather than uniformly low recall.

**Interpretation.** Several plausible, non-exclusive contributing factors are consistent with this pattern: genuine semantic boundary ambiguity (a review that is both mildly positive and mildly critical, or purely factual, sits inherently close to the Positive/Neutral or Negative/Neutral boundary, as illustrated in Section 8.2); Neutral's small and shrinking support, which makes any single-model F1 estimate for this class statistically fragile (a single misclassification changes the Arabic Neutral F1 by roughly 11 percentage points); the three-annotator study's own comparatively weak agreement on this specific class; and, for the English subset specifically, a possible mismatch between the rating-derived original label (which assigns Neutral to 3-star reviews mechanically) and the review text's actual sentiment, which a human reader — annotator or adjudicator — may resolve differently than a numeric midpoint rating would. **This paper does not adjudicate among these candidate explanations; they are offered as plausible, not as established causal mechanisms, and no single factor is identified as the one responsible for the observed pattern.**

**Limitation.** Neutral difficulty in this study cannot be attributed solely to model capability. The evidence supports the narrower, better-grounded statement used throughout this paper (Section 7.7): Neutral remained the least stable and lowest-performing class in the evaluated setting, although its small support — particularly in Arabic — and substantial annotation-boundary instability limit stronger interpretation. A stronger statement, such as "models cannot understand Neutral sentiment," is not supported by this design and is explicitly avoided.

<!-- EVIDENCE TRACE: results/human_gold_evaluation/human_gold_metrics_all_models.csv; results/human_gold_evaluation/disagreement_rate_conditional.csv; paper/annotation/full/adjudication/analyze_adjudication.py outputs; paper/annotation/full/agreement_outputs/overall_agreement_sentiment.json -->

### 9.4 Model-ranking instability

**Observation.** Under the human-adjudicated reference set, the Arabic model ranking reorders substantially relative to the original-label ranking (Phase 3B full-fine-tuning realizations fall from the top three positions toward the middle/bottom; a Phase 3A LoRA zero-shot realization and the TF-IDF baselines rise); the English ranking is comparatively stable, with only the top two positions swapping by a small margin (≈0.006 Macro-F1) (Section 7.5).

**Interpretation.** This asymmetry is presented as a finding about **ranking instability under reference-label change**, not as evidence about Arabic and English sentiment classification's inherent relative difficulty. Multiple confounds prevent the stronger reading: the two corpora differ in source dataset, geography, domain, and original label-construction method (Section 3); the Arabic ranking's upper positions involve two rerun realizations whose lost primary counterparts cannot be independently re-evaluated against the reference set at all (Section 5.3, Section 7.4); and the two language subsets' class distributions and original annotation histories differ in ways this study does not control for. Given these simultaneous confounds, this paper draws only the narrower conclusion that the conclusion itself supports directly: **a model ranking computed under one evaluation-label source was not robust to a change in that source, at least for one of the two language conditions studied**, and this instability is reported as the finding, independent of attributing it to any single cause.

**Limitation.** Because the specific confounds above are not disentangled by this study's design, no claim is made, and none should be inferred, about which of them (if any) is responsible for the Arabic ranking's greater sensitivity relative to English's.

<!-- EVIDENCE TRACE: results/human_gold_evaluation/original_vs_human_gold_comparison.csv; results/human_gold_evaluation/prediction_availability.csv; paper/notes/RERUN_LABELING_AUDIT.md -->

### 9.5 Multilingual and zero-shot implications

**Observation.** Multilingual joint training (XLM-R) was not significantly different from matched monolingual standalone training in either language, under either the original labels or the human-adjudicated reference set (Section 7.8). Of the four originally-significant findings, all four involved a zero-shot comparison; three no longer hold under the human-adjudicated reference set, and one (MARBERT rerun vs. EN→AR zero-shot) survives (Section 7.6, Section 9.2).

**Interpretation.** Multilingual training can be described as performing comparably to — not significantly worse than, and not demonstrated to be significantly better than — monolingual training across the specific comparisons this study ran, under both evaluation references; this is reported as the model behaving *competitively within the observed experiments*, not as a general claim that multilingual and monolingual training are equivalent. Separately, most — though not all — of zero-shot cross-lingual transfer's apparent, statistically-supported weakness under the original labels does not survive re-evaluation against the human-adjudicated reference set, while zero-shot realizations remain numerically the weakest or near-weakest in most rankings regardless.

**Limitation.** As in Section 9.2, non-significance is not read as equivalence at any point in this subsection. These findings remain secondary to, and illustrative of, the central evaluation-label-reliability argument (Section 9.1–9.2); they are not presented as this paper's primary contribution.

<!-- EVIDENCE TRACE: results/human_gold_evaluation/statistical_tests_human_gold.csv -->

### 9.6 Implications for sentiment-analysis evaluation practice

**Observation.** Across this study: a rating-derived label scheme (English) and a single-pass human-annotated label scheme (Arabic) both showed substantial disagreement with an independently constructed, multi-annotator, blind-adjudicated reference, concentrated in the Neutral class; this disagreement was sufficient to change which pairwise model comparisons reached statistical significance and how models ranked, at least for one of the two languages studied.

**Interpretation — proportionate, study-specific methodological implications:**
- Rating-derived sentiment labels, where used as an evaluation reference, may warrant validation against an independently constructed human reference before being treated as equivalent to textual sentiment judgment — this study found the Neutral class specifically to be where such validation would have mattered most.
- Annotation disagreement (both among original annotators and between an original label scheme and a later adjudication) is more informative when reported explicitly (as in Section 4, Section 7.1–7.3) than when collapsed into a single aggregate label without a disagreement record.
- Model rankings computed from a single evaluation-label source are, at minimum, worth re-checking against an independently constructed reference where feasible, particularly for classes or language conditions with known or suspected label-construction weaknesses.
- Aggregate inter-annotator agreement statistics (e.g., an overall Fleiss' κ) can obscure class-specific instability (Neutral's agreement and adjudication-overturn rate differed sharply from Negative's and Positive's in this study); class-level agreement reporting is informative beyond the aggregate figure.
- A statistical model comparison inherits whatever uncertainty is present in its evaluation-reference construction; a significance result is a claim conditioned on that reference, not an unconditional claim about the models.

**Limitation.** These are implications proportionate to one study, in one domain (Arabic-English Google-Maps-style reviews), with one annotation design (three annotators, one blind adjudicator, 757 reviews). They are not presented as universal laws of sentiment-analysis evaluation, and no claim is made about how they generalize beyond the setting studied here.

<!-- EVIDENCE TRACE: Sections 4, 7, 8, 9.1-9.5 above; paper/notes/FINAL_SCIENTIFIC_FRAMING.md -->

---

## 10. Limitations

### 10.1 Human-adjudicated reference-set limitations

The human-adjudicated reference set constructed for this study (Section 4) is not an infallible ground truth and is not described as one anywhere in this paper. Two limitations are specific to its construction. First, all 179 adjudicated disagreement cases (23.6% of the full 757-review set) were resolved by a single, independent bilingual adjudicator; no second adjudicator was used, and adjudicator reliability itself was not independently estimated the way the three original annotators' reliability was (Section 7.1). Second, the mixed-sentiment flag collected during the original annotation round showed low three-rater reliability (κ ≈ 0.269) and was consequently excluded from the reference-set construction and from every downstream analysis in this paper; it is reported only as an exploratory, unvalidated variable. We additionally note, as a methodological-hygiene point rather than a result-affecting limitation, that the confidence scale recorded alongside the sentiment label (High/Medium/Low) was self-reported by each annotator and the fourth adjudicator independently, with no calibration exercise conducted across raters to confirm that "High" meant the same threshold of certainty to every rater; confidence values are accordingly not used anywhere in this paper's quantitative analysis, only descriptively (Section 7.3's by-class confidence note and `agreement_outputs/confidence_analysis.json`).

### 10.2 Neutral support

The human-adjudicated reference set contains only 42 Neutral-labeled reviews of 757 overall, and only 9 of 369 for the Arabic subset specifically. Every Neutral-specific statistic reported in this paper (Section 7.7, Section 8.1, Section 9.3) — per-model Neutral F1/precision/recall, and any claim about Neutral being the lowest-performing class — should be read with this support size in mind; a single misclassification changes the Arabic Neutral F1 estimate by roughly 11 percentage points. This limits both the precision and the generalizability of any Neutral-specific conclusion in this paper, independent of whether the underlying pattern (low Neutral performance) is itself real.

### 10.3 Dataset comparability

The Arabic and English primary corpora differ simultaneously in geography (Saudi Arabia vs. two U.S. states), domain match (direct tourism-site match for Arabic vs. a domain-proxy-filtered match for English), source (two distinct third-party data releases), original label-construction history (single-pass human annotation vs. rating-derived heuristic), and, potentially, other unmeasured review-characteristic differences (Section 3.5). No finding in this paper — including the model-ranking-stability asymmetry (Section 7.5, Section 9.4) and the annotation-agreement difference (Section 7.1) — is interpreted as evidence that Arabic is inherently harder or easier to classify than English; any such inference would require a design that isolates language from these other, simultaneously-varying factors, which this study does not provide.

### 10.4 Experimental comparability (Phase 3A vs. Phase 3B)

Phase 3A (laptop, LoRA fine-tuning, unweighted loss, 64-token sequences) and Phase 3B (GPU, full fine-tuning, weighted loss, 128-token sequences) differ in multiple training-configuration dimensions simultaneously (Section 5.2). No performance difference reported anywhere in this paper between a Phase 3A and a Phase 3B realization is attributed to GPU hardware, to LoRA specifically, or to full fine-tuning specifically, in isolation; every such comparison is reported as a difference between two bundled configurations.

### 10.5 Lost primary predictions

The original Phase 3B primary row-level predictions for standalone Arabic MARBERT and standalone Arabic XLM-R were lost before this study's human-adjudicated re-evaluation phase began (Section 5.3). Every figure in this paper involving either model under the human-adjudicated reference set uses the corresponding reproducibility-rerun realization, labeled explicitly as such throughout (Section 7.4–7.6, Table 5a, Table 6). No comparison in this paper treats a rerun figure as equivalent to the lost primary run's own result, and no human-adjudicated-reference figure exists, or is claimed to exist, for either primary realization. This limits direct before/after interpretation specifically for these two models: the "before" figure available (0.785025, 0.740295) and the "after" figure available (via rerun: 0.765263→reference-set value; 0.740126→reference-set value) are not strictly the same realization on both sides of the comparison.

### 10.6 Reproducibility gaps

Not every software/hardware detail of this study's training environments could be recovered from preserved artifacts. Specifically unrecoverable: the exact Python, PyTorch, and CUDA/driver versions used during Phase 3B's Kaggle-based training (one partial, caveated exception — see below); the specific CPU model used for Phase 3A's laptop training; and the implementation script that produced the original Phase 3B significance-testing outputs (the output CSVs are preserved; the code that generated them is not). One partial recovery is available with an important caveat: a saved deployment-checkpoint configuration file records a Transformers library version (5.16.1) from a Kaggle-trained pass, but this checkpoint is a separate training pass from the Phase 3B research runs discussed in this paper and is not confirmed to be the identical notebook session. These gaps are disclosed here rather than omitted or guessed; full detail is in the project's reproducibility manifest (not a manuscript section).

### 10.7 Statistical protocol history

The original Phase 3A significance analysis used 2,000 bootstrap iterations; the original Phase 3B significance analysis and this paper's own human-adjudicated-reference statistical re-evaluation (Section 6.3, Section 7.6) both use a standardized 10,000-iteration protocol (bootstrap and permutation alike), under the same seed (42). This difference in historical iteration count is noted for completeness and is not treated anywhere in this paper as an explanation for the significance-status changes reported in Section 7.6/9.2; none of the four originally-significant comparisons discussed in this paper are Phase 3A comparisons, so the 2,000-vs-10,000 distinction does not directly affect those specific findings.

### 10.8 Code-switching

Only 9 genuine Arabic-English code-switched reviews were identified in the full 1,050,832-document corpus after exhaustive manual audit of all heuristically-flagged candidates (Section 3.3, Section 7.9). No quantitative code-switch model-performance conclusion is supported by this sample size, and none is drawn anywhere in this paper; the 9 examples are retained only for qualitative illustration.

### 10.9 Licensing and data release

The English primary dataset's source (UCSD/McAuley Google Local Review Dataset) has no verified public redistribution license, confirmed by direct, dated inspection of the dataset's official release page during this project. Consequently, public redistribution of the English-side raw review text, review identifiers, linked human-adjudicated annotations, and any model checkpoint trained on this data is restricted pending further clarification from the data provider (full release plan: project data-availability documentation, not a manuscript section). This is a data-**release** limitation; it does not invalidate, and is not evidence against, any experiment, metric, or statistical result reported in this paper, all of which were computed under ordinary research use of the data.

<!-- EVIDENCE TRACE: docs/known_limitations.md (all items, esp. #2, #16-#28); docs/decisions.md (D1-D19); paper/notes/REPRODUCIBILITY_MANIFEST.md/.json; paper/notes/DATA_LICENSING_AND_RELEASE.md; paper/notes/RERUN_LABELING_AUDIT.md; paper/annotation/full/README.md -->

---

## 11. Reproducibility and Data Availability

This section distinguishes four things that are easy to conflate: what can be reproduced from artifacts already preserved by this project; what is planned for public release; what will not be publicly redistributed at this time; and what historical metadata could not be recovered at all. Not every item in the first category is promised in the second — in particular, this paper does not promise public release of all research data or model checkpoints (Section 11.3).

### 11.1 Reproducibility resources

The following are preserved and available to support reproduction of this paper's analysis (though not all are planned for public release — see Section 11.3):

- **Frozen dataset splits**, group-aware (by place for Arabic, by business for English), recorded in `data/splits/frozen_v1/manifest.json` and per-pool identifier lists; cross-verified by byte-for-byte MD5 comparison against the data bundle used for Phase 3B training, confirming both phases trained on the identical frozen split.
- **The human-adjudicated reference set**, with a fixed cryptographic identity: SHA-256 `7b53ca621d237106413e27395010ad9ba2417d733b2bc5694d49749a03be53fd`, re-verified at the start of every downstream analysis script in this study.
- **Deterministic seeds** throughout: model training seed = 42 (both Phase 3A and Phase 3B); annotator presentation-order seeds = 1001, 2002, and 3003 (one per annotator, Section 4.1); adjudication presentation-order seed = 9009 (Section 4.3); human-adjudicated-reference statistical re-evaluation seed = 42, with 10,000 iterations for both the paired bootstrap confidence interval and the paired permutation test (Section 6.3).
- **Model identifiers**: `UBC-NLP/MARBERT` and `FacebookAI/xlm-roberta-base` (Hugging Face Hub checkpoint names).
- **Experimental configurations**: the full Phase 3A and Phase 3B hyperparameter records (Section 5.2).
- **Annotation and adjudication protocol documents**, including the pre-registered justification for not defaulting to majority vote (Section 4.3) and the blinding procedure's verification record.
- **Preserved row-level prediction files** for 16 of 18 candidate model/language realizations (Section 5.3, Section 6.3); the two exceptions (Arabic standalone MARBERT and XLM-R primary runs) are documented as lost, not silently omitted.
- **The statistical-analysis scripts used for this paper's own human-adjudicated re-evaluation** (Section 6.3, Section 7.6), which are preserved in full and are distinct from the historical Phase 3B significance-testing script discussed in Section 11.2 below — the former exists and was used to produce every human-adjudicated-reference statistical result in this paper; the latter, an earlier, separate script from before this paper's re-evaluation phase, is the one not preserved.

### 11.2 Known reproducibility gaps

Despite the above, several historical implementation details could not be recovered from any preserved artifact and are disclosed rather than guessed. The Python interpreter version used for either training track is not recorded anywhere in the preserved project history. The specific PyTorch and CUDA/driver versions used during Phase 3B's GPU training session are not recorded; one partial, caveated exception exists — a saved deployment-checkpoint configuration file records a Transformers library version (5.16.1) from a Kaggle-trained pass, but this checkpoint is a separate training pass from the Phase 3B research runs reported in this paper and is not confirmed to be the identical notebook session. The specific CPU model used for Phase 3A's laptop training is not recorded. Finally, the implementation script that produced the original (pre-human-adjudication) Phase 3B significance-testing output files is not preserved; those output files themselves are preserved and are cited in this paper (Section 7.6), but the code that generated them is not available for re-execution. This last gap is specific to that one historical script and does not extend to the statistical-analysis code for this paper's own human-adjudicated re-evaluation, which is fully preserved (Section 11.1).

### 11.3 Data availability and licensing

**Arabic datasets.** The primary Arabic tourism corpus (Zenodo record 17011574; Alahmadi, 2025) is distributed under a Creative Commons Attribution 4.0 International (CC-BY-4.0) license, per the official Zenodo record. The auxiliary Jordanian restaurant corpus (Zenodo record 22061934; Sammour, 2026) is likewise distributed under CC-BY-4.0, per direct verification of its official Zenodo record conducted during this project. Both datasets' derivatives may be released with attribution to their original sources, consistent with this license.

**English (McAuley Lab Google Local Reviews) source.** This project's direct review of the official McAuley Lab release pages found a citation requirement for two specific companion papers (Li, Shang, & McAuley, 2022; Yan, He, Li, Zhang, & McAuley, 2023) but did not find any explicit redistribution license or terms of use authorizing republication of the underlying review text. Accordingly, this project will not publicly redistribute the English-side raw review text or review identifiers until the permission or licensing status is clarified with the data provider. For the same reason, the human-adjudicated sentiment labels produced by this study, where keyed to English review identifiers, will also not be publicly released while this issue remains unresolved, since publishing them alongside identifiers resolvable against the source dataset would have a similar practical effect to publishing annotated raw text. English-trained model checkpoints (the Phase 3B English research models and the separate deployment checkpoint) are likewise being withheld under this project's conservative release policy pending the same clarification. We state this as **not released pending clarification**, not as a claim that such release would be legally prohibited — no such prohibition has been verified, and none is asserted here; the restriction reflects this project's own conservative policy choice in the absence of an explicit grant of redistribution rights.

**Materials planned for release.** Subject to final repository preparation at the time of publication, this project intends to make available: the project's code (preprocessing, training, evaluation, and statistical-analysis scripts); the annotation and adjudication methodology and protocol documents; the reproducibility manifest; derived aggregate statistics and result tables (as opposed to row-level data); and the Arabic-side dataset derivatives, consistent with their source licenses. No repository URL, DOI, or archive identifier is included in this draft because none currently exists; release location and identifier information will be provided together with the final publication or repository package, not promised in advance of its creation.

### 11.4 Privacy and annotation release

Consistent with Section 11.3, this paper distinguishes between aggregate annotation statistics (agreement rates, κ values, class-level disagreement rates — releasable, and already reported in full in this paper), the annotation and adjudication protocol and methodology materials (releasable), and individual English-review-linked annotation records (withheld, for the data-redistribution reason stated above, not for a separate privacy concern specific to the annotators or adjudicator — no personally identifying information about any annotator, adjudicator, or reviewer is reported or released anywhere in this project's materials).

<!-- EVIDENCE TRACE: paper/notes/REPRODUCIBILITY_MANIFEST.md; paper/notes/REPRODUCIBILITY_MANIFEST.json; paper/notes/DATA_LICENSING_AND_RELEASE.md; paper/notes/DATASET_PROVENANCE.md (Stage-4-corrected Jordan license row); paper/notes/LITERATURE_VERIFICATION.md (rows 1-4); paper/annotation/full/human_gold_757.csv (SHA-256); data/splits/frozen_v1/manifest.json; results/human_gold_evaluation/README_PROVENANCE.md -->

---

## 12. Conclusion

This paper asked whether model rankings and statistical conclusions in a bilingual sentiment-classification study are sensitive to how the evaluation reference label is constructed, using a frozen 757-review Arabic-English test slice as a concrete setting. The original evaluation labels — rating-derived for English, single-pass human-annotated for Arabic — agreed with an independently constructed human-adjudicated reference set (three bilingual annotators, one blinded fourth adjudicator for every non-unanimous case) on 82.6% of reviews, a substantial but clearly imperfect level of agreement. Disagreement was not spread evenly across classes: it was concentrated overwhelmingly in reviews originally labeled Neutral, the large majority of which were revised to Positive or Negative under independent adjudication.

Re-evaluating sixteen previously-trained, unretrained model realizations against this reference set changed more than a single aggregate number. Per-class performance shifted, most sharply for Neutral. Model rankings shifted as well, substantially for the Arabic evaluation condition and only modestly for English. And the statistical picture changed in a way that is, on its own, this paper's clearest single result: of four pairwise model comparisons found significant under the original evaluation labels, three no longer reached significance under the human-adjudicated reference set, one survived, and one comparison that had not been significant under the original labels became significant under the reference set. A significance result, in other words, was not a fixed property of the two models being compared alone; it also depended on which evaluation reference the comparison was computed against.

The secondary findings reported alongside this central result became more nuanced, not simpler, once re-evaluated: multilingual joint training remained statistically indistinguishable from monolingual training under both evaluation references, and several zero-shot cross-lingual transfer gaps that appeared statistically robust under the original labels did not survive re-evaluation against the reference set, though zero-shot realizations remained numerically among the weakest in most rankings regardless. Neither finding is read as establishing equivalence between the models or settings compared; both are read as evidence that the original significance pattern was, in part, a property of the original labels.

Taken together, these results support treating the construction and reliability of the evaluation reference as a first-class part of experimental design in sentiment-classification research — something to measure and report alongside model architecture and training configuration — rather than as a fixed background assumption. This is offered as a conclusion scoped to the present study: one bilingual review-sentiment dataset, one annotation design, two training configurations. It is not offered as a claim that human adjudication recovers the "true" sentiment of a review, that the original labels were simply wrong, that one language is inherently harder to classify than the other, that any one model architecture is universally superior, or that this study's specific findings generalize to rating-derived sentiment datasets in general.

Looking ahead, the limitations disclosed throughout this paper (Section 10) point to concrete, bounded next steps rather than a general call for more data: independently replicating the adjudication stage with a second blinded adjudicator on a subsample of the disagreement cases, and extending evaluation-reference auditing of this kind to other multilingual sentiment-classification settings where rating-derived or single-pass-annotated labels are currently treated as a fixed evaluation reference.

<!-- EVIDENCE TRACE: Sections 4, 7, 9, 10 of this manuscript; results/human_gold_evaluation/statistical_tests_human_gold.csv; results/human_gold_evaluation/label_agreement_overall_by_language.json -->

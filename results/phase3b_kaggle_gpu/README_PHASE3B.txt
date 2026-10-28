PHASE 3B — FINAL GPU EXPERIMENT PACKAGE

Project:
Arabic-English Google Reviews Sentiment Analysis

Metric:
Macro-F1

Arabic Primary Results:
- MARBERT Full FT + Weighted: 0.785025
- XLM-R Multilingual: 0.767865
- XLM-R Full FT + Weighted: 0.740295
- TF-IDF + Logistic Regression: 0.705000
- English→Arabic Zero-shot: 0.679992
- XLM-R + LoRA Laptop: 0.623300

Arabic Reproducibility Reruns:
- MARBERT: 0.765263
- XLM-R: 0.740126

English Primary Results:
- XLM-R Multilingual: 0.739722
- XLM-R Full FT + Weighted: 0.727644
- TF-IDF + Logistic Regression: 0.687000
- Arabic→English Zero-shot: 0.680415

Statistical testing:
- 10,000 paired bootstrap samples
- Seed = 42
- Metric = Macro-F1
- Holm-Bonferroni correction
- alpha = 0.05

IMPORTANT:
MARBERT paired statistical tests use the reproducibility rerun
predictions (Macro-F1 = 0.765263), NOT the original primary
MARBERT run (Macro-F1 = 0.785025).

Arabic significant after Holm:
- XLM-R Standalone rerun > EN→AR Zero-shot
- MARBERT rerun > EN→AR Zero-shot
- XLM-R Multilingual > EN→AR Zero-shot

English significant after Holm:
- XLM-R Multilingual > AR→EN Zero-shot

Do not interpret non-significant numerical differences as
statistically significant superiority.

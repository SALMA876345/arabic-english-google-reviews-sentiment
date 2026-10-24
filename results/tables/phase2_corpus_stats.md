# Phase 2 Corpus Statistics (real, computed from downloaded data)

```
Arabic raw:                 12,214
Arabic usable:              12,189

English raw:                1,993,624
English usable:             1,038,643

Arabic-English mixed:       109

Positive:                    80.7%
Neutral:                     6.8%
Negative:                    12.4%

Human labels:                0.4%
Rating-derived:              98.8%
LLM weak labels:             0.8%

Duplicates removed:         132,317
```

## Per-source breakdown

- Arabic tourism (Zenodo 17011574): raw=3543, usable=3525, dropped (no derivable label)=6, dedup_removed=12, label_source=human_annotated (kappa=0.87)
- Jordan restaurant (Zenodo 22061934): raw=8671, usable=8664, dedup_removed=6, label_source=300 human_annotated (gold) + 8364 llm_weak_label. **No Neutral class exists in this source** (binary Positive/Negative only, confirmed by direct inspection).
- English UCSD/McAuley (Wyoming+Vermont subset): raw_lines=1993624, usable (non-null text + rating)=1170942, after_dedup=1038643, dedup_removed=132299, label_source=rating_derived (1-2=Neg,3=Neu,4-5=Pos), **not human-validated against a gold sample in this pass -- see known_limitations.md**

## Script-group distribution (CMI-style heuristic, methodology_plan.md S4-5)

                        count
script_group                 
english_only          1028776
arabic_only             11903
ambiguous_short         10044
mixed_arabic_english      109

## Sentiment class distribution (combined corpus)

            pct
sentiment      
Positive   80.7
Negative   12.4
Neutral     6.8

## Label-source distribution (combined corpus)

                  pct
label_source         
rating_derived   98.8
llm_weak_label    0.8
human_annotated   0.4

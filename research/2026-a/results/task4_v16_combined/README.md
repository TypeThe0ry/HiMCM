# Cumulative school-travel evidence: conditional V16 comparison

The combined calculation changes exactly two travel-utility cells. Mexico City uses official2020 microdata with uncertain school-stage membership retained; São Paulo uses the2023 current-high-school cohort with the exploratory household sampling envelope. Other V7 inputs and weights stay fixed. This makes the cumulative effect reproducible instead of leaving each new city isolated in its own comparison.

| Scenario | São Paulo rank | Mexico City rank | Phoenix rank | Mean score width | Possible champions |
| --- | ---: | ---: | ---: | ---: | ---: |
| V7 baseline | 14 | 21 | 24 | 38.0831 | 25 |
| Mexico2020 only | 14 | 20 | 24 | 38.0822 | 25 |
| Combined, Mexico age3–17 | 6 | 20 | 24 | 37.8657 | 25 |
| Combined, Mexico all-age alternative | 6 | 21 | 24 | 37.8721 | 25 |

The default combined case changes11 decision ranks; Kendall tau versus V7 is0.94. Mean score-interval width decreases about0.57%. Singapore remains the minimax-regret choice and its worst regret stays28.1736. New information changes intermediate decisions and local uncertainty; it has not improved the final minimax bound or reduced the possible-champion set. All25 cities also remain possible over continuous auxiliary weights alpha=[.05,.2].

## Source conditions remain part of the result

- Mexico's2020 interval replaces the2015 value. Its new upper endpoint0.554445 exceeds the old0.544893, so intersecting years would create unsupported precision. The school stage is reconstructed from current attendance and completed grade, with unknown-stage current attenders retained. Unknown attendance and reconstruction errors are not fully identified.
- São Paulo's2023 cohort directly identifies current high-school enrollment, includes all ages, and uses a public research mirror. Official byte identity is still unverified, and its household resampling envelope is exploratory.
- Mexico's default age3–17 and São Paulo's all-age high-school cohort are not perfectly harmonized. The all-age Mexico alternative is reported separately and retains its different decision rank.
- Combining intervals does not grant global source admission or create a simultaneous confidence interval. Original historical outputs and source flags are preserved. `source_inputs.json` records the exact derived-input hashes and conditions. Withdrawing the São Paulo mirror corresponds to the Mexico-only row.

## What additional evidence could exclude a candidate?

The acquisition calculation fixes all rival lower bounds, considers only measurements of the candidate city, and enumerates subsets of its uncertain indicators. It asks whether the most favorable permissible exact outcomes for exclusion could rule that city out **for every alpha in[.05,.2]**. This is a necessary best-case count, not a predicted outcome, field-cost estimate or guaranteed elimination. Real collection can return intervals and require more evidence; collecting information about rivals can change the answer.

| Candidate | Minimum exact indicators, fixed alpha=.1 | Minimum over continuous preference range |
| --- | ---: | ---: |
| Phoenix | 4 | 4 |
| Mexico City | 3 | 4 |
| São Paulo | 3 | 4 |
| Istanbul | 1 | 2 |

None of these minimum counts decreased after the combined update. São Paulo has12 minimal four-cell bundles instead of the former15 because its improved travel lower bound rules out some formerly conceivable very poor outcomes. `minimal_bundles.csv` lists all combinations; these hypothetical outcomes are never inserted as observations. Singapore has no city-local exclusion bundle within the current bounds, which does not make it a guaranteed champion: rival evidence could still change its comparison.

For a candidate i and measured subset B, define u_i^B to equal its current lower utility on B and upper utility otherwise. The diagnostic is:

    k_i = min |B| such that for every alpha in[.05,.2],
          S_i(u_i^B,w(alpha)) < max(k != i) S_k(lower_k,w(alpha)).

The existing continuous polynomial feasibility solver tests the preference range; this is not a three-weight grid approximation. The score is S=100 sqrt(sum(w*u²))/(sqrt(sum(w*u²))+sqrt(sum(w*(1-u)²))). Weights are (1-alpha)/8 for each main criterion and alpha/2 for each auxiliary criterion. Possible champions satisfy U_i>=max(k!=i)L_k; decision ranks order max(0,max(k!=i)U_k-L_i).

## Validation and next source

An independent agent recomputed the score and regret formulas directly and matched all25 combined decision ranks, both changed cells, mean width, Kendall tau and possible-champion counts. The script verifies the exact two-cell change and that a continuous-preference acquisition minimum cannot be smaller than its fixed-preference counterpart. Existing V8 acquisition baselines use the unchanged V7 source matrix; the preceding admission regression already checked all250 endpoints against it.

Istanbul was investigated because its necessary acquisition size is lower. The current IBB household-survey page and CKAN API timed out. The B40 page only links to IBB and is not a downloadable microdata mirror. Current high-school stage, travel duration and survey weights therefore remain unverified; no Istanbul observation was added. Exact resource leads are archived at `../../data/task4_v16_istanbul/source_leads.json`.

```sh
python3 research/2026-a/scripts/task4_combined_evidence.py
```

# V125: method sensitivity migrated to V124 evidence

On V124's 16-city evidence, fixed-weight midpoint TOPSIS selects Zurich while classic midpoint VIKOR selects Dublin. Their Kendall tau-b is 0.5000, compared with 0.4833 on V121. Under equal weights, Oslo has the smallest VIKOR Q but fails both classical acceptance conditions. The primary interval model continues to recommend Zurich and retains 16 possible champions.

| Evidence / weights | Midpoint TOPSIS first | Minimum VIKOR Q | TOPSIS–VIKOR tau-b | Single VIKOR compromise accepted? |
|---|---|---|---:|---|
| V121 fixed control | Zurich | Dublin | 0.483333 | Yes |
| V124 fixed | Zurich | Dublin | 0.500000 | Yes |
| V121 equal control | Zurich | Oslo | 0.766667 | No |
| V124 equal | Zurich | Oslo | 0.750000 | No |

For V124 fixed weights, the first/second Q gap is 0.21320297, exceeding `1/(16−1)=0.06666667`, and Dublin satisfies stability. Under equal weights the gap is 0.03969924, below the threshold, and Oslo is neither S-minimal nor R-minimal. Minimum Q alone therefore does not establish an accepted unique compromise.

The comparison keeps each evidence arm's same midpoint utilities and weights. TOPSIS uses fixed 0/1 ideals; classic VIKOR uses sample best/worst utilities and equally weights normalized total and maximum weighted shortfall (`v=0.5`). Midpoints are declared, unobserved scenarios. They do not replace missing measurements or the interval minimax recommendation.

## What changed from V121

Only V124's admitted Madrid transport and Tokyo pool lower bounds change the utility inputs. Fixed-weight midpoint TOPSIS ranks are unchanged; two fixed-weight VIKOR ranks change (before/after tau-b 0.983333). Equal-weight midpoint TOPSIS changes two ranks (tau-b 0.983333), while equal-weight VIKOR ranks are unchanged. The primary interval decision ranks remain unchanged in both references.

[method_ranks.csv](method_ranks.csv), [method_components.csv](method_components.csv) and [method_utility_inputs.csv](method_utility_inputs.csv) preserve V121 control and V124 current arms. Every V121 rank/score component is reconciled with the frozen V122 output; the old V122 analysis remains on V121.

## Historical cases remain independent and unchanged

The main sample still has 16 different countries and no within-country pair. Six case/coverage CSV files are byte-identical to the V122 archive and are independently regenerated to verify numerical equality:

- United States and India comparisons retain the separate historical 25-city V117 bounds and fixed weights. Neither pair identifies a necessary overall winner.
- Shanghai retains its 2025 school-location district resource case: pooled utility 0.60448141, pupil-weighted district mean 0.60326691 and fractional bottom-20% pupil-mass utility 0.58095358. District-homogeneous resource exposure is not individual or resident accessibility.
- Istanbul retains 2012 broad age groups and overlapping marginal travel-utility bounds; shared unknown-age mass prevents assuming jointly attainable extrema.
- Singapore retains 2020 start-of-year secondary-enrolment ages and counts. These do not supply measured age-specific preferences or a matching Census resident-travel denominator.

Original case labels and scope statements are preserved verbatim, including their former V121 separation label. The cases remain separate from both V121 and current V124; none supplies new rows or cells to the main 16-city ranking. [summary.json](summary.json) records their original versions and frozen file hashes.

## Reproduction and checks

```sh
python research/2026-a/scripts/task4_v125_method_country.py
```

The script reuses the earlier pure method/case functions and adds direct vector-norm TOPSIS, independent relative-shortfall VIKOR and acceptance-condition checks in all four method arms. It verifies V121 control alignment, byte/numeric equality of six historical files, current V124 bounds, original CSV, registry and frozen old-result hashes. [audit.json](audit.json) records successful checks. No historical output, main model, input or manuscript was edited.

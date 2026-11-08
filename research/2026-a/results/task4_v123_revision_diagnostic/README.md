# A controlled model revision that preserves uncertain evidence

Retaining V121's 48 non-point-identified utility cells separates a conservative recommendation from evidence that identifies the best city. On the same 16 cities, weights, anchors and TOPSIS formula, an explicit midpoint completion and the interval model both recommend Zurich. Their decision orders differ for 13 cities under fixed weights, and the retained rectangular model admits a completion in which Dublin beats Zurich. The revision changes the treatment of uncertainty and the decision rule rather than adding another city-quality score.

| Controlled formulation | Midpoint scenario | Retained-interval decision |
|---|---|---|
| Utility input | `z=(lower+upper)/2` | Original V121 `[lower,upper]` |
| Information represented | One chosen completion | 112 point cells, 27 partial intervals, 21 fully missing intervals |
| Criterion weights and anchors | Unchanged | Unchanged |
| TOPSIS distances | Weights enter squared distances once | Same formula |
| Decision | Highest score within that completion | Minimum worst-case regret over the rectangle |
| Fixed-weight first choice | Zurich | Zurich |
| What the first choice establishes | First in the declared scenario | Conservative recommendation; 16 cities remain possible champions |

This is a controlled formulation comparison built for model diagnosis. It does not claim that the team previously used the midpoint formulation as its historical initial model. Midpoints and witnesses are declared scenarios, not newly admitted data or estimates replacing missing measurements. The authoritative evidence and ranking remain V121.

## The same recommendation can express different evidence

For utility completion `z`, keep the existing score

`Dminus=sqrt(sum(w*z²)); Dplus=sqrt(sum(w*(1-z)²)); S=100*Dminus/(Dminus+Dplus)`.

Collapsing the intervals to `z=(lower+upper)/2` gives a conditional point order. The revised representation keeps `L=S(lower)` and `U=S(upper)`, then uses

`R_i=max(0,max_{k!=i} U_k-L_i)` and `choice=argmin_i R_i`.

The possible-champion condition is `U_i>=max_{k!=i}L_k`; necessity requires `L_i>=max_{k!=i}U_k`. Competitor maxima exclude the focal city itself.

| City | Fixed-weight midpoint rank | Interval decision rank |
|---|---:|---:|
| Zurich | 1 | 1 |
| Dublin | 2 | 6 |
| Helsinki | 3 | 8 |
| Paris | 4 | 9 |
| Oslo | 5 | 3 |
| Singapore | 7 | 2 |
| Stockholm | 8 | 4 |
| Prague | 9 | 5 |

Fixed weights change 13 of the 16 decision ranks, with Kendall tau-b 0.6000. Equal weights change 15 ranks, with tau-b 0.6667; Zurich remains the first choice in both formulations. Full results, including all city score bounds and regret values, are in [rank_comparison.csv](rank_comparison.csv).

At the midpoint, Zurich scores 64.35258 and its regret in the collapsed point model is zero. Once the evidence intervals are retained, its score range is [53.53548,72.18379] and its maximum regret is 17.36805. This is the risk exposed by the richer uncertainty representation; the change does not represent newly observed city performance.

## A reproducible counterexample to a certain-champion claim

The model's closed rectangular set permits a full endpoint completion that places Dublin at its upper utility endpoints and every other city at its lower endpoints. Under fixed weights:

- Dublin scores 70.90353 and is strictly first.
- Zurich scores 53.53548.
- Their difference is 17.36805, exactly Zurich's independently recomputed maximum regret.

The construction demonstrates why being first at the midpoint does not certify a necessary champion. It also witnesses the meaning of the regret bound rather than using a second ranking model. Some endpoints are closures or suprema of raw measurements, so this endpoint completion establishes a statement about the declared utility rectangle, not an observed or physically reconstructed city population.

A separate counterexample stays strictly inside every one of the 48 uncertain intervals. Keep all other cities at their midpoints and set Zurich's uncertain utilities to `lower+0.1*(upper-lower)`, retaining all 112 point values. Dublin then scores 62.31483, Zurich scores 55.54326, and Zurich is thirteenth in that completion. Thus the result does not depend on attaining exact boundary utilities. The same construction under equal weights gives Dublin 61.45870 and Zurich 56.61347, with Zurich tenth. Interior membership remains a model-feasibility statement, not proof of joint attainability under unmodelled raw-data constraints.

[witness_utilities.csv](witness_utilities.csv) saves every utility in the midpoint, full endpoint and strict-interior completions; [witness_scores.csv](witness_scores.csv) saves all city scores and scenario ranks. Every witness preserves point-identified cells and lies within the original intervals.

For each of the 16 cities, setting that city to its upper endpoint and all others to their lower endpoints also gives a strictly winning model completion under both weight references. The 32 constructive checks are in [possible_champion_witnesses.csv](possible_champion_witnesses.csv). Consequently, the necessary-champion set under the rectangle is empty even though a conservative action can still be selected.

## What this revision contributes

The controlled comparison supports a specific change within one TOPSIS framework: retain the evidence bounds instead of treating one completion as all available information, then select an action using self-excluded maximum regret. The evidence for the change is constructive: a completion consistent with the retained model reverses the midpoint winner, the computed regret is realized by a model endpoint witness, and the revised report preserves all cities that remain possible champions.

The experiment isolates this modelling change by holding all evidence, weights, anchors and score equations fixed. The fifteen earlier data supplements are a separate evidence improvement; they are not counted as the mechanism of this comparison. No accuracy gain, sampling coverage, future forecast or representative student preference is inferred here. The score intervals remain conditional on V121's mixed-vintage proxies and the retained rectangular uncertainty set.

## Reproduction and audit

Run from the repository root:

```sh
python research/2026-a/scripts/task4_v123_revision_diagnostic.py
```

The script uses only `task4_user_v121_revision.revised_bounds()` as its city evidence input. Independent vector norms and explicit competitor loops reproduce the production TOPSIS scores, maximum regrets, ranks and champion sets, and agree with the saved V121 rankings. It verifies endpoint membership, strict interior membership, unchanged point values, all possible-champion witnesses and equality between the adverse endpoint gap and the revised choice's maximum regret.

[utility_inputs.csv](utility_inputs.csv) contains the frozen 160 bounds and diagnostic midpoints. [summary.json](summary.json) records full numerical comparisons and source hashes; [audit.json](audit.json) records the checks. The original CSV hash, registry, V121 saved outputs and all 160 source bounds remain unchanged. No legacy 25-city model or manuscript file is used or modified.

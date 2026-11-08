# V125: controlled uncertainty-revision diagnosis on V124

Preserving V124's 48 uncertain utility cells distinguishes a conservative action from a certain-champion claim. At fixed weights, both an explicit midpoint scenario and the retained-interval minimax model recommend Zurich, but their orders differ for 13 cities (Kendall tau-b 0.6000). Under equal weights 15 ranks differ, with tau-b 0.6500. Both interval references retain 16 possible champions and no necessary champion.

This is a controlled formulation comparison using the same V124 evidence, weights, anchors and TOPSIS score. It does not assert that a midpoint model was the team's historical initial method. The model change being diagnosed is the retention of evidence bounds and replacement of conditional point-score ordering with a conservative maximum-regret decision.

## Updated evidence, controlled mechanism

| Quantity | V121 control (frozen V123) | V124 current (V125) |
|---|---|---|
| Point / partial / fully missing cells | 112 / 27 / 21 | 112 / 29 / 19 |
| Fixed midpoint-vs-interval changed ranks | 13 | 13 |
| Fixed diagnostic tau-b | 0.6000 | 0.6000 |
| Equal midpoint-vs-interval changed ranks | 15 | 15 |
| Equal diagnostic tau-b | 0.6667 | 0.6500 |
| Midpoint first / interval recommendation | Zurich / Zurich | Zurich / Zurich |
| Possible / necessary champions, either reference | 16 / 0 | 16 / 0 |

V124's two new facility lower bounds leave all primary interval decision ranks unchanged. Fixed-weight midpoint ranks also remain unchanged; equal-weight midpoint ranks change for two cities. That is why the equal-weight diagnostic tau changes even though its count of differing ranks remains 15. [summary.json](summary.json) records the controlled evidence comparison. The V121 control reproduces every column of the old V123 rank comparison, saved byte-identically as [v121_control_rank_comparison.csv](v121_control_rank_comparison.csv).

## A constructive reason to retain the intervals

The score remains

`S(z)=100*sqrt(sum(w*z²))/(sqrt(sum(w*z²))+sqrt(sum(w*(1-z)²)))`.

The point comparator uses `z=(lower+upper)/2`. The interval formulation retains `L=S(lower)`, `U=S(upper)` and `R_i=max(0,max_{k!=i}U_k−L_i)`, then recommends minimum R. It preserves 112 point values and all 48 non-point bounds; the maxima exclude the focal city itself.

At fixed weights Zurich's midpoint score is 64.35258. A full endpoint completion puts Dublin at its upper endpoints and every other city at its lower endpoints. Dublin then scores 70.90353 and Zurich 53.53548. The gap, 17.36805, exactly realizes Zurich's maximum regret. Thus midpoint first place does not certify a necessary champion under the retained rectangle.

The strict-interior witness keeps all other cities at their midpoints and sets Zurich's uncertain cells to `lower+0.1*(upper−lower)`. All 48 uncertain utilities are strictly inside their V124 bounds. Dublin scores 62.31483, Zurich 55.54326, and Zurich is thirteenth. Equal weights give Dublin 61.45870, Zurich 56.61347 and Zurich tenth. The key Dublin/Zurich scores match the V121 examples because V124 supplements different cities; all underlying witness utilities are recomputed on V124, including the Madrid and Tokyo updates.

Endpoint utility 1 can be a closure/supremum for raw resources or travel moments. The endpoint witness therefore establishes model feasibility, not a physically reconstructed city population. The strict-interior witness removes dependence on exact boundary values, while retaining the same model-feasibility interpretation. Neither is a new observation or a missing-value estimate.

Every city also has a strictly winning rectangular-model completion obtained by taking its upper endpoint and every competitor's lower endpoint. The 32 fixed/equal constructive checks in [possible_champion_witnesses.csv](possible_champion_witnesses.csv) support the model's 16-city possible set and empty necessary set.

## Files and validation

```sh
python research/2026-a/scripts/task4_v125_revision_diagnostic.py
```

[rank_comparison.csv](rank_comparison.csv) retains the old schema for all 32 city/reference comparisons. [utility_inputs.csv](utility_inputs.csv) saves V124's 160 input bounds; [witness_utilities.csv](witness_utilities.csv) saves 960 completion coordinates and [witness_scores.csv](witness_scores.csv) saves all 96 completion scores/ranks. The summary retains the compatible `results` field plus explicit V121-control and V121→V124 comparisons.

Pure norm/self-excluded-regret functions from V123 are reused and checked against production calculations and current saved V124 ranks. [audit.json](audit.json) records endpoint/interior membership, all point-value protection, possible/necessary sets, regret realization, old-control alignment and source hashes. V124's original CSV, registry, saved ranks, all 160 bounds and frozen V123 outputs remain unchanged. The diagnostic contains no legacy 25-city data and does not edit manuscript files.

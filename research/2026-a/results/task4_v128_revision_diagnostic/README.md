# V128: uncertainty-revision diagnosis migrated to V127

On V127's same 160-cell matrix, midpoint ordering and interval minimax decision both select Zurich, but fixed-weight orders differ for 13 cities with Kendall tau-b 0.583333. Equal-weight orders differ for 15 cities with tau-b 0.650000. The interval model retains 16 possible champions and no necessary champion. Explicit endpoint and strict-interior completions still demonstrate why midpoint first place does not certify a certain champion.

This is a controlled comparison of uncertainty representations and decision rules within the same TOPSIS score. It does not claim that the team historically used the midpoint comparator as its initial method. Chosen completions are model scenarios, not newly admitted observations.

## Actual migration differences

| Comparison | V121 / frozen V123 | V124 / frozen V125 | V127 / V128 |
|---|---:|---:|---:|
| Fixed midpoint-vs-interval changed ranks | 13 | 13 | 13 |
| Fixed diagnostic tau-b | 0.600000 | 0.600000 | 0.583333 |
| Equal changed ranks | 15 | 15 | 15 |
| Equal diagnostic tau-b | 0.666667 | 0.650000 | 0.650000 |
| Point / partial / fully missing cells | 112/27/21 | 112/29/19 | 112/31/17 |

Relative to V125, midpoint ranks are unchanged under both references. Two fixed-weight primary decision ranks change, while equal-weight primary ranks do not. That changes the fixed-weight tau even though its count of differing ranks remains 13. Fixed/equal mean score widths change from 16.15002092/19.02662147 to 16.10728557/18.94657608; Zurich remains the conservative choice. The new evidence changes lower utility bounds while retaining all upper bounds and the same score formula.

V121→V127 includes four admitted lower-bound additions. Direct input comparison with frozen V125 verifies that the incremental V124→V127 changes are exactly Prague and Vienna transport. [v125_v128_rank_comparison.csv](v125_v128_rank_comparison.csv) preserves the actual city-level comparison; `controlled_V125_V128` in [summary.json](summary.json) preserves its summaries. The V121 control reproduces every earlier V123 rank column and is saved byte-identically in [v121_control_rank_comparison.csv](v121_control_rank_comparison.csv).

## Constructive witnesses on current bounds

Both formulations retain the original weights, anchors and score

`S(z)=100*sqrt(sum(w*z²))/(sqrt(sum(w*z²))+sqrt(sum(w*(1−z)²)))`.

The midpoint comparator sets `z=(lower+upper)/2`. The interval formulation retains `L=S(lower)`, `U=S(upper)` and `R_i=max(0,max_{k!=i}U_k−L_i)`. The competitor maximum excludes the focal city.

Under fixed weights, the endpoint completion with Dublin at its upper utility endpoints and every other city at its lower endpoints gives Dublin 70.90353 and Zurich 53.53548. Their 17.36805 gap realizes Zurich's maximum regret. A strict-interior completion instead keeps every other city at its midpoint and sets Zurich's uncertain cells to `lower+0.1*(upper−lower)`: Dublin scores 62.31483, Zurich 55.54326, and Zurich is thirteenth. Equal weights give Dublin 61.45870, Zurich 56.61347 and Zurich tenth.

These key two-city scores are unchanged from V125 because the new primary lower bounds concern other cities. Every witness utility is nevertheless regenerated within V127, including the Prague/Vienna additions. All 112 point cells are retained exactly; all 48 non-point utilities in the interior witness lie strictly between their bounds.

Endpoints can be closures/suprema for raw measurements. Endpoint feasibility concerns the declared rectangular model, not a reconstructed population. The interior witness avoids reliance on exact boundaries while retaining that model-feasibility interpretation. Neither witness estimates missing measurements or establishes raw-data joint attainability.

Every city also has a strictly winning rectangular completion obtained by taking its own upper endpoints and all competitors' lower endpoints. The 32 fixed/equal constructions in [possible_champion_witnesses.csv](possible_champion_witnesses.csv) verify 16 possible and zero necessary champions under this model.

## Files and validation

```sh
python research/2026-a/scripts/task4_v128_revision_diagnostic.py
```

The fixed V127 snapshot SHA256 is `8f754bb3b666fdea8030bacf0551dea8a455bb0fc22df56c1860d4f4e747e45d`. The script checks that receipt and all its primary-source hashes before and after execution. It reuses the earlier pure norm/self-excluded formulas, reconciles current production/saved primary ranks, and checks the V121 control, endpoint membership, strict interior membership, all point cells, champion constructions and regret realization. [audit.json](audit.json) records success.

The compatible current `results` and rank/witness CSV schemas are retained; explicit control and intermediate-evidence comparison fields are added. V127's original CSV, registry, snapshot and all 160 bounds remain unchanged, as do V121/V124 and old extension outputs. No legacy 25-city case enters this diagnosis and no manuscript file was edited.

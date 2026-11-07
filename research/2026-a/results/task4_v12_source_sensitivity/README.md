# Source sensitivity: how much unmodeled mass changes the recommendation

São Paulo remains decision rank 6 until an additional unrepresented population share exceeds 15.4172%, or an adversarially contaminated observed-utility share exceeds 10.6906%, under the two distinct models below. These are sensitivity thresholds, not measured error rates or probabilities that a source is authentic. They use the municipal exploratory sampling interval [0.4370715213,0.6114325152]. All other cities and criteria retain their V7 bounds. Weights are fixed at alpha=0.1: eight main criteria receive 0.1125 each and two auxiliary criteria receive 0.05 each. Thresholds have not been certified uniformly over other weights.

## Two different mixture assumptions

Let [l,h] denote the existing source utility interval and v an unrestricted utility in [0,1]. The share e is a fraction of distributional/weighted mass, not necessarily a fraction of records.

1. **Unrepresented population share:** true mean=(1-e)*source mean+e*v. Its sharp mean interval is [(1-e)*l,(1-e)*h+e]. This tests added population not represented by the source; it does not describe corrupted observations.
2. **Contaminated observed distribution:** observed mean=(1-e)*clean mean+e*v. For e<1, invert to [max(0,(l-e)/(1-e)),min(1,h/(1-e))]; at e=1 the interval is [0,1]. This tests a specific adversarial contamination model, not arbitrary errors in all survey variables.

Both envelopes nest the original interval and expand with e. The source already retains students with missing journeys; e is an additional sensitivity assumption, not another estimate of those same missing students. The original bootstrap interval is exploratory, so neither extension establishes a confidence level. Main admission remains false.

## Complete municipal decision-rank transitions

Equality is a competition-rank tie. The listed worse rank applies immediately above the threshold.

| Rank immediately after threshold | Unrepresented share | Contaminated observed share | Rival overtaking São Paulo |
| --- | ---: | ---: | --- |
| 7 | 15.4172% | 10.6906% | Barcelona |
| 8 | 18.7635% | 12.7159% | Toronto |
| 9 | 22.5011% | 14.8722% | Istanbul |
| 10 | 34.0227% | 20.8961% | Bogota |
| 11 | 36.9848% | 22.3095% | Dubai |
| 12 | 39.3949% | 23.4228% | Warsaw |
| 13 | 52.2075% | 28.8434% | Cape Town |
| 14 | 57.8265% | 30.9859% | Santiago |

## Why the threshold search is complete

The score is coordinatewise increasing: S=100 sqrt(B)/(sqrt(A)+sqrt(B)), B=sum(w*u²), A=sum(w*(1-u)²). São Paulo lower score decreases as its travel lower utility decreases. Even at e=1, its upper score (70.7928) is below the second-highest other upper score (76.4028). Thus changing its travel interval cannot change any rival maximum regret. Its own regret is R_SP(e)=max(other U)-L_SP(e), which is nondecreasing. Solving its equality with each fixed rival regret yields all rank transitions; no Monte Carlo rank-frequency assumption or coarse share grid is needed for the transition search. In the contamination case clipping eventually creates a constant tail, but no rival regret equals that tail in these inputs.

The 25 possible champions at e=0 remain possible throughout [0,1]: the uncertainty sets only expand. This is a mathematical nesting result, also checked on 101 shares per scope and mixture direction. It is not evidence that every city is equally good. The metro alternative has first-loss thresholds 18.1738% (unrepresented) and 13.0266% (contamination).

## Validation and use

The implementation checks the constant-rival prerequisite, root residuals, full-model regret/rank consistency on 101 shares for each of four scenarios, and original-baseline recovery at e=1. An independent agent reproduced all eight municipal coverage thresholds. Additional checks verified 1,260 generated contamination inversions and independently converted all 16 coverage thresholds to contamination thresholds algebraically. Files summary.json and rank_scenarios.csv contain the complete intervals and 25-city snapshots.

This changes the question from “trust the mirror or discard it?” to “what explicitly modeled source deviation would change this recommendation?” It does not assign a trusted share without evidence or tighten missing intervals to manufacture a winner. Bogotá2023 acquisition still failed; the newly archived2019 questionnaire does not identify current grade, so no Bogotá high-school observation was admitted.

Reproduce from the research repository:

```sh
python3 research/2026-a/scripts/task4_source_sensitivity.py
```

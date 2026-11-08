# How far can Istanbul-only data collection reduce the champion set?

Within the existing V114 utility bounds, collecting data only for Istanbul can reduce the possible-champion set by at most one city, from 25 to 24. If its travel interval stays `[0,1]`, the set remains 25 even when every other uncertain Istanbul indicator is resolved at its least favorable endpoint. These are mathematical endpoint certificates, not new observations or forecasts of data collection.

| Fixed weight vector | Lowest Istanbul score upper bound with travel unresolved | Highest rival score lower bound | Highest attainable Istanbul score lower bound | Lowest rival score upper bound |
|---|---:|---:|---:|---:|
| Inherited: eight main indicators 0.1125 each, two facilities 0.05 each | 44.632626 | 43.538541 | 55.341830 | 60.642476 |
| Equal: ten indicators 0.1 each | 44.122693 | 42.846609 | 58.733606 | 63.059018 |

The fixed-ideal weighted TOPSIS score is

`C(z) = 100 sqrt(Σ w_j z_j²) / [sqrt(Σ w_j z_j²) + sqrt(Σ w_j (1−z_j)²)]`.

For positive fixed weights and utilities in `[0,1]`, increasing any utility cannot decrease the score: distance from the worst point increases and distance from the best point decreases. A city can be champion under the independent interval model exactly when its upper score is at least every rival's lower score.

First, leave travel at `[0,1]` and set every other Istanbul utility exactly to its existing lower endpoint. This minimizes its attainable score upper bound over all such nested refinements. The resulting upper bound still exceeds Singapore's lower bound, which is the largest rival lower bound. Istanbul therefore remains possible under every legal refinement that leaves travel unresolved.

Second, even setting all Istanbul utilities exactly to their upper endpoints cannot raise its score lower bound above the original upper score. That maximum is below every other city's current upper score. Since all 24 rivals were possible before, no Istanbul-only nested refinement can exclude any of them. The only city that could be excluded is Istanbul itself. Setting all of its utilities, including travel, to their lower endpoints does exclude it mathematically, so 24 is attainable within the independent closed-box model. This does not predict what future evidence will show.

The certificate fixes all other cities' cells, all utility transformations and each of the two weight vectors separately. It does **not** apply automatically to arbitrary preferences, Monte Carlo weight draws, widened or shifted bounds, or changes to other cities. It concerns possible champions, not minimax-regret decision ranks.

Reproduce from the repository root with `python3 research/2026-a/scripts/task4_istanbul_acquisition_limits.py`. The script asserts the inequalities, the original 25-city champion set and unchanged input matrices, and writes the numerical certificate and input hash to `summary.json`. It does not alter the model registry or any existing bounds.

# V113 champion-exclusion acquisition diagnostic

At both fixed inherited weights and the neutral equal-weight reference, observing one uncertain utility cell cannot reduce the 25-city possible-champion set, regardless of the realized value within its existing interval. This differs from earlier acquisition analyses that asked which city could become the minimum-regret recommendation.

Two monotone endpoint checks establish this conditional result: (1) reducing the target city's upper score as much as possible by exactly learning its current lower endpoint never places it below another city's existing lower score; (2) raising the target city's lower score as much as possible by exactly learning its current upper endpoint never places it above another city's existing upper score. Intermediate values cannot improve either exclusion mechanism. No observed data or intervals are changed.

The closest inherited single-cell self-exclusion is Istanbul travel: even its smallest hypothetical post-information upper score, 46.569127, remains above the best rival lower score, 43.457014. The closest benchmark-raising cell is Singapore travel: its largest hypothetical lower score is 50.963232, below the smallest rival upper score, 55.341830.

For inherited weights, Istanbul alone has a two-cell lower-endpoint exclusion bundle: travel plus homicide, public transport density, or pool density. Lagos, Mumbai, Delhi, Dhaka and Shanghai require at least three cells; 15 cities need four, three need five, and Singapore cannot be excluded through its own evidence alone while competitors remain unchanged. Equal weights require at least three cells in Istanbul, four in eight cities, and five in 15 cities; Singapore remains unexcludable by own-cell updates alone.

These counts concern *optimistic information acquisition*, not plausible observations: all selected utilities are hypothetically revealed at their existing lower endpoints. Joint endpoint attainability is not asserted. Real data can change decision ranks or narrow score intervals without excluding a possible champion. Interval-valued new evidence is weaker than the exact observations tested here.

Files:
- `single_cell_thresholds.csv`: maximal own-upper reduction and any exclusion threshold; none of the current cells has such a threshold, so threshold fields are empty.
- `single_cell_benchmark_raise.csv`: maximal lower-score rise and excluded competitors.
- `city_requirements.csv`: smallest cardinality of a hypothetical self-exclusion bundle.
- `minimum_bundles.csv`: all minimum-cardinality successful endpoint bundles.
- `summary.json`: pinned input hash and invariant declarations.
- `audit.py`, `validation.json`: independent exhaustive subset verification using a squared-distance inequality rather than the scoring function.

Reproduce from repository root:

```
python3 research/2026-a/scripts/task4_champion_exclusion_priority.py
python3 research/2026-a/results/task4_v113_exclusion_priority/audit.py
```

The model stays V108; the V112 equal-weight reference is a comparison scenario. No observations were admitted, registry updated, or manuscript modified by this analysis.

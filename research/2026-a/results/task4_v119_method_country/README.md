# Method sensitivity and within-country cases

On the same16-city V118 utility midpoints and fixed inherited weights, TOPSIS ranks Zurich first whereas classic VIKOR ranks Dublin first. Kendall tau-b is0.516667. This is a useful disagreement: the recommendation depends on the aggregation rule and its treatment of shortfalls. The midpoints are illustrative scenarios only; they do not fill missing data or replace the main interval-TOPSIS/minimax recommendation.

The weights remain0.1125 for each of eight main indicators and0.05 for each of two facility indicators. For midpoint utility z, TOPSIS uses the existing fixed ideal vectors0and1 and the existing weighted-distance convention. VIKOR uses sample maxima/minima for each indicator, as in its classic definition:

`d_ij=(max_i z_ij−z_ij)/(max_i z_ij−min_i z_ij)`

`S_i=Σ_j w_j d_ij`, `R_i=max_j(w_j d_ij)`

`Q_i=0.5(S_i−min S)/(max S−min S)+0.5(R_i−min R)/(max R−min R)`.

Lower Q is preferred. A constant criterion contributes zero shortfall; a zero S or R range contributes zero to Q. Competition ranks preserve ties. Since TOPSIS uses fixed ideals and VIKOR sample ideals, this comparison includes both the classic methods' ideal-point conventions and aggregation choices; it does not isolate aggregation alone. Agreement is not external validation of the data or proof of ranking correctness. The stored Kendall p-value is descriptive, not evidence that either model is true.

Dublin minimizes both S and R. Its Q advantage over second-place Stockholm is0.257891, exceeding the classic threshold`1/(16−1)=0.066667`; its stability condition also holds. These acceptance conditions apply only to this illustrative point scenario. Zurich is VIKOR rank8 because VIKOR penalizes its largest weighted relative shortfall more strongly; no result changes the main missingness intervals.

## What can be compared within one country?

The attachment has16countries and exactly one city per country, verified from its country column. Within-country comparisons cannot be conducted within this sample, and city effects cannot be separated from country effects. Adding a same-country narrative does not solve that sampling limitation.

Two separate cases use the existing25-city V117 bounds and the same fixed weights. Their data and results are never combined into the16-city ranking:

| Country | City A score interval | City B score interval | Identified overall winner |
|---|---|---|---|
| United States | Phoenix[31.3906,71.6809] | New York[30.2177,72.8059] | Neither |
| India | Mumbai[28.8218,60.6425] | Delhi[32.5904,63.8955] | Neither |

A is necessarily strictly better only if`lower_A > upper_B`; the reverse is checked separately. Both pairs overlap, and either city in each pair can win under its retained intervals. No overall winner is forced. Phoenix has higher cost-of-living and housing-affordability utilities than New York under the existing observations. Mumbai has the higher PM2.5 utility, while Delhi has higher cost, housing, student–teacher-resource and broadband utilities. The remaining uncertain dimensions prevent these component differences from identifying an overall winner. These are two cases, not representative estimates for all cities in either country.

`method_ranks.csv` contains both point-scenario rankings and VIKOR S/R/Q; `weights_and_ideals.csv` records weights and VIKOR sample endpoints. `country_indicator_bounds.csv` retains every original indicator interval, and `country_score_comparison.csv` reports pairwise tests. `user16_country_coverage.csv` verifies the one-city-per-country limitation. `summary.json` records scope, tests and input hashes. Reproduce with`python3 research/2026-a/scripts/task4_v119_method_country.py`. No inputs or main registry are edited.

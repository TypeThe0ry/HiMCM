# V114: Istanbul facility evidence, fixed model rules

Two verified 2025 facility subsets improve Istanbul’s minimum-regret decision rank from 15 to 7 under the inherited weights (15 to 4 under equal weights). All 25 cities remain possible champions. This is an information-driven change in a conservative decision ranking, not proof that Istanbul’s actual performance is seventh or that its conditions improved over time.

## Evidence

- IETT’s original 2025 annual report identifies 12,426 Istanbul physical stops equipped with Braille/QR signs. This is the reported actual stop count, distinct from the 7,000 target and the broader 16,134 operator inventory. It supplies a verified subset, not a complete city-wide multimodal count.
- The official IBB January 1, 2025 swimming-services list contains 24 distinct public swimming venues. Fitness-only venues and multiple basins at one site are not added. The successful official rendering was manually transcribed and independently checked against two official indexed excerpts; failed HTML retrievals are clearly labeled. Public paid operation does not establish year-round or teenage access at every site.
- The same 2025 provincial population, 15,754,053, and existing utility anchors remain fixed. The transit utility changes [0,1] to [0.6120269803,1]; the pool utility changes [0,1] to [0.1322018835,1]. Both upper bounds remain unknown.

Source packages: ../../data/task4_v114_istanbul_facilities/, ../../data/task4_v114_istanbul_safety/ and ../../data/task4_v114_istanbul_travel/. Safety and education bounds are unchanged. No admissible new high-school travel duration observation was obtained; travel stays [0,1]. A newly acquired historical high-school survey and parliamentary-response lead are documented without treating unverified or inaccessible contents as data.

## Controlled results

| Inherited weights | Istanbul decision rank | Score lower | Score upper |
|---|---:|---:|---:|
| V113 before |15|32.443480|55.341830|
| Transit only |8|34.774710|55.341830|
| Pools only |14|32.754359|55.341830|
| Both (V114) |7|35.107064|55.341830|

The interval width falls from 22.898350 to 20.234766 (11.6322%). Istanbul’s maximum regret falls from 45.085981 to 42.422397. Eight other cities shift down one decision position. Under equal weights Istanbul moves 15 to 4. The default recommendation remains Singapore; all four evidence arms under both weight references retain 25 possible champions. Every upper endpoint and all other 248 cells remain identical. Withdrawal of both additions exactly restores V113.

The same 60,000 random weight draws from V113 were reused, with identical seed, two centers and concentrations 20/100/500. Independent audit verifies all six weight hashes. Possible-champion unions remain all 25 cities in each simulation. At concentration 100, Istanbul’s illustrative midpoint mean rank changes 24.8414 to 23.9047 under inherited-centered weights and 24.8028 to 22.0656 under equal-centered weights. These midpoint statistics are not the minimum-regret decision ranking and do not represent observed performance probabilities.

The previous V113 conditional Tokyo/Singapore preference transition remains: both cities occur in the restricted-weight numerical certificate, with three unresolved leaves around the transition. No all-range Singapore stability claim is restored.

## What must be learned next?

The independent endpoint enumeration in ../task4_v114_revision_review/istanbul_priority.json checks all 31 nonempty uncertain-cell subsets per version and weight reference. Holding other cities fixed, every remaining minimal hypothetical bundle capable of excluding Istanbul now contains travel. Under inherited weights the minimal bundles are safety plus travel; travel plus pools; or education plus transit plus travel. These are information limits at current lower utility endpoints, not observations or forecasts. The new verified facility lower bounds eliminate some formerly conceivable exclusion routes, rather than artificially making exclusion easier.

Future collection should target actual Istanbul resident high-school travel time, current enrollment stage, age and survey weights, with district coverage. Facility locations, capacity, opening hours, fees and age eligibility are required to assess within-city equality and stage-specific usable access. The present count-density indicators cannot answer those questions. No age-based preferences or district exposure values are invented in V114.

## Reproduce

From research/2026-a:

```sh
python3 data/task4_v114_istanbul_facilities/extract.py
python3 data/task4_v114_istanbul_safety/audit.py
python3 scripts/task4_v114_istanbul_revision.py
python3 scripts/task4_current_model.py
python3 scripts/task4_ahp_mc_baseline.py --output results/task4_v114_ahp_mc
python3 scripts/task4_v114_istanbul_revision.py --compare-mc
python3 results/task4_v114_revision_review/audit.py
python3 results/task4_v114_revision_review/mc_audit.py
python3 results/task4_v114_revision_review/istanbul_priority.py
```

The registry selects V114. Historical diagnostics remain labeled by their input versions. No Overleaf manuscript was edited.

## Unchanged formulas

For facility count n, population P and fixed anchor a: d=100000*n/P, lower utility=d/(a+d), upper utility=1 for a partial inventory. Transit a=50; pools a=1.

S_i=100 sqrt(sum_j w_j*u_ij^2)/(sqrt(sum_j w_j*u_ij^2)+sqrt(sum_j w_j*(1-u_ij)^2)).
L_i=S_i(lower_i), U_i=S_i(upper_i), R_i=max(0,max_{h!=i}U_h-L_i).
Recommend argmin_i R_i; possible champion iff U_i>=max_{h!=i}L_h.
Monte Carlo samples weights only: w~Dirichlet(kappa*w0); missing data intervals remain unchanged.

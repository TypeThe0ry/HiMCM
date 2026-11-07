# V21: real transport-stop journeys recover a small amount of missing evidence

Seven known high-school students and one optional member now have reconstructable home-to-school elapsed times using only transport-related stops. Fifteen chains containing other activities are excluded from the update; three known students lack a home departure record. [Extraction, definitions and eight witnesses](../../data/task4_v21_nyc_chains/README.md).

This is a same-source comparison against V20: the 2010–2011 survey population, school-level definition, weights, optional members and bootstrap draws remain fixed. Every previously observed direct journey is unchanged. The improvement comes from real diary segments, not a changed missing-data prior or an imposed shorter travel-time limit.

| Model | Age scope | NYC rank before→after | NYC score width before→after | Possible champions |
| --- | --- | --- | --- | ---: |
| Ten criteria | All current-high-school ages | 22→22 | 44.61160→44.40376 | 25→25 |
| Ten criteria | Under19 | 22→21 | 43.95222→43.69708 | 25→25 |
| Graduation outcome weight .10 | All current-high-school ages | 5→5 | 39.81428→39.62518 | 25→25 |
| Graduation outcome weight .10 | Under19 | 5→5 | 39.20981→38.97777 | 25→25 |

The under-19 travel envelope narrows from [.21398056,.56200752] to [.22395134,.54664429]. Its width falls about7.28%; the corresponding ten-criterion score width falls about0.58%. Only two city decision ranks change in that scenario. Phoenix remains24; Singapore remains the minimax-regret choice. The best worst-case regret and possible-champion set do not improve.

All25 remain possible at alpha=.10 and over the continuous auxiliary weight range [.05,.20]. The eleven-criterion comparison fixes outcome weight beta=.10. Full200 city/model/scope/version rows are in `ranks.csv`; old score endpoints are asserted equal to their archived V20 counterparts.

## Mathematics

For each recovered transport-stop journey, elapsed time is the final school-purpose arrival minus the last explicit home departure, including transport-related dwell. Utility is exp(-T/30). Other activity episodes are not scored as commute. Missing journeys keep[0,1]; optional membership uses the existing exact weighted-ratio extrema.

The city scoring rule stays:

    A_beta=(1-beta)*sum_j w_j*(1-u_j)^2 + beta*(1-q)^2
    B_beta=(1-beta)*sum_j w_j*u_j^2 + beta*q^2
    S_beta=100*sqrt(B_beta)/(sqrt(A_beta)+sqrt(B_beta)).

Use beta=0 for ten criteria, or .10 for the conditional graduation dimension q. The eight main w_j are (1-alpha)/8 and the two auxiliary weights alpha/2. Possible champions satisfy U_i>=max(k!=i)L_k; minimax-regret ranks order max(0,max(k!=i)U_k-L_i). Continuous-alpha checks use all roots of the comparison polynomial.

## Limits and checks

The update reduces a specific missing-journey problem; it does not make the historical source current, identify all usual campuses, or turn the household bootstrap into a design-based confidence interval. Under19 still uses direct current grade9–12 enrollment, with unknown ages optional; age alone never identifies school stage.

Independent reviewers reproduced the eight recovered chains and the membership extrema from raw CSV. Unit checks cover cross-midnight chronology, home returns, skipped place numbers, overlapping timestamps, invalid durations, missing home flags and discretionary work stops. The extractor verifies unchanged direct observations, nested utility bounds and paired-bootstrap envelope nesting. The model verifies the old baseline scores against archived V20 results.

```sh
python3 research/2026-a/data/task4_v21_nyc_chains/extract_chains.py
python3 research/2026-a/data/task4_v21_nyc_chains/test_chains.py
python3 research/2026-a/scripts/task4_nyc_chain_comparison.py
```

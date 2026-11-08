# V117: cross-city evidence revision

Four previously unknown cells now have verified administrative lower utility bounds. With the inherited fixed weights, Toronto moves from minimax-regret decision rank11 to3, NewYork21 to19, and Singapore stays1. All25 cities remain possible champions. This improves the evidence behind conservative decisions; it does not establish a unique best-performing city.

| City | Previous score bounds | V117 score bounds | Decision rank before→after |
|---|---:|---:|---:|
| Toronto | 34.10699–75.43410 | 40.58141–75.43410 | 11→3 |
| New York | 29.10885–72.80593 | 30.21770–72.80593 | 21→19 |
| Singapore | 43.53854–71.59464 | 43.81633–71.59464 | 1→1 |

Toronto's score interval narrows by6.47441 points (15.67%). Under equal weights its decision rank changes11→2; NewYork21→16; Singapore remains1. Kendall tau-b between old and new decision rankings is0.93333 for inherited and0.90667 for equal weights. These correlations describe agreement, not external validation of city quality.

## Admitted evidence

- Toronto:45 deceased victims in the official current2025 homicide snapshot, population3,271,830. The police definition includes murder and manslaughter; the count is used as a conditional upper bound for the intentional-homicide subset in the recorded-crime universe. Thus the benefit utility gains a lower bound, while its upper bound remains1. The earlier44 count is retained as a source-version difference, not averaged or treated as a sampling interval.
- Toronto:59 outdoor pool locations as a partial public inventory. The2025 municipal inventory uses a category explicitly defined as locations in the earlier official masterplan. No2025 independent address deduplication is claimed. The reported64 indoor pools are not added because colocation/unit equivalence remains unresolved.
- NewYork:53 municipally operated outdoor pool venues in the June2025 release; population8,584,629. Mini pools, entry restrictions and seasonal operation mean this is facility supply, not a count of venues universally accessible to high-school students.
- Singapore:7 named distinct public ActiveSG swimming venues in the April2025 source; population6,111,175. Other facilities remain unknown. A selected official list provides a lower bound, not a complete inventory.

Copenhagen's49 nationwide fatal-offence candidate is not admitted: the reviewed categories have not been proved to cover all intentional killings. The criterion was preserved and this route skipped. Source packages and raw-file hashes are under ../../data/task4_v117_*/; ../../design/task4_v117_admissions.json pins the admitted records and source captures. Provider-extracted text is distinguished from downloaded original bytes.

## Controlled comparison and sensitivity

`ranks.csv` and `utility_bounds.csv` include V114, four single-cell revisions, the combined V117 and complete withdrawal. Exactly4 of250 cells change; all upper endpoints remain unchanged. Every Istanbul cell and every city's travel interval remain unchanged. Istanbul's relative decision rank nevertheless moves7→8 under inherited weights because Toronto overtakes it; this is not worsening Istanbul data.

The current model entry point verifies all250 cells and reproduces the selected baseline. Withdrawal restores the old inputs and outputs. An independent reviewer recalculated weighted Euclidean TOPSIS distances, competitor regret, decision ranks and champion sets directly from the saved CSVs.

The Monte Carlo rerun in ../task4_v117_ahp_mc/ uses the same seed20261108, two centers and concentrations20/100/500,10,000 draws each (60,000 total). At inherited center/concentration100, Singapore's minimax recommendation frequency changes68.04%→71.49%, Tokyo31.81%→27.35%, Toronto0%→1.06%. These are frequencies under the specified analyst weight distribution, not empirical student preferences or real-world winning probabilities. `comparison_v114.csv` contains all150 city-scenario comparisons. Midpoint completion ranks are explicitly illustrative; no missing input was replaced in the main model. Continuous alpha[.05,.2] certification still contains both Singapore and Tokyo winners with2 unresolved transition leaves; it does not certify Singapore throughout the range.

## Model and reproduction

Fixed weights are0.1125 for each main indicator and0.05 for each of the two facility indicators. For utility u:

    S(u)=100*sqrt(sum(w*u²))/(sqrt(sum(w*u²))+sqrt(sum(w*(1-u)²)))
    L_i=S(lo_i), U_i=S(hi_i)
    R_i=max(0,max_{k!=i} U_k-L_i), recommendation=argmin R_i
    possible champion iff U_i>=max_{k!=i}L_k

Facility density x=100000*count/population gives utility lower x/(1+x), upper1. Toronto's crime-count superset gives rate upper r=100000*45/3271830 and utility[2/(2+r),1]. These are unchanged transformations and evidence rules.

From repository root:

```sh
python3 research/2026-a/scripts/task4_v117_city_revision.py
python3 research/2026-a/scripts/task4_current_model.py
python3 research/2026-a/scripts/task4_ahp_mc_baseline.py --output research/2026-a/results/task4_v117_ahp_mc
```

The newly supplied16-city CSV is preserved byte-for-byte at ../../data/task4_v117_team_intake/. It is reviewed separately for sources, geography, school stage and count/rate consistency. Its flags do not authorize overwriting verified observations or replacing the25-city candidate set. No Overleaf text was changed.

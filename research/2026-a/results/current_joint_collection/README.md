# Joint data-collection limits in the retained V203 model

The smallest optimistic certificate uses **three exactly resolved utility cells**, with Zurich as target, under either retained weight set. Oslo's corresponding minimum is11 under both sets. These are information limits inside the current rectangular model. They are not new measurements, recommendations to replace existing values, or estimates of feasible research effort. PrimaryV203 recommendations, score intervals and all16 possible champions remain unchanged.

## What one resolution means

An uncertain utility cell becomes exactly known inside its retained interval. This is stronger than obtaining another facility lower bound or a travel mean: exact travel utility generally needs the relevant duration distribution. One cell may require multiple matched source components. The experiment assigns no acquisition probability, monetary cost or collection time. Rounded survey summaries and incomplete inventories do not constitute exact resolutions.

## Why the minimum is global within this experiment

The TOPSIS score is coordinatewise increasing on the retained utility box for fixed positive weights. For candidate c, a measured subset gives its largest possible post-measurement lower score when the selected values are at their upper endpoints. Each rival's smallest post-measurement upper score uses its selected values at their lower endpoints. The rivals' upper bounds otherwise stay unchanged.

Enumerate every local subset. For each count p, retain the candidate's maximum lower score Lc(p), and for each rival j/count q its minimum upper score Uj(q). A strict certificate requires Lc(p)>Uj(q) for every rival. Thus the minimum count for c is

`min_p [ p + sum_(j != c) min { q : Uj(q) < Lc(p) } ]`.

An absent feasible q rejects that candidate count. Independence of the declared box makes these row-wise choices jointly admissible in the utility model. Conversely, no same-cardinality observation can outperform the favourable endpoints; this proves the count lower bound. The saved measurement witnesses move all selected coordinates strictly inside their original intervals and retain a positive score margin. They do not establish attainable integer facility counts, realistic pupil–teacher ratios, or physically coherent joint raw observations.

## Reading the results

- `candidate_minimums.csv`: minimum counts and interior strict margins for all32 city/weight targets.
- `frontiers.csv` and `all_budgets.csv`: the complete local count frontiers and candidate-count search.
- `measurements.csv`: a representative interior observation witness per target; repeated cells across different hypothetical plans are separate scenarios.
- `certificates.csv`: post-resolution score bounds; the target lower bound strictly exceeds every rival upper bound.
- `tie_completion.csv`: numerical simultaneous16-city tie completions, with the original point cells retained.
- `summary.json` and `verification.json`: calculation bindings and separate independent validation. No Monte Carlo is needed.

The representative fixed-weight three-cell plan resolves Zurich's teacher ratio and travel utility plus Dublin's teacher ratio. The representative equal-weight plan resolves Zurich's teacher ratio, travel and transport utilities. These are favourable-value existence certificates, not unique cell sets. Independent enumeration of all17,296 three-cell sets per weight finds five fixed-weight and two equal-weight minimum sets, all targeting Zurich and including its teacher ratio and travel utility. Under fixed weights, the third cell can be Zurich transport or pool utility, or Dublin teacher ratio, transport or travel. Under equal weights, it can be Zurich transport or pool utility. `optimal_three_cell_sets.csv` lists all seven. The independent frontiers also rule out certificates with fewer cells.

Matching matters: exact utility identification retains each cell's source population, observation period and definition. The Zurich work-commute proxy cannot be exactly identified by substituting an unrelated school-trip distribution. A compatible full distribution, rather than another mean, is needed for the travel-utility experiment. Likewise, school headcounts do not identify teaching FTE.

The common score intervals are [56.4318314843,60.4349830570] under fixed weights and [58.1048004402,61.4808135900] under equal weights. Continuity along each city's lower-to-upper utility segment establishes a simultaneous tie within the declared box; the CSV approximates such a completion. Therefore even resolving every uncertain cell cannot guarantee a unique winner for every possible outcome admitted by this model. This is a mathematical information limit, not an observed or forecast real-world tie.

Run `scripts/task4_current_joint_collection.py` with `.venv-v120/bin/python`, then the independent audit. The source CSV, weights, anchors,48 retained uncertain cells and current single-main manuscript stay unchanged. Do not substitute these hypothetical utility values into the primary analysis.

## All retained targets

Minimum optimistic resolved-cell counts, in original city order. This is an information-budget table, not a city-quality ranking.

| Target city | Fixed weights | Equal weights |
| --- | ---: | ---: |
| Vienna | 17 | 16 |
| Zurich | 3 | 3 |
| Helsinki | 5 | 5 |
| Berlin | 15 | 17 |
| London | 8 | 10 |
| Amsterdam | 19 | 19 |
| Stockholm | 10 | 9 |
| Paris | 6 | 6 |
| Madrid | 7 | 7 |
| Milan | 10 | 9 |
| Dublin | 4 | 4 |
| Oslo | 11 | 11 |
| Prague | 13 | 13 |
| Warsaw | 11 | 13 |
| Singapore | 13 | 11 |
| Tokyo | 17 | 16 |

The independent auditor checks the existing `optimal_three_cell_sets.csv` byte for byte and prints JSON to stdout by default. Saving a report requires `--output PATH`, with `--overwrite` for an existing file. Rebuilding the derived CSV additionally requires `--rebuild-optimal-table` and an explicit overwrite of this directory’s canonical verification report.

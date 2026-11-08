# V114 independent review

The deterministic and Monte Carlo checks passed. Reproduce from the repository root:

```sh
python3 research/2026-a/results/task4_v114_revision_review/audit.py
python3 research/2026-a/results/task4_v114_revision_review/mc_audit.py
python3 research/2026-a/data/task4_v114_istanbul_safety/audit.py
```

The deterministic audit pins the V113 factory, derives the two new lower bounds independently, and checks four ablations under both existing weight references. Only Istanbul public transport and public pool utility lower bounds change; all 250 upper bounds and 248 other cells remain unchanged.

| Weight reference | Istanbul minimax decision rank, V113 → V114 | Score lower bound, V113 → V114 | Score upper bound |
|---|---:|---:|---:|
| Inherited | 15 → 7 | 32.44348 → 35.10706 | 55.34183 |
| Equal | 15 → 4 | 30.32443 → 35.63517 | 58.73361 |

All four ablations retain 25 possible champions and Singapore as the minimum-regret recommendation. The Monte Carlo audit independently checks 60,000 draws and 1.5 million city-draw results; all six sampled-weight hashes match V113. Each sampled possible-champion union remains 25. Fully unknown cells fall from 131 to 129, while nonpoint intervals remain 151.

The decision rank is a minimax-regret ordering, not a measured performance rank. At concentration 100, Istanbul illustrative midpoint mean ranks improve from 24.8414 to 23.9047 under inherited weights and from 24.8028 to 22.0656 under neutral weights.

The evidence establishes lower bounds from 12,426 physical bus stops and 24 distinct municipal swimming venues. It does not establish complete all-mode inventories, basin counts, teen-specific access at every venue, or annual continuous operation. The independent primary-source cross-check and safety rejection audit are in `../../data/task4_v114_istanbul_safety/`. No new homicide or high-school education bound was admitted.

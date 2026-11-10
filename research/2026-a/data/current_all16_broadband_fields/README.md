# Archived broadband field classification for the 16-city intake

The original 16-city CSV has 15 values that exactly match the archived Speedtest Global Index **fixed broadband median download** city rows. Singapore's submitted **667.71 Mbps** instead matches the Singapore **fixed broadband mean download** country row; that snapshot lists Singapore fixed median at **476.02 Mbps**. The publisher match classifies the field in which each submitted number occurs. It does not establish the CSV's original extraction route.

The comparison checks all four displayed fields: fixed median, fixed mean, mobile median, and mobile mean. The archived HTML contains city-level median rows; its mean panels are country-level. For that reason, mean fields are left blank for the other 15 cities rather than populated from country values. Singapore's four publisher rows are retained as explicitly country-level because the intake identifies Singapore as a country-city-state and flags its submitted broadband value `NATIONAL`. It is not labeled a city-row match. Blank means that the corresponding row was unavailable at that geography level, not zero.

Matching requires both city (or the explicit alias) and country before comparing values. `Zurich` maps explicitly to publisher spelling `Zürich`; no cross-city value matching is used. Nonmatches, if any, mean no exact match in the available corresponding rows and do not establish that an input is erroneous. Ookla's table does not define municipal polygons, so publisher-city boundary equivalence to the CSV's city-proper label remains unverified.

The archive is the official [Speedtest Global Index](https://www.speedtest.net/global-index), retained at `research/2026-a/data/task4_v5_resources/ookla_global_index.html` and checked against its existing manifest. Its publication label is **September 2026**. The page says results are updated mid-month for the previous three months; it does not provide exact window boundaries in the displayed snapshot. The original intake is retained unchanged at `research/2026-a/data/task4_v117_team_intake/city_indicators.csv`.

Run offline:

```sh
python research/2026-a/data/current_all16_broadband_fields/deterministic_offline_extract.py
python research/2026-a/data/current_all16_broadband_fields/deterministic_offline_extract.py --write
```

Default mode prints the summary JSON. `--write` deterministically creates `comparison.csv` and `summary.json` in this directory. The extractor uses regular expressions and standard-library modules, not an HTML parser or network requests. Source and input hashes, exact field values, row ranks, publisher links, flags, year, geography level, and alias are recorded in the outputs.

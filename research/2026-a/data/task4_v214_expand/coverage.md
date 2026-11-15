# Coverage

| City | Indicators with a value (of 10) | Missing indicators |
|---|---:|---|
| New York | 7 | public transport density, commute_min, pools_per_100k |
| Los Angeles | 10 | — |
| Chicago | 10 | — |
| San Francisco | 10 | — |
| Shanghai | 7 | public transport density, commute_min, pools_per_100k |
| Beijing | 6 | cli, pir, pupil_teacher_ratio, pools_per_100k |
| Shenzhen | 8 | pupil_teacher_ratio, pools_per_100k |
| Guangzhou | 7 | pupil_teacher_ratio, public transport density, pools_per_100k |
| Hong Kong SAR | 9 | pupil_teacher_ratio |
| Macao SAR | 7 | cli, pir, pupil_teacher_ratio |
| New Delhi | 7 | public transport density, commute_min, pools_per_100k |
| Mumbai | 10 | — |
| Moscow | 6 | homicide_per_100k, pm25_ugm3, pupil_teacher_ratio, pools_per_100k |
| Toronto | 8 | homicide_per_100k, he_per_million |
| Sao Paulo | 10 | — |
| Mexico City | 9 | pools_per_100k |
| Buenos Aires | 9 | pupil_teacher_ratio |
| Copenhagen | 9 | he_per_million |
| Luxembourg | 10 | — |
| Reykjavik | 9 | he_per_million |
| Doha | 8 | he_per_million, pools_per_100k |
| Dubai | 7 | pupil_teacher_ratio, commute_min, pools_per_100k |
| Abu Dhabi | 9 | pupil_teacher_ratio |
| Istanbul | 9 | public transport density |
| Cairo | 6 | homicide_per_100k, pupil_teacher_ratio, public transport density, broadband_mbps |
| Johannesburg | 10 | — |
| Nairobi | 6 | pupil_teacher_ratio, public transport density, commute_min, pools_per_100k |
| Seoul | 10 | — |
| Sydney | 8 | pupil_teacher_ratio, public transport density |
| Bangkok | 8 | he_per_million, pools_per_100k |
| Kuala Lumpur | 7 | pupil_teacher_ratio, broadband_mbps, pools_per_100k |

Cities missing 3 or more of the 10 indicators: New York, Shanghai, Beijing, Guangzhou, Macao SAR, New Delhi, Moscow, Dubai, Cairo, Nairobi, Kuala Lumpur.

## Assembly and model compatibility

- All 45 original header columns are retained in order. Appended columns are public_transport_density_per_100k, its year and flag, public_transport_count, and pools_count. transit_share_pct stays empty because stop density is a different measure. pool_count and pools_count contain the same public-pool venue counts.
- Coverage and indicators_present/indicators_total count the ten requested indicators, including stop density. usable_present equals the number with a value because build() does not exclude proxy or lower-bound flags. A value is not an independent quality certification.
- The existing build() reads pools_per_100k and divides he_per_million by 10 internally. It accepts these rows, but FIELDS[6] is None, so it ignores transit density and retains transit utility as [0,1]. To use stop density, the model owner must map that field to public_transport_density_per_100k. The original model script was not edited.
- Main part_c.csv and part_k.csv already contain all nonmissing supplemental values. No duplicate supplemental rows were added. Main files parse as nine-column CSVs. City aliases Luxembourg City and Mumbai (Greater Mumbai/BMC) were normalized.
- Abu Dhabi input rates contain factor-of-ten arithmetic errors. The supplied notes give 4,070 stops, 3 pool venues, and 4,135,985 residents. Densities are corrected to 98.404612202 stops and 0.072534112 pools per 100,000 (input values were 984.046122 and 0.725341122). The bibliography identifies these corrected calculations.
- Counts explicitly stated in notes were retained as counts; rounded rates were not inverted to fractional counts. Rate-specific population years and denominators were retained, including Toronto 2021 and Sao Paulo 2022, even when the main population row is newer.
- Population_basis records the supplied population boundary note. Academic-year strings and observation dates are preserved. Missing values and their flags are empty. Sources list observations with values, rather than unsuccessful searches. Source URLs were carried from the supplied files and were not independently re-fetched.
- Validation passed: 31 unique requested cities in order, exact original-header prefix, numeric indicator values, complete flags for nonmissing values, integer supporting counts, full measurement-to-bibliography joins, and agreement between coverage counts and the matrix. The unmodified build() ran successfully with a (31, 10) utility array and 310 audit rows.
- lower_bound takes precedence over a metro proxy when transit is only partly counted. The source scope is retained in the bibliography. Other flags follow supplied scopes and explicit lower-bound notes.

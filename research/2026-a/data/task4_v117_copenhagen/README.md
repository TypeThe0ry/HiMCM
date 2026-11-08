# Copenhagen: 2025 national fatal-offence superset

Official Statistics Denmark data supply a finite national upper bound for Copenhagen's recorded homicide victims. The bound uses **49 fatal-offence victim records**, not the combined homicide-and-attempt total of 167.

| STRAF5 code | Fatal-offence class | Denmark, 2025 |
|---|---|---:|
| 123073111 | Homicide | 46 |
| 123073121 | Child murder | 0 |
| 125873262 | Serious assault resulting in death | 3 |
| 128673131 | Killing by request | 0 |
| Total | | 49 |

[Statistics Denmark's release](https://www.dst.dk/da/Statistik/udgivelser/NytHtml?cid=53910) independently reports the 46 homicide victims separately from attempts. STRAF5 provides the other fatal classes. The [Justice Ministry's homicide report](https://www.ft.dk/samling/20231/almdel/REU/bilag/113/2815790/index.htm) identifies homicide under sections 237, 238, 239 and fatal assault under 246; this older report supplies the scope definition, **not the 2025 counts**. The Statistics Denmark classification valid through December 2025 also separately identifies these codes and attempted homicide.

FOLK1A gives **667,574** Copenhagen municipality residents on **1 July 2025** (municipality 101, all ages, sexes and marital statuses). The existing HE evidence used 2026 population; this calculation obtains the correct 2025 population separately.

Within the recorded fatal-offence reporting universe, Copenhagen's count cannot exceed Denmark's 49. Therefore the raw city-rate bound is `[0, 7.3400102461]` per 100,000. The existing cost utility `2/(2+rate)` gives **`[0.21413252740752906, 1]`**. This is a geographic superset bound, not a city point estimate. It does not bound unreported deaths, resident vital mortality, or precisely incident-year deaths: the source is the 2025 reported-victim series.

`observations.json` contains one candidate in the integration format, with admission pending. `lower_bound_only` refers to utility; `raw_rate_upper_bound_only` explicitly records the opposite direction for the cost input. The model and registry were not edited.

Run `python3 data/task4_v117_copenhagen/extract.py` from `research/2026-a`. The offline script checks saved response hashes, exact codes and filters, population geography/date, component totals and the utility calculation. `crime_query.json` and `population_query.json` preserve the POST bodies for `https://api.statbank.dk/v1/data`. `raw/` contains original response bytes; `definition_provider_excerpt.txt` is a clearly labeled Exa text excerpt, not original PDF or HTML bytes.

## Cross-review admission decision

Not admitted in V117. The four national fatal-offence classes have not been proved to cover every intentional killing: the official definition review identifies other assault provisions with potentially intentional fatal outcomes. Thus49 is not a verified upper bound for the full current homicide indicator. Copenhagen remains[0,1]; this source was skipped rather than redefining the criterion.

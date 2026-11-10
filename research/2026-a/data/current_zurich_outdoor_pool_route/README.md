# Zürich outdoor pool route: four unadmitted venue candidates

The municipal summer-bath directory and individual venue pages support four distinct Zürich-address outdoor venues with explicit swimming pools, public ticket information and 2026 swimming schedules. Each venue counts once irrespective of its number of basins. All four are additional to the twelve retained indoor/school venue addresses in `../task4_v196_zurichpool/school_candidates.json`:

| Venue | Zürich address | Main swimming pool | 2026 scheduled period |
|---|---|---|---|
| Freibad Allenmoos | Ringstrasse 79, 8057 | 50 × 20 m | 9 May–20 September |
| Freibad Heuried | Wasserschöpfi 71 (Freibad), 8055 | 50 × 20 m | 9 May–20 September |
| Freibad Letzigraben | Edelweissstrasse 5, 8048 | 50 × 25 m | 1 May–27 September |
| Freibad Seebach | Glatttalstrasse 43, 8052 | 50 × 20 m | 11 April–25 October |

Exact original time slots and status fields are retained in `extraction.json` and in the `stzh-datatable` components of each original page. The 2026 schedule footnote limits swimming from August to periods when supervision is possible in the available light. Seebach's 11–30 April and 28 September–25 October footnote states that only the 50-metre pool is accessible. The individual status components say all four were closed when captured; Allenmoos and Letzigraben show `Saisonende`, while Heuried and Seebach do not give a reason in that component. Allenmoos and Letzigraben describe winter access to their **parks**, not winter swimming. The page records a seasonal schedule; it does not establish year-round or actual individual teen access, affordability, universal access, or continuous operation. Verify the applicable entry rules and any venue restrictions separately before a student-access interpretation.

**Hold:** Freibad Auhof, Luegislandstrasse 160, 8051 Zürich, has a 50 × 13 m pool and is separate by address. Its page says the bath is closed for renovation and expansion, with reopening planned for the 2029 season. The archived page also retains a 2026 schedule and `Saisonende` status; neither overrides the specific renovation notice. Do not include it in the current available subset without resolving the operating period and the intended inventory date.

**Exclude from this municipal-address subset:** Freibad Zwischen den Hölzern's official contact address is 8102 Oberengstringen, although it appears in the city's directory and has a 50 m pool. Other directory lake/river bathing areas, wading-only facilities and unexamined sites are not counted. This bounded search is not a complete census or claim that every such facility is excluded elsewhere. Municipal postal address is used here as a practical screening criterion; a formal boundary check remains a separate qualification step.

`retrievals.json` binds each untouched original HTML to URL, final URL, HTTP status, content type, UTC retrieval time, byte length and SHA-256. Captured 2026-11-10 UTC (2026-11-11 Singapore); the source's inventory reference date is not identified. The population 440,935 labeled 2025 is retained from user inputs without revalidation; a 2026 source snapshot must not be relabeled as a 2025 inventory. `python research/2026-a/data/current_zurich_outdoor_pool_route/verify.py` checks hashes, source links, explicit pool descriptions, old and new addresses, hours and the Auhof closure; it regenerates `extraction.json`. Address differentiation is evidence of distinct named venues, not an independent spatial boundary or operational audit.

These are four **unadmitted candidates** for independent qualification and review; no model input, score, registry, manuscript or population was changed. Admission is zero. A possible combined count of 16 is a conditional preview, not an established model result.

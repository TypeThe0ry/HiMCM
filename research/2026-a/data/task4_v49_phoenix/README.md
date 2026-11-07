# Hope Academy: verified 2023–24 record

NCES reports **83 students and 4 teacher FTE (20.75 students per FTE)** for Hope College and Career Readiness Academy in 2023–24. Grade counts are 6, 7, 19, and 51 in grades 9–12. The record identifies the school as a nonvirtual alternative high school at 6401 S 16th St, Phoenix, with school ID `040386003535`.

This historical observation is kept separate from the missing 2024–25 membership record. It supplies neither a replacement nor an upper bound for 2024–25. Consequently, this acquisition alone does not narrow Phoenix's current education interval or change its model rank.

## Original sources and verification

The current NCES EDGE service links its historical collection to [Public School Characteristics 2023–24](https://nces.maps.arcgis.com/home/item.html?id=78ebe2d5e18c4274bf0a4266b9f26d84), owned by `OpenDataMgr_NCES`. That item's URL points to the original [NCES historical layer](https://nces.ed.gov/opengis/rest/services/K12_School_Locations/EDGE_ADMINDATA_PUBLICSCH_2324/MapServer/1).

- `item_2023_24.json`: original collection metadata and official source URL.
- `layer_2023_24.json`: original layer metadata, variable definitions and missing codes.
- `hope_2023_24.json`: original exact-school query response, retaining every returned field.
- `manifest.json`: request URLs, retrieval timestamps and SHA-256 hashes.
- `audit.json`: extracted historical values and admission decision.

Checks passed: returned school ID and year; grade sum = male + female sum = race-group sum = membership = 83; membership / teacher FTE = reported ratio = 20.75. Raw JSON bytes are unchanged.

The ADE documentation search returned the already-reviewed 2026 quick guide and general public-data descriptions; neither established the FY2025 enrollment chart's snapshot compatibility. Previously failed ADE workbook, suppressed same-year LEA and video-login routes were not retried. The next useful Phoenix evidence is an actual 2024–25 count or documentation that establishes a compatible snapshot, not extrapolation from this older count.

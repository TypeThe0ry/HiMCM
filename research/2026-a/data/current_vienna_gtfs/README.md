# Vienna: passenger-call evidence for a larger dated candidate

The operator's archived OGD index links the GTFS text files directly. Seven new HTTP200 originals supply stops, routes, agencies, trips, stop times, weekly calendars and date exceptions. Their Last-Modified headers are9November2026; requests were made10November UTC. The analysis uses the10November2026 **GTFS service day**, including its after-midnight times, rather than claiming a civil-day operating census. A published schedule is distinct from observed actual operation.

`storage.json` maps every original body to its stored bytes and records both hashes. The772,581,069-byte stop-times and45,000,377-byte trips originals are stored losslessly as XZ; decompressing recovers the exact receipt bytes. Other files retain their original bytes. No feed is replaced with a third-party reconstruction. GTFS Markdown and its Apache2.0 licence were successfully fetched from the official repository linked by the specification site. The direct specification HTML request returned403, was not retried and supplies no retained original.

## A conservative identity bridge

GTFS `stops.txt` has no parent-station field in this feed. Its stop-ID prefixes are not interpreted as station-area IDs. Instead the candidate joins to the frozen [V127 native DIVA sources](../task4_v127_vienna_transport/README.md). A GTFS name must equal a globally unique DIVA area name and a native stopping-position name. Its longitude/latitude, compared at seven decimal places, must match a source position key assigned globally to that same DIVA alone. This corroborates source identity; it does not assert seven-decimal real-world accuracy or merge locations into newly invented clusters.

The DIVA representative point, GTFS point and every known native stopping position for the DIVA must be inside the official Vienna polygon. Lohnergasse60200810 fails the all-position check and is excluded. DIVA's grouping definition comes from the frozen operator schema, not a geographic distance threshold. The grouping snapshot is8November, while the timetable is a9November export: the cross-date identity is documented rather than renamed a single2025 census.

Eligible witnesses have an active trip after weekly calendars and date additions/removals, a regular pickup or drop-off, agency04 (Wiener Linien), route type3 and a digits-plus-A route name. Empty pickup/drop-off follows the GTFS regular-service default. A same-name screen removes52 groups with other active route types; this is not an exhaustive cross-alias nonbus inventory. The script retains378 candidate DIVA groups, each with an explicit trip/stop-sequence witness. It substitutes the candidate count for99 in a controlled copy; it never adds bus and metro counts.

**Public-service eligibility for every exceptional trip remains to be established before primary admission.** Agency, route-name pattern and pickup/drop-off flags provide schedule evidence, but are not a universal access certificate. This package does not activate a new primary lower bound or modify the manuscript. The [candidate results](../../results/current_vienna_gtfs_candidate/README.md) separate conditional score changes from actual primary improvement.

## GIS layers remain diagnostic

Two new city WFS originals are retained: HALTESTELLEWLOGD has1,807 features and OEFFHALTESTOGD10,471. The first includes named Betriebshof objects; the second has null DIVA_ID in every feature. They cannot independently certify the earlier rejected broad operational list or supply an exact DIVA bridge. For example, WL_NUMMER1 is named Absberggasse in the GIS layer while the frozen operator area at nearby coordinates is Schrankenberggasse; neither source name is silently overwritten. These layers do not enter the candidate count.

Source attribution: Wiener Linien; Datenquelle Stadt Wien – data.wien.gv.at; GTFS specification contributors. No realtime requests, credentials or agency contacts were used. Population2025, original CSV, model weights/anchors and the current V203 remain fixed.

# Oslo: metro stations as a public-transport lower bound

The official Oslo municipal transport map identifies **89 named metro stations inside municipality 0301**, after merging their 186 platform records. These stations form a subset of public-transport stops. With the user-supplied population **727,797**, this gives density at least **12.2287 per 100,000 residents**, and the existing transform `density / (50 + density)` gives utility **[0.1965120220, 1]**. No traffic-share percentage is used or overwritten.

The data copy timestamps are **6 July 2026**. The web-map metadata was modified in 2025, but that metadata does not date the live features. This evidence can support a clearly labelled 2026 infrastructure scenario; it does not establish a 2025 stop count. The attachment population is retained without replacement.

## Sources and reproduction

- Oslo Bymiljøetaten's official ArcGIS item `ac2387eff2ea49698cd93e44355a64cd` describes stops and routes within Oslo municipality. Its linked municipal service is `geodata.bymoslo.no/arcgis/rest/services/geodata/Temadata_Publikum/MapServer`.
- Layer 800 query returns all modes from the common underlying table; layers 801/802 must not be added to it. The query returned 2,109 distinct object IDs without a transfer-limit flag.
- Kartverket's public municipality API supplies the Oslo 0301 polygon in longitude/latitude. Point-in-polygon filtering retains 2,104 records across modes; all 186 metro-platform records lie inside.
- Restrict to `transporttype = Tbane` and `holdeplasstype = Tbanestasjon`; merge identical station names. Different station names have nearest platform coordinates more than 276 metres apart, reducing co-location alias concerns. The service lacks stable Entur parent StopPlace IDs, so the much larger cross-mode count is deliberately not claimed as a physical-stop inventory.
- All source features attribute Entur data under the Norwegian Licence for Open Government Data (NLOD). No personal records are included.

`request_urls.json` records exact original requests, accessed 2026-11-08. The three `*_raw.json` files preserve HTTP response bytes. `summary.json` records hashes, checks and source dates. `oslo_metro_station_subset.csv` exposes each included station and supporting object IDs. Run `python3 data/task4_v118_transit/verify.py` from the research directory to regenerate the aggregate outputs offline.

`observations.json` is a proposed evidence update for independent review. This folder does not modify the supplied CSV, model, weights, anchors, or 25-city registry. Other transport modes remain uncounted and the utility upper bound stays 1. The lower bound is conditional on the municipal map's station identities and 2026 time coverage; it is not a sampling confidence bound.

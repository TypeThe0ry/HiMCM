# Trosterud and Midtstuen: native identity and service check

The 2026-11-09 Entur Oslo NeTEx export identifies four separate StopPlaces, each without a `ParentSiteRef` or a child StopPlace referring to it in that export. This establishes their registry structure, not whether each bus/metro pair is one or two physical stop units. `netex_extract.json` lists each quay and available public codes, extracted from the preserved archive in `../current_oslo_transport/03_Oslo_latest.zip`. Null parent means no parent element in that export; no common parent cannot establish physical distinctness.

| Place | StopPlace | Mode | Quay IDs (public codes) | Journey Planner response |
| --- | --- | --- | --- | --- |
| Trosterud | 5677 | bus | 10402 (E), 10403 (F) | 10 calls, including RUT lines 110, 300, 400 |
| Trosterud | 6197 | metro | 11373 (1), 11374 (2) | 10 calls, RUT line 2 |
| Midtstuen | 6302 | metro | 11577 (1), 11576 (2) | 10 calls, RUT line 1 |
| Midtstuen | 6313 | bus | 11596, 101510, 11597 (public codes absent) | zero calls in queried horizon |

All abbreviated IDs carry the `NSR:StopPlace:` or `NSR:Quay:` prefix. The one batched Journey Planner query asked for at most 10 calls per stop within 72,100 seconds; empty results do not prove a stop is inactive outside that query. Calls report planned and expected times around 2026-11-10, with a realtime indicator; they are predictions, not verified completed journeys, 2025 observations, or evidence of student access. Service evidence does not resolve whether each cross-mode pair is physically one unit. Neither different IDs nor proximity alone determines that identity.

`request.json` contains exact POST bytes; `response.json` preserves response bytes; `metadata.json` records endpoint, request headers, timestamp, HTTP status and both hashes. The public [Journey Planner API documentation](https://developer.entur.org/pages-journeyplanner-journeyplanner/) describes its departure-board endpoint and client-identification header. Entur's [NSR documentation](https://developer.entur.org/pages-nsr-nsr/) identifies the daily NeTEx export as the preferred stop data source. No model or paper was modified.

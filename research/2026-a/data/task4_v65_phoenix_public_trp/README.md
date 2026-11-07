# Phoenix: public TRP service audit (2026-11-08)

New path examined: MAG's public ArcGIS TRP dashboard, rather than another review of the coordinator handbook. The public service exposes `avgTripLengthMC` (table 1), with `avgMins`, `avgMiles`, `totalTrips`, and `totalForCluster`. Its remaining dimensions are industry cluster, subregion, live/work grouping, and travel mode. It has no school-site, student status, age, or grade field.

The service identifies its input as the **2022 regional workforce** TRP survey and lists an update date of 2023-04-28. Thus the existence of an average-minutes field does not establish observed high-school travel time. Neither count field is verified as a student survey denominator. Education-industry employee observations would not establish student observations either.

**Result:** zero admissible Phoenix high-school observations. Preserve the existing missing interval; this audit provides no basis for narrowing it or the possible-winner set. This is a finding about the inspected public service, not proof that student results do not exist elsewhere.

## Sources and archive

- [TRP dashboard service](https://geo.azmag.gov/arcgis/rest/services/infograph/TRPdashboard/MapServer): survey year and workforce population in Document Info.
- [Average trip table schema](https://geo.azmag.gov/arcgis/rest/services/infograph/TRPdashboard/MapServer/1): full ten-field schema inspected.
- [MAG Live-Work Patterns](https://azmag.gov/Programs/Maps-and-Data/Commute-and-Workforce/Live-Work-Patterns): official page independently describes employee commuting; initial browser retrieval succeeded but archive retry timed out.
- [2025 employment service](https://geo.azmag.gov/arcgis/rest/services/maps/StateEmployment_2025_v2/MapServer): additional lead, employer/employee geography. No archived usable high-school results obtained; layer-0 archive retrieval timed out.

`web_tool_response.json` preserves the actual serialized web-reader response, including failures. `manifest.json` hashes those saved bytes. It is **not a downloaded origin JSON response**; the service index was indexed three months earlier and the table schema was reported crawled today. Direct requests to the TRP service timed out. ArcGIS Online item metadata requests returned JSON errors; `retrieval.json` records assertion failures, not successful downloads or inferred HTTP codes. The live-work direct request produced no saved source file. No failed retrieval is treated as evidence that data are absent.

`audit.json` records the exclusion decision. `python3 audit.py` verifies archive integrity and that the archived schema and workforce description support that decision. No model, manuscript, or existing interval was changed.

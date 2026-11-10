# PID stop-node semantics and bus evidence audit

Source audit, not a candidate count or manuscript revision. The raw PID JSON was generated at `2026-11-10T04:12:17` as printed in the source; its timezone is not supplied in the file. `manifest.json` records actual UTC retrieval time, requested and final URL, HTTP status, size and SHA-256. The 2026-11-09 letter-list snapshot is in `../task4_v127_prague/`, not re-requested. No full GTFS feed was downloaded.

## Definitions and scope

PID's [open-data documentation](https://pid.cz/o-systemu/opendata/) defines a **group** as stops with the same name within one node. A node can contain multiple differently named groups: node 237 includes Karlovo náměstí, Palackého náměstí, Moráň and Novoměstská radnice. A stop is a distinct post, identified as `node/post`, with its own coordinates and platform code. A group is a source-defined aggregate; neither a node nor a group automatically proves one physical site under another city's definition. A node combining multiple places may undercount those places; that observation alone does **not** establish overcount or invalidate a lower bound. To establish possible overcount of the chosen physical unit, seek evidence of one such unit split across nodes. Deduplicate modes at the explicitly chosen unit; do not sum separate metro and bus totals without addressing overlap.

Each stop in the [official JSON](https://data.pid.cz/stops/json/stops.json) has individual `lines`; documentation defines `name` as its passenger-facing name, `type` as transport mode, `isNight` as night route. The [XSD](https://data.pid.cz/stops/xml/StopsByName.xsd) distinguishes `bus` and `trolleybus`; `mainTrafficType` is the *dominant* mode, not the complete list. For example node 876 Albertov has group `mainTrafficType=tram` but a stop includes `X90`, `type=bus`, `isNight=true`. Its X90 JSON line ID is 890, while the archived webpage link uses `line=673`. The webpage's `line` query parameter and JSON line ID must not be assumed to be the same ID. The archived Ametystová link `line=176` displays 245; the JSON calls its 245 route ID 245. Join on node and display name only as a dated cross-check, not proof that records or routes were unchanged between snapshots.

The archived official list labels the page as Prague stops; the page uses `in_prague=1`, and its links use `inprague=1`, as documented in `../task4_v127_prague/README.md`. This is a provider listing classification; a separately verified administrative polygon was not used. Fare zone is not an administrative boundary. PID's GTFS documentation specifically defines `zone_region_type=1` as a stop in the capital city, while `zone_id` is a fare classification and a physical post can have multiple virtual fare-zone records. The present JSON check does not establish equivalence between these fields and the archived page flag.

## Timetables and inclusion gates

A list entry and route link support a published route–stop association in that archived webpage snapshot. They do not alone establish that an actual public departure operates on a chosen day, during daytime, or throughout a year. In the two test requests, the server returned the same generic HTML shell (identical hash), rather than independently recovered dated timetable content. The archived Albertov X90 link itself had a short-term/disruption icon with expiry on 2026-11-10; this also shows that replacement and short-lived routes can be present. Do not infer a historical date's service from the newer JSON.

Official PID [bus information](https://pid.cz/autobusy/) describes Prague city buses 100–299 and night buses 901–917; regional and airport services use other ranges or labels, and the same page describes seasonal cycle buses. Numbers and published documents can change. The [PID 2026 fare guide](https://pid.cz/wp-content/uploads/ke-stazeni/tiskoviny/2026/T2603-DLP.pdf) distinguishes school lines 251–299 and groups buses and trolleybuses in the classification. PID's [service calendar](https://pid.cz/jizdni-rady-podle-linek/kalendar-provozu/) notes dates when school services do not operate. [Seasonal service notice](https://pid.cz/sezonni-vlaky-privozy-i-cyklobus-brdy-letos-naposledy-vyjedou-1-listopadu/) states the 2026 Brdy cycle-bus season ended November 1. A numerical range is a useful conservative route subset only where its interpretation matches the metric; it is neither a complete bus inventory nor a substitute for mode or calendar evidence.

For a strict dated public-passenger bus supply estimate: (1) declare the source-defined counting unit and geographical classification; (2) retain distinct target units after handling duplicates and metro overlap; (3) establish `type=bus` from a version-matched official mode crosswalk, including exclusions for trolleybus and non-passenger auxiliary points; (4) decide explicitly whether night, replacement, school, seasonal, regional, and special-tariff lines meet the estimand; (5) establish at least one allowed public pickup/dropoff in the relevant date/time window from dated schedule and service-calendar evidence; and (6) record unmatched, changed, exceptional and uncertain records rather than silently counting them. If the outcome is instead **source-defined nodes associated with published bus routes**, report precisely that narrower unit and snapshot, with timetable and cross-date limitations.

PID documents that the GTFS stops file covers stops used on at least one day of the feed, not necessarily every day; it also includes non-stop nodes and boarding areas. Its `routes.txt` has `is_night` and `is_substitute_transport`, and schedule/calendar and stop-time files are required to establish date-specific service. These observations do not imply that any GTFS feed was obtained or joined in this audit.

## Reproduction

From this repository root, verify saved bodies using the manifest:

```bash
python - <<'PY'
import hashlib, json, pathlib
p = pathlib.Path('research/2026-a/data/current_prague_node_semantics')
m = json.loads((p / 'manifest.json').read_text())
for r in m['requests']:
    if r.get('file'):
        b = (p / r['file']).read_bytes()
        assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256'], r['file']
print('verified', sum(bool(r.get('file')) for r in m['requests']), 'raw response bodies')
PY
```

The two generic timetable response bodies are retained as received and must not be treated as extracted timetables. No bus-node count, primary input, model, manuscript, registry, or other team's work was modified.

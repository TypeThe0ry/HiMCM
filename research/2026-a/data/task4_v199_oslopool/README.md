# Oslo pool source corroboration (V199 candidate only)

## Result

The current Oslo municipality swimming-hall directory names eight indoor municipal halls and the seasonal outdoor Frognerbadet. The archived directory index response supplies one physical address and a map coordinate per named entry. The municipal page describes the directory as facilities operated by Oslo municipality; venue pages show public ticket purchase. This is useful source-quality context for the Oslo pool indicator.

This capture does not authorize a count replacement or supplement. It is a current 2026 website snapshot, not a reconstructed 2021 inventory. The official 2025–2034 sports-needs plan says Tøyenbadet was completed in 2024, Stovner bad opened in 2026, and Frognerbadet rehabilitation is proposed during the plan period. These dated changes demonstrate that the live named set cannot be projected backward onto 2021. The original user pool point is `pools_per_100k = 5.29` for 2021, with `helper_pool_count = 37` and `flag = ok`; this package cannot certify or recompute that rate. Preserve it unchanged. The separate user-supplied population is 727,797 for 2025; it is not the pool-point year. Do not combine the 2026 directory count with that population or infer a replacement rate/count.

The directory covers municipally operated venues, not private/member facilities, every school pool, or every public pool in Oslo. It establishes venue operation and ticketing, not that every teenager can use every pool at every time. Pages state that children under 10 and nonswimmers require continuous adult supervision; some pool space is reserved for organized lessons or training. Frognerbadet is an outdoor seasonal venue; Tøyenbadet's outdoor area is also seasonal, but it is part of the same physical facility and is not an additional venue. No venue is classified as children-only from these records; child-specific pools or sections remain part of their parent physical venue. Pool basins, lanes, and pool areas are not counted as facilities. The sports plan's proposed rehabilitation is a future plan item, not proof of a current closure.

No model, CSV, navigation, or P file was changed. This is supporting source evidence for the root audit only; it is not an admission or score change.

## Sources captured

1. Oslo municipality, [Svømmehaller i Oslo](https://www.oslo.kommune.no/natur-kultur-og-fritid/svommehaller-i-oslo/), retrieved 2026-11-10 UTC. The archived HTML page identifies the directory as municipality-operated and configures its searchable directory. The directory's public search response is archived separately with request URL, method, body, UTC capture time, status, response headers, and SHA-256 in `directory_search_retrieval.json`.
2. Oslo municipality, [Behovsplan for idrett 2025–2034](https://www.oslo.kommune.no/get-file/1122656/3c643686920a04b1d511fca5aaa16f191c43d95016505073a9a76535e78eedc4/), retrieved 2026-11-10 UTC. The original PDF is preserved. `sports_facilities_plan_extracted.txt` is a `pdftotext -layout` convenience extraction; cite the PDF, not the extraction.

## Reproduction

Run `python extract_directory.py` to regenerate `directory_facilities_extracted.json` from `directory_search_response_original.json`. That output keeps the distinct physical facility names, official venue-page URLs, record update timestamps, addresses, WGS84 coordinates, and page text snippets. The eight indoor rows and Frognerbadet are separated by facility type in the report; the extraction flags Frognerbadet as seasonal outdoor. Review any proposed interpretation against the preserved originals.

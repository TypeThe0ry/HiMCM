# Zürich Urban Audit boundary: official 2024 geometry and 2021 correspondence

GISCO's 2024 Urban Audit per-unit region file identifies `CH002C` as `Zurich (greater city)`, category `C`, and records `FUA_CODE=CH002F`. It contains one Polygon in EPSG:4326 at the published 1:100,000 resolution. The corresponding `CH002F` region is named `Zurich`, category `F`, and contains one MultiPolygon. The points repeat the same identifiers and labels. They are different geographic levels, and neither the label nor polygon establishes the perimeter used to produce the 2024 commute statistic.

The official [metadata](https://gisco-services.ec.europa.eu/distribution/v2/urau/urau-2024-metadata.pdf) says the dataset includes revisions through 1 January 2024, geometry derived from EuroBoundaryMap 2025 with LAU reference date 1 January 2024, and publication in December 2025. It defines C as City and F as Functional Urban Area. The GISCO [per-unit index](https://gisco-services.ec.europa.eu/distribution/v2/urau/urau-2024-units.html) explicitly links each downloaded feature. The [release notes](https://gisco-services.ec.europa.eu/distribution/v2/urau/urau-2024-release-notes.txt) say that the 2021 and 2024 releases are based on Census, degree of urbanisation and commuting data; the 2024 Norway code update does not say the Swiss perimeter changed. No claim is made about survey-specific boundary vintages.

Eurostat's [correspondence page](https://ec.europa.eu/eurostat/web/nuts/local-administrative-units) labels `CITY-LAU-2021.xlsx` validated and 2021. Its `CITY_LAU2021` sheet associates 22 LAUs with CH002C, including Zürich `CH_CH0261`; `city-lau-2021-CH002C.csv` is a direct row extraction. The same table also links the separate Winterthur city `CH007C` to `CH002F`. This 2021 correspondence has not been established as the municipality membership of the 2024 GISCO geometry or the commute data. No 2024 CITY–LAU table was identified in the examined page.

## Captures and reproduction

- `files.raw`, `units.raw`, `metadata.raw`, `correspondence.raw`: responses to the four sources linked above (files index: https://gisco-services.ec.europa.eu/distribution/v2/urau/urau-2024-files.html). `metadata.raw` is a PDF.
- `CH002{C,F}-{label-4326,region-100k-4326}-2024.geojson`: direct responses from the exact relative links in `units.raw`, resolved under `https://gisco-services.ec.europa.eu/distribution/v2/urau/`.
- `city-lau-2021.xlsx`: https://ec.europa.eu/eurostat/documents/345175/501971/CITY-LAU-2021.xlsx, linked by the correspondence page. `extract_2021.py` derives the CSV using openpyxl.
- `release-notes.txt`: release notes above. Each downloaded response has a sidecar `.headers` retaining actual curl status/response headers including redirect hops, with Set-Cookie fields omitted from the public copy and `.utc` recording UTC immediately before the request (except `correspondence.utc`, recorded immediately after the request). `SHA256SUMS` binds downloaded bodies and extraction artifacts. These are local captures; URLs can serve later revisions.
- `AREA_SQM` appears in GISCO properties, but its unit was not verified; no area interpretation is asserted.

GISCO distribution is subject to its linked download provisions and attribution. No map, replacement input, or model change is implied.

Administrative boundaries: © EuroGeographics. Source: Eurostat—GISCO, Urban Audit2024. The archived metadata specifies acknowledged non-commercial use; these captures support the HiMCM research record. No publication map is produced in this package.

`public_header_redactions.json` records omitted cookie fields and original/public header hashes. Original header copies remain outside Git; downloaded data bodies and their checksums are unchanged.

For the openpyxl-based correspondence extractor, use `UV_CACHE_DIR=/data/scratch/uv-cache uv run --with openpyxl==3.1.5 python research/2026-a/data/current_zurich_boundary2024/extract_2021.py` from the repository root. The independent combined audit uses the same pinned package; uv provides an isolated environment.

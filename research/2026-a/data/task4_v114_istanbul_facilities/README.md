# Istanbul 2025: verified public-facility lower bounds

Two previously unknown facility indicators gain evidence-based lower bounds. Both upper bounds remain 1 because the source lists are subsets, not complete inventories of all public providers. Existing weights, population denominator and utility anchors are unchanged.

| Indicator | Verified count | Density per 100,000 | Utility interval |
|---|---:|---:|---|
| Physical public transport stops | at least 12,426 | at least 78.874941 | [0.6120269803, 1] |
| Public swimming venues | at least 24 | at least 0.152342 | [0.1322018835, 1] |

## Transport evidence

The original [IETT 2025 activity report](https://www.iett.istanbul/BBImages/Slider/Image/2025_iett_faaliyet_raporu_-16923.pdf) is saved byte-for-byte as `iett2025.pdf` with its SHA256. PDF page 63 (printed 124–125) states that installation of Braille/QR signs was completed at 12,426 stops across Istanbul in 2025. PDF page 91 (printed 180–181) independently distinguishes the actual count, 12,426, from the target, 7,000. These are physical stops with installed signs, not routes, passenger trips or repeated visits. `transit_verified_pages.txt` is extracted text, not another original source.

The same report lists an operator-wide open/sheltered-stop inventory of 16,134. This larger number is not substituted for a complete all-mode city inventory. The conservative lower bound uses the explicitly in-city, physically equipped subset. The official administrative count is accepted as distinct stops; no separate GTFS geocoding or spatial deduplication is claimed. Network stop supply does not measure a high-school student's travel time or accessibility.

## Swimming evidence

The official [IBB article dated 1 January 2025](https://istanbulseninhaber.ibb.istanbul/haber-detay/emeklilere-1-tlye-yuzme-ve-fitness-salonu) has separate fitness and swimming venue lists. `pool_venues2025.csv` contains the 24 distinct venues in the swimming section only. Each named venue counts once, regardless of the number of pool basins. The article advertises paid public swimming membership; the specific 1 TL offer is for pensioners and older people, not a high-school discount. This establishes public operation, not guaranteed access for every teenager, year-round opening, free entry or spare capacity.

This list was manually transcribed from a successful official-page rendering on 2026-11-08. Original HTML bytes were not downloaded: subsequent direct attempts and refetches failed. `pool_source_verification.json` identifies the successful rendering and the limits of the extraction. `failed_pool2025_refetch.json` is explicitly the failed later retrieval, never the source of the 24 names. An independent agent checked indexed official-source excerpts and the separate 2025 student discount announcement; its crosscheck is stored in `../task4_v114_istanbul_safety/`. The current Spor Istanbul facility and membership page downloads returned HTTP 403 and are preserved as failed acquisitions in the manifest, not used as evidence.

The pool list is a January 2025 snapshot and is paired with December 2025 population, not a claim about daily or all-year operation. Broader public, district, nonprofit and other venues are unknown, so there is no justified finite upper count. Membership rules and facilities can change; the current 2026 web directory is not relabeled 2025.

## Denominator and calculation

Population remains 15,754,053, the previously verified 2025 Istanbul province count in `../task4_v7_istanbul/official_web_verified_values.json`; its hash is recorded. For count lower bound n and population P, density is d=100000n/P. The utility lower bound is d/(a+d), with existing anchor a=50 for transport and a=1 for pools. The upper utility remains 1.

Run `python3 data/task4_v114_istanbul_facilities/extract.py` from `research/2026-a`. It verifies source hashes, the actual/target stop distinction, same-year denominator and 24 unique pool names, then writes `observations.json`. The manual source transcription remains a human-readable provenance dependency rather than an automated original-HTML extraction claim.

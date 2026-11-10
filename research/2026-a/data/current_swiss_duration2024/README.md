# Swiss national work-duration bins, 2024

The Federal Statistical Office publishes five work-journey duration bins for Switzerland in 2024. This is a usable national source with explicit unknown-duration coverage, but it cannot tighten the retained Zurich city interval. Its national resident-worker population differs from the incoming/internal commuters and greater-city boundary associated with the separate Eurostat candidate.

The [official table](https://statistik.admin.ch/de/asset/36351624), number `T 11.4.4.3`, was released on 29 January 2026 and covers 1990, 2000 and 2010–2024. `duration.xlsx` is the linked original response; `asset.html` preserves the metadata identifying Switzerland as its geography. `retrievals.json` records exact URLs, retrieval times, statuses, byte counts and SHA-256 hashes. Source: Swiss Federal Statistical Office; OPEN-BY, attribution required. The 2024 observations are not relabelled as a 2025 baseline.

`selected_2024.json` extracts sheet `T 11.4.4.3`, columns AV–AX, rows 15–22 and methodological notes. The five categories are 0–15, 16–30, 31–45, 46–60 and more than 60 minutes for one outward journey. Shares use commuters with known duration as their denominator; unknown-duration commuters are listed separately. Counts are survey-weighted population estimates and retain their source precision. The VI column is copied as reported, without treating it as a bound on individual travel times.

The source includes employed residents aged 15 or above with a fixed workplace outside their residential building; it excludes specified collective-household and diplomatic groups. This is not an upper-secondary student sample. The open-ended final bin is not a finite maximum travel time. National bin frequencies are not transferable to a city without an additional sampling and geography justification.

Run `python research/2026-a/data/current_swiss_duration2024/extract.py` to validate both receipts and print the deterministic selection to stdout. No model input is written. New primary admissions and actual primary score-width reduction are both zero.

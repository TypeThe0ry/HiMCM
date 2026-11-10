# Zurich broadband source match

The retained 16-city intake lists Zurich broadband at **286.35 Mbps** for 2026 with flag `ok`. The archived Speedtest Global Index contains the same value in its **fixed broadband median download** table for **Zürich, Switzerland**, at rank 18. The archived page is labeled **September 2026**. Its footer says results are updated mid-month for the previous three months; the saved city row does not give exact start and end dates, so the publication label should not be presented as a 2025 annual observation or as an exact single-month measurement.

This is a point-source match against a publisher archive already retained for the Oslo check. It confirms that the number and statistic can be found in that source. The original intake CSV does not record an extraction URL or time, so the match cannot establish that this was the team's extraction route. The page also does not establish that Ookla's Zürich city area is equivalent to Zurich city proper. The archive manifest's access date is 2026-11-07; no UTC retrieval timestamp is recorded.

The exact archived row, hashes, source path, line and byte coordinates are in [`source_reuse_receipt.json`](source_reuse_receipt.json). The source is referenced in place at `research/2026-a/data/task4_v5_resources/ookla_global_index.html`; it is not duplicated here. The independent extractor checks the archive against its manifest, matches the city row inside `column-fixedMedian`, and checks the original CSV value, year and flag:

```sh
python research/2026-a/data/current_zurich_broadband_source/extract.py
```

The result documents Zurich's broadband point for provenance. No input value, flag, model, model run, paper, or registry was changed. No primary admission or uncertainty-width reduction is claimed. The existing equal-weight ignorance-stress calculation remains as registered; this source check does not itself quantify a change to that stress result.

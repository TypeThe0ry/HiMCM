# São Paulo first-school chain audit

None of V48's 15 unresolved non-home first-school journeys can be recovered as a documented transport-only home–school chain. All have one intermediate stop: 5 commerce work, 8 services work, and 2 personal affairs. The original Portuguese layout codes establish these purposes. A two-minute commerce-work stop remains work; elapsed time alone does not establish passenger drop-off or transfer.

All 15 chains have consecutive journey numbers, a common reported date, matching reported purpose and zone at the intermediate stop, clocks consistent with reported durations, and non-overlapping pre-school journeys. These checks establish diary continuity, not transport-only intent. Zone equality is coarser than exact location equality. The 60 passenger-service origin/destination fields are raw `N`; the layout documents numeric `1`/`2`. This audit preserves that encoding difference and does not invent a translation or affirmative service flag.

The 1,489 direct journeys, 186 students without a recorded school journey, and these 15 unresolved students retain their V48 bounds. All 1,690 are current high-school students aged 14–18 living in municipality 36. The point interval remains [0.4608835465, 0.5882776733], with exploratory household-bootstrap envelope [0.4417949654, 0.6071350870]. No input changes means no change to the paired V48 bootstrap replicates; no duplicate bootstrap is run. No ranking change or narrower champion set can be attributed to this audit.

`audit.py` reads the existing V10 compressed DBF and XLSX, verifies the decompressed source hash, and selects the V48 person IDs. Run with Python plus `dbfread`:

```sh
python research/2026-a/data/task4_v49_saopaulo_chains/audit.py
```

`chain_audit.csv` contains all 15 checks and unchanged person bounds; `summary.json` records codebook excerpts and counts; `manifest.json` hashes the reused inputs. Source provenance remains the existing public research mirror; official byte identity has not been established. Reported dates and day codes are retained separately without calendar recoding. This bounded audit changes no model code, manuscript, or source file.

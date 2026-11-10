# A378-group candidate has a measurable conditional effect

Substituting378 Vienna DIVA groups for the retained99 metro subset in a temporary copy raises its transport utility lower endpoint from0.0889328463 to0.2715128112. Population2,028,399 and anchor50 stay fixed. Only that lower cell changes; the other159 lower cells and all160 upper cells remain unchanged. Bus and metro counts are not added.

Under fixed weights the candidate mean score-interval width is15.7767827274 instead of15.8223269533, a conditional reduction of0.0455442259 points. Under equal weights it is18.3021208336 instead of18.3918116239, a conditional reduction of0.0896907903 points. Conservative choices remain Oslo and Zurich respectively; all four cases retain16 possible and0 necessary champions. These are **candidate-copy results**, not an activated model improvement or a certain champion.

`station_witnesses.csv` preserves one source stopping-position/GTFS call witness per candidate DIVA, including trip, service, route, pickup/drop-off and source coordinates. `excluded_mixed_modes.csv` retains52 same-name groups screened for active nonbus modes. `bounds.csv` has320 baseline/candidate utility records and `ranks.csv`64 city/scenario/weight records. The summary records94 active services,35,541 active trips and8,853,107 scanned stop-time rows. It counts68,682 qualifying A-route calls before taking one witness per group; calls, platforms and routes are never counted as separate DIVA areas.

The [source note](../../data/current_vienna_gtfs/README.md) explains the exact-name/coordinate bridge, source-defined DIVA unit, all-known-position city test, cross-date snapshots, service-day convention and lossless storage. No stop-ID prefix or invented proximity cluster defines the group. Public-service eligibility of all exceptional trips and full scientific integration remain pending; nonbus screening is not an exhaustive cross-alias mode audit. The original99 lower bound stays authoritative, primary admissions and actual primary interval improvement are zero, and paper assets remain unchanged.

Reproduce into a new external directory using the locked environment:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_vienna_gtfs_candidate.py --output-dir /data/scratch/vienna-gtfs-candidate-new
```

The source files are substantial; the extractor streams stop times from the lossless archive. Independent checks separate original-byte recovery, calendar/call/crosswalk structure, scalar score correctness and pending real-world eligibility. MC, future scenarios, manuscript integration and server compilation have not been run for this candidate.

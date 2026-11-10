# All88 witness routes have public passenger catalogue entries

`catalogue_entries.csv` retains93 entries for89 A-route names, including the duplicate citybus/callbus and weekday/weekend versions. `route_coverage.csv` joins the378 chosen station-area witnesses to88 route names and records each route's headings, source categories and conditions. Every witness route is advertised in the operator's passenger timetable catalogue.

The nine condition-bearing route names are41A,43A,56A,58A,73A,74A,86A,89A and92A. Their selected witnesses represent36 distinct DIVA groups; a conservative withhold leaves342. This counts selected witnesses, not all available trips or all ways to qualify those groups. Winter, detour, weekday and callbus labels remain visible. File `Stand` labels are not converted into effective dates, and current catalogue dates are not substituted for the frozen GTFS service calendar.

The independent semantic decision supports a source-defined scheduled-public-supply subset. It does not certify actual operation, universal access or individual linked-PDF conditions. Fourteen document responses are retained as unusable HTML, with zero original PDFs admitted. The earlier structural record's unresolved public-nature question is answered by this new evidence; its historical record remains unchanged.

Reproduce with the locked environment into a new external directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_vienna_passenger_qualification.py --output-dir /data/scratch/vienna-passenger-qualification-new
```

The audit checks both raw index receipts, all14 rejected response bodies, every candidate route, condition counts and exact reproduction of three derived files. Source qualification does not activate a new primary model or edit the manuscript; subsequent V204 scientific staging retains those boundaries.

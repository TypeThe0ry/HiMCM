# Count teacher FTE once per institution and retain site candidates

The joined2025 research table has154 pupil UAIs and153 teacher matches. A single teacher record per UAI prevents an extra1,870.52 FTE from entering through the27 GT/PRO overlaps. The matched institution FTE sum is7,920.09; the missing UAI0754401B has117 GT pupils and retains an empty teacher field. No city ratio is calculated.

`pupil_teacher_join.csv` records the two pupil-stream presence flags, their values, teacher presence/FTE/type/sector and the current annuaire candidate count and post-bac state. An absent stream is blank with a false presence flag; it is not an observed zero. Whole-institution teacher FTE and pre-baccalaureate pupil totals do not identify upper-stage teaching allocation.

`annuaire_candidates.csv` retains all246 original candidate rows from the lycée-filtered response and the separate exact-UAI EREA query. `annuaire_key_review.csv` groups them into240 keys with full flag/contract sets; no first/last row wins. Six UAIs have multiple candidates, four with differing site flags. Within the154 pupil keys, the states are88 post-bac,60 no-post-bac flag,4 mixed and2 unknown. The latter two categories are retained explicitly; the60 no-post-bac flags are also current observations, not a2025 stage-allocation certificate. Three EREA keys explain the lycée-filtered misses without changing institution type.

`summary.json` records only source-join counts and sums. The [source note](../../data/current_paris_teacher_join/README.md) explains the075/75 coding correction, institution/site distinction, provider exclusions and snapshot dates. Primary Paris PTR utility remains`[0,1]`; neither the original data nor the model or manuscript changes.

Reproduce into a new external directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_paris_teacher_join.py --output-dir /data/scratch/paris-teacher-join-new
```

The independent audit checks seven response receipts, archived field/scope metadata, unique teacher and pupil keys, all candidate rows and exact decimal FTE sums, the missing record and all154 joined rows. Four derived files are replayed byte-for-byte. Scientific and paper inputs remain protected; no city ranking, MC or TeX replay is claimed.

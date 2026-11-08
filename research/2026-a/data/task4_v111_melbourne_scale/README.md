# V111: current Melbourne direct scale sensitivity and verified NYC reuse

`reproduce.py` rebuilds the current V44 Melbourne target from the original person, education-journey and destination-stop files. It applies `exp(-elapsed_minutes/tau)` at tau15,20,30,45,60 and repeats the original linear jackknife endpoint calculation with all10 official person replicate weights, variance factor9/10 and t9 critical value. Tau30 reproduces **[0.23979992183224927, 0.7927869308191794]** and all20 archived endpoint replicate estimates within1e-14. No obsolete V23 roster is used.

The target remains weekday Greater Melbourne residents reporting Secondary study and ageband15–19; it does not become exact14–18 or City of Melbourne municipality. Of171 eligible records,170 have complete main/replicate weights. Among those170,100 have a verified secondary-school destination and valid elapsed duration; the other70 retain[0,1], including63 with no recorded journey. The remaining person's unbounded missing weight means the strict full171-person target still has interval[0,1] at every scale. Reported model-comparable scenarios therefore remain conditional on the same complete-weight target. The linear endpoint envelope is unchanged methodology, not a new simultaneous-coverage claim.

NYC uses the existing V26 paired-bootstrap scenarios only after verifying all archived source hashes, rebuilding the V21 roster from the original ZIP and checking the603 people,410 observed journeys,5766 households and archived roster fields. Under19 membership remains460 known and33 optional. Tau30 exactly matches current V21 sampling bounds. The historical household bootstrap was not rerun: input identity, membership and output consistency gave no reason to do so. Its original historical2010–11, unknown-age and exploratory fixed-weight bootstrap limitations remain.

`summary.json` contains ten standardized `scenarios`: city, tau_minutes, utility_lower/upper (the model-comparable sampling envelope), and point_lower/upper (identification bounds). Detailed Melbourne endpoint replicates and verified NYC reuse metadata are retained separately. `sources` records hashes. No personal records are emitted or copied into this directory; historical files, model and registry are unchanged.

```sh
python3 research/2026-a/data/task4_v111_melbourne_scale/reproduce.py
```

These five scales are discrete sensitivity scenarios, not a proof over every intermediate scale. Recomputing sampling intervals at another scale does not automatically inherit containment in distribution-free bounds transformed from the tau30 interval; they are separate inferential constructions.

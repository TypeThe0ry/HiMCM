# Participation, interest and barriers answer different questions

Oslo's2026 main report gives a direct school-grade comparison: reported sports-club participation during the preceding month is74%,68%,57%,46%,38%,31% across grade8 through Vg3. The displayed endpoint difference is43 percentage points. This cross-sectional profile shows why a citywide supply count cannot stand in for the same reported activity at every school stage. It does not estimate how an individual changes with age or supply age-specific model weights.

Among respondents who had not visited a youth club in the previous month,5% were very willing and18% might visit in the coming months. Their displayed sum is23%. Non-attendance therefore must be distinguished from expressed interest. The item denominators and joint responses were not obtained; multiplying this conditional percentage by a participation percentage from another question would not recover an observed proportion of all pupils.

In the separate reasons chart for non-attenders, sums of the two stronger displayed response categories are: school time44%, other regular activities43%, no suitable activities36%, not fitting in30%, no companion25%, distance9%, cost6%, parental permission3%. These nonexclusive reports distinguish practical barriers from competing activities, time and fit. They do not attribute causes, establish that costs are unimportant for every group, or transfer to swimming facilities. The financial-constraint item in the earlier district tables has a broader activity scope and a different respondent base.

`grade_participation.csv` preserves36 grade/activity cells; `club_reasons.csv` preserves32 response cells and their explicit sums; `club_willingness.csv` preserves4 cells. `summary.json` contains the derived quantities and population boundaries. Root visually checked all72 source cells on physical pages35/39; a bounded independent review separately checked the six sports-grade values, four willingness cells, the16 stronger barrier cells and methods. Those checks do not claim access to survey microdata.

Reproduce with a new external output directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_oslo_youth_main.py --output-dir /data/scratch/oslo-main2026-new
```

Extraction uses layout text for grade rows and raw text for the small adjacent barrier labels. All four derived files are checked against a fresh extraction. Source metadata, PDF text/identity, receipts and unchanged scientific/manuscript inputs are checked separately. No MC or TeX run is needed for this research-only package.

Primary admissions and actual primary interval-width improvement are zero. V203 remains fixedOslo/equalZurich with16possible/0necessary champions; original inputs, score rules, current manuscript and PDF are preserved. The earlier upper-stage source quarantine remains in force. Paper integration requires a specific authorised revision scope.

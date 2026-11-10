# Complete the provider bridge before validating the city count

`crosswalk.csv` links all27retained DBH provider codes to national NOKUT identities, increasing identity matches from25to27. All25positive reported codes in each examined semester now have a bridge. The two additions, NSKI and Norsk Gestaltinstitutt, remain programme-accredited-only institutions; the distinction from institutional accreditation is preserved. The inherited25rows are unchanged.

`location_flags.csv` records the exact DBH organisation numbers and municipality-coded campus observations beside the current registered business municipalities. Code1405has an Oslo-versus-Bærum discrepancy, also informed by the2024NOKUT report and current Sandvika course location. The flag prevents a successful identity match from being mistaken for a verified Oslo campus. No provider is excluded, no source count is corrected and no new score scenario is inferred from this discrepancy. NSKI's registered address agrees with Oslo, which alone does not certify all its campuses.

`summary.json` keeps the original source-lineage, city-inventory and accreditation-time qualifications false. The previous23identity matches among25positive codes were a different set from the23selected by teaching modes1/4; the completed25identity set also remains distinct from that teaching-mode subset. No filter is substituted for another. Definition-sensitivity results23/25/26/27remain historical controlled alternatives, not verified inventory bounds.

Reproduce into a new external directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_oslo_he_identity_completion.py --output-dir /data/scratch/oslo-he-completion-new
```

The current112-point ledger updates only Oslo HE's evidence path, scope description and next-evidence need. Original values/years/flags/utilities, classification, priorities and every other point remain fixed. All source receipts, inherited decisions, bridges, organisation numbers, geography flags and three derived files are independently checked. The numerical16-city model and manuscript are preserved; no MC or TeX rebuild is claimed.

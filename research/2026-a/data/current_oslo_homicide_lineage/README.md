# Oslo 2008 homicide point: bounded source check

**Classification suggestion: reviewed; original rate and extraction lineage unresolved.** The current Eurostat crime tables publish 12 for 2008 and Oslo code NO001C, matching the supplied numerator, but their published rate is **2.14 per 100,000**, not the supplied **1.71**. This is a count-only numerical match, not identification of the supplied source or proof of an error in it. Recommend zero primary admissions from this packet.

The preserved [team input](../task4_v117_team_intake/city_indicators.csv) identifies the 1.71 rate as 2008 and STALE, gives a numerator of 12, and separately lists 727,797 for 2025 as city-proper population. Its [intake audit](../task4_v117_team_intake/issues.csv) already noted the rate/year/denominator mismatch and [intake README](../task4_v117_team_intake/README.md) states that original URLs, row details and extraction rules were not supplied. The prior [bounded point ledger](../../results/current_point_source_ledger/README.md) did not classify this cell; that does not mean it had never been reviewed.

## Archived official extracts

- [Eurostat offences response](eurostat_offences_2008.json): `CRIM_HOM_OCIT`, annual `A`, `NO001C`, 2008, `NR` = 12 and `P_HTHAB` = 2.14. Its current geography label is “Oslo (greater city)”. The response reports its dataset updated 2026-04-29.
- [Eurostat victims response](eurostat_victims_2008.json): `CRIM_HOM_VCIT`, sex total `T`, otherwise the same year, geography, units and values. Offences and victims are separate statistical concepts, even though these cells agree numerically.
- [Eurostat methodological guide, pp. 11–12](eurostat_guide_2008_2016.pdf), distinguishes city proper from wider agglomeration, recommends matching numerator and population geography, and describes using 1 January Urban Audit population for city rates. This general method does not establish the precise boundary or denominator used in the particular 2008 cell. [Crime metadata](eurostat_crime_metadata.html) supplies current dataset context; it cannot establish the original input's extraction vintage or historical definition.

The present label alone does not prove the historical 2008 boundary. The Eurostat value is a current published historical-series extract, not the original source or an original 2008 publication. The exact source, numerator definition, geographic scope, historical denominator and computation of 1.71 remain unknown. The separate 2025 population is not evidence of that rate's denominator; do not combine it with the 2008 count as a correction. No CSV, model, registry or manuscript was changed.

[sources.json](sources.json) records request URLs, retrieval timestamps, file sizes and SHA-256 of the unchanged responses; [scope.json](scope.json) records the input and bounded comparison. Verify with the following command from the repository root:

```bash
python3 -c 'import json,hashlib,pathlib; p=pathlib.Path("research/2026-a/data/current_oslo_homicide_lineage"); s=json.loads((p/"sources.json").read_text()); assert all(hashlib.sha256((p/x["file"]).read_bytes()).hexdigest()==x["sha256"] for x in s["sources"]); print("all archived source hashes match")'
```

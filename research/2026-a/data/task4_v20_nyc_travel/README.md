# Reported journeys of current NYC high-school students, 2010–2011

The official NYMTC/NJTPA Regional Household Travel Survey supplies household, person and linked-trip records. Current enrollment is directly reported: `STUDE` is full- or part-time and `SCHOL` is Grade 9 to 12. This uses neither adult commuters nor completed educational attainment to identify high-school students. The records are historical, not current 2026 travel estimates.

Original downloads and SHA256 are in `download_manifest.json`; dictionary locations and source checks are in [README.source.md](README.source.md) and `source_schema_audit.json`. The original 34 MB ZIP is retained; large CSV members are read directly from it without adding oversized uncompressed files to Git.

## Population and journey definition

NYC residence uses the five county FIPS codes in the household file, checked against person-file county labels. Among 11,732 NYC roster members, 479 report current grade 9–12 enrollment; three are homeschooled and excluded from this physical-school target. All 476 remaining members retain their person-file `HH_WHT2` weights. The person and household fields differ slightly in published decimal precision, so the extractor uses a documented floating tolerance and consistently preserves person weights.

A school-purpose journey has destination activity 12 (class/study) or 13 (other school activity). Select the first such linked trip within each person's 03:00-to-02:59 diary day. Its origin must be home and duration positive and consistent with departure/arrival clocks. Transfer legs are already linked. `LTRIPNO` alone resets within tours: `(SAMPN,PERNO,TOUR_ID,LTRIPNO)` is unique, whereas omitting `TOUR_ID` produces 34,072 duplicates. The extractor sorts clocks rather than the resetting number.

Of the 476 known members, 365 have a qualifying reported journey; 92 have none and 19 first reach a school-purpose destination from elsewhere. These 111 persons remain in the denominator with utility [0,1]. They are not silently excluded, assigned a zero-minute commute, or treated as zero utility. This estimates an interval for the roster target's travel utility, not merely a mean among observed journeys. Purpose codes identify class/study activity but do not independently authenticate the usual school campus: 360 of the 365 destinations lie in the same positive TAZ as the roster's usual school. Same TAZ is only a consistency check, not exact school identity.

The roster also has 127 optional members: 21 current students with DK/RF school level, 73 with Other school type, and 33 with unknown student status. Optional inclusion preserves uncertainty rather than assigning them to high school. Of these, 37 have a qualifying journey. The default target includes all reported current high-school ages; the known cohort contains 10 aged 19–24, two aged 35–54 and four with unknown age. These anomalous/older records are explicit rather than silently cleaned away.

The under-19 alternative retains 460 known current high-school members and 33 optional members. Known adult ages are outside that target; unknown ages remain optional. Age does not substitute for current school level, and no lower age cutoff is inferred from the coarse Younger-than-16 category.

## Utility and optional membership

For a reported duration t minutes, u=exp(-t/30). A missing or unqualified journey has [l,h]=[0,1]. With known members K, optional members O, weights w and inclusion z in {0,1}:

    L = min_z (sum_K w*l + sum_O z*w*l)/(sum_K w + sum_O z*w)
    U = max_z (sum_K w*h + sum_O z*w*h)/(sum_K w + sum_O z*w).

Sorting optional lower endpoints ascending (upper endpoints descending) and checking every cumulative prefix gives the exact ratio extrema. The independent audit additionally solves a Charnes–Cooper linear program directly from the raw data and reproduces both endpoints.

| Scope | Identification interval | Exploratory sampling envelope |
| --- | --- | --- |
| Known current-high-school cohort only | [.254982,.495318] | Not separately used |
| All-age current high school with optional membership | [.221551,.556605] | [.192461,.606114] |
| Under-19 alternative with optional membership | [.247167,.513389] | [.213981,.562008] |

The envelope uses 1,000 seeded household bootstrap draws within the five residence counties, resampling **all 5,766 NYC sampled households**, including those without high-school members. Same-household persons move together; final weights stay fixed. The lower 2.5th and upper 97.5th percentiles widen, rather than truncate, the original endpoints. Original survey stratification and calibration are not reconstructed, so this is exploratory sensitivity, not an official design-based confidence interval. It does not cover temporal change since 2010–2011 or every reporting error.

## Why the 2024 survey does not replace this with recent minor data

The separately retrieved [2024 NYC coverage audit](../task4_v20_nyc_school_survey/README.md) found a real current-school-type field but adult-only weighted travel diaries. All 286 minor high-school roster members had zero personal weights and no own diary. The 35 weighted adult high-school participants cannot represent the missing minors. No 2024 adult-only utility enters the model.

## Reproduction

```sh
python3 research/2026-a/data/task4_v20_nyc_travel/extract_commute.py
python3 research/2026-a/data/task4_v20_nyc_travel/test_extract.py
python3 research/2026-a/scripts/task4_nyc_reported_travel.py
```

Global admission remains false. [Model comparison](../../results/task4_v20_nyc_reported_travel/README.md) replaces the old 2013–2014 modeled-route alternative; the two years and measurement concepts are not intersected.

# V110: India TUS2024 school-travel source audit

Five official public documents were acquired and hashed from the [TUS2024 catalogue](https://microdata.gov.in/NADA/index.php/catalog/236/related-materials): codes, file layout, field instructions, user note and metadata. This is a new diary-survey route, distinct from earlier NHTS research. **No city indicator is admitted.**

The [person dictionary](https://microdata.gov.in/NADA/index.php/catalog/236/data-dictionary/F2?file_name=tus106PER) has41 fields, including age, district, activity sequence, time fields, activity code, location and weights. Its10,211,478 records must not be called distinct respondents. The household file has37 fields. There is no current-grade/enrollment-stage field in either layout. Highest education means highest *completed* level (instructions PDF43–44, §3.3.7); principal status91 is based on the major activity over the previous365 days (§3.3.8), not direct current attendance.

## The material timing distinction

**Thirty-minute slots, not ten-minute exact episodes.** Instructions PDF59–61 (§3.6.4, §3.6.7, §3.6.10) prescribe48 half-hour slots, at most3 activities per slot, generally recording activities lasting at least10 minutes. Identical consecutive activity patterns can be combined into longer records; multiple activities share recorded slot boundaries. PDF75 also documents recording only the largest activity when all are shorter than10 minutes. Thus a recorded start/end does not supply exact trip departure/arrival, absent travel is not necessarily zero, and repeated slot durations must not be summed as independent travel episodes.

PDF83 labels611 as school/university attendance and640 as learning-related travel. Neither isolates high school, nor does640 isolate home-to-school outward travel. Location is only own dwelling / outside fixed / outside nonfixed ([official field definition](https://microdata.gov.in/NADA/index.php/catalog/236/variable/F2/V74?name=Activity_Location)); it is not a school-location identifier. Dividing daily640 time by2 would impose an unsupported roundtrip symmetry assumption.

## What a legitimate next analysis would require

The [official data access page](https://microdata.gov.in/NADA/index.php/catalog/236/get-microdata) requires login through a free account. No account, identity details or application was submitted; no microdata were obtained. If authorized records become available, retain them local-only and publish only nonidentifying aggregates.

The layout permits Delhi state07 and Mumbai districts22/23 in Maharashtra27, NSSregion271 (PDF94); those domains still require alignment with the model's city definitions and an assessment of sampled target households. Age14–18 and documented611/640 sequences could support a *conditional, coarsened diary-day* study, with ambiguous membership, short omitted activities, simultaneous activities, non-school days and incomplete journeys explicitly retained. It cannot yet identify the model's city-level high-school single-trip utility. Any chronology bounds must be derived from actual records and slot rules, not imputed half-roundtrip times. The user note additionally cautions against deriving standalone population estimates from auxiliary demographic fields.

Run `python3 research/2026-a/data/task4_v110_india/audit.py` to verify hashes and the cited instruction clauses. No model, registry or paper was changed.

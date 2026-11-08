# V96: all Warsaw post-primary youth routes, with adult teacher allocation left unknown

The official **Statistical Yearbook of Warsaw 2025** supplies 2024/25 data for all six source-defined post-primary youth school routes, including public and non-public establishments. Their **119,740 students** can be paired with a partial allocation of teaching FTE: three published teacher groups belong to these youth routes, while the general-secondary group also includes adults. Keeping that allocation unknown gives a conditional resource-utility interval **[0.237543, 0.505125]** after a stated one-FTE outward rounding guard per published teacher cell.

This extends the earlier [V32 general-school-only evidence](../task4_v32_education/README.md). It is not a time-trend estimate, an individual age14–18 statistic, a resident-based school catchment measure or an examination-quality score. This source package has `main_admitted=false`; model admission and its rank comparison are separate decisions.

## Original data and scope

The [official publication](https://new.stat.gov.pl/en/publications-portal/statistical-yearbook-warsaw-2025) links the PDF and Excel ZIP archived here. `manifest.json` records their URLs, original byte counts and SHA-256 hashes. `education2025.xlsx` is the exact `08_Edukacja.xlsx` member of that ZIP, not an independently edited workbook. The text files are derived reading aids.

| Source-defined youth route | Students, 2024/25 | Published teaching-FTE group |
|---|---:|---|
| Special job-training | 404 | Included with stage I |
| Stage I sectoral vocational | 3,900 | 454, including special job-training |
| Stage II sectoral vocational | 480 | 7 |
| General secondary, youth | 87,748 | 5,654, including adult general schools |
| Technical secondary, youth | 26,142 | 2,029, including professional general art |
| Professional general art | 1,066 | Included with technical secondary |
| Total | **119,740** | Adult general-teacher allocation unresolved |

Table12 separates 5,754 adult general-school students from the youth total. Post-secondary and higher education are excluded. Table1's teacher footnotes include special job-training in the stage-I pool and professional general art in the technical pool; no teacher pool is counted twice.

The PDF's general education notes provide the coverage:

- Printed148 / PDF156, §§3–4: government, local-government and other legal/natural providers; public and non-public schools.
- Printed149 / PDF157, §6: all six routes listed above under children/youth post-primary schools, including stage II and professional general art. Primary art schools not granting professional qualifications appear separately under primary education.
- Printed150 / PDF158, §10: adult general schools are separate; former adult vocational/technical programmes had ceased in earlier years.
- Printed151 / PDF159, §§16–17: compulsory educational teaching, full-time and part-time converted to FTE, measured at the beginning of the school year. Librarians, day-room staff and exclusively extracurricular teachers are excluded.
- Printed152 / PDF160, Table1: published teacher pools and student totals. Printed157 / PDF165, Table12: general youth/adult split. Named workbook sheets `1(87)` and `12(98)` reproduce these values.

The source's six-route classification is retained rather than asserting an independently established international ISCED crosswalk or exact pupil ages. School-location totals should not be converted into resident totals: [V95 official flows](../task4_v95_warsaw/README.md) document substantial cross-municipality attendance.

## Resource interval

Let G be youth teaching FTE within the adult-inclusive general-school pool. Before rounding protection, `0 <= G <= 5654`; the other pools sum to `454+7+2029=2490`. Thus published-cell allocation gives `T in [2490,8144]`.

General note14 (PDF22) acknowledges rounding; teacher cells are published as whole FTE in both PDF and workbook. The direction is unspecified. We allow one FTE outward per cell, enclosing ordinary unit rounding or truncation:

`T_lower=(454−1)+(7−1)+(2029−1)=2487`

`T_upper=(454+1)+(7+1)+(5654+1)+(2029+1)=8148`.

This is conditional on unit-rounding error, not a sampling confidence interval or protection against future revisions or arbitrary reporting error. No positive lower allocation is imputed to youth general schools. Using `u_E=15*T/(119740+15*T)` gives the stated utility bounds. The three non-general pools supply the positive lower bound; excluding adult pupils while assigning every general teacher to youth would instead create an unjustified point estimate.

## Verification and reproduction

`extract.py` verifies source hashes and ZIP integrity, matches the extracted workbook member, reads exact XML cells, cross-checks the separate route tables and youth/adult sum, and checks the PDF's scope/FTE/rounding notes. The published overview page was rendered and visually inspected. BDL's youth-specific teacher API request returned HTTP429; it supplied no additional numbers. A historical English note about prior technical-school duration disagrees with Polish; the current five-year definition and observed tables are unaffected and the discrepancy is recorded.

```sh
python3 research/2026-a/data/task4_v96_warsaw/collect.py
python3 research/2026-a/data/task4_v96_warsaw/extract.py
```

Both `extract()` and `main()` return the reconstructed result; `main()` also writes [summary.json](summary.json). No other data, model, registry, ranking or manuscript is changed by this package. Source attribution: Źródło danych GUS. Opracowanie własne na podstawie danych GUS.

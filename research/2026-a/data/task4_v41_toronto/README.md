# Toronto V41 — verified examination denominators

The official EQAO2024–25 achievement downloads supply the examination counts missing in V40. Exact school identifiers join to the municipal roster. **These results describe participating students in publicly reportable schools, not all Toronto students.** Suppressed school counts remain unavailable.

## Results

| Assessment | Roster schools | Matched | Numeric/reportable | Successful | Fully participating | Count-weighted result |
|---|---:|---:|---:|---:|---:|---:|
| Grade9 mathematics, Levels3–4 |155|117|108|12395|21604|57.3736345%|
| OSSLT first-time-eligible, successful |155|132|109|16775|19756|84.9109131%|

Grade9 matched records additionally contain7 nonparticipation records (`Suppressed=3`) and2 privacy-suppressed records (`Suppressed=1`);38 roster schools are unmatched. OSSLT has9 nonparticipation and14 privacy-suppressed records;23 schools are unmatched. None is treated as a zero score. No attempt is made to reconstruct suppressed cells.

In usable schools, Grade9 `cntStudents_All` totals23101; OSSLT `cntEligible` totals21180. These contextual totals are not the achievement denominator. Achievement uses **fully participating students with outcomes**, as defined in the source workbooks. Enrollment in all grades is never used as a test denominator.

## What improves

V40 reported equal-school medians55.5% and84%, because its workbook lacked test counts. V41 now computes `sum(successful)/sum(fully participating)` from observed counts. It correctly allows schools with different tested cohort sizes to contribute proportionally. This is a change of estimand, not evidence that educational performance improved. The values are not a causal or longitudinal comparison.

## Source and join

The [EQAO Open Data catalogue](https://www.eqao.com/about-eqao/open-data/) links the four raw assets preserved here: Grade9 and OSSLT achievement ZIPs plus their2025 aggregate-field definitions. Resource URLs, byte lengths and SHA-256 hashes appear in `manifest.json`. The catalogue was readable with the web tool; a local HTTP request returned403. Direct published download links all returned200. No login or private endpoint was used.

`aggregate.py` reads `G9_2025.csv` and `G10_2025_FTE.csv` directly from those ZIPs. In the latter filename, **FTE means first-time eligible, not full-time equivalent**. It selects `OrgType=S`, joins six-digit `SchoolMident` to the155 four-board V40 school numbers, and verifies board identifiers. It uses the annual `Administration=Overall`, `Eligibility=1` record. Previously eligible records and fall/spring administration tables are not added, preventing repeated counting.

Grade9 numerator `cntOverallM_L34` counts fully participating students at Levels3–4; OSSLT numerator `cntSuccessful` counts successful fully participating eligible students. Both use `cntFullyParticipating`. These meanings are verified against the downloaded definitions, also extracted to text. `ApplySuppression=1` indicates the disclosure-protected release; usable school records additionally require `Suppressed=0` and numeric numerator/denominator.

## Reproduction and validation

Run `python3 aggregate.py`. Outputs:

- `summary.json`: exact counts, rates, coverage and scope.
- `grade9_matched.csv`, `osslt_first_time_matched.csv`: school-level source values, including suppression.
- `*_unmatched_roster.csv`: unjoined municipal school IDs and names.

Checks assert155 unique target IDs, no duplicate school identifiers within each assessment, matching board IDs, annual first-time-eligible OSSLT scope, disclosure-protected release, positive denominators and `0 <= successful <= participating`. The script completed successfully.

## Remaining scope

The denominator problem is resolved for the108/109 reportable matched schools. Participation coverage for the full municipal cohort remains unidentified because unmatched and privacy-suppressed schools have no usable counts here. The roster covers publicly funded district-board schools rather than private schools or all resident adolescents. Grade9 mathematics and OSSLT measure different curricular outcomes; they cannot be substituted for another country's tests without a justified comparison framework. Original city teacher-ratio cells and possible-winner ranges are unchanged. These are verified descriptive education results available for a separately defined achievement model, not automatic replacements in the existing model.

## Nonparticipation diagnostic within the same reporting schools

For the same108/109 usable schools, define `E` as registered assessment students (Grade9 `cntStudents_All`, field-definition spelling `cntStudents_all`) or first-time-eligible students (OSSLT `cntEligible`), `P` as fully participating students, and `Y` as successful participants. If each non/partially participating student has a binary potential result under completion of the same assessment, and observed participant results are held fixed, unknown successes range from0 to `E-P`. Hence:

`Y/E <= potential full-cohort success proportion <= (Y+E-P)/E`.

| Same reporting-school cohort | E | P | Y | Unknown outcomes E−P | Conditional range |
|---|---:|---:|---:|---:|---:|
| Grade9 registered |23101|21604|12395|1497|53.6557%–60.1359%|
| OSSLT first-time eligible |21180|19756|16775|1424|79.2021%–85.9254%|

These are **conditional potential-outcome bounds, not official observed pass rates**. The mathematical upper endpoint assumes every missing outcome would succeed; the lower assumes none would. No missing-at-random assumption or fitted outcome model is imposed. A potential test result must be meaningful under the stated completion scenario; these are not forecasts of later graduation or intervention effects.

Cohort checks pass separately for every reporting school: `0 <= Y <= P <= E`. Grade9 additionally verifies `E = P + cntNoData`; the definition identifies `cntNoData` as uncompleted/partly completed tests. OSSLT verifies `E = P + cntAbsent + cntDeferred + cntOSSLC + cntInsufficientEvidence`. The109 OSSLT schools have927 absent,457 deferred,0 OSSLC and40 insufficient-evidence records, summing to1424. Although the definitions separately list exempt students, the28 reported exempt records are not part of this numerical `E` decomposition and are **not added** to the potential-result denominator. No outcome is assigned to exempt students.

This diagnostic retains the1497/1424 missing outcomes within reportable schools instead of dropping them from interpretation. It does not solve coverage of unmatched/suppressed schools, extend to every city pupil, or change the main model's input matrix. Both the original participant rates and the conditional ranges remain in `summary.json`.

# London V106: historical Year10 school-trip measurements

A newly retrieved DfES-commissioned NFER report supplies real **Year10** journey-to-school duration for **22,451 pupils attending London schools in 2006**. Table15 (printed page25; PDF page38) reports:

| Duration | Published percentage |
|---|---:|
| Less than15 minutes |30|
| 15–30 minutes |36|
| 31–45 minutes |15|
| 46–60 minutes |7|
| More than1 hour |3|
| No response |8|

The rounded percentages total99, as allowed by the source note. They remain unchanged: no invented exact cell counts, midpoint times, or renormalization. The question concerns time to school, rather than combined daily travel or modelled access to the nearest school.

This is historical **school-location** evidence, not a current London-resident estimate. The report invited411 maintained London secondary schools;200 returned pupil and/or teacher questionnaires. It does not establish exact ages14–18, all-school coverage, a complete resident denominator, or current travel patterns. Missing responses remain visible. These limitations prevent admission to the current city model; London's utility interval remains[0,1].

## Retrieval and reproduction

The original report was retrieved from the [UCL Institute of Education archive](https://dera.ioe.ac.uk/id/eprint/7788/1/RR823.pdf). `manifest.json` records original bytes and SHA256. `extract.py` uses `pdftotext` and Python's standard library to verify the hash, select the London Year10 column, retain all five time categories plus nonresponse, and check the published respondent total. It produces `historical_year10_aggregates.json`. No individual survey records were downloaded or redistributed.

Existing V52 NTS England-duration and V65 London LTDS public-table findings were read first. Current official NTS ad-hoc searches did not yield a newly verified London-resident × current-secondary × duration table; the new evidence above comes from a separate historical school survey. No restricted UKDA/LTDS extracts were requested or accessed. No model or manuscript was changed.

## Rounding and weighting interpretation

Table15 states that percentages may not sum to100 because of rounding. Other descriptive tables in this same report (including Tables7–8) explicitly specify rounding to the nearest integer. Applying a half-percentage-point envelope to Table15 is therefore a supported **conditional convention**, not a recovered set of exact cell proportions; a one-percentage-point envelope provides an additional sensitivity check. Neither interval is a sampling-confidence interval. The reviewed methods section1.4 describes descriptive statistics and separate multilevel analyses, but does not establish a weighting scheme for Table15. Its percentages are not labelled here as population-weighted estimates. N=22,451 does not authorize inversion to exact category counts.

The separate result directory `../../results/task4_v106_london_historical` quantifies these two rounding envelopes using bin-wise utility limits and keeps nonresponse utility in[0,1]. It is a historical school-Year10 subgroup diagnostic, with no current-city admission. The open-ended time-bin lower utility0 is a limiting bound, not an assumed finite observed travel time.

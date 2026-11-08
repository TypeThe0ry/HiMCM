# Copenhagen: four verified higher-education institutions

The official sources establish a partial count of **4 distinct recognized HE institutions** with central addresses or legal seats in Copenhagen municipality. With Statistics Denmark's **670,389 residents on 1 July 2026**, this gives at least **0.5966685014 institutions per 100,000 residents** and utility **0.3736959180** under the existing transformation `u = d / (1 + d)`. The utility upper bound remains **1**. This package does not establish a complete city inventory or a finite count upper bound.

| Counted institution | Recognition evidence | Municipal institutional location |
| --- | --- | --- |
| University of Copenhagen (KU) | Government supervisor list | Current statute §2 places its legal seat in Copenhagen; central postal address Nørregade10,1165 CopenhagenK |
| IT University of Copenhagen (ITU) | Government supervisor list | Central contact and rector address Rued Langgaards Vej7; the university-hosted energy certificate identifies this exact building as municipality101 |
| University College Copenhagen (KP) | Government supervisor list | Statute §1 explicitly gives Copenhagen municipality; current main address Humletorvet3 |
| Business Academy Copenhagen (EK) | Government supervisor list | Statute §1 explicitly gives Copenhagen municipality; §2 establishes the merger on1July2025 |

EK is counted once. Its predecessors KEA and Cphbusiness dissolved on30June2025. KP's former institutions and each institution's faculties, campuses and departments are also counted only within the single institutional entity. This follows the existing model's recognized-HE-institution supply definition; the legacy criterion name `research_he_density` does not restrict eligibility to research universities.

The sources are current institutional pages retrieved8November2026 and published statutes, combined with population at the start of2026Q3. They share calendar year2026, with different observation dates. The result is a conditional institutional-supply lower bound; it does not measure high-school admission, access to university facilities, student commute time or secondary-school quality.

## Why the upper bound stays unknown

The government HE database's coverage page explicitly excludes defence, police and other authorities' institutions whose programmes serve government services. It also includes historical institutions from2000 onward. Neither the eight-university list, the supervisor list nor a raw database row count establishes a complete contemporary universe under the broad model criterion. The registry endpoint could not be retrieved in this session. Other possible Copenhagen institutions, including art and design institutions, remain outside this verified subset; no zero counts are assigned to them.

## Reproduce and audit

Run from the repository root:

```sh
python3 research/2026-a/data/task4_v102_copenhagen/extract.py
```

`extract()` verifies all archived SHA-256 hashes, government-list membership, municipal-seat/address evidence, merger deduplication, API query dimensions and the single population record, then returns the summary without writing files. `summary.json` is its captured output. Python dependencies are `beautifulsoup4` and `pypdf`.

- [Manifest](manifest.json): exact source URLs, unmodified response hashes, dates and methods.
- [Population query](population_query.json): POST payload for the Statistics Denmark API, municipality101, all sexes/ages/marital statuses,2026K3.
- [Raw sources](raw/): original responses; metadata states population is measured on the quarter's first day.
- [Extraction](extract.py) and [summary](summary.json): derived values, scope and temporal alignment.

Verification: extraction completed successfully; saved summary equals the returned object. Only this source package was changed. Model adoption, ranking changes and regret effects must be computed by the integrating run.

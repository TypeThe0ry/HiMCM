# Phoenix student travel: two new concrete sources

## Result

No admissible high-school commute observation was added. The existing Phoenix missing interval remains unchanged. This round inspected actual student survey evidence rather than workforce interfaces; two distinct exclusions prevent an unsupported narrowing of the interval.

1. **Actual Phoenix-area student survey, wrong school level.** Ross, Godwyll and Adams (2020), *The Moderating Effect of Distance on Features of the Built Environment and Active School Transport*, DOI [10.3390/ijerph17217856](https://doi.org/10.3390/ijerph17217856). The archived [PMC original](https://pmc.ncbi.nlm.nih.gov/articles/PMC7662262/) reports 2,751 parent surveys at 35 Greater Phoenix schools, collected 2010–2014, explicitly restricted to grades 3–8. It measures reported travel mode and distance. This is real student evidence, but it cannot supply a Phoenix high-school duration distribution. The successful HTTP 200 HTML download is archived with SHA256.

2. **Separate student duration appears in an old county annual report, original table unverified.** [Arizona State Library catalogue node 91367](https://azmemory.azlibrary.gov/nodes/view/91367) describes Maricopa County TRP FY2004–05. Its indexed text reports a student mean of 15.0 minutes and 6.5 one-way miles, separately from employees. This is a new promising student-results lead, not a new model input. Direct access returned HTTP 403. We did not obtain the original table, grade-specific definition, Phoenix student denominator, or duration distribution. The archived search response is explicitly search-index evidence, not an original PDF. Neither the older county student mean nor an assumed conversion from that mean can narrow the current city high-school utility interval.

The MAG 2017 household travel report was recognized as already audited in V8 and was not reprocessed. No private access, registration, contact request, or model/manuscript modification occurred.

## Verification

Run `python3 audit.py`. The check verifies hashes, archived original's grade/year/sample statements, and exclusion decisions. `retrieval.json` records the successful article download and failed catalogue request. `manifest.json` hashes source and tool-response bytes separately from derived conclusions. The source archive has different evidence levels: original article HTML versus library search extraction. No PDF or survey microdata download is claimed.

# V86: measured secondary-student walking journeys in Barcelona

Published GPS-study aggregates provide 48 retained pedestrian journeys at eight Barcelona schools. Their participant-weighted mean is approximately **8.54 minutes before privacy truncation**, versus **7.85 minutes in the released processed trajectories**. The 41.79-second difference shows why directly scoring released GPS durations can overstate accessibility. These means are reconstructed from rounded school means in Table 4; they are not estimates for all Barcelona students.

Source: Larroya et al., [Home-to-school pedestrian mobility GPS data from a citizen science experiment in the Barcelona area](https://arxiv.org/html/2302.07585v2), Scientific Data 10, 428 (2023), DOI [10.1038/s41597-023-02328-3](https://doi.org/10.1038/s41597-023-02328-3). Table 1 defines school municipalities, Table 2 the retained sample, and Table 4 reports the before/after privacy duration means. `published_school_durations.csv` transcribes Table 4 for all ten schools; `summarize.py` reproduces the Barcelona-school aggregate.

## Measurement scope

- Collection: one chosen school day per school during 5–16 November 2018.
- Participants: ages 14–16, current third/fourth secondary grades (ESO), rather than upper-secondary Batx.
- The experiment recruited 427 students; 262 supplied phone records. Filtering retained 83 pedestrian trajectories across ten metropolitan-area schools, including 35 at schools in L’Hospitalet and Viladecans.
- Collection permits home-to-school or school-to-home journeys. The published aggregate table does not separate direction. School municipality does not establish every participant's residence municipality.
- Sampling is voluntary and smartphone-dependent. Nonpedestrian, invalid and non-origin/destination trajectories were removed. Published GPS paths also remove approximately 20–50 seconds of movement near home for privacy; Table 4 supplies the original aggregate means before that step.

This package supports an external measurement diagnostic. It changes no city indicator, missing interval, rank, or possible-champion set. Applying these short walking journeys to all-mode upper-secondary city travel would select a different population.

## Provenance and access

`provenance.json` records the HTML source hash. The fetched source is retained in `/tmp/travel86_barcelona.html`; no individual GPS coordinates or trajectories are stored in this package. `python3 research/2026-a/data/task4_v86_travel/summarize.py` checks the 83/48 counts and recomputes the means.

The underlying dataset is [CORA DOI 10.34810/data523](https://doi.org/10.34810/data523). Its DOI metadata was accessible through DataCite; its Dataverse host timed out during this retrieval, so the results here use published aggregates, not downloaded microdata. [Author code](https://github.com/ferranlarroyaub/Beepath-Schools) also identifies the collection period and direction options. The paper's later privacy-adjusted Table 4 takes precedence over earlier counts in that code README.

A distinct Copenhagen microdata route is [Danish National Archives accession 50683](https://digidata.rigsarkivet.dk/aflevering/50683), DOI 10.5279/dk-ra-50683, covering TU 2011–2023. Its catalogue lists municipality identifiers and session/trip/journey tables, with a “Søg om adgang” access-application link. This is an application route, not an open download; no application or external message was submitted.

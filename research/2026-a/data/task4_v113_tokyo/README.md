# Tokyo: 2025 recorded-criminal-death superset bound

The newly obtained Japanese National Police Agency 2025 Table 53 reports **631 criminal-death victims nationwide**, excluding traffic negligence (workbook `R07_053.xlsx`, F6). This is a count of deaths, not attempted-homicide cases. The murder-only row is 232; it is not used as a total intentional-homicide count because other offence categories can contain fatal intentional violence.

The national report's introductory notes (`R07_ALL.pdf`, second PDF page) state that the statistics combine reports from all prefectural police headquarters. Thus Tokyo's recorded intentional-homicide victims are a subset of the national criminal-death victims, conditional on that reporting universe and coverage. Keeping even nonintentional deaths in the national numerator makes the upper bound deliberately broad.

Using the **unchanged V46 Tokyo Metropolis population estimate 14,254,039 (May 2025)** yields:

- recorded intentional-homicide rate in `[0, 631/14254039*100000] = [0,4.4268154451]`;
- unchanged cost transformation `u=2/(2+rate)` yields `[0.3111961153,1]`.

This is a national-superset constraint on a city value, not a national rate substituted for a city rate. It does not bound unrecorded actual deaths or resident vital-statistics mortality. Admission requires accepting the recorded-crime scope; if the target demands complete actual deaths, retain `[0,1]`. Population vintage is the original published estimate, not a claim to the latest rebased census. No prior city observation is overwritten.

`extract.py` verifies every original SHA256, checks death-column labels and reconciliation of all offence rows (excluding the duplicated assault-death subtotal), verifies the inherited population and derives `observation.json`. NPA PDF and workbook independently display the total. Original URLs and access dates are in `manifest.json`; the official index links the workbook and PDFs.

Tokyo high-school travel remains missing. The new 2025 Tokyo athlete survey concerns a selected sporting population; it cannot fill the general resident high-school pupil cell. Earlier daily-total commute and mixed-city PT sources remain inadmissible for the same reason documented in prior rounds. No new travel observation is claimed.

Reproduce: `python3 research/2026-a/data/task4_v113_tokyo/extract.py` from the research repository root.

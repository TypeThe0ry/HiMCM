# V66 London: alternative public LTDS access audit

Result: **0 new admissible high-school travel observations**. Do not change London's travel interval. No model, manuscript, or Git operation was performed; no access request or external message was sent.

## New leads checked (2026-11-08)

1. **Official procurement attachment containing a dictionary lead.** Search indexing for [Contracts Finder attachment](https://www.contractsfinder.service.gov.uk/Notice/Attachment/5d7880cc-f55d-4a4f-a4ca-6c1f43437bfd) identifies a TfL contract for LTDS 2024/25–2027/28 and an appendix described as a 2022/23 data dictionary. This is an alternative discovery path, not the V65 survey webpage. Both direct HTTP download and web-reader opening returned 403. Parent ordinary Chrome navigation additionally redirected to the Contracts Finder signed-out page; no public attachment was obtained there. No dictionary bytes were obtained; no age, current-school-stage or trip-duration field was verified from this lead. The index description does not establish that the appendix's full contents are included or publicly downloadable. Revisit only when the attachment is accessible; do not treat search snippets as a usable codebook.

2. **New official 2025 LTDS thematic report.** [TfL original PDF](https://content.tfl.gov.uk/travel-in-london-2025-the-travel-behaviour-of-london-residents-based-on-the-ltds-acc.pdf) downloaded successfully as `ltds2025_report.pdf`. Pages 22–23 compare education-purpose trip-rate changes for London and England, not high-school journey duration. Review did not locate a joint current-school-stage × target-age × outbound-school-duration table. This report cannot provide the missing commute utility.

3. **September 2026 school-run publication.** [London City Hall](https://www.london.gov.uk/new-data-confirms-school-run-transformed-and-childrens-health-improved-due-mayor-londons-policies), dated 8 September 2026, was readable through the web tool, while direct HTTP returned 403. It discusses school car-trip counts and primary-school active-mode share, citing LTDS 2015/16–2024/25. It supplies neither target-age secondary-school duration nor a linked microdata download. No HTML original was archived and no model value was extracted.

4. **Earlier disclosure route cross-check.** [FOI-4774-2324](https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-4774-2324) describes permissioned SharePoint delivery; [FOI-2000-2425](https://tfl.gov.uk/corporate/transparency/freedom-of-information/foi-request-detail?referenceId=FOI-2000-2425) points back to that anonymised release. Neither inspected public page provided a downloadable dataset/codebook attachment. No private link was accessed. These are confirmation of the access obstacle, not additional observations.

## Reproducibility and remaining requirement

`manifest.json` records successful original download bytes/hash and unsuccessful requests separately. `audit.py` checks the saved PDF hash and reports matching pages for education/travel keywords; it does not manufacture individual records or infer population coverage from keywords. Run:

```sh
python3 research/2026-a/data/task4_v66_london/audit.py
```

A future admissible source must jointly identify London residence, ages 14–18, verified current secondary/sixth-form stage, observed outbound school time and appropriate survey weights/sample counts. An education-purpose trip, Student work status, or primary-school modal statistic cannot substitute for that joint population. This search has not shown that no suitable extract exists anywhere; it has not obtained one through the public routes inspected.

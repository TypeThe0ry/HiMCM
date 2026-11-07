# V57 — PXU programme attribution and historical coverage

The official specialty-schools page supplies a graduation attribution statement for Camelback Montessori and Maryvale Gifted and Talented Academy: their students graduate with the host campus class. This strengthens V56's co-location evidence for those two programmes. It does not supply a cohort2024 membership reconciliation or a separate ARCH attribution record. The current page mixes vintages: it describes three micro-schools in its introduction but names two in its graduation paragraph, and uses the 2026 Cactus Canyon name. Treat it as current programme guidance, not a dated 2024 administrative extract.

The already archived official history page lists Cyber High's closure in 2010 and Educator Preparatory's closure in 2024; the latter is the only listed closure during the normal cohort2024 high-school window. That is useful historical evidence but the page is not explicitly an exhaustive graduation-responsibility register. No numerical upper bound on additional excluded historical members was established. V56's B remains unidentified.

## Preserve the existing school-location target

The newly archived **2023–24 PXU City application** and the existing 2023–24 course catalogue describe in-person and online credits from PXU campuses. The application gives 3839 W Camelback Rd as its document-delivery office. This confirms the distinction between an administrative address and an individual student's teaching locations. It does **not** make all PXU City students non-target: the existing comparison excludes fully virtual schools, not every hybrid programme; the stated PXU campuses have already been checked against the city boundary. No new PXU City exclusion is applied.

The reused official FY2025 graduation response for PXU City (entity1001158, cohort2024) reports 56 in the All cohort and suppresses both graduate count and rate with −11. This is an existing observation, not a new count. It cannot be substituted for B or converted to zero graduates. The specialty-schools page also permits concurrent Digital Academy/home-school enrolment; this describes enrolment options, not duplication in the state's adjusted graduation cohort.

## Sources and checks

- [Official specialty-schools page](https://www.pxu.org/page/specialty-schools), raw `specialty_schools.html`. Relevant content is embedded in the page's application payload, so a plain visible-DOM text extraction can miss it.
- [Official PXU City application, 2023–24](https://core-docs.s3.us-east-1.amazonaws.com/documents/asset/uploaded_file/4844/pxu/4398862/PXU_City_Application_2023-2024.pdf), raw `pxu_city_application2023_24.pdf`, PDF pages 1–2.
- [V56 official history and course catalogue](../task4_v56_pxu_roster/README.md), reused byte-for-byte.
- [V9 original school response](../task4_v9_phoenix/school_outcomes/1001158.json), reused; source request is recorded in V9 `school_outcome_audit.csv`.

`manifest.json` records original hashes, sizes and retrieval times. Run `python3 research/2026-a/data/task4_v57_pxu_history/audit.py` from the repository root. It verifies all five originals, checks the relevant programme text, extracts the dated application with pdftotext and validates the existing suppressed cohort row. This source audit changes neither the numerical city interval nor the model definition.

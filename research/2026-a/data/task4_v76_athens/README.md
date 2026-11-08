# Athens V76: historical school identity audit

Two original Ministry of Education PDFs, recorded with SHA-256 in `manifest.json`, establish that school codes 551010 and 551040 persist across different names/types. The 2014 list (PDF page 1) labels them model-experimental; the 2020 committee invitation (PDF page 10, repeated page 13) labels them model schools. Both page-1 and page-10 table rows were visually checked against PDF text extraction. These documents are used for identity evidence only; their numerical columns are not treated as whole-school enrollment or teacher totals.

- [2014 official list](https://www.minedu.gov.gr/publications/docs2014/140304_dt_depps_pps.pdf)
- [2020 official committee invitation](https://www.minedu.gov.gr/publications/docs2020/ΠΡΟΣΚΛΗΣΗ_ΕΠΕΣ_9Ο3446ΜΤΛΗ-ΞΕ6.pdf)

A search-index extract of the [official June 2018 staffing table](https://depps.minedu.gov.gr/wp-content/uploads/2018/06/PINAKAS-B-1.pdf) additionally names 551010 as experimental 2nd Athens and 551040 as experimental 1st Athens–Gennadeio. Direct original download failed. This is a discovery lead, not an archived-original verification. The 2014/2020 originals corroborate continuity, but the contemporaneous historical original remains outstanding; no automatic word/type substitution is introduced into V75 linkage.

`candidate_rows.csv` preserves the six exact source student rows (three candidate schools × two year labels), their type differences, and candidate identity status. They total 843 pupils for label 2018 and 853 for label 2019, including the still-unverified 540752 abbreviation match. These are candidate-row totals, NOT newly admitted city pupils. The two historically supported general schools separately contain 733 and 731 pupils; the vocational candidate contains 110 and 122.

For 540752, later official lists retain the expanded name already present in the directory. An authoritative historical record joining that code to the source's abbreviated name has not been acquired. Similarity of names is insufficient under the retained linkage rule.

## Period and admission outcome

The student package has literal year labels `2018` and `2019`; no official field definition was found establishing whether each is the starting school year, ending school year, or snapshot year. The directory itself is undated. Historical naming helps resolve identity, not observation period. Matching pupil totals to an external table cannot supply the missing year definition.

Consequently V75's 48 punctuation-only linked schools are retained unchanged, and V76 admits **zero** new model cells. No city teacher denominator or student commuting measure is supplied. Athens education and travel bounds remain unchanged. The next useful acquisition is the original historical code/name table plus an official definition of the student export's `year` field, followed by same-period/city/school-scope teachers. Adding a pupil-only candidate aggregate to a region-level denominator would not resolve that problem.

Reproduce the six-row extraction and original-file hash checks:

```sh
python3 research/2026-a/data/task4_v76_athens/audit.py
```

The audit reuses V75's verified original ZIP reader and checks name uniqueness per year. Failed downloads are represented as failures in the manifest; they are not claimed as local source documents. No ranking/model/Overleaf file was modified by this audit.

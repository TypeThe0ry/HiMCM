# Istanbul 2011 high-school survey: full-document travel-field audit

All 126 PDF pages have now been rendered and scanned with Turkish OCR, extending the previous inspection of PDF pages 55–74. No usable home-to-school time distribution was found. Istanbul travel remains `[0,1]`; no observations, weights or model rules change.

The source is the original publisher's 2011 report already archived in `../task4_v114_istanbul_travel/`. It is not duplicated. `audit.json` pins its SHA256. `page_scan.csv` covers every PDF page, records OCR hashes, and records text length, including seven empty OCR outputs (PDF pages 2, 6, 24, 54, 88, 114 and 125). Empty OCR output is not proof that a page has no visual content. The full temporary OCR output is not republished here. This was a full-document field scan plus targeted visual inspection, not a claim that every page received a manual visual review. OCR keyword absence alone is not proof that a field does not exist.

The most relevant findings were visually checked:

- PDF pages 30–31 (printed 28–29): the design deliberately contrasts school types and relative advantage. It targets grades 9 and 11; grade 12 is expressly excluded because of entrance-exam preparation and expected absence. There are 21 schools, 2,037 returned questionnaires and 2,035 analyzed questionnaires. The planned/rounded 2,100 students should not be reported as the analyzed sample.
- PDF page 55 (printed 53), Table 47: term-time living arrangements, such as family versus dormitory, do not provide district, route or duration.
- PDF page 75 (printed 73), Table 84: transport is an allowance-expenditure priority, not a travel-time or mode measurement. Its ranked spending categories cannot be converted into AHP numerical judgments.
- The full scan found no usable district-by-age resource-access tabulation or verified expansion weights for Istanbul residents aged 14–18. School type and sex comparisons are not substitutes for those cross-classifications.

The report can inform future questionnaire design about school-stage differences and affordability. Its selected grades and schools do not establish representative coverage of 14-year-olds versus 18-year-olds. Historical data are not rejected merely because they are old—the earlier New York input explicitly carries historical scope—but this source also lacks the required travel measurement and compatible target population. There is therefore no travel value to transfer even in a labeled historical sensitivity arm.

To reproduce the scan with `pdftoppm` and Tesseract's `tur` language installed:

```sh
python3 research/2026-a/data/task4_v115_istanbul_survey/scan.py
```

OCR PNG/text output stays in a temporary directory. On macOS, the resolved `/private/tmp` path is used because Tesseract failed to open inputs through the `/tmp` symlink in this environment. `verify.py` checks the saved audit, source hash and complete page index without repeating OCR.

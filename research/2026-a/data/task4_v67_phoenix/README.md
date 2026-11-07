# Phoenix TRP student evidence: original report and current access route

**Zero new admissible Phoenix high-school observations. Existing missing bounds remain unchanged.**

## New original acquired

The City of Glendale's [2019 Active Transportation Plan](https://www.glendaleaz.gov/files/assets/city/v/1/transportation/documents/transportation-services/glendaleatp_finalreport-_06102019-reduced.pdf) was downloaded successfully (HTTP 200, 18,718,032 bytes). PDF page 30 / printed page 26 cites the **2015 Maricopa County TRP survey**, reporting student distance of **7.1 miles**, separately from employees' **15.0 miles**. It also reports that **8.6% of alternative-mode student users** walk. That percentage is conditional on alternative-mode use, not a proportion of all students. The nearby Copper Canyon H.S. intersection pedestrian count is an intersection traffic count, not an identified student cohort.

These are actual published student-related results in a municipal original. They provide neither Phoenix city-resident high-school counts nor observed travel-time distributions. Distance cannot be converted to minutes without unsupported mode/speed assumptions. The document is useful evidence that student TRP aggregates exist, but it does not shrink Phoenix's interval.

The PDF is byte-preserved; extracted text and a page-30 excerpt are supplied. `pdftotext` produced font/optional-content warnings but successfully extracted the quoted numeric fields; no claim of visual inspection is made.

## FY2005 and current results access

The [FY2005 library catalogue](https://azmemory.azlibrary.gov/nodes/view/91367) remains the exact original-source lead inherited from V66. No new authorized downloadable original URL was located in this bounded follow-up. The FY2025 county report at DocumentCenter item 110701 is already covered by V59 and was not represented as new evidence here.

The current [county TRP program page](https://www.maricopa.gov/2388/Travel-Reduction-Program) confirms annual school-site surveys and public Task Force review of survey results. It exposes a concrete [public agenda/packet directory](https://www.maricopa.gov/AgendaCenter/Travel-Reduction-Program-61/). However, the inspected [October 6, 2026 packet](https://www.maricopa.gov/AgendaCenter/ViewFile/Agenda/_10062026-3865?packet=true) is only four pages of agenda items; it contains no student observations or microdata download. The captured web response records this inspection.

Thus a public meeting entry is verified, **a public current student microdata entry is not**. A useful future release would need school level, survey year, Phoenix residence, valid student responses, duration bins and denominator, and explicit treatment of imputed nonresponses. None of these fields can be inferred from the existence of a school plan. No messages, information requests, registration or private access were performed.

`manifest.json` hashes the original PDF, derived extraction and exact web-tool response. Run `python3 audit.py` to verify integrity and the numeric/denominator distinction. No model, manuscript, or existing data file changed.

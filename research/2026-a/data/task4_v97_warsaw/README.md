# Warsaw V97: youth teacher FTE split identified, pending primary values

**Decision: retain the V96 interval.** Official BDL metadata identifies the three required series, but the primary Warsaw 2024 value response was not obtained. These files add a precise retrieval target; no new teacher FTE enters the model.

| BDL variable | Official school type | Sex | Coverage shown in metadata |
| --- | --- | --- | --- |
| 378626 | licea ogólnokształcące dla młodzieży bez specjalnych | ogółem | Gmina, 2011–2025 |
| 378627 | licea ogólnokształcące specjalne dla młodzieży | ogółem | Gmina, 2011–2025 |
| 378628 | licea ogólnokształcące dla dorosłych | ogółem | Gmina, 2011–2025 |

The official parent series is “Nauczyciele pełnozatrudnieni i niepełnozatrudnieni w przeliczeniu na etaty” (full- and part-time teachers converted to FTE), BDL subgroup 3235. Saved metadata postbacks expand the ordinary-youth row (`metadata_session_expanded.html`), special-youth row (`metadata_split_0.html`) and adult row (`metadata_split_1.html`). This verifies FTE rather than headcount, series IDs, school types, overall sex and availability years. It does not provide Warsaw observations, school ownership coverage, or sufficiently detailed mandatory-teaching-role/date definitions to establish full comparability by itself.

## Secondary lead, excluded from model

The archived Polska w liczbach Warsaw page labels its education data GUS 2024 and displays ordinary-youth FTE 5443.9, special-youth FTE 127.7, and adult FTE 82.0. Their sum is 5653.6, consistent with the V96 yearbook pooled general-school teacher count 5654 at integer publication precision. The page also displays ordinary-youth students 86967 and special-youth students 781, whose sum 87748 matches V96. This arithmetic agreement is a useful cross-check, not primary-source verification. Displayed decimal precision must not be taken as the original BDL precision.

These numbers remain a retrieval lead. There is no proportional allocation of pooled FTE, no point imputation, and no replacement of the published V96 teacher bounds [2487, 8148]. Do not report an observed narrowing from this package.

## Access outcomes and next retrieval

- Official API variables request returned HTTP 429: 100 requests per 12 hours exceeded. The complete response is preserved. No repeated API retry or rate-limit bypass was attempted.
- Official BDL metadata HTML returned HTTP 200; normal session postback expansion revealed the three exact variable IDs.
- Official *Panorama dzielnic Warszawy 2025* PDF downloaded successfully. Its text does not supply a teacher FTE table resolving this split.
- The initial metadata postback without a matching session produced no expanded rows; `metadata_expanded.html` is preserved as an unsuccessful navigation response, not evidence of absent data.
- Longseries HTML was fetched as an additional secondary lead; it supplied no primary Warsaw value response.

Once API access is available, retrieve the three IDs for Warsaw municipality, year 2024. Verify the returned geographic identifier/name, units, flags, public/private coverage, beginning-of-school-year convention, and mandatory-teaching definition against the V96 yearbook before admission. Sum the two youth series and exclude the adult series. Preserve uncertainty from all other youth routes and from publication precision. The parent V96 source package remains the authority for the existing bounds and harmonization.

Raw files are byte-preserved and SHA-256 indexed in `source_manifest.json`; text files are derived reading aids. No manuscript, registry, model, or existing dataset was edited.

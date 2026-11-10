# Three influential Oslo point-source checks

The source review separates a rolling publisher match from an annual edition and identifies a different official pupil–teacher statistic. **All three original values remain unchanged. There are zero primary admissions, zero score-width reduction and no recommendation change.**

| Original CSV point | Independently checked source | What this establishes |
| --- | --- | --- |
| CLI 92.9, year 2026 | Archived Numbeo annual 2026: 90.2; Mid-Year: 92.1; rolling Current: 93.0 | No exact match among the three checked editions. The original value is not proved erroneous or absent from every historical snapshot. |
| PIR 9.8, year 2026 | Archived Numbeo annual 2026: 11.6; Mid-Year: 11.0; rolling Current: 9.8 | Exact numerical match to the archived Current row; original extraction time, edition and municipal-boundary equivalence remain unproved. |
| Pupil/teacher ratio 18.2, year 2025 | SSB table 12609, Oslo code 0300, metric KOSelevperlarsv0000: 12.5 in 2025 and 10.9 in 2024 | Official values are directly verified but do not identify the original 18.2 observation or authorize its replacement. |

The six Numbeo tables are byte-identical copies of existing publisher archives, not six new observations. Their archive metadata records access on 7 November 2026; exact original HTTP times and statuses are unknown. Only the Oslo rows are used here; the old 25-city model is not activated. Two newly retrieved Numbeo definition pages confirm the New York baseline and rent-excluding CLI, plus the PIR calculation based on a 90 m² apartment and assumed family income of 1.5 times average net salary. These are publisher conventions, not measured student budgets or household income medians.

The SSB route preserves five new HTTP response bodies and the exact POST query. The API labels the metric reference period 31 December. A historical same-named indicator definition in table 06942 describes county-run schools, includes vocational college pupils there, deducts long absences from contracted teacher man-years and assigns pupils by school county on 1 October. Exact continuity of that older definition with current table 12609 has not been established; the API label alone does not put both numerator and denominator on 31 December. Provider, stage and date equivalence to the original CSV remain unknown.

`research/2026-a/scripts/audit_current_oslo_cost_ptr_sources.py` independently parses the Oslo HTML rows by column headings, checks edition labels and definition passages, decodes the SSB query/dimensions/values and verifies all 13 archived bodies. Seven bodies are new HTTP responses and six are existing table copies. The original three utilities remain 0.5184033177812338, 0.5050505050505051 and 0.4518072289156626. Their previously verified individual [0,1] withdrawal cases change the fixed-weight recommendation from Oslo to Zurich; this prioritizes review and supplies no measurement-error probability.

The audit also protects 548 science bindings, 77 supplementary bindings, ten withdrawal-evidence entries, both seven-file manuscript copies and the current PDF. Original extraction lineages newly established: zero. The general source-quality requirement remains partial. Current V203 still recommends Oslo under fixed weights and Zurich under equal weights, with 16 possible and zero necessary champions.

The selected route index now contains 24 entries. Reopen these routes with an actual original extraction record, a matching publisher capture or evidence tying the current SSB definition to the retained observation. Do not silently replace inputs with the annual Numbeo figures or the differently scoped official ratio. No manuscript change, extra Overleaf version or agency contact occurred.

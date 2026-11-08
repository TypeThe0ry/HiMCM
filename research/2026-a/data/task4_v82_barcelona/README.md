# Barcelona: school staffing table exposes coverage and timing gaps

The [official CEB 2024/25 staffing PDF](https://www.edubcn.cat/rcs_gene/extra/00_transparencia/recursos_humans/Plantilles_2024_2025/02_Plantilles_secundaria_24_25.pdf) reports 58 institutes, 7,712 Batxillerat pupils and 2,924.5 aggregated teaching allocations. It explicitly leaves teachers unallocated across stages. The prose dates enrollment to November 26, 2024, while the table header says February 27, 2025. Stage totals sum to 29,100 versus the printed 29,093. Pedralbes alone has 1,471 from its stage cells versus 1,470 printed total.

The [V81 official municipal CSV](../task4_v81_barcelona/README.md) has 9,161 public Batxillerat pupils for 2024/25, a difference of 1,449. Different dates and institution coverage prevent interpreting that difference as missing pupils. Neither dividing 7,712 by all-stage staffing nor pairing that staffing with citywide enrollment yields a matched high-school ratio. Main intervals remain unchanged. Next work needs aligned school coverage, enrollment dates and actual stage-specific teaching resources, including private provision.

## Evidence status

Direct HTTPS download timed out; no original PDF was obtained or visually checked. `reader_observations.json` is a selected numerical transcription from the web reader, not original bytes. Its manifest hash protects this transcription only. No full article or table is reproduced.

Run `python3 research/2026-a/data/task4_v82_barcelona/verify.py` to check transcription integrity, arithmetic and the comparison with V81. Output is [summary.json](summary.json). The script does not authenticate the underlying PDF or resolve its conflicting dates. `main_admitted=false`; no model or manuscript file was edited.

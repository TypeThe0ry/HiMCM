# V118 education: missing Amsterdam cell only

DUO official 2025 workbook contains Amsterdam separately from Groot Amsterdam. The 1 October 2025 Amsterdam row (AMR36) reports student/teacher-FTE ratio **14.6**, students **48,116**, teaching FTE **3,288**. Published 21 August 2026; original workbook and metadata saved.

This is a useful **whole-secondary FTE scenario candidate**, not an admitted upper-secondary headcount point. DUO assigns institution totals by head-office region and explicitly cannot split personnel by branch; nonreporting institutions and excluded temporary staff affect coverage. The original ten-indicator headcount rule therefore cannot silently accept it. The original CSV's nonempty values were not researched or replaced. No model edits.

A separate official DUO persons workbook exists, but region totals use nonresponse weights while institution totals do not, and it does not resolve upper-secondary/location allocation. Mixing that denominator with this workbook is not justified.

Sources and machine-readable observation: observations.json. All download evidence is public, with no personal records.

## London fallback

DfE 2025/26 aggregate dataset downloaded and filtered to Inner/Outer London secondary rows (extract and whole-download hash saved). The two disjoint State-funded secondary totals give 575,645.5 pupil FTE / 36,087.5 teacher FTE = **15.951382057499133** across 514 schools. This is whole-secondary, state-funded-only, FTE/FTE; it is another explicit scenario candidate, not a compatible upper-secondary headcount replacement. Nested academy rows must not be added to their parents. Milan bounded search yielded no immediately usable city-stage teacher denominator; no failure files saved.

## 本轮准入结论

Amsterdam总部跨校区归属和London仅公立中学FTE都未证明完整城市指标覆盖，本轮未准入主模型，保留原缺失区间。只保存新取得的真实资料，未修改附件已有数值。

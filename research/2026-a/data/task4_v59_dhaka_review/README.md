# V59 — Independent Dhaka stage-allocation review

The proposed lower bounds of 141095 HSC students and 7075 HSC teachers were too strong. Table 4.3.3 (PDF297, printed264) shows that **School and College (College Section)** includes tertiary students: nationally 402723 students comprise 401970 higher-secondary, 152 degree-pass and 601 honours students. It cannot be treated as a pure HSC category. The **Higher Secondary College** category has 375288 students nationally, all in the higher-secondary column.

The Dhaka city-corporation row in Table 4.1.10 (PDF215, printed182) gives 103904 School-and-College students, 37191 Higher-Secondary-College students, and 426900 across all five college types. A same-category national cap allows at most 753 non-HSC students within the first category in Dhaka. Therefore

`N_lower = 37191 + max(0, 103904 - 753) = 140342`, while `N_upper = 426900`.

Only the pure Higher Secondary College category supplies a directly stage-matched **published teacher-role** lower count:2238. Its School-and-College counterpart4837 and all degree/masters teachers remain an unallocated pool. The city total gives `T_upper=12016`. Under the published teacher-role resource interpretation, the diagnostic envelope is

`u_lower = 15*2238/(426900+15*2238) = 0.072903772233`,

`u_upper = 15*12016/(140342+15*12016) = 0.562227448827`.

For the primary envelope allowing school heads to be non-instructional, Table4.4.2's **Higher Secondary College Total** columns report1195 principals and78 vice-principals nationwide. Their sum1273 is an upper cap on such roles inside the city's pure-HSC2238, not a proxy for its actual headcount. Subtraction therefore supplies a conservative non-head teacher-role lower bound `max(0,2238−1273)=965`. The primary bounds become `T∈[965,12016]`, with the same student interval, and

`u_primary∈[0.032795242141,0.562227448827]`.

This leaves head instructional participation unidentified, consistent with the preceding Jakarta revision. Other named teacher roles remain as defined by BANBEIS, including demonstrators and library/information-science assistant teachers; the interval does not establish classroom-only FTE or teaching hours.

A simple counterexample to the original proposal is one of the nationally reported753 tertiary students being in Dhaka's School-and-College category, with one teacher assigned to that tertiary provision. This is consistent with the published category totals but violates the proposed141095/7075 lower counts. It is a hypothetical allocation showing why the bounds need revision, not an observed student or teacher assignment. The corrected envelope is conservative; endpoint joint attainability is not claimed.

Teacher totals are **published administrative teacher roles**, not teaching FTE or a count restricted to classroom-only staff. Table4.4.2 (PDF304, printed271) explicitly includes principals and vice-principals. The source's labelled Dhaka city-corporation area is distinct from its district/division rows, but this audit did not establish an independent polygon match or a North/South split.

The report labels its tables2025, while the methodology on printed2 gives collection dates20.10.2024–21.11.2024. Preserve that inconsistency; do not assert a verified2025 census reference date. The source-defined general college HSC universe excludes other educational systems unless separately incorporated.

[Audit numbers and original-file hash](audit.json). No model or manuscript was edited by this review.

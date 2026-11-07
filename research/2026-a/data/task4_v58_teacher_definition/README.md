# V58 — Teacher denominator review

The home-school attachment (induk) is distinct from full-time employment. In the original SMA2025/26 tables, DKI's11530 induk teachers comprise9004 permanent/full-time and2526 other/part-time teachers. Neither count is FTE. Table1.10.1, printed p102, separately lists1188 noninduk attachments and says subsequent teacher tables use induk records. Table1.8.2, printed p72, includes453 headmasters in its11983 headline total.

The Ministry's2019 FAQ Q66 directs a teacher serving two schools to designate only one school as induk. The [current Ministry guidance reviewed in the education package](../task4_v58_jakarta_education/induk_rule_audit.json) also requires deactivating the old home assignment on transfer. These administrative rules support counting distinct home-assigned teachers across SMA and SMK, while preserving the source's role definitions.

## Implications for the proposed city indicator

For a **home-assigned teaching-staff** indicator, SMA+SMK induk teacher counts may be summed under the single-home rule. Explicitly describe the denominator as administrative home assignment; do not call it all instructional providers or full-time-equivalent capacity.

For a target covering **all unique people providing instruction in these schools**, noninduk attachments cannot automatically be removed as duplicates within DKI SMA+SMK. A teacher's home may lie outside this city or these stages. Such attachments can add between zero and their reported count to a conservative unique-person envelope. Unknown teaching duties of headmasters require their own allocation interval.

If MA's2008 reported headmasters/teachers form an unresolved pool, additional distinct teachers between0and2008 already allow overlap with the known Dapodik teachers. No assumption that every MA record is a distinct new teacher is needed for this upper bound. This is an envelope, not a claim that every endpoint is simultaneously attainable or that the three administrative streams have identical workload definitions.

No model inputs were edited. `audit.py` independently verifies the SMA original table arithmetic and records the definitional distinction. The2019 FAQ original request returned503; `faq2019_reader_audit.json` is a labelled official-search-reader paraphrase.

# Bounded source ledger for 112 retained point utilities

This ledger gives every retained point utility a source classification without changing the original 16-city CSV, its flags, weights or utility rules. It covers the 112 point cells, not every nonempty CSV field: the other 48 interval cells and supplemental inventories remain in their existing registries.

| Imported classification | Points |
| --- | ---: |
| Exact publisher value; original extraction/geography unresolved |43|
| Exact publisher value at a different statistic: Singapore broadband mean |1|
| No match in the three checked cost editions |4|
| Documented number at another school stage: Tokyo/Singapore PTR |2|
| No match in the examined Oslo PTR series |1|
| Reviewed but lineage unresolved: Oslo HE/PM2.5, Zurich homicide and Vienna/Berlin PTR |5|
| Not included in this bounded classification |56|

The last category does not mean never reviewed. Publisher matching does not establish the original extraction route, geographic equivalence, population/denominator comparability or student representativeness. The Tokyo/Singapore stage warnings are imported from archived checks, not a fresh certification of all underlying raw material. No point is marked as a fully certified measurement or as having verified original extraction lineage.

`review_priority.csv` orders the same 112 records by the largest excess regret of retaining the original policy after that point is temporarily replaced by [0,1], across the fixed/equal-weight cases. This imports the existing ignorance stress: 10 fixed-weight and35equal-weight withdrawals change the conservative choice. These are deterministic conditional tests, not error probabilities or proof of incorrect measurements. A matched point can still merit geographic or source-scope review. The user currently lacks the Oslo institution roster and Zurich homicide source, so the ledger does not repeat those requests.

`ledger.csv` retains each original value/year/flag and utility, links the bounded evidence, states the unresolved scope and records the existing withdrawal comparisons. `teacher_scope.json` under the data directory covers five supplied PTR points; Its original Vienna/Berlin entries remain a historical inventory; new follow-up packages separately record the bounded checks without establishing their original point lineage. Future evidence should update this ledger with a precise source and scope rather than convert a match into automatic model admission.

The independent auditor verifies all112point keys against the active V203 point mask, every original field and utility, the source classifications and teacher-reference hashes, priority ordering and the preserved scientific/manuscript inputs. It prints JSON by default; saved output requires explicit flags. Primary admissions and actual primary score-width reduction remain zero.

The Oslo HE evidence includes public municipality-coded DBH records and the [completed national identity bridge](../../data/current_oslo_he_identity_completion/README.md). Each semester has25positive public-value institution codes, matching the submitted count numerically. All27registry identities and all25positive codes now have national bridges;1404/1405remain programme-accredited only. Gestalt1405has an Oslo DBH campus code but current Bærum registration and Sandvika location evidence, retained as a flag without exclusion. The identity set and teaching-mode23are distinct. Neither numeric agreement nor national identity establishes original provider/campus coverage, contemporaneous accreditation or original extraction lineage; the point stays in the reviewed-unresolved category. Existing count-definition scenarios remain separate from source certification, and no failed response confirms an identity.

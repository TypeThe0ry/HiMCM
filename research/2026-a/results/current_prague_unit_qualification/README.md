# Prague bus-associated node unit: independent qualification

**The 942 candidate PID nodes are supportable as a conditional source-defined, bus-associated node inventory**, under the same source-inventory standard applied to the Oslo 626 onstreetBus groups. The appropriate unit is a PID node with an eligible bus witness, counted once even when it contains several named groups or modes. This is not a count of universally comparable physical facilities. Unit qualification does not itself admit the count to the model or establish dated service; the separate service audit and other admission checks remain relevant.

PID's [stop data documentation](https://pid.cz/o-systemu/opendata/) defines a group as same-name stops in the same node; a node may include several named groups. A stop ID represents `node/pole`, not a stand-alone group. A single candidate node may have bus witnesses among other modes and named groups. Of 942 nodes, 892 contain one current group, 45 contain two, four contain three and one contains five; 999 groups in total. Node 237 is the provider's documented example of multiple named groups. Combining places inside a node can make a count smaller relative to a finer group or physical-site unit; that fact does not establish a split across nodes or overcount. Nor does it make every node a single physical place.

The 942 witnesses all match an archived list occurrence exactly on node, group name, displayed route, file and locator; each node plus name identifies exactly one group in the later PID snapshot. The two snapshots are 2026-11-09 and 2026-11-10 respectively; matching labels and identifiers supports a cross-snapshot association, not proof of unchanged identity or service through time. These checks reproduce the existing conditional crosswalk rather than independently validating its route or service eligibility.

## Cross-node identity checks

The audit compares all groups and poles in the 2026-11-10 PID JSON, recording every matching key across distinct nodes when at least one node is a candidate. No such collision was found for nonzero `cis`, `idosName`, `uniqueName`, exact pole ID, GTFS pole alias, or exact latitude/longitude pair. All 999 candidate groups have a nonzero CIS value; all 2,597 candidate poles have IDs prefixed by their owning node. The provider defines the pole ID as unique within the file and stable across updates, so lack of identical pole IDs across nodes is structurally expected. The schema exposes `cis`, but the archived prose does not define its semantics; unique values are a screening result, not proof of independent physical sites. Equal coordinates would likewise be a flag, not automatic proof of one facility.

Five exact group-name keys recur across nodes involving a candidate: Háje, Krakov, Lhotka, Nové Dvory and Višňová. Each involves only one candidate node; all other same-name records have municipalities other than Praha. Unicode NFKC, case folding and whitespace normalization produced the same five keys and no candidate-to-candidate name collision. The PID documentation explicitly warns that same names can represent different groups. No proximity or name-based merge was applied. Distinct names or identifiers do not rule out a provider splitting one physical place between nodes, so the audit supports a source-defined inventory rather than certifying a physical census.

## Scope and comparison

All 942 matched witness groups, and all 999 groups within their candidate nodes, carry `municipality=Praha` in the later PID data; the archived list links carry `inprague=1`. PID describes municipality as the municipality in whose territory the stop lies. These are provider classifications, not independently verified polygon membership, and equivalence of the two fields was not established. The current mode witness and archived route association are from different dates; `isNight` is absent for every selected witness, so daytime operation cannot be inferred from its absence. The population baseline is 2025. The 942 nodes overlap 47 of the existing 57 metro nodes and must not be added to that metro count.

Oslo's 626 retained NSR groups are source-defined onstreetBus inventory records, with a documented city-polygon and source-validity review; they are not proof of service, universal access, or equal cross-city physical units. Prague's node and Oslo's parent-collapsed group are different provider constructions. Applying the same inventory standard supports qualification with this explicit distinction; it does not establish equal granularity or equivalent city boundary methods. Service, mode, dates, replacement and other eligibility rules remain separate from this identity audit. No universal student or day access is claimed.

## Reproduction and files

Run from the repository root:

```sh
python research/2026-a/results/current_prague_unit_qualification/audit.py
```

`receipt.json` records input SHA-256 hashes, source generation timestamp, populations and collision counts. `candidate_groups.csv` enumerates every current group within each candidate node, including all pole IDs. `cross_node_collisions.csv` lists every exact or normalized cross-node key involving a candidate, including records outside the candidates. Candidate nodes and the archived witness are taken from `results/current_prague_bus_crosswalk/witness.csv`; source descriptions and retrieval dates are in `data/current_prague_node_semantics/manifest.json`. No network request or model, registry, manuscript, or source change was made. Cross-node collision checks are bounded to the saved PID snapshot and tested fields, not an exhaustive semantic linkage audit.

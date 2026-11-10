# Archived ROR rosters for the current 16 cities

The archived ROR v2.14 snapshot does not reproduce 12 of the 16 submitted institution counts under the stated education-tag/city-label rule. Four counts agree: Zurich 23, Stockholm 24, Dublin 28 and Singapore 118. Oslo has 28 matching records versus the submitted 25; Tokyo has 223 versus 85. These are registry record counts, with higher-education eligibility and the original extraction lineage still unresolved. The original CSV and primary V203 inputs remain unchanged.

## Scope and source

The source is the complete [ROR v2.14 snapshot, dated 2026-10-06](https://zenodo.org/records/23187250), already archived at `../task4_v5_resources/ror_2026_10_06.zip`. The SHA256 is `555b38a4b586759de1fa278b0e751433a13dd541f375097db53b186cfcdc768a`. The original archive records an access date of 2026-11-07; this offline check adds no new HTTP retrieval, status or timestamp. No duplicate ZIP is stored here.

The selection requires active status, a type list containing `education`, and at least one location matching both the submitted country code and normalized GeoNames city name. Normalization removes Unicode combining accents, case-folds and collapses whitespace; no fuzzy match or alternative spelling is used. Each city count uses unique ROR IDs. Matching locations and all original locations are retained so that a city-label match remains distinct from a municipal polygon or an accredited institution inventory. Paris and Milan each involve two GeoNames IDs carrying the same city label.

The full JSON member is the selection authority. The CSV member retains only the first location for the two examined omitted records: `https://ror.org/01fj67v51` has London among several JSON locations but Oxford in the CSV, and `https://ror.org/0563zdp54` has Paris in JSON but Orlando in CSV. Consequently JSON yields London 156 and Paris 105, versus CSV first-location counts 155 and 104. The CSV-derived candidate roster is not a complete implementation of an any-location rule.

Singapore has 118 matching city-label records and 120 education-tagged records across country SG; the additional two carry the Jurong West label. The earlier archived diagnostic includes Raffles Institution, Hwa Chong Institution and NUS High School, illustrating why the education tag cannot establish higher-education eligibility. ROR IDs describe organizations; they do not directly measure student places, admission eligibility, campus access or facility capacity. A numeric match does not identify the original source, and a difference does not by itself prove a submitted value erroneous.

## Reproduction and verification

Run `python3 research/2026-a/data/current_all16_ror_rosters/extract_rosters.py` from the research checkout. It only regenerates this new evidence directory; no legacy model entry is run. The independent auditor `research/2026-a/scripts/audit_current_all16_ror_rosters.py` reparses the archive and checks membership, names, status, types and geographic IDs, alongside preservation of the current scientific and manuscript bindings. Its saved result is `research/2026-a/results/current_all16_ror_review/verification.json`.

This source review admits zero new primary observations and produces zero primary interval-width reduction. The next useful evidence is a city-scoped accredited higher-education roster with explicit provider/campus/branch rules and the population boundary used for its density. The current source ledger remains a separately frozen bounded classification until an explicit import; this diagnostic is registered in the acquisition record and route index.

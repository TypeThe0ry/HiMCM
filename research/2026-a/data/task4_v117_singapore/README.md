# Singapore: seven verified public swimming venues in April2025

ActiveSG's official article dated23April2025 names seven distinct public swimming complexes with advertised hours and admission prices: Bukit Canberra, Sengkang, Our Tampines Hub, Heartbeat@Bedok, Jurong West, Jurong East and Delta. Current official facility pages separately corroborate their identities and distinct postal addresses. Each venue counts once, regardless of how many pools or lanes it contains.

The article also lists SAFRA Yishun, SAFRA Toa Payoh and Splash@Kidz Amaze. These are excluded: the first two have membership/guest conditions, while the third is an under12 waterplay venue. The dated article is an editorial selection, so seven is a **verified inventory lower bound**, not a complete city total. The current directory was also inspected but returned only ten listed entries and a November2026 update; it does not establish a2025 complete inventory.

Use the existing total-population convention and unchanged one-venue-per100000 anchor. The archived official SingStat2025 population is6,111,175, reused from `../task4_v100_singapore/population.json`. Thus the density lower bound is`7×100000/6111175=0.1145442570`, and the original transform gives utility`d/(1+d)=0.1027722823`. The upper utility remains1 because no finite complete count is established.

This supplies a dated April2025 facility-presence bound. It is not a year-end census, a continuous-open guarantee or evidence that every high-school student can afford or reach a venue. No travel-time, stage-specific educational outcome or neighborhood-equity value is inferred. Current pages corroborate identity, not historical hours. The official article's incidental descriptions of slides/wave pools are not used.

`provider_pool_sources.json` and `provider_pool_details.json` contain Exa-extracted official page text, not originalHTML bytes. `extract.py` checks the dated article, seven unique venue identities/postal codes, population record, unchanged transform and bounds; it generates `summary.json` with hashes. Run`python3 research/2026-a/data/task4_v117_singapore/extract.py` from the repository root. Main model and registry are untouched.

Source: [ActiveSG dated article](https://www.activesgcircle.gov.sg/read/editors-pick-must-hit-pools-in-singapore). Per-venue official links and source hashes are recorded in`summary.json`.

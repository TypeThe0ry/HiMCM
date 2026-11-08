# Two missing pool cells: verified partial venue inventories

Zurich's official current directory names seven public indoor swimming venues. Count these once each; do not add individual basins, school pools, lake/river bathing areas or outdoor facilities. This is a November2026 directory snapshot, not a2025 census.

Milan's official Milanosport tariff effective1June2025 names13 indoor venues in tariffA and4 in tariffB. It offers single-entry admission; it is not merely an annual-club list. The current facility directory corroborates operator venue identities. The PDF filename suggests9October2025 while its footer says9September2025; the effective date and2025year are explicit, but the update month is not used. Other operators and outdoor venues are uncounted, and tariffs do not prove continuous opening of every site.

Both observations are partial facility inventories, with upper utility1. They describe supply, not universal teenage accessibility, affordability or year-round capacity. The existing attachment population is used unchanged and not externally verified: Zurich440,935 and Milan1,399,079, both labeled2025. Zurich therefore explicitly mixes a2026venue snapshot with the provided2025population.

With original density anchor1venue/100000, `d=count*100000/population`, `utility=[d/(1+d),1]`. Zurich gives`[0.6135318839,1]`; Milan gives`[0.5485500692,1]`. These fill only previously blank pool cells; no attachment value is overwritten.

`extract.py` verifies official source-name anchors, unique facility names, empty attachment cells and unchanged populations, then writes`observations.json` and`manifest.json`. The two provider captures are explicitly Exa-extracted official text, not originalHTML/PDF bytes. The manifest also hashes the reused attachment. No model or registry changes are made here.

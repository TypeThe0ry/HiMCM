# Prague source and reproducibility review

The independent review matches all 7,326 archived link occurrences and the 942-node cross-snapshot candidate. It recomputes the 64 numerical preview cases with maximum score/regret discrepancy 1.42e-14. The candidate remains unadmitted; the evidence establishes source associations, not a dated physical-stop census or actual passenger departures.

`peer_review.json` records the independent lxml parser, exact crosswalk, observed missing night flags, metro overlap and scalar checks. `verification.json` binds nine newly archived HTTP bodies, twenty-one reused directory responses and the derived packets, and checks the 658 frozen scientific bindings. Offline regeneration preserves the stored derived bytes. File hashes and parser agreement do not certify facility identity, target coverage or operations.

The inventory uses Beautiful Soup, which is absent from the locked model environment. Reproduce its source-packet verification in an isolated environment without changing that environment:

```bash
UV_CACHE_DIR=/data/scratch/uv-cache uv run --no-project \
  --python /data/scratch/himcm-current-check-env/bin/python \
  --with beautifulsoup4==4.14.3 \
  python research/2026-a/scripts/task4_current_prague_source_packets.py
```

The verifier refuses to overwrite its frozen proof; use a scratch checkout with that output absent. It regenerates the two packet extractors before comparing their output bytes. Run the separate numeric preview in the locked current-check environment, also with an absent output directory in a scratch checkout. No primary Monte Carlo, manuscript build or online preview was rerun for this source-only candidate.

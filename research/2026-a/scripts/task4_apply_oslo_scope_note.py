#!/usr/bin/env python3
"""Apply the Oslo commute source-scope note to the 720aa75 manuscript."""
from pathlib import Path
import sys
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/data/projects/HiMCM-Overleaf/main.tex')
s = p.read_text()
changes = [
("both; withdrawing all twelve supplied means selects Singapore and Zurich,\nrespectively. Both preference profiles select Oslo.", "both; withdrawing Oslo's commute proxy alone selects Zurich under both.\nWithdrawing all twelve means selects Singapore and Zurich, respectively. Both preference profiles select Oslo."),
("28.8 minutes for 2011 and Zurich's 39.9 for 2024 as journeys to work, currently\nlabelled ``greater city''; Zurich's value is flagged estimated", "28.8 minutes for 2011, Zurich's 39.9 for 2024, and Oslo's 31.0 for 2009 as\njourneys to work, currently labelled ``greater city''; Zurich's value is flagged estimated"),
("Withdrawing Zurich's commute proxy or both identified proxies selects Oslo under\n", "Withdrawing Oslo's commute proxy alone selects Zurich under both weights; all\nsixteen remain possible champions and none is necessary. Withdrawing Zurich's\ncommute proxy, or both Zurich's and Dublin's proxies, selects Oslo under\n"),
("Both education and independent-living priority profiles select Oslo. In separate\nhypothetical ten-per-cent changes, baseline weights also select Oslo in all three", "Setting aside Oslo's work-commute proxy selects Zurich under both weight sets.\nIn hypothetical ten-per-cent changes, baseline weights select Oslo in all three"),
("Retrieved 10 November 2026: IE001C/2011, 28.8; CH002C/2024, 39.9,\nflag e (estimated). Current labels are Dublin and Zurich (greater city);", "Retrieved 10 November 2026: IE001C/2011, 28.8; CH002C/2024, 39.9,\nflag e (estimated); NO001C/2009, 31.0. Current labels are Dublin, Zurich and\nOslo (greater city);")
]
for a, b in changes:
    if s.count(a) != 1:
        raise ValueError(f'Expected exactly one occurrence: {a!r}')
    s = s.replace(a, b, 1)
p.write_text(s)

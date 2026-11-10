#!/usr/bin/env python3
"""Apply the Oslo registry sensitivity disclosure to the 12e1cd2 paper source."""
from pathlib import Path
import sys

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/data/projects/HiMCM-Overleaf/main.tex')
s = path.read_text()
changes = [
('all sixteen remain possible champions within the retained evidence intervals.\n', 'all sixteen remain possible champions within the retained evidence intervals.\nAn alternative Oslo transport counting definition selects Oslo under both weights.\n'),
('similarly separates 19 Helsinki stations from 11 in Espoo \\cite{helsinki}.\n', 'similarly separates 19 Helsinki stations from 11 in Espoo \\cite{helsinki}.\nEntur\'s 9 November 2026 Oslo registry export yields 829 mode-bearing\nadministrative stop places after native parent grouping \\cite{enturstop}, using\nthe same population of 727,797. Used only in the check below, it is not added\nto the 89 stations.\n'),
('Dates and flags are screening criteria, not error probabilities.\n', 'Dates and flags are screening criteria, not error probabilities.\n\nConditionally treating Oslo\'s 829 registry groups as comparable stop units\ninstead of the 89-station lower bound selects Oslo under both weight sets;\nall sixteen cities remain possible champions and none is necessary. The\nregistry does not establish deduplicated physical facilities or current service,\nso the primary analysis retains the 89-station bound.\n'),
('\\bibitem{vbz} Verkehrsbetriebe', '\\bibitem{enturstop} Entur. National Stop Place Registry, Oslo export dated 9 November 2026; NeTEx stop-place and parent-group definitions. \\url{https://developer.entur.org/pages-nsr-nsr/}; \\url{https://enturas.atlassian.net/wiki/plugins/viewsource/viewpagesrc.action?pageId=3846668311}.\n\\bibitem{vbz} Verkehrsbetriebe')
,
("Every primary city belongs to a different country, so the main sample cannot\nidentify within-country city contrasts. We use the existing United States and\nIndia cases as frozen legacy25 V117 examples with the same ten indicator\ndefinitions and scoring formula \\cite{legacycase}. They do not enter the sixteen-city ranking,\nand comparison within a country does not remove differences in source year,\ncity boundary or educational coverage.\n", "The primary sample has one city per country. Frozen US and India cases use the same\nten indicators and scoring formula, outside the sixteen-city ranking \\cite{legacycase}.\n"),
("Affordability uses Numbeo's 2025 named-city aggregates \\cite{numbeocase};\nMumbai--Delhi air uses 2021 WHO monitoring means \\cite{whocase}.\nThe retained historical city and education scopes identify neither a necessary\nwinner nor a national causal effect.\n", "These historical city and education scopes identify neither a necessary winner nor a national causal effect.\n")
,
("We adapt TOPSIS \\cite{topsis} using fixed reference anchors to preserve a common scoring scale across evidence,\npreference and future scenarios. For benefit and cost measurements respectively,\n", "Fixed-anchor TOPSIS \\cite{topsis} gives benefit and cost utilities, respectively:\n")
]
for old,new in changes:
    if s.count(old) != 1:
        raise ValueError(f'Expected exactly one occurrence: {old!r}')
    s = s.replace(old,new,1)
path.write_text(s)

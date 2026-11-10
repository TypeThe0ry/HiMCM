#!/usr/bin/env python3
"""Apply the Oslo–Zurich spatial comparison to manuscript HEAD 30fe18f."""
from pathlib import Path
import sys
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/data/projects/HiMCM-Overleaf/main.tex')
s = p.read_text()
old = r'''An auxiliary spatial view retains the residents and generic Learning POIs in
Bruno et al.'s published grids \cite{brunogrids}. In Singapore, 94.13\% of retained
residents live in cells with modelled mean walking time at most 30 minutes to
20 Learning POIs; Zurich's share is 99.97\% (Figure~\ref{fig:walktime-context}).
These grid means describe neither student trips nor access to the counted pools;
they remain separate from the primary scores.'''
new = r'''An auxiliary spatial view retains residents and generic Learning POIs in
Bruno et al.'s published grids \cite{brunogrids}. In Oslo, 99.18\% of retained
residents live in cells with modelled mean walking time at most 30 minutes to
20 Learning POIs; Zurich's share is 99.97\% (Figure~\ref{fig:walktime-context}).
These grid means describe neither student trips nor access to the counted pools;
they remain separate from the primary scores.'''
oldcap = r'''\caption{Modelled access to general learning facilities in retained resident grids.
Colours and heights encode each cell's mean walking time to 20 Learning POIs,
using a common 0--150 minute scale; height is not terrain or buildings.
The labelled percentages weight qualifying cells by retained resident population.
The cities have different horizontal extents, and empty cells are not a water mask.
Zurich's NASA HLS S30/GIBS background was requested for 27 June 2024;
cloud remains visible, and Singapore has no satellite backdrop \cite{nasagibs}.
Grids are the author-platform snapshot accessed 7 November 2026; underlying
city input dates are unstated. They do not measure high-school or pool access
\cite{brunogrids}.}'''
newcap = r'''\caption{Modelled walking time to 20 generic Learning POIs in retained resident
cells. Colours and heights use a common 0--150 minute scale; height is not terrain.
Percentages weight cells with mean time at most 30 minutes by retained residents.
Grids were captured on 10 November (Oslo) and 7 November 2026 (Zurich); input
years are unstated and boundaries differ \cite{brunogrids}. Oslo's retained 686,862
residents differ from the primary population of 727,797. Three Oslo NASA HLS
requests were transparent, so its backdrop is geometry only. Zurich's requested
27 June 2024 background is cloudy; the granule date is unverified \cite{nasagibs}.
Neither panel measures student, high-school or pool access.}'''
for a,b in [(old,new),(oldcap,newcap)]:
    if s.count(a)!=1: raise ValueError('Expected exactly one matching passage')
    s=s.replace(a,b,1)
p.write_text(s)

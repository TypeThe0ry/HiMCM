from pathlib import Path
import hashlib,json,shutil,difflib
D=Path(__file__).resolve().parent; R=Path('/data/projects/HiMCM/research/2026-a')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def edit(s,a,b):
 assert s.count(a)==1,(a,s.count(a)); return s.replace(a,b)
proof=json.loads((R/'results/task4_v200_transition/verification.json').read_text()); assert proof['status']=='pass'
for section in ['source_sha256','result_sha256']:
 for n,h in proof[section].items(): assert sha(R/n)==h,n
names=['paper','front','core','conclusion','news','vintage','references','ai','evidence_figure']
t={n:(D/f'task4_v198_{n}.tex').read_text().replace('task4_v198_','task4_v201_').replace('V198','V201').replace('V197','V200') for n in names}
t['core']=edit(t['core'],r'''Named subsets include seven Singapore venues from April 2025, twelve Zurich
venues captured in November 2026 and seventeen Milan indoor venues under the
June 2025 tariff \cite{sgpool_2025,zurichpool,milanpool2025}.''',r'''Named subsets include 25 Singapore venues in the ActiveSG directory captured
10 November 2026, twelve Zurich venues and seventeen Milan indoor venues under
the June 2025 tariff \cite{sgpool_directory,sgpool_2025,zurichpool,milanpool2025}.
The Singapore inventory counts physical venues, not currently open pools or
teen access; four pool-specific temporary notices affect three venues. Withholding
those three venues leaves 22 and retains Zurich under both weight references.''')
t['core']=edit(t['core'],'''At baseline concentration 100, Zurich has a smaller sample mean decision rank
(2.0269) than Oslo (2.1779) and the higher sample recommendation frequency.''','''At baseline concentration 100, Singapore, Zurich and Oslo have sample mean
decision ranks 2.0764, 2.1586 and 2.3354 respectively; Zurich has the highest
sample recommendation frequency.''')
t['core']=edit(t['core'],'''Oslo minus Zurich at baseline concentration
100 gives $[-0.563,0.865]$, leaving their expected mean-rank order unresolved
by this guarantee.''','''The simultaneous certificate resolves 4,259 of 4,440 pairwise mean-rank
comparisons, leaves 181 unresolved, and certifies a unique smallest expected
rank in 17 of 37 settings. The baseline top-city mean-rank ordering remains
unresolved by this guarantee.''')
t['vintage']=t['vintage'].replace('from 16.01 to 48.37','from 15.96 to 48.34').replace('0.31194 and 1.15472','0.14951 and 1.03432').replace('54.05 minutes','40.53 minutes').replace('13.01105\\% (baseline) and 63.44548\\% (equal)','1.57080\\% (baseline) and 63.44548\\% (equal)').replace('at it Oslo can tie','at it Singapore (baseline) or Oslo (equal) can tie')
t['front']=edit(t['front'],'Oslo. \\SummaryWeightMC{}','Singapore. \\SummaryWeightMC{}'); t['front']=edit(t['front'],'Three uniform ten-per-cent development scenarios retain Zurich; separate','Under uniform ten-per-cent changes, resource expansion selects Singapore under baseline weights; the other scenarios retain Zurich. Separate')
t['conclusion']=t['conclusion'].replace('Education priority selects Oslo.','Education priority selects Singapore.')
t['news']=t['news'].replace('points to Oslo.','points to Singapore.').replace('Oslo then becomes the cautious recommendation.','Singapore then becomes the cautious recommendation.').replace('Zurich remains the cautious recommendation under both baseline and equal priorities.','resource expansion selects Singapore under baseline priorities; Zurich remains the recommendation in the other scenarios and under equal priorities.')
pos=t['references'].index('\\bibitem{sgpool_2025}');t['references']=t['references'][:pos]+r'''\bibitem{sgpool_directory} Sport Singapore, ActiveSG Circle. Swimming pool
facility directory and 25 linked venue details, retrieved 10 November 2026.
\url{https://www.activesgcircle.gov.sg/facilities/swimming-pools}.
'''+t['references'][pos:]
t['front']=r"""\begin{abstract}
We compare sixteen cities for high-school life across ten indicators. Fixed-anchor
TOPSIS and maximum regret recommend Zurich under baseline and equal weights;
all sixteen remain possible champions within the retained evidence intervals.

Official records supplement 25 originally missing city--indicator entries without
replacing team values. The mean score-interval width falls from 18.81077 to
\CurrentMeanWidth{}, a \TotalWidthReduction\% reduction. The interval revision
retains 48 uncertain entries and changes \RevisionRankChanges{} fixed-weight ranks
from midpoint completion; separate interior completions let each city lead.

Withholding Zurich's homicide point selects Singapore under baseline weights and
Oslo under equal weights. Withdrawing its work-commute proxy selects Singapore
under baseline weights and retains Zurich under equal weights. Doubling the
education emphasis selects Singapore. \SummaryWeightMC{} These frequencies
are conditional on the chosen weight distribution.

Under uniform ten-per-cent development changes, resource expansion selects
Singapore under baseline weights; other scenarios retain Zurich. City-specific
shocks are illustrative, not forecasts. Country, district and age-group cases
distinguish facility supply from student access and broad observed groups from
unsupported age-specific preferences.
\begin{keywords}
high-school opportunities; TOPSIS; interval evidence; maximum regret; preference sensitivity.
\end{keywords}
\end{abstract}
\maketitle
\clearpage
\tableofcontents
"""
t['conclusion']=r"""\section{Conclusion and decision use}
Zurich minimizes maximum regret under baseline and equal weights; all sixteen
cities remain possible champions. Education priority selects Singapore. Evidence
supplements narrow the mean score interval by \TotalWidthReduction\%; the interval
revision changes 13 decision ranks. Families can compare priorities and source bounds.
"""
t['front'] += (D/'task4_v198_front.tex').read_text().split('\\tableofcontents',1)[1]
t['references']=t['references'].replace('\\raggedright','\\raggedright\n\\setlength{\\parskip}{0pt}\\setlength{\\itemsep}{0pt}\\interlinepenalty=10000',1)
for n,s in t.items(): (D/f'task4_v201_{n}.tex').write_text(s)
(D.parent/'task4_v201_review_entry.tex').write_text('% Owned independent review; default Main unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v201_paper.tex}\n')
(D/'task4_v201_prose_diff.txt').write_text('\n'.join(''.join(difflib.unified_diff((D/f'task4_v198_{n}.tex').read_text().splitlines(keepends=True),t[n].splitlines(keepends=True),fromfile='V198/'+n,tofile='V201/'+n)) for n in names))
m={'version':'V201 staged','science':'V200 staged','source_sha256':{**proof['source_sha256'],**proof['result_sha256']},'source_directory_manifest_sha256':sha(R/'data/task4_v199_sgpool/manifest.json'),'base_sha256':{f'task4_v198_{n}.tex':sha(D/f'task4_v198_{n}.tex') for n in names},'exact_prose_diff':'task4_v201_prose_diff.txt','activation':False,'registration':'18213 provisional'}
(D/'task4_v201_manifest.json').write_text(json.dumps(m,indent=2)+'\n')

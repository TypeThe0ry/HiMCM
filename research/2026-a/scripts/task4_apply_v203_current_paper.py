"""Apply V203 numerical evidence to the single current Overleaf entry."""
from pathlib import Path
import re,shutil,hashlib
import pandas as pd
R=Path('/data/projects/HiMCM/research/2026-a'); P=Path('/data/projects/HiMCM-Overleaf'); main=P/'main.tex';s=main.read_text();original=s
# Only accept the reviewed V202 entry.
assert hashlib.sha256(main.read_bytes()).hexdigest()=='4291a471ff653f3b25aeb48c400e389d43d2ad445ec9111e8a81a19dab5d19f0'
assert 'Zurich minimizes maximum regret, followed by Singapore and Oslo' in s
for line in (R/'results/current_paper_assets/generated.tex').read_text().splitlines():
 m=re.match(r'\\newcommand\{\\(\w+)\}',line)
 if m and m.group(1) not in {'EquityCase','AgeCase','CountryInterpretation','CaseReferences'}:
  pattern=r'^\\newcommand\{\\'+m.group(1)+r'\}\{.*\}$'
  if re.search(pattern,s,re.M):s=re.sub(pattern,lambda _:line,s,count=1,flags=re.M)
def rep(old,new):
 global s
 assert s.count(old)==1,old[:100];s=s.replace(old,new)
def section(start,end,new):
 global s
 assert s.count(start)==1 and end in s[s.index(start):]
 a=s.index(start);b=s.index(end,a);s=s[:a]+new+'\n\n'+s[b:]
rep('TOPSIS and maximum regret recommend Zurich under baseline and equal weights;\nall sixteen remain possible champions within the retained evidence intervals.\nAn alternative Oslo transport counting definition selects Oslo under both weights.','TOPSIS and maximum regret recommend Oslo under baseline weights and Zurich\nunder equal weights; all sixteen remain possible champions within the retained\nevidence intervals. An alternative registry counting definition selects Oslo under both.')
section("Withholding Zurich's homicide point selects Singapore under baseline weights and",'\\begin{keywords}',r'''Withholding Zurich's homicide point retains Oslo under baseline weights and selects
Oslo under equal weights. Withdrawing its work-commute proxy selects Oslo under
both; withdrawing all twelve supplied means selects Singapore and Zurich,
respectively. Both preference profiles select Oslo. \SummaryWeightMC{} These
frequencies are conditional on the chosen weight distribution.

Under uniform ten-per-cent development changes, Oslo is selected in all three
scenarios under baseline weights; equal weights select Oslo, Zurich and Oslo.
City-specific shocks are illustrative, not forecasts. Country, district and
age-group cases distinguish facility supply from student access and broad
observed groups from unsupported age-specific preferences.''')
section("Selecting Oslo's municipal GIS records within the city boundary yields 89",'For a verified subset count $c$',r'''Entur's 9 November 2026 registry export supplies 626 Oslo bus stop groups
under the source-defined pure on-street bus subset and native parent grouping
\cite{enturstop}. The questioned Tveten bru entry is excluded as a precaution,
without a confirmed closure. The 2026 inventory uses the supplied 2025 population of
727,797; it is not a 2025 count or a count of all currently served stops. The
alternative 829 mode-bearing registry groups use a broader counting definition;
they are not added to the 626, which replaces the earlier 89-station metro subset. Zurich's 2025 VBZ report distinguishes 446 city
stops from 235 outside the city \cite{oslo,vbz}. Helsinki's November 2026
operator snapshot separates 19 Helsinki stations from 11 in Espoo \cite{helsinki}.''')
section('Zurich minimizes maximum regret, followed by Singapore and Oslo','\\begin{table}[!ht]\\centering',r'''Oslo minimizes maximum regret, followed by Zurich and Singapore
(Table~\ref{tab:baseline}). Oslo's lower score bound is 56.43 and its maximum
regret is 15.75; Zurich's corresponding values are 53.97 and 16.94. All sixteen
cities remain possible champions, and none is necessary. These rankings express
a conservative recommendation under the stated criteria and intervals.''')
a=s.index('\\begin{table}[!ht]\\centering',s.index('\\subsection{Scoring results and interpretation}'));b=s.index('\\end{table}',a)+len('\\end{table}')
df=pd.read_csv(R/'results/task4_user_v203_revision/current_ranks.csv');df=df[(df.scenario=='after_conditional')&(df.weight_reference=='fixed')].sort_values('decision_rank').reset_index(drop=True);assert len(df)==16
lines=[]
for i in range(8):
 l,r=df.iloc[i],df.iloc[i+8]
 lines.append(f"{int(l.decision_rank)} & {l.city} & {l.score_lower:.2f}--{l.score_upper:.2f} & {l.max_regret:.2f} & {int(r.decision_rank)} & {r.city} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f} \\\\")
table=r'''\begin{table}[!ht]\centering
\caption{Conservative baseline decision ranks with unchanged weights.}\label{tab:baseline}
\begingroup\setlength{\tabcolsep}{2pt}
\begin{tabular}{rlrr@{\quad}rlrr}\toprule
Rank & City & Score interval & Regret & Rank & City & Score interval & Regret\\\midrule
'''+ '\n'.join(lines)+r'''
\bottomrule\end{tabular}\endgroup\end{table}'''
s=s[:a]+table+s[b:]
rep("Earlier additions improved Stockholm's decision position. Withdrawal of the historical Paris and Dublin transport inventories still recommends Zurich; withdrawal of Singapore's historical school-stage travel proxy also preserves this recommendation.","The revised Oslo transport subset changes the baseline conservative recommendation. Withdrawing Singapore's historical school-stage travel proxy retains Oslo under baseline weights.")
a=s.index('\\subsection{A significant revision: retaining uncertain evidence}');b=s.index('\\subsection{Sensitivity to the accepted input information}',a);s=s[:a]+(R/'results/current_paper_assets/revision.tex').read_text()+'\n'+s[b:]
a=s.index('\\begin{table}[!ht]\\centering',s.index('\\subsection{Sensitivity to the accepted input information}'));b=s.index('\\end{table}',a)+len('\\end{table}');s=s[:a]+(R/'results/current_paper_assets/vintage_table.tex').read_text()+s[b:]
section('Withdrawing 28 flagged points selects Berlin','\\section{Model revision and extension}',r'''Withdrawing 28 flagged points selects Oslo under both weights; removing 13
pre-2020 points selects Singapore or Zurich, respectively. Removing 64 post-2025
points selects Zurich under both and widens the baseline mean range from 15.82
to 48.23. The 95-point union selects Singapore under both. Dates and flags are
screening criteria, not error probabilities.

Withdrawing the 626 bus subset and restoring the earlier 89 metro stations
selects Zurich under both weight sets. Treating 829 registry groups as
comparable units instead of the 626 bus subset selects Oslo under both weight sets. The broader definition does not establish
separate physical facilities or current service. Withholding the two replacement
bus groups, the Midtstuen bus group, or both retains Oslo under baseline and
Zurich under equal weights.

Withholding Zurich's homicide point retains Oslo under baseline weights and
selects Oslo under equal weights; withholding Amsterdam's retains Oslo and Zurich,
respectively. Varying Zurich's rate between zero and five per 100,000 does not
change the fixed-weight selection; under equal weights the tie occurs near
0.14981. These are hypothetical rates with other inputs fixed.

Withdrawing Zurich's commute proxy or both identified proxies selects Oslo under
both weights; withdrawing all twelve means selects Singapore under baseline and
Zurich under equal weights. Dublin alone leaves the baseline choices unchanged.
Varying only Zurich's mean gives ties at 28.10 minutes under baseline weights and
40.50 under equal weights: Zurich is selected below each tie and excluded above.
At the retained 39.9 minutes, the baseline selection is Oslo.

Jointly vary each of the twelve means $t_i$ independently in
$[(1-\delta)t_i,(1+\delta)t_i]$, $0\leq\delta\leq1$, retaining all other
entries. Fixed upper scores make each regret increase with its own mean. The
largest target mean and the other eleven smallest maximize the target's regret
relative to the best rival. The critical radii are 15.6063\% for baseline
winner Oslo and 0.6483\% for equal-weight winner Zurich. Below each boundary the
respective winner uniquely minimizes regret throughout the box; at it the other
can tie, and above it a counterexample exists. These conditional ranges are not
measured errors or future probabilities.''')
a=s.index('\\begin{table}[!ht]\\centering',s.index('\\subsection{Perturbing weights}'));b=s.index('\\end{table}',a)+len('\\end{table}');s=s[:a]+(R/'results/current_paper_assets/preferences.tex').read_text()+s[b:]
section('At baseline concentration 100, Singapore, Zurich and Oslo have sample mean','We retain minimum maximum regret',r'''\MonteCarloInterpretation{} Oslo has the highest sample recommendation frequency.''')
rep('resolves 4,260 of 4,440 pairwise mean-rank\ncomparisons, leaves 180 unresolved, and certifies a unique smallest expected\nrank in 18 of 37 settings. The baseline top-city mean-rank ordering remains\nunresolved by this guarantee.','resolves 4,271 of 4,440 pairwise mean-rank\ncomparisons, leaves 169 unresolved, and certifies a unique smallest expected\nrank in 23 of 37 settings.')
section('Zurich minimizes maximum regret under baseline and equal weights; all sixteen','\\clearpage\n\\phantomsection\\addcontentsline{toc}{section}{News article}',r'''Oslo minimizes maximum regret under baseline weights and Zurich under equal
weights; all sixteen cities remain possible champions. Both preference profiles
select Oslo. Evidence supplements narrow the mean score interval by
\TotalWidthReduction\%; the interval revision changes 14 decision ranks.''')
section('Our comparison of sixteen cities across ten aspects of high-school life','\\label{news-end}',r'''Our comparison of sixteen cities across ten aspects of high-school life gives
families a starting point for weighing everyday trade-offs. Oslo is the cautious
recommendation under baseline and education-priority weights; Zurich is selected
when all ten measures receive equal weight. The priorities are analyst-designed,
not drawn from a student survey. All sixteen cities remain possible leaders, so a
family's choice can depend on the evidence and priorities it considers relevant.

\subsection*{How the comparison works}

The measures cover safety, air quality, housing and living costs, teaching
resources, higher education, transport stops, journey time, broadband and
swimming facilities. Their units differ: a travel time and a pool count cannot
be compared directly. The model puts each measure on a common reference scale,
then combines them using the stated priorities. Missing or partial figures remain
ranges instead of being filled with invented averages.

A single completed table could make one city look certain to win even when the
missing information matters. We therefore compare each city's largest possible
shortfall behind another city within the retained ranges. The cautious choice is
the city with the smallest such shortfall. This gives families a way to discuss
trade-offs while keeping uncertain information visible.

\subsection*{What new records change}

Additional evidence narrows the average city-score range by about sixteen per cent
while retaining the team's original values and scoring rules. For Oslo, a 2026
registry provides a source-defined subset of 626 on-street bus stop groups. It
replaces the earlier subset of 89 metro stations, rather than being added to it;
the comparison uses the supplied 2025 population. Restoring the earlier subset
selects Zurich under both baseline and equal weights. This change shows how a
source definition can affect a recommendation, and invites a closer look at what
each city count includes.

The counts describe supply, not an individual student's access. A nearby stop may
still require a suitable route, service time, fare and accessible connection. A
pool count does not describe fees, opening hours or neighbourhood reach. Families
can check these details alongside school options, budgets and daily routines.

\subsection*{Trying different priorities}

Both education and independent-living priority profiles select Oslo. In separate
hypothetical ten-per-cent changes, baseline weights also select Oslo in all three
scenarios. Equal weights select Oslo for resource expansion and balanced
improvement, and Zurich under living pressure. These are conditional tests of the
model, not forecasts or a city's real chance of being best. The comparison is most
useful as a prompt to identify which priorities and local facts matter for a
particular student.''')
s=s.replace('particular student.\n\n\\label{news-end}','particular student.\n\\label{news-end}')
rep('Source: V202 utility bounds.','Source: V203 utility bounds.')
rep('% Current manuscript assets from V202 evidence and controlled extensions; historical cases retained.','% Current manuscript assets from V203 evidence and controlled extensions; historical cases retained.')
rep('the V202 primary\nevidence. The V202 validation','the V203 primary\nevidence. The V203 validation')
assert s!=original
main.write_text(s)
for name in ['score_intervals.pdf','identification_matrix.pdf']:shutil.copyfile(R/'results/current_paper_assets'/name,P/'figures'/name)
print('Updated current main and two figures')

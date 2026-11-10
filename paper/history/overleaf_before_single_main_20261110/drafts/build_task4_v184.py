"""Clarify matched work-commute provenance and its controlled decision sensitivity."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
R=D.parent.parent/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def swap(text,a,b):assert text.count(a)==1,(a,text.count(a));return text.replace(a,b)
def main():
    names=['paper','front','core','conclusion','news','references','ai']
    sources={n:(D/f'task4_v182_{n}.tex').read_text() for n in names}
    report=json.loads((R/'results/task4_v184_source_review/summary.json').read_text());assert len(report['cases'])==10 and report['primary_admissions']==0
    assert next(x for x in report['cases'] if x['scenario']=='withdraw_Zurich_work_commute' and x['weight_reference']=='fixed')['conservative_recommendation']==['Singapore']
    core=sources['core'];a=core.index('The nominal reference year is 2025');b=core.index('We use official statistical tables',a)
    paragraph=r'''The nominal reference year is 2025; supplements retain their actual years and
supplied population denominators. Matching Eurostat records give Dublin's
28.8 minutes for 2011 and Zurich's 39.9 for 2024 as journeys to work, currently
labelled ``greater city''; Zurich's value is flagged estimated \cite{eurostatcommute}.
These matches establish neither the team's source lineage nor the historical
boundary. We retain the supplied means, years and flags as conditional
general-commute proxies. They do not identify high-school journeys.
Mixed-year densities and historical inventories remain conditional;
withdrawal scenarios examine their role in the decision.

'''
    core=core[:a]+paragraph+core[b:];core=swap(core,'task4_v182_assets/vintage.tex','task4_v184_vintage.tex')
    vintage=r'''\subsection{Sensitivity to the accepted input information}\label{sec:sourcepolicy}
Point-withdrawal tests keep the primary data, weights, supplements and 48
non-point bounds fixed, replacing selected point utilities by $[0,1]$.
Of 112 points, 64 are dated 2026, two 2025 and 46 earlier. The 28
non-\texttt{ok} points comprise 16 \texttt{MODELLED}, eight \texttt{STALE},
three \texttt{SUSPECT} and one \texttt{NATIONAL}. Groups cover dates before
2020, after 2025, non-\texttt{ok} flags and their union; overlaps count once.

\input{task4_v182_assets/vintage_table.tex}

Withdrawing 28 flagged points selects Berlin under baseline weights and Paris
under equal weights. Removing 13 pre-2020 points selects Singapore under
baseline weights and retains Zurich under equal weights. Removing 64
later-dated points retains Zurich under both, widening the baseline mean
range from 16.05 to 48.41. The 95-point union selects Singapore under both.
All sixteen remain possible champions. Labels and cutoffs are not error
probabilities or proof that flagged entries are wrong.

Withholding Zurich's homicide-rate point selects Singapore under baseline
weights and Oslo under equal weights; withholding Amsterdam's retains Zurich
under both. Other entries remain fixed, without a replacement rate.
Varying only Zurich's point rate gives regret ties at about 0.23002 per 100,000
under baseline weights and 0.90473 under equal weights. Below each respective
cutoff Zurich uniquely minimizes regret; above it Zurich does not. These are
hypothetical cutoffs, not measured rates or confidence limits.

Separately withdraw commute proxies by replacing their travel intervals with
$[0,1]$, fixing other entries. Withholding Zurich's alone, both identified
proxies, or all twelve supplied commute means selects Singapore under baseline
weights; equal weights retain Zurich. Withholding Dublin's alone retains Zurich
under both. All sixteen remain possible champions. The baseline recommendation
therefore depends on retaining Zurich's work-commute proxy.
'''
    front=sources['front'];a=front.index('A controlled formulation revision');b=front.index('Preferences and development conditions',a)
    front=front[:a]+r'''The interval revision retains 48 uncertain entries and Zurich's recommendation,
while \RevisionRankChanges{} fixed-weight ranks change from midpoint completion.
Separate interior completions let each city rank first. Withholding Zurich's
homicide point selects Singapore under baseline weights and Oslo under equal
weights. Separately withdrawing its work-commute proxy selects Singapore under
baseline weights; equal weights retain Zurich. These tests show dependence
on accepted inputs.

'''+front[b:]
    conclusion=r'''\section{Conclusion and decision use}
Zurich minimizes maximum regret under baseline and equal weights; all sixteen
cities remain possible champions. Education priority selects Oslo. Withholding
Zurich's homicide point selects Singapore under baseline weights and Oslo under
equal weights; withdrawing its work-commute proxy selects Singapore under
baseline weights but retains Zurich under equal weights. Withdrawing 28 flagged points
selects Berlin and Paris, respectively.

Verified supplements narrow mean score-interval width by \TotalWidthReduction\%
while preserving supplied values. At fixed evidence, the interval revision changes
13 decision ranks and allows each city to lead in a separate completion.
Families can use the recommendation as a starting point, then examine their
priorities and source bounds.
'''
    news=swap(sources['news'],"The original figure remains in the declared baseline; no replacement rate is assumed.","Separately setting aside Zurich's general work-commute proxy also points to Singapore under the original priorities; equal priorities retain Zurich. The supplied figures remain in the baseline; these checks test which information the recommendation depends on.")
    refs=swap(sources['references'],r'\end{thebibliography}',r'''\bibitem{eurostatcommute} Eurostat.
\textit{Transport---cities and greater cities}, dataset urb\_ctran,
TT1019V, average time of journey to work (minutes).
Retrieved 10 November 2026: IE001C/2011, 28.8; CH002C/2024, 39.9,
flag e (estimated). Current labels are Dublin and Zurich (greater city);
exact historical boundary and survey window are not established here.
\url{https://ec.europa.eu/eurostat/databrowser/view/urb_ctran/default/table?lang=en}.
\end{thebibliography}''')
    ai=swap(sources['ai'],r'used 8--9 November 2026. The task log',r'used 8--10 November 2026. The task log')
    paper=sources['paper']
    for n in names:
        if n=='paper':continue
        paper=swap(paper,f'task4_v182_{n}.tex',f'task4_v184_{n}.tex')
    paper=swap(paper,'% V182 owned review;','% V184 owned review;')
    values=dict(core=core,vintage=vintage,front=front,conclusion=conclusion,news=news,references=refs,ai=ai,paper=paper)
    for n,s in values.items():(D/f'task4_v184_{n}.tex').write_text(s)
    (D.parent/'task4_v184_review_entry.tex').write_text('% Owned independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v184_paper.tex}\n')
    (D/'task4_v184_manifest.json').write_text(json.dumps(dict(version='V184',primary='V181 unchanged',base_review='V182',base_input_sha256={f'drafts/task4_v182_{n}.tex':sha(D/f'task4_v182_{n}.tex') for n in names},controlled_diagnostic_sha256=sha(R/'results/task4_v184_source_review/summary.json'),shared_class_sha256=sha(D.parent/'mcmthesis.cls'),AI_frozen_capture_extended=False,project_settings_changed=False),indent=2)+'\n')
    print('V184 ownedsources generated; baselineV181/allpriorfigures unchanged')
if __name__=='__main__':main()

"""Migrate the current owned V189 paper to independently audited V192 science."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent.parent/'HiMCM/research/2026-a'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def change(s,old,new,n=1):
    assert s.count(old)==n,(old,s.count(old),n)
    return s.replace(old,new)
def main():
    plan=json.loads((R/'results/task4_v192_transition/paper_migration_plan.json').read_text())
    for name,h in plan['authoritative_inputs'].items():assert sha(D.parent/name)==h,name
    proof=json.loads((R/'results/task4_v192_transition/verification.json').read_text());assert proof['status']=='pass'
    for section in ['source_sha256','result_sha256']:
        for name,h in proof[section].items():assert sha(R/name)==h,name
    core=(D/'task4_v189_core.tex').read_text();core=core.replace('rebased to V181 evidence','rebased to V192 evidence').replace('task4_v182_','task4_v193_').replace('task4_v189_vintage.tex','task4_v193_vintage.tex')
    core=change(core,'112 point values, 35 partial intervals and\n13 fully missing intervals: eight teacher-ratio, two transport and three\ntravel entries.','112 point values, 37 partial intervals and\n11 fully missing intervals: eight teacher-ratio and three travel entries.')
    core=change(core,'twenty-three','twenty-five',2)
    addition=r"""Tokyo's Oedo ticket-service directory lists 38 distinct stations in the 23
wards; machine flags are not added. September 2026 updates describe the catalogue; its inventory
date is unstated \cite{tokyooedo}. Warsaw's 21 M1 and 18 M2 entries yield 38
complexes after merging \'Swi\k{e}tokrzyska. Its 2024 map distinguishes planned
stations \cite{warsawmetro}; a 2025 fire report locates the lines within Warsaw
\cite{warsawfirescope}. Counts use Tokyo's 2026 and Warsaw's 2024 populations.

"""
    core=change(core,"Amsterdam's municipal map contains",addition+"Amsterdam's municipal map contains")
    start=core.index("Amsterdam's municipal map contains");end=core.index("London's inventory mixes",start)
    old_amsterdam=core[start:end]
    compact=r"""Amsterdam's 39 provider-grouped Metro locations give 35 inside both municipal
2026 and CBS 2025 boundaries; a declared 100-metre nominal boundary screen
retains 32 \cite{amsterdammetro2026,cbsboundary2025}. The screen defines a subset,
not an accuracy guarantee. The 2026 metadata leave its inventory date unspecified.
The retained 2025 population of 941,927 gives a conditional lower bound,
leaving other transport supply unknown.

"""
    core=change(core,old_amsterdam,compact)
    front=change((D/'task4_v184_front.tex').read_text(),'twenty-three','twenty-five')
    news=change((D/'task4_v184_news.tex').read_text(),'twenty-three','twenty-five')
    conclusion=(D/'task4_v184_conclusion.tex').read_text()
    ai=(D/'task4_v184_ai.tex').read_text();ai=change(ai,'V181','V192',2)
    vintage=(D/'task4_v189_vintage.tex').read_text().replace('task4_v182_','task4_v193_')
    vintage=change(vintage,'from 16.05 to 48.41','from 16.04 to 48.41')
    refs=(D/'task4_v184_references.tex').read_text()
    extra=r'''\bibitem{tokyooedo} Tokyo Metropolitan Government, Bureau of Transportation.
\textit{Oedo Line station list, Toei Subway ticket-service directory}.
Original CSV, 38 named stations; catalogue created 1 September and updated
4 September 2026; inventory reference date unstated. Retrieved 9 November 2026 UTC.
CC BY (version unspecified).
\url{https://spec.api.metro.tokyo.lg.jp/spec/t000018d0000000027-2911e010ab42b6f8fad459fc7dc10e83-0?lang=en};
\url{https://www.opendata.metro.tokyo.lg.jp/kotsu/subway/subway_branch_o_stationlist.csv}.
\bibitem{warsawmetro} Metro Warszawskie.
\textit{M1 and M2 route station directories}; retrieved 9 November 2026 UTC.
\url{https://metro.waw.pl/metro-warszawskie/linia-m1/przebieg/};
\url{https://metro.waw.pl/metro-warszawskie/linia-m2/przebieg/}.
\textit{Network plan}, marked April 2024; the hosting path is not its content date.
\url{https://metro.waw.pl/wp-content/uploads/2026/02/PLAN-METRA_2.pdf}.
\bibitem{warsawfirescope} Mazovian Provincial Headquarters, State Fire Service.
\textit{Information bulletin for 2025}, published February 2026, physical p.~4.
Locates 21 M1 and 18 M2 station appearances within Warsaw; the shared interchange
is consolidated using the operator directories.
\url{https://www.gov.pl/attachment/2b7775c0-aa52-487e-809a-66df1b991b59}.
'''
    refs=change(refs,r'\end{thebibliography}',extra+r'\end{thebibliography}')
    for name,text in [('core',core),('front',front),('news',news),('conclusion',conclusion),('ai',ai),('vintage',vintage),('references',refs)]:
        (D/('task4_v193_'+name+'.tex')).write_text(text)
    paper=(D/'task4_v189_paper.tex').read_text();paper=change(paper,'% V189 owned review;','% V193 owned review;')
    for old,new in [('task4_v182_generated','task4_v193_generated'),('task4_v184_front','task4_v193_front'),('task4_v189_core','task4_v193_core'),('task4_v184_conclusion','task4_v193_conclusion'),('task4_v184_news','task4_v193_news'),('task4_v184_references','task4_v193_references'),('task4_v184_ai','task4_v193_ai')]:paper=change(paper,old,new)
    (D/'task4_v193_paper.tex').write_text(paper)
    (D.parent/'task4_v193_review_entry.tex').write_text('% Owned independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v193_paper.tex}\n')
    original=[D/n for n in ['task4_v189_core.tex','task4_v184_front.tex','task4_v184_news.tex','task4_v184_conclusion.tex','task4_v184_ai.tex','task4_v189_vintage.tex','task4_v184_references.tex','task4_v189_paper.tex']]
    manifest=dict(version='V193',primary='V192',base_owned_review='V189',actual_registered_number_verified=False,display_control_number='18213',edited_scope='New science paths/counts, owned source paragraph and compact Amsterdam explanation; front/news supplement count; inherited jointparagraph widths;3newsource references;AIverificationversiononly',source_sha256={str(p.relative_to(R)):sha(p) for p in [R/'results/task4_v192_transition/verification.json',R/'results/task4_v192_transition/paper_migration_plan.json',R/'design/task4_user_v192_snapshot.json',R/'results/task4_v192_source_diagnostics/summary.json']},paper_input_sha256={str(p.relative_to(D.parent)):sha(p) for p in original+[Path(__file__)]},default_main_setting_changed=False,teammate_files_changed=False,AI_history_complete=False)
    (D/'task4_v193_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('V193ownedsourcegenerated')
if __name__=='__main__':main()

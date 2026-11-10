"""Rebase only owned V196 review to audited V197 pool-refinement evidence."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent.parent/'HiMCM/research/2026-a'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def change(s,a,b,n=1):
 assert s.count(a)==n,(a,s.count(a),n)
 return s.replace(a,b)
def main():
 plan=json.loads((R/'results/task4_v197_transition/paper_migration_plan.json').read_text())
 for n,h in plan['authoritative_inputs'].items():assert sha(D.parent/n)==h,n
 proof=json.loads((R/'results/task4_v197_transition/verification.json').read_text());assert proof['status']=='pass'
 for section in ['source_sha256','result_sha256']:
  for n,h in proof[section].items():assert sha(R/n)==h,n
 core=(D/'task4_v193_core.tex').read_text().replace('V192','V197').replace('task4_v193_','task4_v198_')
 old="""Other named pool subsets contain seven Singapore venues from April 2025,
seven Zurich indoor venues accessed in November 2026, and seventeen Milan
indoor venues under the June 2025 tariff \\cite{sgpool_2025,zurichpool,milanpool2025}.
They count physical venues, not basins or lanes, and leave other providers unknown."""
 new=r"""Named subsets include seven Singapore venues from April 2025, twelve Zurich
venues captured in November 2026 and seventeen Milan indoor venues under the
June 2025 tariff \cite{sgpool_2025,zurichpool,milanpool2025}.
Zurich includes five distinct school pools with limited public sessions, some
women/girls-only, closed during school holidays and non-school days; adult-only
K\"ugeliloo is excluded. Venue supply does not establish adolescent access;
other providers remain unknown."""
 core=change(core,old,new)
 old="""At baseline concentration 100, Oslo has a smaller sample mean decision rank (2.1092)
than Zurich (2.2620), while Zurich has the greater sample recommendation
frequency and is the fixed-weight minimax choice. These summaries describe
different features of the chosen weight distribution. We retain minimum maximum
regret as the predeclared decision rule; weight perturbations report its
sensitivity. A low AHP consistency ratio checks calculation properties,
not representative student opinion."""
 new="""At baseline concentration 100, Zurich has a smaller sample mean decision rank
(2.0269) than Oslo (2.1779) and the higher sample recommendation frequency.
We retain minimum maximum regret as the predeclared decision rule; these
conditional summaries describe its weight sensitivity. A low AHP consistency
ratio checks calculation properties, not representative student opinion."""
 core=change(core,old,new);core=change(core,'$[-0.867,0.561]$','$[-0.563,0.865]$')
 core=change(core,'then supplement only empty cells.','then supplement only fields empty in that original table.')
 old=r'''The current 160 cells comprise 112 point values, 37 partial intervals and
11 fully missing intervals: eight teacher-ratio and three travel entries. The original table had 112 points, 12 partial
intervals and 36 fully missing cells. The twenty-five supplements therefore improve
information without replacing the team's existing measurements. Facility supply,
general commute proxies and school resources remain distinct from adolescent
access, school travel and learning quality.'''
 new=r'''The 160 cells comprise 112 points, 37 partial intervals and 11 fully unknown
entries: eight teacher-ratio and three travel entries. The original table had
112 points, 12 partial intervals and 36 unknowns. Evidence for twenty-five distinct
city--indicator cells fills original gaps while preserving supplied measurements.
Facility supply, commute proxies and school resources remain distinct from
adolescent access, school travel and learning quality.'''
 core=change(core,old,new)
 core=change(core,'70.90353-53.53548=17.36805','70.90353-53.96521=16.93832')
 core=change(core,'the twenty-five admitted supplements narrow','evidence for twenty-five distinct city--indicator cells narrows')
 vintage=(D/'task4_v193_vintage.tex').read_text().replace('task4_v193_','task4_v198_')
 for a,b in [('from 16.04 to 48.41','from 16.01 to 48.37'),('0.23002 and 0.90473','0.31194 and 1.15472'),('46.59 minutes','54.05 minutes'),('7.14733\\% (baseline) and 51.42357\\% (equal)','13.01105\\% (baseline) and 63.44548\\% (equal)')]:vintage=change(vintage,a,b)
 refs=(D/'task4_v196_references.tex').read_text()
 old=r'''\bibitem{zurichpool} City of Z\"urich. Municipal indoor swimming-pool directory,
retrieved 8 November 2026; archived provider-extracted representation.
Current directory snapshot, including W\"armebad K\"aferberg.
'''
 new=r'''\bibitem{zurichpool} City of Z\"urich. Municipal indoor and school-pool directory
and linked venue details. Original HTML retrieved 10 November 2026, including
W\"armebad K\"aferberg; public-session and holiday restrictions retained.
'''
 refs=change(refs,old,new)
 assert 'updated 9 September 2025' in refs
 ai=change((D/'task4_v193_ai.tex').read_text(),'V192','V197',2)
 for name,text in [('core',core),('vintage',vintage),('references',refs),('ai',ai)]:
  (D/f'task4_v198_{name}.tex').write_text(text)
 for name in ['front','news','conclusion']:(D/f'task4_v198_{name}.tex').write_bytes((D/f'task4_v193_{name}.tex').read_bytes())
 figure=(D/'task4_v193_evidence_figure.tex').read_text().replace('V193','V198').replace('V192','V197').replace('task4_v193_','task4_v198_')
 (D/'task4_v198_evidence_figure.tex').write_text(figure)
 entry=(D/'task4_v196_paper.tex').read_text().replace('V196 owned review','V198 owned review').replace('task4_v193_','task4_v198_').replace('task4_v196_references.tex','task4_v198_references.tex')
 (D/'task4_v198_paper.tex').write_text(entry)
 (D.parent/'task4_v198_review_entry.tex').write_text('% Owned independent review; default Main unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v198_paper.tex}\n')
 meta=dict(version='V198',primary='V197',base_review='V196',scope='Only owned evidence paths, pool collection/reference, current numerical results and MC interpretation; frozenAI scope preserved',source_sha256={str(p.relative_to(R)):sha(p) for p in [R/'results/task4_v197_transition/verification.json',R/'results/task4_v197_transition/paper_migration_plan.json',R/'design/task4_user_v197_snapshot.json']},input_paper_sha256=plan['authoritative_inputs'],teammate_content_changed=False,default_Main_changed=False,actual_registered_number_verified=False,display_number='18213 provisional')
 (D/'task4_v198_manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('V198 owned sources generated; no teammate or current registry changes')
if __name__=='__main__':main()

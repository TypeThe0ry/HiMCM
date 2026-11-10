"""Propose/apply the minimum owned V205 manuscript update against a fixed base."""
import argparse,difflib,hashlib,json,re,shutil,subprocess
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1];P=R.parents[1].parent/'HiMCM-Overleaf';A=R/'results/task4_v205_paper_assets'
BASE='48f65d6c2dcdecf3dc9b5577e3d10256f21301bd'
EXPECTED='c1d1a9c2f570c8f716ddc0966107c146a3a3fab525a5f54d1e04588018f82dac'
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--apply',action='store_true');ap.add_argument('--check-applied',action='store_true');args=ap.parse_args();assert not(args.apply and args.check_applied)
 path=P/'main.tex';original=subprocess.check_output(['git','show',BASE+':main.tex'],cwd=P,text=True) if args.check_applied else path.read_text()
 assert hashlib.sha256(original.encode()).hexdigest()==EXPECTED,'Latest manuscript differs; inspect team edits before applying'
 s=original
 for line in (A/'generated.tex').read_text().splitlines():
  m=re.match(r'\\newcommand\{\\(\w+)\}',line)
  if m and m[1] not in {'EquityCase','AgeCase','CountryInterpretation','CaseReferences'}:
   pattern=r'^\\newcommand\{\\'+m[1]+r'\}\{.*\}$'
   if re.search(pattern,s,re.M):s=re.sub(pattern,lambda _:line,s,count=1,flags=re.M)
 def rep(a,b):
  nonlocal s
  assert s.count(a)==1,a[:120];s=s.replace(a,b)
 rep('% Current manuscript assets from V204 evidence and controlled extensions; historical cases retained.','% Current manuscript assets from V205 evidence and controlled extensions; historical cases retained.')
 rep('Source: V204 utility bounds.','Source: V205 utility bounds.')
 rep("Prague retains 57 current\nmetro complexes; Flora's closure explains its omission from the 58 distinct\ncomplexes in the 2025 report, whereas Florenc's partial accessibility restriction\ndoes not close the whole complex \\cite{pidmetro,dpp2025,floraclose}.","Prague's 10 November 2026 service-day GTFS links 942 native PID bus nodes\nusing node/post IDs, calendar checks and administrative city classification.\nFifty have ordinary calls; 892 more use public driver-request calls. This planned,\nsource-defined supply replaces 57 metro complexes (47 shared IDs), without\ncertifying physical-site uniqueness or actual operation \\cite{pidmetro}.\nThe 57-metro subset remains the withdrawal fallback \\cite{dpp2025,floraclose}.")
 rep('Vienna, Berlin and London use November 2026 inventories.','Vienna, Prague, Berlin and London use November 2026 inventories.')
 start=s.index('Rank & City & Score interval & Regret & Rank & City & Score interval & Regret');a=s.index('\n',start)+1;b=s.index('\\bottomrule',a)
 df=pd.read_csv(R/'results/task4_user_v205_revision/current_ranks.csv');df=df.loc[df.weight_reference.eq('fixed')].sort_values('decision_rank').reset_index(drop=True);assert len(df)==16
 table=[]
 for i in range(8):
  l,r=df.iloc[i],df.iloc[i+8];table.append(f'{int(l.decision_rank)} & {l.city} & {l.score_lower:.2f}--{l.score_upper:.2f} & {l.max_regret:.2f} & {int(r.decision_rank)} & {r.city} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f} '+r'\\')
 s=s[:a]+'\n'.join(table)+'\n'+s[b:]
 revision='\\subsection{A significant revision: retaining uncertain evidence}\nRetaining 48 non-point entries selects Oslo with fixed weights and changes 14 decision ranks from midpoint completion ($\\tau_b=0.583$); equal weights change 14 ranks ($\\tau_b=0.750$). This compares diagnostic $z_{ij}=(\\ell_{ij}+h_{ij})/2$ with Equation~\\ref{eq:regret} on identical entries, weights, anchors and TOPSIS scores. The midpoint neither estimates missing observations nor reconstructs a historical model.\n\nFor each target $c$, separately set uncertain utilities to $\\ell_{ij}+\\alpha_i(h_{ij}-\\ell_{ij})$, with $\\alpha_c=0.95$ and $\\alpha_i=0.05$ otherwise. Keep all 112 points fixed and all 48 other values strictly interior. Each target leads under both weights; minimum margins are 2.941 baseline and 2.222 equal-weight points. These completions establish utility-rectangle feasibility, without probabilities or joint physical attainability.\n\nAll sixteen cities remain possible champions. Admitted data give the \\TotalWidthReduction\\% width reduction; the formulation comparison uses identical inputs.'
 a=s.index('\\subsection{A significant revision: retaining uncertain evidence}');b=s.index('\\subsection{Sensitivity to the accepted input information}',a);s=s[:a]+revision+'\n\n'+s[b:]
 a=s.index('\\begin{table}[!ht]\\centering',s.index('\\subsection{Sensitivity to the accepted input information}'));b=s.index('\\end{table}',a)+len('\\end{table}');s=s[:a]+(A/'vintage_table.tex').read_text().rstrip()+s[b:]
 rep('Withdrawing 28 flagged points selects Oslo under both weights; removing 13','Withdrawing 28 flagged points selects Prague and Oslo, respectively; removing 13')
 rep('points selects Zurich under both and widens the baseline mean range from 15.78\nto 48.20.','points selects Zurich under both and widens the baseline mean range from 15.63\nto 48.09.')
 rep("Restoring Vienna's 99 metro areas preserves both choices.","Prague's 57-metro fallback retains both choices. Withholding request-dependent\nwitnesses leaves 50 ordinary bus nodes; the larger 57-metro lower bound remains,\nwithout addition. Restoring Vienna's 99 metro areas also preserves both choices.")
 a=s.index('\\begin{table}[!ht]\\centering',s.index('\\subsection{Perturbing weights and point assumptions}'));b=s.index('\\end{table}',a)+len('\\end{table}');s=s[:a]+(A/'preferences.tex').read_text().replace('for selected cities at concentration 100.','at concentration 100.').rstrip()+s[b:]
 pm=pd.read_csv(R/'results/task4_user_v205_extensions/preferences/mc_city_summary.csv');rows=pm.loc[pm.profile.eq('baseline')&pm.concentration.eq(100)].set_index('city')
 rep('At concentration 100, mean decision ranks are Oslo 1.5680, Zurich 2.5167 and\nSingapore 2.4634.','At concentration 100, mean decision ranks are Oslo '+f'{rows.loc["Oslo","mean_decision_rank"]:.4f}'+', Zurich '+f'{rows.loc["Zurich","mean_decision_rank"]:.4f}'+' and\nSingapore '+f'{rows.loc["Singapore","mean_decision_rank"]:.4f}'+'.')
 rep('Difference intervals resolve 4,274 of 4,440 pairwise mean-rank comparisons;\n166 remain unresolved. Under the declared simulation laws, 23 of 37 settings','Difference intervals resolve 4,278 of 4,440 pairwise mean-rank comparisons;\n162 remain unresolved. Under the declared simulation laws, 22 of 37 settings')
 rep('Prague-only station lists and linked metro timetables, accessed 9 November 2026.\n\\url{https://pid.cz/zastavky-pid/zastavky-v-praze/}.','Prague-only station lists (9 November 2026), native stop data and GTFS\nservice dated 10 November 2026; public request-stop policy from June 2024.\n\\url{https://pid.cz/o-systemu/opendata/};\n\\url{https://pid.cz/vsechny-zastavky-autobusu-a-trolejbusu-v-ramci-pid-budou-na-znameni/}.')
 rep('equal weights. Over $\\epsilon\\in[0,0.2]$, fixed weights certify Oslo through\n0.08135 and Zurich from 0.08136, with unresolved radii between; equal weights\nselect Zurich throughout.','equal weights. Over $\\epsilon\\in[0,0.2]$, padded numerical enclosures retain Oslo\nthrough 0.08135 and Zurich from 0.08136, with unresolved radii between; equal\nweights retain Zurich throughout.')
 rep('The research calculations preserve the original city CSV and the V204 primary\nevidence. The V204 validation independently recomputes weighted norms and','The research calculations preserve the original city CSV and the V205 primary\nevidence. The V205 validation independently recomputes weighted norms and')
 s='\n'.join(line.rstrip() for line in s.splitlines())+'\n'
 assert 'V204' not in s
 assert re.findall(r'\\bibitem\{([^}]+)\}',s)==re.findall(r'\\bibitem\{([^}]+)\}',original)
 for line in original.splitlines():
  if 'We define' in line or '\\mcmsetup' in line or 'tcn=18213' in line:assert line in s
 if args.check_applied:assert s==path.read_text(),'Applied owned diff differs from guarded proposal'
 print(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='main.tex V204',tofile='main.tex V205')))
 if args.apply:
  path.write_text(s)
  for n in ['score_intervals.pdf','identification_matrix.pdf']:shutil.copyfile(A/n,P/'figures'/n)
  print('Applied owned V205 diff; unchanged class/bib/auxiliaryfigures')
if __name__=='__main__':main()

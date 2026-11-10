"""Apply a guarded minimal V204 update to the existing owned manuscript."""
import argparse,hashlib,json,re,shutil,difflib,subprocess
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1];P=R.parents[1].parent/'HiMCM-Overleaf';A=R/'results/task4_v204_paper_assets'
EXPECTED='bad629dd767340f02da9c53a1bb2379f83c849385cd16ea129eb2dfbe00f2fd8'
def read(p):return json.loads(p.read_text())
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--apply',action='store_true');ap.add_argument('--check-applied',action='store_true');args=ap.parse_args();assert not (args.apply and args.check_applied)
    path=P/'main.tex';original=subprocess.check_output(['git','show','1cbec98:main.tex'],cwd=P,text=True) if args.check_applied else path.read_text();assert hashlib.sha256(original.encode()).hexdigest()==EXPECTED
    s=original
    # Preserve every historical case macro and all unmentioned text, including teammate definitions.
    for line in (A/'generated.tex').read_text().splitlines():
        m=re.match(r'\\newcommand\{\\(\w+)\}',line)
        if m and m[1] not in {'EquityCase','AgeCase','CountryInterpretation','CaseReferences'}:
            pattern=r'^\\newcommand\{\\'+m[1]+r'\}\{.*\}$'
            if re.search(pattern,s,re.M):s=re.sub(pattern,lambda _:line,s,count=1,flags=re.M)
    def rep(a,b):
        nonlocal s
        assert s.count(a)==1,a[:100];s=s.replace(a,b)
    rep('% Current manuscript assets from V203 evidence and controlled extensions; historical cases retained.',
        '% Current manuscript assets from V204 evidence and controlled extensions; historical cases retained.')
    rep('Source: V203 utility bounds.','Source: V204 utility bounds.')
    rep('Vienna illustrates why record totals\nalone are insufficient: 1,695 named areas include unverified depot objects,\nso only 99 metro areas individually matched to existing-station geodata and\nthe city polygon are retained \\cite{viennaogd,viennagis}.',
        'Vienna\'s broader register includes depot objects. Its 10 November 2026 GTFS\nservice-day subset retains 378 native DIVA areas with regular passenger-call\nwitnesses on publicly listed A-routes. Exact name/source-coordinate matches and\nall-position city tests qualify the groups, replacing rather than adding to\n99 metro areas. Seasonal, detour and callbus conditions are not verified for each\ntrip; the scheduled 2026 subset uses the supplied 2025 population \\cite{viennaogd,viennagis}.')
    # Replace only the numerical baseline table body, retaining its caption and format.
    start=s.index('Rank & City & Score interval & Regret & Rank & City & Score interval & Regret')
    a=s.index('\n',start)+1;b=s.index('\\bottomrule',a)
    df=pd.read_csv(R/'results/task4_user_v204_revision/current_ranks.csv')
    df=df[df.weight_reference.eq('fixed')].sort_values('decision_rank').reset_index(drop=True);assert len(df)==16
    table=[]
    for i in range(8):
        l,r=df.iloc[i],df.iloc[i+8]
        table.append(f'{int(l.decision_rank)} & {l.city} & {l.score_lower:.2f}--{l.score_upper:.2f} & {l.max_regret:.2f} & {int(r.decision_rank)} & {r.city} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f} '+r'\\')
    s=s[:a]+'\n'.join(table)+'\n'+s[b:]
    old='\\subsection{A significant revision: retaining uncertain evidence}';end='\\subsection{Sensitivity to the accepted input information}'
    a=s.index(old);b=s.index(end,a);s=s[:a]+(A/'revision.tex').read_text().rstrip()+'\n\n'+s[b:]
    a=s.index('\\begin{table}[!ht]\\centering',s.index(end));b=s.index('\\end{table}',a)+len('\\end{table}')
    s=s[:a]+(A/'vintage_table.tex').read_text().rstrip()+s[b:]
    rep('points selects Zurich under both and widens the baseline mean range from 15.82\nto 48.23.',
        'points selects Zurich under both and widens the baseline mean range from 15.78\nto 48.20.')
    rep('Withholding Zurich\'s homicide point retains Oslo under baseline weights and\nselects Oslo under equal weights;',
        'Restoring Vienna\'s 99 metro areas preserves both choices. A conservative\ncheck withholds 36 selected witnesses on nine condition-bearing routes, leaving\n342 areas; Oslo and Zurich remain selected. It uses selected witnesses without\nrematching.\n\nWithholding Zurich\'s homicide point retains Oslo under baseline weights and\nselects Oslo under equal weights;')
    a=s.index('\\begin{table}[!ht]\\centering',s.index('\\subsection{Perturbing weights and point assumptions}'));b=s.index('\\end{table}',a)+len('\\end{table}')
    preferences=(A/'preferences.tex').read_text().replace('for selected cities at concentration 100.','at concentration 100.')
    s=s[:a]+preferences.rstrip()+s[b:]
    pm=pd.read_csv(R/'results/task4_user_v204_extensions/preferences/mc_city_summary.csv')
    rows=pm[pm.profile.eq('baseline')&pm.concentration.eq(100)].set_index('city')
    rep('At concentration 100, mean decision ranks are Oslo 1.5680, Zurich 2.5125 and\nSingapore 2.4630.',
        'At concentration 100, mean decision ranks are Oslo '+f'{rows.loc["Oslo","mean_decision_rank"]:.4f}'+', Zurich '+f'{rows.loc["Zurich","mean_decision_rank"]:.4f}'+' and\nSingapore '+f'{rows.loc["Singapore","mean_decision_rank"]:.4f}'+'.')
    cert=read(R/'results/task4_user_v204_extensions/mean_rank_comparisons/summary.json')
    rep('Difference intervals resolve 4,271 of 4,440 pairwise mean-rank comparisons;\n169 remain unresolved. Under the declared simulation laws, 23 of 37 settings\ncertify a unique smallest expected rank.',
        'Difference intervals resolve '+f'{cert["certified_pairs"]:,}'+ ' of 4,440 pairwise mean-rank comparisons;\n'+str(cert['unresolved_pairs'])+' remain unresolved. Under the declared simulation laws, '+str(cert['settings_with_unique_smallest_expected_mean_rank'])+' of 37 settings\ncertify a unique smallest expected rank.')
    rep('The research calculations preserve the original city CSV and the V203 primary\nevidence. The V203 validation independently recomputes weighted norms and',
        'The research calculations preserve the original city CSV and the V204 primary\nevidence. The V204 validation independently recomputes weighted norms and')
    rep('8 November 2026; accessed 9 November 2026. DIVA station areas are distinguished\nfrom individual stopping positions.\n\\url{https://www.wienerlinien.at/ogd_realtime/doku/}.',
        '8 November 2026; accessed 9 November 2026. DIVA areas group stopping\npositions. GTFS and passenger timetable catalogue retrieved 11 November 2026;\nGTFS service-day subset dated 10 November.\n\\url{https://www.wienerlinien.at/ogd_realtime/doku/};\n\\url{https://www.wienerlinien.at/fahrplaene}.')
    # Keep the necessary V204 update within the existing page budget.
    rep("Vienna's broader register includes depot objects. Its 10 November 2026 GTFS\nservice-day subset retains 378 native DIVA areas with regular passenger-call\nwitnesses on publicly listed A-routes. Exact name/source-coordinate matches and\nall-position city tests qualify the groups, replacing rather than adding to\n99 metro areas. Seasonal, detour and callbus conditions are not verified for each\ntrip; the scheduled 2026 subset uses the supplied 2025 population \\cite{viennaogd,viennagis}.","Vienna's 10 November 2026 GTFS subset replaces 99 metro areas with 378 DIVA areas, qualified by public A-route regular calls, exact name/source-coordinate matches and all-position city tests \\cite{viennaogd,viennagis}.")
    rep("Restoring Vienna's 99 metro areas preserves both choices. A conservative\ncheck withholds 36 selected witnesses on nine condition-bearing routes, leaving\n342 areas; Oslo and Zurich remain selected. It uses selected witnesses without\nrematching.","Restoring Vienna's 99 metro areas preserves both choices. Seasonal, detour and callbus conditions remain unverified for individual trips. Withholding 36 selected witnesses on nine condition-bearing routes leaves 342 areas; Oslo and Zurich remain selected, without rematching.")
    rep('As a method diagnostic, TOPSIS and VIKOR use the same illustrative midpoint\nutilities and weights. VIKOR balances total and largest weighted shortfalls\nequally and uses sample best/worst values \\cite{vikor}. \\MethodComparison\nThe midpoint comparison does not replace the interval decision in\nEquation~\\ref{eq:regret}. Agreement indicates similarity within the chosen\nconventions; disagreement exposes method dependence rather than justifying a\npost-hoc choice of the preferred winner.','At the same illustrative midpoint utilities and weights, VIKOR equally balances\ntotal and largest shortfalls using sample best/worst values \\cite{vikor}.\n\\MethodComparison This diagnostic reveals method dependence;\nEquation~\\ref{eq:regret} retains TOPSIS and the evidence intervals.')
    rep('Evidence improves precision and changes decisions before it\nnecessarily reduces the possible-champion set.','')
    rep('Oslo minimizes maximum regret under baseline weights and Zurich under equal\nweights; all sixteen cities remain possible champions. Both preference profiles\nselect Oslo. Evidence supplements narrow the mean score interval by\n\\TotalWidthReduction\\%; against midpoint completion, the interval revision changes 14 fixed-weight decision ranks.','Baseline weights recommend Oslo; equal weights recommend Zurich by minimax regret. All sixteen cities remain possible champions. Supplements narrow mean score-interval width by \\TotalWidthReduction\\%.')
    s='\n'.join(line.rstrip() for line in s.splitlines())+'\n'
    if args.check_applied:assert s==path.read_text(),'Applied owned diff differs from guarded proposal'
    assert 'V203' not in s
    assert re.findall(r'\\bibitem\{([^}]+)\}',s)==re.findall(r'\\bibitem\{([^}]+)\}',original)
    # The agreed definition and shared formatting are preserved as exact existing lines.
    for line in original.splitlines():
        if 'We define' in line or '\\mcmsetup' in line or 'tcn=18213' in line:assert line in s,line
    print(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='main.tex before',tofile='main.tex V204')))
    if args.apply:
        path.write_text(s)
        for n in ['score_intervals.pdf','identification_matrix.pdf']:shutil.copyfile(A/n,P/'figures'/n)
        print('Applied reviewed owned V204 diff and two numerical figures')
if __name__=='__main__':main()

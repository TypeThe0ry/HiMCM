"""Build selected paper tables/figures from frozen research outputs, without model changes."""
from pathlib import Path
import argparse
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--research-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.research_root.resolve()
    tables, assets = HERE/'task4_v122_tables', HERE/'task4_v122_assets'
    tables.mkdir(exist_ok=True)
    assets.mkdir(exist_ok=True)
    paths = {
        'baseline': root/'results/task4_user_v121_revision/current_ranks.csv',
        'preferences': root/'results/task4_v122_preferences/summary.json',
        'mc': root/'results/task4_v122_preferences/mc_city_summary.csv',
        'future': root/'results/task4_v122_future/summary.json',
        'future_ranks': root/'results/task4_v122_future/ranks.csv',
        'thresholds': root/'results/task4_v122_future/thresholds.csv',
        'future_mc': root/'results/task4_v122_future/future_mc_city_summary.csv',
        'method': root/'results/task4_v122_method_country/summary.json',
        'age': root/'results/task4_v122_method_country/istanbul_historical_age_groups.csv',
        'source': root/'data/task4_v117_team_intake/city_indicators.csv',
        'admissions': root/'design/task4_user_v121_admissions.json',
    }
    hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()}
    base = pd.read_csv(paths['baseline'])
    fixed = base[base.weight_reference == 'fixed'].sort_values('decision_rank')
    assert len(fixed) == 16 and fixed.iloc[0].city == 'Zurich'
    assert fixed.possible_champion.all()
    prefs = read_json(paths['preferences'])
    method = read_json(paths['method'])
    mc = pd.read_csv(paths['mc'])
    k100 = mc[mc.concentration == 100]
    future = pd.read_csv(paths['future_ranks'])
    future_mc = pd.read_csv(paths['future_mc'])
    thresholds = pd.read_csv(paths['thresholds'])
    for path in paths.values():
        assert path.exists()
    indicator_rows = [
        ('Homicide', 'Deaths per 100,000; cost; supplied city proxy', '2'),
        ('PM$_{2.5}$', r'$\mu$g/m$^3$; cost; supplied concentration proxy', '15'),
        ('Living costs', 'Supplied living-cost index; cost', '100'),
        ('Housing', 'Supplied price-to-income ratio; cost', '10'),
        ('School resources', 'Pupils per teacher or explicitly scoped FTE; cost', '15'),
        ('Higher education', 'Institutions per 100,000; benefit; supply proxy', '1'),
        ('Transport stops', 'Unique stops per 100,000; benefit; partial inventories', '50'),
        ('Travel', r'Duration in minutes; $\exp(-t/30)$; commute or stage proxy', '30 min'),
        ('Broadband', 'Supplied Mbps; benefit; city/general-use proxy', '100'),
        ('Swimming pools', 'Venues per 100,000; benefit; supply proxy', '1'),
    ]
    lines = [r'\begin{longtable}{p{.22\linewidth}p{.56\linewidth}r}',
             r'\caption{Retained indicators, units and reference anchors. Supplied values are retained; supplements have explicit source scope.}\label{tab:indicators}\\',
             r'\toprule Indicator & Measurement and interpretation & Anchor\\\midrule',
             r'\endfirsthead', r'\toprule Indicator & Measurement and interpretation & Anchor\\\midrule\endhead']
    lines.extend(f'{a} & {b} & {c} \\\\' for a,b,c in indicator_rows)
    lines.extend([r'\bottomrule', r'\end{longtable}'])
    (tables/'indicators.tex').write_text('\n'.join(lines)+'\n')
    lines = [r'\begin{longtable}{rlrr}',
             r'\caption{Conservative baseline decision ranks with unchanged weights.}\label{tab:baseline}\\',
             r'\toprule Rank & City & Score interval & Maximum regret\\\midrule',
             r'\endfirsthead', r'\toprule Rank & City & Score interval & Maximum regret\\\midrule\endhead']
    for r in fixed.itertuples():
        lines.append(f'{r.decision_rank} & {r.city} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f} \\\\')
    lines.extend([r'\bottomrule',r'\end{longtable}'])
    (tables/'baseline.tex').write_text('\n'.join(lines)+'\n')
    profile_names = {'baseline':'Baseline', 'education_priority':'Education priority',
                     'independent_living_priority':'Independent living'}
    lines = [r'\begin{table}[htbp]\centering',
             r'\caption{Conditional recommendation frequencies (\%) at concentration 100.}',
             r'\begin{tabular}{lrrr}\toprule Preference centre & Zurich & Oslo & Singapore\\\midrule']
    for profile, label in profile_names.items():
        rows = k100[k100.profile == profile].set_index('city')
        lines.append(label+' & '+' & '.join(f'{100*rows.loc[c,"minimax_recommendation_frequency"]:.2f}' for c in ['Zurich','Oslo','Singapore'])+r' \\')
    lines += [r'\bottomrule\end{tabular}\end{table}']
    (tables/'preferences.tex').write_text('\n'.join(lines)+'\n')
    lines = [r'\begin{table}[htbp]\centering',
             r'\caption{Separate historical country cases using the legacy 25-city V117 evidence.}',
             r'\begin{tabular}{llr}\toprule Country & City & Score interval\\\midrule']
    for row in method['country_pairs']:
        lines.append(f'{row["country"]} & {row["city_a"]} & {row["a_score_lower"]:.2f}--{row["a_score_upper"]:.2f} \\\\')
        lines.append(f' & {row["city_b"]} & {row["b_score_lower"]:.2f}--{row["b_score_upper"]:.2f} \\\\')
    lines += [r'\bottomrule\end{tabular}\end{table}']
    (tables/'country.tex').write_text('\n'.join(lines)+'\n')
    fixed.to_csv(assets/'source_intervals.csv',index=False)
    k100.to_csv(assets/'source_preference_mc_k100.csv',index=False)

    plt.rcParams.update({'font.size':11,'axes.labelsize':11,'xtick.labelsize':10,
                         'ytick.labelsize':10,'legend.fontsize':10,'pdf.fonttype':42,
                         'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    fig, ax = plt.subplots(figsize=(6.35,5.4),layout='constrained')
    ys=np.arange(16)
    ax.hlines(ys,fixed.score_lower,fixed.score_upper,color='#247088',linewidth=2)
    ax.scatter(fixed.score_lower,ys,color='#247088',s=22,label='Lower bound',zorder=3)
    ax.scatter(fixed.score_upper,ys,facecolor='white',edgecolor='#247088',s=22,label='Upper bound',zorder=3)
    ax.set_yticks(ys,[f'{r.city} ({r.decision_rank})' for r in fixed.itertuples()])
    for y,r in zip(ys,fixed.itertuples()):
        ax.text(r.score_upper+1,y,f'{r.score_lower:.1f}–{r.score_upper:.1f}',va='center',fontsize=9)
    ax.set_xlim(0,100);ax.invert_yaxis();ax.set_xlabel('TOPSIS score (0–100)')
    ax.grid(axis='x',color='#dddddd',linewidth=.6);ax.set_axisbelow(True)
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.01),frameon=False,ncol=2)
    for suffix in ['pdf','svg','png']:
        fig.savefig(assets/f'score_intervals.{suffix}',dpi=180)
    plt.close(fig)

    fig,ax=plt.subplots(figsize=(6.35,2.9),layout='constrained')
    cities=['Zurich','Oslo','Singapore']
    values=np.array([[100*k100[(k100.profile==p)&(k100.city==c)].iloc[0].minimax_recommendation_frequency for c in cities] for p in profile_names])
    values=np.column_stack([values,100-values.sum(1)])
    left=np.zeros(3)
    for j,(name,color) in enumerate(zip(cities+['Other cities'],['#74b3ce','#efbb75','#b8caa8','#dedede'])):
        ax.barh(np.arange(3),values[:,j],left=left,color=color,label=name,height=.6)
        for i,v in enumerate(values[:,j]):
            if v>=8:ax.text(left[i]+v/2,i,f'{v:.1f}%',ha='center',va='center',fontsize=10)
        left+=values[:,j]
    ax.set_yticks(np.arange(3),list(profile_names.values()));ax.invert_yaxis()
    ax.set_xlim(0,100);ax.set_xlabel('Conditional recommendation frequency (%)')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,1.28),ncol=2,frameon=False)
    for suffix in ['pdf','svg','png']:
        fig.savefig(assets/f'preference_frequencies.{suffix}',dpi=180)
    plt.close(fig)

    macros={}
    original=read_json(root/'results/task4_user_city_indicators/summary.json')['results']['fixed']['mean_score_interval_width']
    macros['TotalWidthReduction']=f'{100*(original-(fixed.score_upper-fixed.score_lower).mean())/original:.2f}'
    case=next(x for x in method['method_cases'] if x['evidence_version']=='V121' and x['weight_reference']=='fixed')
    macros['MethodComparison']=(f'TOPSIS selects Zurich at the midpoint, whereas VIKOR selects Dublin; Kendall\'s '
        rf'$\tau_b={case["kendall_tau_b"]:.3f}$. Dublin satisfies VIKOR\'s advantage and stability conditions. '
        r'Under equal weights, Oslo has the lowest VIKOR index but fails those acceptance conditions, so it is not an accepted unique compromise solution.')
    macros['FutureDeterministic']=(r'All three uniform-change scenarios retain Zurich as the conservative recommendation and all sixteen cities as possible champions under both weight references, including the Singapore-proxy withdrawal arm. Balanced improvement changes the fixed-weight second and third decisions from Singapore--Oslo to Oslo--Singapore.')
    t=thresholds[thresholds.weight_reference=='fixed'].set_index('city')
    macros['FutureThresholds']=(f'Oslo reaches the tie at approximately {100*t.loc["Oslo","required_cost_reduction_fraction"]:.3f}'
        rf'\% reduction, Singapore at {100*t.loc["Singapore","required_cost_reduction_fraction"]:.3f}\%, '
        rf'and Stockholm at {100*t.loc["Stockholm","required_cost_reduction_fraction"]:.3f}\%. Zurich already minimizes regret at baseline. '
        r'A slightly greater reduction produces a strict recommendation switch in these calculations.')
    fr=future_mc[(future_mc.weight_reference=='fixed')&(future_mc.city=='Zurich')].set_index('scenario')
    macros['FutureMonteCarlo']=(r'Specifically, $C\sim U[0,1]$ is shared across cities and $I_i\sim U[0,1]$ varies by city, independently; '
        r'$\delta_i=0.05C+0.05I_i$. The relevant raw multipliers are $1+\delta_i$ or $1-\delta_i$, '
        r'and affected criteria within a city share that multiplier. With 10,000 draws per scenario, Zurich\'s fixed-weight recommendation frequencies are '
        +', '.join(f'{100*fr.loc[s,"recommendation_frequency"]:.2f}'+r'\%' for s in ['resource_expansion','living_pressure','balanced_improvement'])
        +r' for resource expansion, living pressure and balanced improvement respectively.')
    profiles={x['profile']:x for x in prefs['profiles']}
    macros['PreferenceResults']=(rf'Education priority changes the conservative recommendation from Zurich to Oslo, with decision-rank $\tau_b={profiles["education_priority"]["kendall_tau_b_vs_baseline"]:.3f}$ relative to baseline. '
        rf'Independent-living priority retains Zurich and gives $\tau_b={profiles["independent_living_priority"]["kendall_tau_b_vs_baseline"]:.3f}$. '
        r'All sixteen cities remain possible champions in each profile.')
    b=k100[k100.profile=='baseline'].set_index('city')
    macros['MonteCarloInterpretation']=(f'At concentration 100, Oslo has a better mean decision rank ({b.loc["Oslo","mean_decision_rank"]:.4f}) than Zurich ({b.loc["Zurich","mean_decision_rank"]:.4f}), '
        'although Zurich has the greater recommendation frequency and is the fixed-weight minimax choice. '
        r'At concentration 20 under education priority, Singapore is the most frequently recommended city, whereas the fixed education-priority decision is Oslo.')
    e=method['equity']
    macros['EquityCase']=(f'A separate Shanghai school-resource case uses {e["districts"]} districts, {e["students"]:,} regular senior-secondary pupils and {e["teacher_headcount"]:,} full-time teachers in the 2025 school year. '
        f'The pooled utility is {e["pooled_utility"]:.6f}; the student-weighted mean of district utilities is {e["student_weighted_district_utility"]:.6f}. '
        f'Ordering districts by resource utility and averaging the bottom 20\% of pupil mass, with fractional inclusion of the boundary district, gives {e["bottom20_student_mass_district_utility"]:.6f}, '
        f'{e["bottom20_gap_from_student_mean"]:.6f} below the weighted mean. '
        r'These are district-homogeneous school-location resource scenarios, not observed individual teacher exposure or resident accessibility \cite{shanghai}.')
    macros['AgeCase']=(r'A historical Istanbul household survey offers current-high-school groups aged 14--15 and 16--18. Their travel-utility marginal bounds overlap: '
        r'$[0.35961,0.55711]$ and $[0.29347,0.59346]$, respectively. They include unknown durations and optional members; shared unknown-age mass means their extrema need not be jointly attainable. '
        r'They describe 2012 broad groups, not exact ages fourteen and eighteen today. Singapore\'s MOE table records 38,555 students aged fourteen and only 165 aged eighteen at the start of 2020 still in secondary schooling; the latter is not an all-eighteen-year-old resident denominator. '
        r'These counts cannot be joined to census school-stage travel bins without a matching population/reference-day table \cite{istanbul,sgage}.')
    macros['CountryInterpretation']=(r'Phoenix has higher retained affordability utilities than New York. Mumbai has the higher PM$_{2.5}$ utility, while Delhi has higher living-cost, housing, school-resource and broadband utilities in the retained evidence. '
        r'The cases inherit the historical study\'s geographic and educational scope; their score pairs overlap, so neither case identifies a necessary overall winner.')
    macros['CaseReferences']=(r'\bibitem{shanghai} Shanghai Municipal Education Commission. Regular secondary-school pupil and teacher tables, school year 2025. '
        r'\url{https://edu.sh.gov.cn/xxgk2_zhzw_tjsj_01/20260610/890926a33cbf443d9abf07c6f65b7734.html}. '
        r'\bibitem{istanbul} Istanbul Metropolitan Municipality. 2012 household transport survey, official data-portal response resource '
        r'\texttt{a75118db-28c9-4fdf-b367-d5933b7bb810}; questionnaire, report and nonidentifying aggregate audit archived. '
        r'\bibitem{sgage} Singapore Ministry of Education. Secondary enrolment by level and age, 2020. '
        r'\url{https://data.gov.sg/datasets/d_cc84fc751ef5106d9e26cfdbf61776c8/view}.')
    (HERE/'task4_v122_generated.tex').write_text('% Generated from frozen research outputs; do not hand-edit numerical claims.\n'+
        '\n'.join('\\newcommand{\\'+name+'}{'+value.replace("\\'s", "'s")+' }' for name,value in macros.items())+'\n')
    manifest=dict(input_version='V121 user16',extension='V122',source_hashes=hashes,
                  figure_inches={'score_intervals':[6.35,5.4],'preference_frequencies':[6.35,2.9]},
                  minimum_figure_font_pt=9,compiler='tectonic',
                  scope='Selected standalone contribution, no edits to main.tex, team prose or shared bibliography')
    (assets/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for p in paths.values():
        assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p.relative_to(root))]
    print('Built 4 tables, 2 figures (PDF/SVG/PNG), numerical macros and selected source CSVs.')


if __name__ == '__main__':
    main()

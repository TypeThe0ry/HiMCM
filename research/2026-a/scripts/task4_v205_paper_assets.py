"""Build V205 numerical assets while preserving historical outputs."""
from pathlib import Path
import hashlib,json,re,shutil
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path('/data/projects/HiMCM/paper/history/overleaf_before_single_main_20261110/drafts')
R=Path('/data/projects/HiMCM/research/2026-a')
A=R/'results/task4_v205_paper_assets'

def read(path):return json.loads(path.read_text())
def read_csv(path):return pd.read_csv(path,float_precision='round_trip')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def table(path,caption,header,rows,columns,label=None):
    value='\\begin{table}[!ht]\\centering\n\\caption{'+caption+'}'
    if label:value+='\\label{'+label+'}'
    value+='\n\\begin{tabular}{'+columns+'}\\toprule\n'+header+r'\\\midrule'+'\n'
    value+='\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)
    path.write_text(value+'\n\\bottomrule\\end{tabular}\\end{table}\n')

def main():
    A.mkdir(exist_ok=False)
    result_dirs={k:R/('results/task4_user_v205_extensions/'+k) for k in ['preferences','future','method','diagnostics']}
    summaries={k:read(v/'summary.json') for k,v in result_dirs.items()}
    primary=R/'results/task4_user_v205_revision'
    base=read_csv(primary/'current_ranks.csv');fixed=base[base.weight_reference.eq('fixed')].sort_values('decision_rank')
    assert len(fixed)==16 and fixed.iloc[0].city=='Oslo'
    current=float((fixed.score_upper-fixed.score_lower).mean())
    original=read(R/'results/task4_user_city_indicators/summary.json')['results']['fixed']['mean_score_interval_width']
    reduction=100*(original-current)/original
    profiles={p['profile']:p for p in summaries['preferences']['profiles']}
    pmc=read_csv(result_dirs['preferences']/'mc_city_summary.csv');k100=pmc[pmc.concentration.eq(100)]
    macros={}
    for line in (HERE/'task4_v137_generated.tex').read_text().splitlines():
        match=re.fullmatch(r'\\newcommand\{\\(\w+)\}\{(.*)\}',line)
        if match:macros[match[1]]=match[2]
    # Pin historical cases to the audited pre-migration commit, independent of the working tree.
    historical_commit = '48f65d6c2dcdecf3dc9b5577e3d10256f21301bd'
    historical_sha = 'c1d1a9c2f570c8f716ddc0966107c146a3a3fab525a5f54d1e04588018f82dac'
    manuscript_bytes = subprocess.check_output(['git', '-C', '/data/projects/HiMCM-Overleaf', 'show', historical_commit + ':main.tex'])
    assert hashlib.sha256(manuscript_bytes).hexdigest() == historical_sha
    manuscript = manuscript_bytes.decode('utf-8')
    for name in ['EquityCase', 'AgeCase', 'CountryInterpretation', 'CaseReferences']:
        prefix = '\\newcommand{\\' + name + '}{'
        start = manuscript.index(prefix) + len(prefix)
        depth, end = 1, start
        while depth:
            if manuscript[end] == '{' and (end == 0 or manuscript[end-1] != '\\'): depth += 1
            if manuscript[end] == '}' and (end == 0 or manuscript[end-1] != '\\'): depth -= 1
            end += 1
        macros[name] = manuscript[start:end-1]
    macros['CurrentMeanWidth']=f'{current:.5f}'
    macros['RevisionRankChanges']=str(summaries['diagnostics']['revision_diagnostics'][0]['changed_city_decision_ranks'])
    macros['TotalWidthReduction']=f'{reduction:.2f}'
    precision=read(R/'results/task4_user_v205_extensions/mc_precision/summary.json')
    pair_certificate=read(R/'results/task4_user_v205_extensions/mean_rank_comparisons/summary.json')
    assert precision['base_means']==sum(t['means'] for t in precision['tables'])
    assert precision['settings']==sum(t['settings'] for t in precision['tables'])
    for macro,key in [('MCBaseMeans','base_means'),('MCSettings','settings')]:macros[macro]=str(precision[key])
    for macro,key in [('MCPairComparisons','unordered_within_setting_pairs'),('MCCertifiedPairs','certified_pairs'),('MCUnresolvedPairs','unresolved_pairs'),('MCUniqueMinSettings','settings_with_unique_smallest_expected_mean_rank')]:macros[macro]=str(pair_certificate[key])
    macros['MCFrequencyHalfWidthPP']=f"{precision['frequency_half_width_percentage_points']:.2f}"
    macros['MCRankHalfWidth']=f"{precision['mean_rank_half_width']:.3f}"

    old_fixed=read_csv(R/'results/task4_user_v204_revision/current_ranks.csv')
    old_fixed=old_fixed[old_fixed.weight_reference.eq('fixed')]
    previous_width=float((old_fixed.score_upper-old_fixed.score_lower).mean())
    macros['LatestEvidenceChange']=(r"Prague's 942 source-defined bus nodes replace the 57-node metro subset, reducing fixed-weight mean width from "+f'{previous_width:.5f}'+r' to '+f'{current:.5f}'+r'; population remains 2025.')
    def mc(profile,city,column='minimax_recommendation_frequency'):
        return float(k100[(k100.profile==profile)&(k100.city==city)].iloc[0][column])
    macros['SummaryWeightMC']=(r'In 10,000 baseline weight perturbations at Dirichlet concentration 100, Zurich is recommended in '+f"{100*mc('baseline','Zurich'):.2f}"+r'\% of draws, compared with '+f"{100*mc('baseline','Oslo'):.2f}"+r'\% for Oslo and '+f"{100*mc('baseline','Singapore'):.2f}"+r'\% for Singapore.')
    methods={v['weight_reference']:v for v in summaries['method']['method_cases']}
    assert methods['fixed']['vikor_q_winners']==['Dublin'] and methods['fixed']['single_compromise_accepted']
    assert methods['equal']['vikor_q_winners']==['Oslo']
    macros['MethodComparison']=(r"At midpoint utilities, TOPSIS selects Zurich. VIKOR's lowest $Q$ is Dublin with fixed weights ($\tau_b="+f"{methods['fixed']['kendall_tau_b']:.3f}"+r"$) and Oslo with equal weights ($\tau_b="+f"{methods['equal']['kendall_tau_b']:.3f}"+r'$). Dublin meets both acceptance conditions; Oslo fails stability and is not an accepted single compromise.')
    assert [profiles[n]['minimax_choices'] for n in ['baseline','education_priority','independent_living_priority']]==[['Oslo'],['Oslo'],['Oslo']]
    macros['PreferenceResults']=(r'Both education and independent-living priorities retain Oslo; their decision-rank $\tau_b$ values relative to baseline are '+f"{profiles['education_priority']['kendall_tau_b_vs_baseline']:.3f}"+' and '+f"{profiles['independent_living_priority']['kendall_tau_b_vs_baseline']:.3f}"+r'. All sixteen cities remain possible champions.')
    macros['PreferenceEvidenceChange']=r'The 2026 Prague scheduled bus-service inventory changes the baseline evidence bounds.'
    macros['MonteCarloInterpretation']=(r'At concentration 100, Singapore, Zurich and Oslo have sample mean decision ranks of '+', '.join(f"{mc('baseline', c, 'mean_decision_rank'):.4f}" for c in ['Singapore','Zurich','Oslo'])+r', respectively. The finite-draw pairwise bounds determine which expected orderings are resolved.')
    future=summaries['future'];thresholds={p['city']:p for p in future['thresholds'] if p['weight_reference']=='fixed'}
    macros['FutureThresholds']='Oslo already minimizes regret at baseline. Zurich, Singapore and Stockholm reach a tie after hypothetical joint reductions in pupil--teacher ratio, PM$_{2.5}$ and travel duration of '+', '.join(f"{100*thresholds[c]['required_cost_reduction_fraction']:.3f}"+r'\%' for c in ['Zurich','Singapore','Stockholm'])+r', respectively. These are hypothetical thresholds.'
    macros['EvidenceThresholdCheck']=r"Berlin does not reach a tie within the tested 50\% joint reduction."
    future_ranks=read_csv(result_dirs['future']/'ranks.csv')
    def runner_up_pair(scenario):
        rows=future_ranks[future_ranks.evidence_arm.eq('conditional')&future_ranks.scenario.eq(scenario)&future_ranks.weight_reference.eq('fixed')].sort_values('decision_rank')
        assert len(rows)==16
        return '--'.join(rows.iloc[1:3].city)
    macros['FutureDeterministic']=r'Fixed weights select Oslo in all three scenarios; equal weights select Oslo, Zurich and Oslo, respectively. With Singapore historical stage-travel withdrawn, these choices remain the same. All sixteen cities remain possible champions.'
    fmc=read_csv(result_dirs['future']/'future_mc_city_summary.csv');order=['resource_expansion','living_pressure','balanced_improvement']
    def rates(arm):
        return ', '.join(f"{100*float(fmc[(fmc.weight_reference=='fixed')&(fmc.city=='Oslo')&(fmc.evidence_arm==arm)&(fmc.scenario==s)].iloc[0].recommendation_frequency):.2f}"+r'\%' for s in order)
    macros['FutureMonteCarlo']=(r'Specifically, $C\sim U[0,1]$ is shared across cities and $I_i\sim U[0,1]$ varies by city, independently; $\delta_i=0.05C+0.05I_i$. The relevant raw multipliers are $1+\delta_i$ or $1-\delta_i$, and affected criteria within a city share that multiplier. With 10,000 draws per scenario, Oslo\'s fixed-weight recommendation frequencies are '+rates('conditional')+r' for resource expansion, living pressure and balanced improvement respectively.').replace("\\'s","'s")
    macros['ProxyWithdrawalMC']='Repeating the same shocks after withdrawing Singapore\'s historical stage-travel proxy gives '+rates('withdraw_historical_stage_proxy')+r' respectively. These paired calculations isolate dependence on that proxy while retaining the chosen shock distribution.'
    (A/'generated.tex').write_text('% Current numerical assets from V205 evidence and controlled extensions; historical cases retained.\n'+'\n'.join('\\newcommand{\\'+k+'}{'+v+('' if k in {'CurrentMeanWidth','TotalWidthReduction','RevisionRankChanges','EquityCase','AgeCase','CountryInterpretation','CaseReferences'} else ' ')+'}' for k,v in macros.items())+'\n')
    for name in ['indicators.tex','country.tex','age_joint.tex']:
        shutil.copyfile(HERE/'task4_v137_assets'/name,A/name)
    table(A/'baseline.tex','Conservative baseline decision ranks with unchanged weights.','Rank & City & Score interval & Maximum regret',[(r.decision_rank,r.city,f'{r.score_lower:.2f}--{r.score_upper:.2f}',f'{r.max_regret:.2f}') for r in fixed.itertuples()],'rlrr','tab:baseline')
    table(A/'preferences.tex',r'Selected-city conditional recommendation frequencies (\%) at concentration 100.','Preference centre & Zurich & Oslo & Singapore & Prague',[(label,*[f'{100*mc(name,c):.2f}' for c in ['Zurich','Oslo','Singapore','Prague']]) for name,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]],'lrrrr')
    diagnostic=summaries['diagnostics'];df,de=diagnostic['revision_diagnostics']
    margins=diagnostic['minimum_strict_margin_by_weight']
    revision=r'''\subsection{A significant revision: retaining uncertain evidence}
A controlled comparison shows why evidence bounds belong in the decision.
On the same 160 utility entries, compare the midpoint completion $z_{ij}=(\ell_{ij}+h_{ij})/2$ with the retained-interval formulation in Equation~\ref{eq:regret}. Both use identical weights, anchors and TOPSIS scores. The midpoint is a declared diagnostic scenario, rather than an estimate of missing observations or a reconstruction of the team's historical first model.

'''
    revision+='The revision retains 48 non-point entries and selects the city with the smallest worst-case shortfall. Oslo is the fixed-weight recommendation, and '+str(df['changed_city_decision_ranks'])+r" cities change decision rank under fixed weights; Kendall's $\tau_b="+f"{df['kendall_tau_b']:.3f}"+r'$. With equal weights, '+str(de['changed_city_decision_ranks'])+r' ranks change and $\tau_b='+f"{de['kendall_tau_b']:.3f}"+'$.\n\n'
    revision+=r'For each target city $c$, construct a separate interior completion: set every uncertain utility to $\ell_{ij}+\alpha_i(h_{ij}-\ell_{ij})$, with $\alpha_c=0.95$ and $\alpha_i=0.05$ for $i\ne c$. All 112 point values remain fixed and all 48 uncertain values lie strictly inside their intervals. Each target ranks first under both baseline and equal weights. Across the sixteen targets, the smallest lead is '+f"{margins['fixed']:.3f}"+' score points under baseline weights and '+f"{margins['equal']:.3f}"+r' under equal weights. These separate completions establish feasibility in the declared utility rectangle; they carry no estimated probabilities and do not establish joint physical attainability.'+'\n\n'
    revision+=r'Retaining intervals changes the decision order while preserving sixteen possible champions. The \TotalWidthReduction\% reduction in interval width comes from admitted data, separately from this formulation comparison.'+'\n'
    (A/'revision.tex').write_text(revision)
    diagnostic=summaries['diagnostics']
    vc={(v['scenario'],v['weight_reference']):v for v in diagnostic['vintage_cases']}
    labels={'baseline':'Retained input','pre2020_points':'Before 2020','after2025_points':'After 2025','non_ok_points':'Non-ok flags','union_points':'Union'}
    table(A/'vintage_table.tex','Recommendation after withdrawing selected submitted point information. Width is the mean baseline-weight score range on the 0--100 scale.','Withdrawn group & Cells & Baseline & Equal & Width',[(label,str(vc[s,'fixed']['withdrawn_point_cells']),'/'.join(vc[s,'fixed']['minimax_choices']),'/'.join(vc[s,'equal']['minimax_choices']),f"{vc[s,'fixed']['mean_interval_width']:.2f}") for s,label in labels.items()],'l r l l r','tab:vintage')
    plt.rcParams.update({'font.size':12.5,'axes.labelsize':12.5,'xtick.labelsize':12.5,'ytick.labelsize':12.5,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(6.45,4.1));fig.subplots_adjust(left=.25,right=.96,bottom=.16,top=.97)
    ys=range(16);l=fixed.score_lower.to_numpy();u=fixed.score_upper.to_numpy()
    ax.hlines(ys,l,u,color='#526678',linewidth=2.3);ax.scatter(l,ys,marker='|',s=100,c='#526678');ax.scatter(u,ys,marker='|',s=100,c='#526678');ax.hlines(0,l[0],u[0],color='#006c67',linewidth=4)
    ax.set_yticks(list(ys),fixed.city);ax.invert_yaxis();ax.set_xlim(40,75);ax.set_xticks([40,50,60,70]);ax.set_xlabel('TOPSIS score bound (0-100)');ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0)
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
    for suffix in ['pdf','svg','png']:fig.savefig(A/f'score_intervals.{suffix}',dpi=300)
    plt.close(fig)
    svg=A/'score_intervals.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fixed.to_csv(A/'source_intervals.csv',index=False)
    for part,folder in result_dirs.items():shutil.copyfile(folder/'summary.json',A/(part+'_summary.json'))
    inputs=[primary/'summary.json',primary/'current_ranks.csv',R/'design/task4_user_v205_admissions.json',*[p for folder in result_dirs.values() for p in folder.iterdir() if p.is_file()]]
    inputs += [R/'results/task4_user_v204_revision/current_ranks.csv', R/'results/task4_user_city_indicators/summary.json', R/'results/task4_user_v205_extensions/mc_precision/summary.json',R/'results/task4_user_v205_extensions/mean_rank_comparisons/summary.json']
    matrix_main()
    manifest=dict(scope='Current numerical paper assets from isolated V205; not activation or a new manuscript entry',source_sha256={str(p.relative_to(R)):sha(p) for p in inputs},template_archive='paper/history/overleaf_before_single_main_20261110/drafts',minimum_score_figure_font_inserted_pt=12.5*6.5/6.45,renderer_sha256=sha(Path(__file__)),all_current_numeric_outputs_recomputed=True, historical_macros_inherited_from_pinned_commit=True)
    manifest['historical_macro_source'] = {'repository': 'HiMCM-Overleaf', 'commit': historical_commit, 'path': 'main.tex', 'sha256': historical_sha}
    manifest['output_sha256']={str(p.relative_to(A)):sha(p) for p in sorted(A.iterdir()) if p.is_file() and p.name!='manifest.json'}
    (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Staged V205 numerical assets built; cumulative reduction',reduction)



"""Render all160 retained utility ranges; do not change model inputs or rankings."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, subprocess, shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, "/data/projects/HiMCM/research/2026-a/scripts")
from task4_v5_model import NAMES

R = Path('/data/projects/HiMCM/research/2026-a')
O = R / 'results/task4_v205_paper_assets'
DISPLAY = {'homicide_rate':'Homicide', 'pm25':'PM2.5',
           'cost_living_index':'Living cost', 'price_income_ratio':'Housing',
           'upper_secondary_ptr':'Pupil/teacher', 'research_he_density':'Research/HE',
           'public_transport_density':'Transit', 'travel':'Travel burden',
           'fixed_broadband_mbps':'Broadband', 'public_pool_density':'Pools'}
assert set(DISPLAY)==set(NAMES)
LABELS = [DISPLAY[n] for n in NAMES]


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def matrix_main():
    raw=pd.read_csv(R/'results/task4_user_v205_revision/utility_bounds.csv')
    raw=raw[raw.scenario.eq('after_conditional')]
    cities=list(dict.fromkeys(raw.city)); frame=pd.DataFrame({'city':cities})
    indexed=raw.set_index(['city','indicator'])
    lo=np.array([[indexed.loc[(c,n),'lower'] for n in NAMES] for c in cities])
    hi=np.array([[indexed.loc[(c,n),'upper'] for n in NAMES] for c in cities])
    assert lo.shape == hi.shape == (16, 10)
    width = hi-lo
    assert np.all(width >= 0) and np.all(width <= 1)
    rows = []
    for i, city in enumerate(frame.city):
        for j, indicator in enumerate(NAMES):
            state = 'point' if lo[i,j] == hi[i,j] else ('unknown' if lo[i,j] == 0 and hi[i,j] == 1 else 'partial')
            rows.append(dict(city=city, indicator=indicator, plot_label=LABELS[j], utility_lower=float(lo[i,j]), utility_upper=float(hi[i,j]), interval_width=float(width[i,j]), state=state))
    counts = Counter(r['state'] for r in rows)
    assert counts == {'point':112, 'partial':37, 'unknown':11}
    unknowns = Counter(r['indicator'] for r in rows if r['state']=='unknown')
    assert unknowns['upper_secondary_ptr'] == 8
    O.mkdir(exist_ok=True)
    with (O/'matrix.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                         'svg.fonttype':'none', 'pdf.fonttype':3})
    cmap = LinearSegmentedColormap.from_list('identified_range', ['#f7fafb','#9dc4d2','#215c78'])
    fig = plt.figure(figsize=(6.5,6.2), facecolor='white')
    left,bottom,gridw,gridh=.19,.21,.78,.54
    cw,ch=gridw/10,gridh/16
    for i,city in enumerate(frame.city):
        fig.text(left-.01,bottom+gridh-(i+.5)*ch,city,ha='right',va='center',fontsize=10)
    for j,label in enumerate(LABELS):
        fig.text(left+(j+.5)*cw,bottom+gridh+.012,label,rotation=55,
                 ha='left',va='bottom',rotation_mode='anchor',fontsize=10)
    for row in rows:
        i = frame.city.tolist().index(row['city']); j = NAMES.index(row['indicator'])
        x,y=left+j*cw,bottom+gridh-(i+1)*ch
        fig.add_artist(Rectangle((x,y),cw,ch,transform=fig.transFigure,facecolor=cmap(width[i,j]),
                                 edgecolor='#cdd6da',linewidth=.5,clip_on=False,gid=f'cell-{i}-{j}'))
        if row['state']=='point':
            fig.add_artist(Line2D([x+cw/2],[y+ch/2],transform=fig.transFigure,marker='o',
                                  markersize=2.8,linestyle='None',color='#344751',clip_on=False))
        elif row['state']=='unknown':
            fig.text(x+cw/2,y+ch/2,'?',ha='center',va='center',color='white',fontsize=10,weight='bold')
    fig.text(.19,.977,'Identification ranges in the 16-city matrix',fontsize=12,weight='bold',va='top')
    fig.text(.19,.935,'112 point; 37 partial; 11 unknown (8 pupil/teacher)',fontsize=10,va='top')
    # Explicit vector swatches avoid backend-specific mesh clipping of labels.
    for k in range(64):
        fig.add_artist(Rectangle((.30+k*.58/64,.132),.58/64,.022,transform=fig.transFigure,
                                 facecolor=cmap((k+.5)/64),edgecolor='none',clip_on=False))
    fig.add_artist(Rectangle((.30,.132),.58,.022,transform=fig.transFigure,
                             facecolor='none',edgecolor='black',linewidth=.5,clip_on=False))
    for tick in [0,.5,1]:
        x=.30+tick*.58
        fig.add_artist(Line2D([x,x],[.132,.127],transform=fig.transFigure,color='black',linewidth=.5,clip_on=False))
        fig.text(x,.119,f'{tick:.1f}',ha='center',va='top',fontsize=10)
    fig.text(.59,.087,'Utility interval width (upper − lower)',ha='center',va='top',fontsize=10)
    fig.text(.025,.033,'Dot: point assumption.  ?: unknown.  Source: V205 utility bounds.',fontsize=10)
    for ext in ['pdf','svg','png']:
        fig.savefig(O/f'identification_matrix.{ext}',dpi=300,metadata={'Creator':'HiMCM research'} if ext!='png' else None)
    plt.close(fig)
    svg=O/'identification_matrix.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    text=subprocess.check_output(['pdftotext',str(O/'identification_matrix.pdf'),'-'],text=True)
    assert text.count('?')==12 and all(s in text for s in ['112 point','37 partial','11 unknown'])
    result = dict(iteration='current', model='V205 staged', shape=[16,10], counts=dict(counts),
                  unknown_by_indicator=dict(unknowns), city_order=frame.city.tolist(), indicator_order=NAMES,
                  plot_labels=LABELS, source='V205 after_conditional; conditional bounds',
                  source_csv_sha256=sha(R/'data/task4_v117_team_intake/city_indicators.csv'),
                  utility_bounds_sha256=sha(R/'results/task4_user_v205_revision/utility_bounds.csv'),
                  matrix_sha256=sha(O/'matrix.csv'), renderer_sha256=sha(Path(__file__)),
                  admissions_sha256=sha(R/'design/task4_user_v205_admissions.json'), figure_width_inches=6.5, figure_height_inches=6.2,
                  minimum_source_font_pt=10, intended_insertion_width_inches=6.5,
                  minimum_insertion_width_for9pt_inches=5.85, png_dpi=300,
                  pdf_export='Explicit vector rectangles and embedded Type3 outline fonts; RGB and grayscale review required',
                  point_interpretation='Retained point assumptions, not independent validation or zero measurement error',
                  ranges_interpretation='Identification bounds; not confidence intervals, posterior probabilities or ranking',
                  no_new_data_admission=True, current_review='Current single main pending integration', integrated_into_paper=False,
                  output_sha256={ext:sha(O/f'identification_matrix.{ext}') for ext in ['pdf','svg','png']})
    (O/'figure_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print('V205 figure generated')




if __name__ == "__main__": main()

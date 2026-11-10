"""Build new V198 numerical assets from audited V197 evidence; freeze old outputs."""
from pathlib import Path
import hashlib,json,re,shutil
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
R=Path('/data/projects/HiMCM/research/2026-a')
A=HERE/'task4_v198_assets'

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
    A.mkdir(exist_ok=True)
    result_dirs={k:R/('results/task4_v197_'+k) for k in ['preferences','future','method','diagnostics']}
    summaries={k:read(v/'summary.json') for k,v in result_dirs.items()}
    primary=R/'results/task4_user_v197_revision'
    base=read_csv(primary/'current_ranks.csv');fixed=base[base.weight_reference.eq('fixed')].sort_values('decision_rank')
    assert len(fixed)==16 and fixed.iloc[0].city=='Zurich'
    current=float((fixed.score_upper-fixed.score_lower).mean())
    original=read(R/'results/task4_user_city_indicators/summary.json')['results']['fixed']['mean_score_interval_width']
    reduction=100*(original-current)/original
    profiles={p['profile']:p for p in summaries['preferences']['profiles']}
    pmc=read_csv(result_dirs['preferences']/'mc_city_summary.csv');k100=pmc[pmc.concentration.eq(100)]
    macros={}
    for line in (HERE/'task4_v137_generated.tex').read_text().splitlines():
        match=re.fullmatch(r'\\newcommand\{\\(\w+)\}\{(.*)\}',line)
        if match:macros[match[1]]=match[2]
    macros['CurrentMeanWidth']=f'{current:.5f}'
    macros['RevisionRankChanges']=str(summaries['diagnostics']['revision_diagnostics'][0]['changed_city_decision_ranks'])
    macros['TotalWidthReduction']=f'{reduction:.2f}'
    precision=read(R/'results/task4_v197_mc_precision/summary.json')
    pair_certificate=read(R/'results/task4_v197_mean_rank_comparisons/summary.json')
    assert precision['base_means']==sum(t['means'] for t in precision['tables'])
    assert precision['settings']==sum(t['settings'] for t in precision['tables'])
    for macro,key in [('MCBaseMeans','base_means'),('MCSettings','settings')]:macros[macro]=str(precision[key])
    for macro,key in [('MCPairComparisons','unordered_within_setting_pairs'),('MCCertifiedPairs','certified_pairs'),('MCUnresolvedPairs','unresolved_pairs'),('MCUniqueMinSettings','settings_with_unique_smallest_expected_mean_rank')]:macros[macro]=str(pair_certificate[key])
    macros['MCFrequencyHalfWidthPP']=f"{precision['frequency_half_width_percentage_points']:.2f}"
    macros['MCRankHalfWidth']=f"{precision['mean_rank_half_width']:.3f}"

    transition=read(R/'results/task4_v197_transition/paper_migration_plan.json')['numeric_updates']
    previous_width=transition['fixed_width_before_after'][0]
    macros['LatestEvidenceChange']=(r"Refining Zurich's pool subset from seven to twelve venues narrows the preceding fixed-weight mean from "+f'{previous_width:.5f}'+r' to '+f'{current:.5f}'+r'; decision ranks stay unchanged. Public-session and holiday limits constrain access.')
    def mc(profile,city,column='minimax_recommendation_frequency'):
        return float(k100[(k100.profile==profile)&(k100.city==city)].iloc[0][column])
    macros['SummaryWeightMC']=(r'In 10,000 baseline weight perturbations at Dirichlet concentration 100, Zurich is recommended in '+f"{100*mc('baseline','Zurich'):.2f}"+r'\% of draws, compared with '+f"{100*mc('baseline','Oslo'):.2f}"+r'\% for Oslo and '+f"{100*mc('baseline','Singapore'):.2f}"+r'\% for Singapore.')
    methods={v['weight_reference']:v for v in summaries['method']['method_cases']}
    assert methods['fixed']['vikor_q_winners']==['Dublin'] and methods['fixed']['single_compromise_accepted']
    assert methods['equal']['vikor_q_winners']==['Oslo'] and not methods['equal']['single_compromise_accepted']
    macros['MethodComparison']=(r"TOPSIS selects Zurich at the midpoint, whereas VIKOR selects Dublin; Kendall's $\tau_b="+f"{methods['fixed']['kendall_tau_b']:.3f}"+r"$. Dublin satisfies VIKOR's advantage and stability conditions. Under equal weights, $\tau_b="+f"{methods['equal']['kendall_tau_b']:.3f}"+r'$; Oslo has the lowest VIKOR index but fails those acceptance conditions, so it is not an accepted unique compromise solution.')
    assert [profiles[n]['minimax_choices'] for n in ['baseline','education_priority','independent_living_priority']]==[['Zurich'],['Oslo'],['Zurich']]
    macros['PreferenceResults']=(r'Education priority changes the conservative recommendation from Zurich to Oslo, with decision-rank $\tau_b='+f"{profiles['education_priority']['kendall_tau_b_vs_baseline']:.3f}"+r'$ relative to baseline. Independent-living priority retains Zurich and gives $\tau_b='+f"{profiles['independent_living_priority']['kendall_tau_b_vs_baseline']:.3f}"+r'$. All sixteen cities remain possible champions in each profile.')
    macros['PreferenceEvidenceChange']=(r'With preference weights fixed, the Zurich pool refinement leaves the education-versus-baseline rank association at '+f"{profiles['education_priority']['kendall_tau_b_vs_baseline']:.3f}"+r'; education priority selects Oslo.')
    macros['MonteCarloInterpretation']=(r'At concentration 100, Zurich and Oslo have sample mean decision ranks of '+f"{mc('baseline','Zurich','mean_decision_rank'):.4f}"+r' and '+f"{mc('baseline','Oslo','mean_decision_rank'):.4f}"+r', respectively. The finite-draw pairwise bound does not resolve their expected ordering.')
    future=summaries['future'];thresholds={p['city']:p for p in future['thresholds'] if p['weight_reference']=='fixed'}
    macros['FutureThresholds']='Oslo reaches the tie at approximately '+f"{100*thresholds['Oslo']['required_cost_reduction_fraction']:.3f}"+r'\% reduction, Singapore at '+f"{100*thresholds['Singapore']['required_cost_reduction_fraction']:.3f}"+r'\%, and Stockholm at '+f"{100*thresholds['Stockholm']['required_cost_reduction_fraction']:.3f}"+r'\%. Zurich already minimizes regret at baseline. A slightly greater reduction produces a strict recommendation switch in these calculations.'
    macros['EvidenceThresholdCheck']="Berlin's hypothetical combined-cost tie threshold is "+f"{100*thresholds['Berlin']['required_cost_reduction_fraction']:.3f}"+r'\% with the current retained inputs. Scenario definitions and weights are unchanged.'
    for p in future['scenarios']:
        assert p['minimax_choices']==['Zurich'] and len(p['possible_champions'])==16
    future_ranks=read_csv(result_dirs['future']/'ranks.csv')
    def runner_up_pair(scenario):
        rows=future_ranks[future_ranks.evidence_arm.eq('conditional')&future_ranks.scenario.eq(scenario)&future_ranks.weight_reference.eq('fixed')].sort_values('decision_rank')
        assert len(rows)==16
        return '--'.join(rows.iloc[1:3].city)
    macros['FutureDeterministic']=(r'All three uniform-change scenarios retain Zurich as the conservative recommendation and all sixteen cities as possible champions under both weight references, including the Singapore-proxy withdrawal arm. Balanced improvement changes the fixed-weight second and third decisions from '+runner_up_pair('baseline')+r' to '+runner_up_pair('balanced_improvement')+r'.')
    fmc=read_csv(result_dirs['future']/'future_mc_city_summary.csv');order=['resource_expansion','living_pressure','balanced_improvement']
    def rates(arm):
        return ', '.join(f"{100*float(fmc[(fmc.weight_reference=='fixed')&(fmc.city=='Zurich')&(fmc.evidence_arm==arm)&(fmc.scenario==s)].iloc[0].recommendation_frequency):.2f}"+r'\%' for s in order)
    macros['FutureMonteCarlo']=(r'Specifically, $C\sim U[0,1]$ is shared across cities and $I_i\sim U[0,1]$ varies by city, independently; $\delta_i=0.05C+0.05I_i$. The relevant raw multipliers are $1+\delta_i$ or $1-\delta_i$, and affected criteria within a city share that multiplier. With 10,000 draws per scenario, Zurich\'s fixed-weight recommendation frequencies are '+rates('conditional')+r' for resource expansion, living pressure and balanced improvement respectively.').replace("\\'s","'s")
    macros['ProxyWithdrawalMC']='Repeating the same shocks after withdrawing Singapore\'s historical stage-travel proxy gives '+rates('withdraw_historical_stage_proxy')+r' respectively. These paired calculations isolate dependence on that proxy while retaining the chosen shock distribution.'
    (HERE/'task4_v198_generated.tex').write_text('% V198 manuscript assets from V197 evidence and controlled extensions; historical cases retained.\n'+'\n'.join('\\newcommand{\\'+k+'}{'+v+('' if k in {'CurrentMeanWidth','TotalWidthReduction','RevisionRankChanges'} else ' ')+'}' for k,v in macros.items())+'\n')
    for name in ['indicators.tex','country.tex','age_joint.tex']:
        shutil.copyfile(HERE/'task4_v137_assets'/name,A/name)
    table(A/'baseline.tex','Conservative baseline decision ranks with unchanged weights.','Rank & City & Score interval & Maximum regret',[(r.decision_rank,r.city,f'{r.score_lower:.2f}--{r.score_upper:.2f}',f'{r.max_regret:.2f}') for r in fixed.itertuples()],'rlrr','tab:baseline')
    table(A/'preferences.tex',r'Conditional recommendation frequencies (\%) for selected cities at concentration 100.','Preference centre & Zurich & Oslo & Singapore',[(label,*[f'{100*mc(name,c):.2f}' for c in ['Zurich','Oslo','Singapore']]) for name,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]],'lrrr')
    diagnostic=summaries['diagnostics'];df,de=diagnostic['revision_diagnostics']
    margins=diagnostic['minimum_strict_margin_by_weight']
    revision=r'''\subsection{A significant revision: retaining uncertain evidence}
A controlled comparison shows why evidence bounds belong in the decision.
On the same 160 utility entries, compare the midpoint completion $z_{ij}=(\ell_{ij}+h_{ij})/2$ with the retained-interval formulation in Equation~\ref{eq:regret}. Both use identical weights, anchors and TOPSIS scores. The midpoint is a declared diagnostic scenario, rather than an estimate of missing observations or a reconstruction of the team's historical first model.

'''
    revision+='The revision retains 48 non-point entries and selects the city with the smallest worst-case shortfall. Zurich remains the recommendation, but '+str(df['changed_city_decision_ranks'])+r" cities change decision rank under fixed weights; Kendall's $\tau_b="+f"{df['kendall_tau_b']:.3f}"+r'$. With equal weights, '+str(de['changed_city_decision_ranks'])+r' ranks change and $\tau_b='+f"{de['kendall_tau_b']:.3f}"+'$.\n\n'
    revision+=r'For each target city $c$, construct a separate interior completion: set every uncertain utility to $\ell_{ij}+\alpha_i(h_{ij}-\ell_{ij})$, with $\alpha_c=0.95$ and $\alpha_i=0.05$ for $i\ne c$. All 112 point values remain fixed and all 48 uncertain values lie strictly inside their intervals. Each target ranks first under both baseline and equal weights. Across the sixteen targets, the smallest lead is '+f"{margins['fixed']:.3f}"+' score points under baseline weights and '+f"{margins['equal']:.3f}"+r' under equal weights. These separate completions establish feasibility in the declared utility rectangle; they carry no estimated probabilities and do not establish joint physical attainability.'+'\n\n'
    revision+=r'Retaining intervals changes the decision order while preserving sixteen possible champions. The \TotalWidthReduction\% reduction in interval width comes from admitted data, separately from this formulation comparison.'+'\n'
    (A/'revision.tex').write_text(revision)
    # Reuse the established source-policy explanation, replacing all affected widths.
    vintage=(HERE/'task4_v154_assets/vintage.tex').read_text().replace('task4_v154_','task4_v198_')
    vc={(v['scenario'],v['weight_reference']):v for v in diagnostic['vintage_cases']}
    for scenario in ['baseline','pre2020_points','after2025_points','non_ok_points','union_points']:
        old=read(R/'results/task4_v143_vintage/summary.json')
        for ref in ['fixed','equal']:
            a=next(x for x in old['cases'] if x['scenario']==scenario and x['weight_reference']==ref)
            assert a['minimax_choices']==vc[scenario,ref]['minimax_choices']
    vintage=vintage.replace('from 16.06 to 48.42',f"from {vc['baseline','fixed']['mean_interval_width']:.2f} to {vc['after2025_points','fixed']['mean_interval_width']:.2f}")
    old_rates=read(R/'results/task4_v145_rate_threshold/summary.json')['thresholds']
    for previous,now in zip(old_rates,diagnostic['hypothetical_rate_thresholds']):
        vintage=vintage.replace(f"{previous['rate_per100000']:.5f}",f"{now['rate_per100000']:.5f}")
    (A/'vintage.tex').write_text(vintage)
    labels={'baseline':'Retained input','pre2020_points':'Before 2020','after2025_points':'After 2025','non_ok_points':'Non-ok flags','union_points':'Union'}
    table(A/'vintage_table.tex','Recommendation after withdrawing selected submitted point information. Width is the mean baseline-weight score range on the 0--100 scale.','Withdrawn group & Cells & Baseline & Equal & Width',[(label,str(vc[s,'fixed']['withdrawn_point_cells']),'/'.join(vc[s,'fixed']['minimax_choices']),'/'.join(vc[s,'equal']['minimax_choices']),f"{vc[s,'fixed']['mean_interval_width']:.2f}") for s,label in labels.items()],'l r l l r','tab:vintage')
    plt.rcParams.update({'font.size':12.5,'axes.labelsize':12.5,'xtick.labelsize':12.5,'ytick.labelsize':12.5,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(6.45,4.5));fig.subplots_adjust(left=.25,right=.96,bottom=.16,top=.97)
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
    inputs=[primary/'summary.json',primary/'current_ranks.csv',R/'design/task4_user_v197_admissions.json',*[p for folder in result_dirs.values() for p in folder.iterdir() if p.is_file()]]
    inputs += [R/'results/task4_v197_mc_precision/summary.json',R/'results/task4_v197_mean_rank_comparisons/summary.json',R/'results/task4_v197_transition/paper_migration_plan.json']
    inputs += [R/name for name in ['results/task4_user_city_indicators/summary.json','results/task4_user_v181_revision/summary.json','results/task4_v181_preferences/summary.json','results/task4_v143_vintage/summary.json','results/task4_v145_rate_threshold/summary.json']]
    paper_inputs=[Path(__file__),HERE/'task4_v137_generated.tex',HERE/'task4_v154_assets/vintage.tex',*[HERE/'task4_v137_assets'/n for n in ['indicators.tex','country.tex','age_joint.tex']]]
    manifest=dict(version='V198',source_sha256={str(p.relative_to(R)):sha(p) for p in inputs},original_review='V189 frozen',primary_science='V197',minimum_figure_font_inserted_pt=12.5*6.5/6.45,figure_scope='score_intervals only; identification matrix has a separate figure_manifest',all_numbers_rebased=True,team_root_unchanged=True,project_settings_changed=False,AI_history_complete=False)
    manifest['paper_input_sha256']={str(p.relative_to(HERE.parent)):sha(p) for p in paper_inputs}
    manifest['output_sha256']={str(p.relative_to(HERE.parent)):sha(p) for p in [HERE/'task4_v198_generated.tex',*[p for p in sorted(A.iterdir()) if p.is_file() and p.name not in {'manifest.json','identification_matrix.pdf','identification_matrix.svg','identification_matrix.png','matrix.csv','figure_manifest.json'}]]}
    (A/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('V198 numerical assets built; cumulative reduction',reduction)

if __name__=='__main__':main()

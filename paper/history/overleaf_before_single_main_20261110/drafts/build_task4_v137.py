"""Generate V137 full-review paper numbers from V136 evidence and audited extensions."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_manifest(root,paths,out):
    protected=['main.tex','ref.bib','mcmthesis.cls',*[f'drafts/task4_v{v}_{kind}.{ext}' for v,kind in [(119,'sections'),(122,'sections'),(123,'paper'),(124,'update'),(125,'paper'),(128,'paper')] for ext in ['tex','pdf']]]
    protected=sorted(set(protected)|set(read(HERE/'task4_v129_support/manifest.json')['protected_manuscript_sha256']))
    protected=sorted(set(protected)|{str(x.relative_to(HERE.parent)) for x in HERE.glob('task4_v131*') if x.is_file() and x.suffix in {'.tex','.pdf'}}|{str(x.relative_to(HERE.parent)) for x in (HERE/'task4_v131_assets').rglob('*') if x.is_file()})
    tracked=set(subprocess.check_output(['git','ls-files'],cwd=HERE.parent,text=True).splitlines())
    protected=[name for name in protected if name in tracked]
    own=[HERE/f'task4_v137_{x}.tex' for x in ['paper','front','core','conclusion','news','ai','references']]
    for key,name in [('ai_provenance','ai_session_manifest.json'),('ai_verification','ai_session_verification.json'),('ai_tools','ai_tool_receipts.json'),('country_sources','country_source_index.json')]:
        (out/name).write_bytes(paths[key].read_bytes())
    for key,name in [('witness_summary','witness_summary.json'),('witness_audit','witness_verification.json'),('witness_cases','witness_cases.csv')]:(out/name).write_bytes(paths[key].read_bytes())
    for key in ['warsaw_retrieval','warsaw_scope','warsaw_verification']:(out/(key+'.json')).write_bytes(paths[key].read_bytes())
    for number in [3,4,58,64]:(out/f'warsaw_page_{number:03d}_extracted.txt').write_bytes(paths[f'warsaw_page{number}'].read_bytes())
    for key in ['london_inventory','london_extraction','london_verification']:(out/(key+'.json')).write_bytes(paths[key].read_bytes())
    (out/'source_berlin_metro_subset.json').write_bytes(paths['berlin_inventory'].read_bytes())
    for key in ['paris_teacher_example','paris_pupil_example','paris_directory_example','paris_teacher_definition','paris_pupil_definition']:(out/(key+'.json')).write_bytes(paths[key].read_bytes())
    for key,name in [('vienna_inventory','source_vienna_metro_subset.csv'),('prague_inventory','source_prague_metro_complexes.csv')]:
        (out/name).write_bytes(paths[key].read_bytes())
    for name in ['summary.json','admitted_sources.csv','indicator_coverage.csv','cell_coverage.csv','verification.json']:
        (out/('source_coverage_'+name)).write_bytes((root/'results/task4_v146_source_coverage'/name).read_bytes())
    manifest=dict(primary_evidence='V136 user16',extensions='V137',documentation_revision='V148',source_hashes={str(p.relative_to(root)):sha(p) for p in paths.values()},manuscript_source_sha256={p.name:sha(p) for p in own},protected_files={x:sha(HERE.parent/x) for x in protected},minimum_figure_font_source_pt=12.5,figure_width_inches=6.45,figure_height_inches=4.5,figure_insert_width_mm=164,minimum_figure_font_inserted_pt=12.5*(164/25.4)/6.45,original_user_csv_sha256=sha(paths['source']),full_paper_uses_frozen_V136_evidence=True,historical_cases_remain_separate=True,private_transcript_included=False,generated_revision_sha256=sha(out/'revision.tex'),generated_vintage_sha256={n:sha(out/n) for n in ['vintage.tex','vintage_table.tex']})
    manifest['generated_age_joint_sha256']=sha(out/'age_joint.tex')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def write_vintage(paths,out):
    summary=read(paths['vintage_summary']);audit=read(paths['vintage_audit'])
    assert audit['status']=='pass' and audit['independently_recomputed_city_cases']==160
    for name,digest in audit['result_sha256'].items():assert sha(paths['vintage_summary'].parents[2]/name)==digest,name
    for key,name in [('vintage_summary','vintage_summary.json'),('vintage_audit','vintage_verification.json'),('vintage_points','vintage_points.csv')]:(out/name).write_bytes(paths[key].read_bytes())
    assert summary['point_year_counts'].get('2026')==64 and summary['point_year_counts'].get('2025')==2 and sum(summary['point_year_counts'].values())==112
    assert summary['point_flag_counts']=={'MODELLED':16,'NATIONAL':1,'STALE':8,'SUSPECT':3,'ok':84}
    labels={'baseline':'Retained input','pre2020_points':'Before 2020','after2025_points':'After 2025','non_ok_points':'Non-ok flags','union_points':'Union'}
    rows=[]
    for case,label in labels.items():
        a=next(x for x in summary['cases'] if x['scenario']==case and x['weight_reference']=='fixed')
        b=next(x for x in summary['cases'] if x['scenario']==case and x['weight_reference']=='equal')
        rows.append([label,str(a['withdrawn_point_cells']),'/'.join(a['minimax_choices']),'/'.join(b['minimax_choices']),f"{a['mean_interval_width']:.2f}"])
    table(out/'vintage_table.tex','Recommendation after withdrawing selected submitted point information. Width is the mean baseline-weight score range on the 0--100 scale.','l r l l r','Withdrawn group & Cells & Baseline & Equal & Width',rows,'tab:vintage')
    (out/'vintage.tex').write_text(r'''\subsection{Sensitivity to the accepted input information}\label{sec:sourcepolicy}
The conservative choice depends on which submitted observations are accepted.
Of the 112 retained point entries, 64 are labelled 2026, two 2025 and 46 earlier;
28 carry non-\texttt{ok} source flags: 16 \texttt{MODELLED}, eight \texttt{STALE},
three \texttt{SUSPECT} and one \texttt{NATIONAL}.
For a controlled test, replace selected point utilities by $[0,1]$, keeping
weights, all supplements and the 48 original non-point bounds unchanged.
The groups are points dated before 2020, after 2025, non-\texttt{ok} points and
their union. The union counts overlapping entries once.

\input{task4_v137_assets/vintage_table.tex}

Withdrawing the 28 flagged points changes the recommendation to Berlin under
baseline weights and Paris under equal weights. Removing the 13 pre-2020 points
selects Singapore under baseline weights; equal weights retain Zurich.
Withdrawing the 64 later-dated points retains Zurich under both references,
while widening the baseline mean range from 16.09 to 48.43. The 95-entry union
selects Singapore under both. All sixteen cities remain possible champions
in every case. These withdrawals test dependence on accepted information:
the labels and date cutoffs are not calibrated error probabilities or a
judgment that every flagged entry is wrong. The experiment preserves the
primary data and does not reconstruct a same-year-only matrix.
''')

def write_homicide_check(paths,out):
    source=read(paths['homicide_scope']);audit=read(paths['homicide_audit']);summary=read(paths['homicide_summary'])
    assert audit['status']=='pass' and source['primary_admissions']==0
    for name,digest in audit['result_sha256'].items():assert sha(paths['homicide_summary'].parents[2]/name)==digest,name
    rows={(x['scenario'],x['weight_reference']):x for x in summary['cases']}
    for ref,city in [('fixed','Singapore'),('equal','Oslo')]:
        assert rows['withdraw_Zurich_homicide',ref]['minimax_choices']==[city]
        assert rows['withdraw_Amsterdam_homicide',ref]['minimax_choices']==['Zurich']
    assert source['amsterdam']['annual_victims']==10 and source['amsterdam']['provisional'] and source['amsterdam']['regional_period_victims']==68
    assert [source['zurich'][f'completed_offences_{y}'] for y in [2024,2025]]==[1,2]
    for key,name in [('homicide_scope','homicide_scope.json'),('homicide_source_audit','homicide_source_verification.json'),('homicide_summary','homicide_summary.json'),('homicide_audit','homicide_verification.json'),('homicide_annual','homicide_cbs_annual_table.json'),('homicide_cells','homicide_cbs_cells.json'),('homicide_page117','homicide_zurich_page117.txt'),('homicide_page118','homicide_zurich_page118.txt')]:(out/name).write_bytes(paths[key].read_bytes())
    path=out/'vintage.tex'
    path.write_text(path.read_text()+r'''\nWithholding Zurich's homicide-rate point alone selects Singapore under baseline
weights and Oslo under equal weights. Withholding Amsterdam's alone retains
Zurich under both. Each single-point test keeps the other 159 entries fixed;
no official count is inserted as an assumed replacement rate.
'''.replace('\\n','\n'))

def write_rate_threshold(paths,out):
    summary=read(paths['rate_threshold_summary']);audit=read(paths['rate_threshold_audit'])
    assert audit['status']=='pass' and audit['independent_city_cases']==224
    for name,digest in audit['result_sha256'].items():assert sha(paths['rate_threshold_summary'].parents[2]/name)==digest,name
    rates={x['weight_reference']:x['rate_per100000'] for x in summary['thresholds']}
    for ref,city in [('fixed','Singapore'),('equal','Oslo')]:assert next(x for x in summary['thresholds'] if x['weight_reference']==ref)['alternative']==city
    for key,name in [('rate_threshold_summary','rate_threshold_summary.json'),('rate_threshold_audit','rate_threshold_verification.json')]:(out/name).write_bytes(paths[key].read_bytes())
    path=out/'vintage.tex'
    text=(r'Holding the other 159 entries fixed while varying this point rate $x_Z$, Zurich ties Singapore in maximum regret at about $x_Z='+f'{rates["fixed"]:.5f}'+r'$ per 100,000 under baseline weights, and Oslo at about $x_Z='+f'{rates["equal"]:.5f}'+r'$ under equal weights. Below each respective cutoff Zurich uniquely minimizes regret; above it Zurich does not. These are hypothetical point-rate cutoffs, not observed rates or confidence limits.')
    path.write_text(path.read_text()+'\n'+text+'\n')

def write_age_joint(paths,out):
    summary=read(paths['age_joint_summary']);audit=read(paths['age_joint_audit'])
    assert audit['status']=='pass' and audit['finite_interior_witnesses']==2 and summary['both_orderings_feasible']
    for name,digest in audit['result_sha256'].items():assert sha(paths['age_joint_summary'].parents[2]/name)==digest,name
    for key,name in [('age_joint_summary','age_joint_summary.json'),('age_joint_audit','age_joint_verification.json'),('age_joint_witnesses','age_joint_witnesses.csv')]:(out/name).write_bytes(paths[key].read_bytes())
    low,high=summary['joint_difference_closure']
    text=(r"The shared-membership constraint permits both historical age-group orderings. For younger-minus-older mean travel utility, the joint closure is $["+f'{low:.5f},{high:.5f}'+r"]$, assigning the shared unknown-age mass once. Two separate completions with unknown utilities 0.05 and 0.95 give contrasts $+0.23842$ and $-0.20848$. Both use finite durations and allocate the shared mass to the younger group. The closure endpoints allow zero utility as a limiting value; the two reversals use strictly interior values. These are feasibility constructions within the retained 2012 aggregate uncertainty set, not observed age effects.")
    (out/'age_joint.tex').write_text(text+'\n')

def witness_paragraph(paths):
    summary=read(paths['witness_summary']);audit=read(paths['witness_audit'])
    assert audit['status']=='pass' and summary['weight_cases']==32 and summary['distinct_completions']==16
    for name,digest in audit['result_sha256'].items():assert sha(paths['witness_summary'].parents[2]/name)==digest,name
    margins=summary['minimum_strict_margin_by_weight']
    return (r'For each target city $c$, construct a separate interior completion: set every uncertain utility to $\ell_{ij}+\alpha_i(h_{ij}-\ell_{ij})$, with $\alpha_c=0.95$ and $\alpha_i=0.05$ for $i\ne c$. All 112 point values remain fixed and all 48 uncertain values lie strictly inside their intervals. Each target ranks first under both baseline and equal weights. Across the sixteen targets, the smallest lead is '+f'{margins["fixed"]:.3f}'+r' score points under baseline weights and '+f'{margins["equal"]:.3f}'+r' under equal weights. These separate completions establish feasibility in the declared utility rectangle; they carry no estimated probabilities and do not establish joint physical attainability.')

def table(path,caption,columns,header,rows,label=None):
    text='\\begin{table}[!ht]\\centering\n\\caption{'+caption+'}'
    if label:text+='\\label{'+label+'}'
    text+='\n\\begin{tabular}{'+columns+'}\\toprule\n'+header+r'\\\midrule'+'\n'
    text+='\n'.join(' & '.join(map(str,row))+r' \\' for row in rows)
    text+='\n\\bottomrule\\end{tabular}\\end{table}\n';path.write_text(text)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--research-root',type=Path,required=True);ap.add_argument('--refresh-manifest-only',action='store_true',help='Update documentation receipts without regenerating numeric assets');args=ap.parse_args();root=args.research_root.resolve();out=HERE/'task4_v137_assets';out.mkdir(exist_ok=True)
    paths={
        'london_inventory':root/'data/task4_v135_london/station_entities.json','london_extraction':root/'data/task4_v135_london/extraction.json','london_verification':root/'data/task4_v135_london/verification.json',
        'baseline':root/'results/task4_user_v136_revision/current_ranks.csv','primary_summary':root/'results/task4_user_v136_revision/summary.json','primary_all_ranks':root/'results/task4_user_v136_revision/all_ranks.csv','primary_audit':root/'results/task4_user_v136_revision/revision_audit.json','primary_snapshot':root/'design/task4_user_v136_snapshot.json',
        'pref':root/'results/task4_v137_preferences/summary.json','mc':root/'results/task4_v137_preferences/mc_city_summary.csv',
        'future':root/'results/task4_v137_future/summary.json','future_ranks':root/'results/task4_v137_future/ranks.csv','thresholds':root/'results/task4_v137_future/thresholds.csv','fmc':root/'results/task4_v137_future/future_mc_city_summary.csv',
        'method':root/'results/task4_v137_method_country/summary.json','diagnostic':root/'results/task4_v137_revision_diagnostic/summary.json',
        'audit':root/'results/task4_v137_revision/audit.json','original':root/'results/task4_user_city_indicators/summary.json',
        'source':root/'data/task4_v117_team_intake/city_indicators.csv','admissions':root/'design/task4_user_v136_admissions.json','registry':root/'design/task4_user_current_model.json',
        'ai_provenance':root/'data/task4_v140_ai_provenance/session_manifest.json','ai_verification':root/'data/task4_v140_ai_provenance/verification.json',
        'ai_tools':root/'data/task4_v126_ai_provenance/tool_receipts.json','country_sources':root/'data/task4_v126_country_sources/source_index.json',
        'previous_preferences_mc':root/'results/task4_v131_preferences/mc_city_summary.csv','previous_thresholds':root/'results/task4_v131_future/thresholds.csv',
        'paris_teacher_example':root/'data/task4_v129_education/paris_teacher_henriiv_original.json','paris_pupil_example':root/'data/task4_v129_education/paris_pupil_henriiv_original.json','paris_directory_example':root/'data/task4_v129_education/paris_annuaire_henriiv_original.json','paris_teacher_definition':root/'data/task4_v129_education/paris_teacher_metadata_original.json','paris_pupil_definition':root/'data/task4_v129_education/paris_gt_pupil_metadata_original.json','berlin_inventory':root/'data/task4_v129_transport/berlin_stations.json','vienna_inventory':root/'data/task4_v127_vienna_transport/vienna_stop_area_subset.csv','prague_inventory':root/'data/task4_v127_prague/station_complexes.csv'}
    paths.update(source_coverage_map=root/'design/task4_v146_source_map.json',source_coverage_summary=root/'results/task4_v146_source_coverage/summary.json',source_coverage_verification=root/'results/task4_v146_source_coverage/verification.json')
    paths.update(age_joint_summary=root/'results/task4_v148_age_contrast/summary.json',age_joint_audit=root/'results/task4_v148_age_contrast/verification.json',age_joint_witnesses=root/'results/task4_v148_age_contrast/witnesses.csv')
    warsaw=root/'data/task4_v138_warsaw'
    paths.update({f'warsaw_{key}':warsaw/(file+'.json') for key,file in [('retrieval','retrieval'),('scope','scope_audit'),('verification','verification')]})
    paths.update({f'warsaw_page{n}':warsaw/f'page_{n:03d}_extracted.txt' for n in [3,4,58,64]})
    paths['warsaw_original_archive']=warsaw/'report_original.pdf.gz'
    homicide=root/'data/task4_v144_homicide'
    paths.update(homicide_scope=homicide/'scope_audit.json',homicide_source_audit=homicide/'verification.json',homicide_summary=root/'results/task4_v144_homicide_sensitivity/summary.json',homicide_audit=root/'results/task4_v144_homicide_sensitivity/verification.json',homicide_annual=homicide/'cbs_annual_table_extracted.json',homicide_cells=homicide/'cbs_cells_extracted.json',homicide_page117=homicide/'zurich_page_117_extracted.txt',homicide_page118=homicide/'zurich_page_118_extracted.txt')
    for name,digest in read(paths['homicide_source_audit'])['source_sha256'].items():assert sha(homicide/name)==digest,name
    paths.update(rate_threshold_summary=root/'results/task4_v145_rate_threshold/summary.json',rate_threshold_audit=root/'results/task4_v145_rate_threshold/verification.json')
    paths.update(vintage_summary=root/'results/task4_v143_vintage/summary.json',vintage_audit=root/'results/task4_v143_vintage/verification.json',vintage_points=root/'results/task4_v143_vintage/submitted_points.csv')
    paths.update(witness_summary=root/'results/task4_v142_witnesses/summary.json',witness_audit=root/'results/task4_v142_witnesses/verification.json',witness_cases=root/'results/task4_v142_witnesses/cases.csv')
    for name,digest in read(paths['witness_audit'])['result_sha256'].items():assert sha(root/name)==digest,name
    assert read(paths['warsaw_scope'])['primary_admissions']==0 and read(paths['warsaw_verification'])['status']=='pass'
    for name,digest in read(paths['warsaw_verification'])['source_sha256'].items():assert sha(warsaw/name)==digest,name
    hashes={str(p.relative_to(root)):sha(p) for p in paths.values()};assert read(paths['audit'])['status']=='pass' and read(paths['registry'])['version'] in {'V130','V136'}
    assert read(paths['ai_verification'])['status']=='pass'
    assert read(paths['ai_verification'])['manifest_sha256']==sha(paths['ai_provenance'])
    assert read(paths['primary_audit'])['status']=='pass'
    for name,expected in read(paths['primary_snapshot'])['source_sha256'].items():assert sha(root/name)==expected,name
    for name,expected in read(paths['audit'])['result_sha256'].items():assert sha(root/name)==expected,name
    if args.refresh_manifest_only:
        previous=read(out/'manifest.json')
        # A documentation-only refresh cannot silently bless changed science inputs.
        for name,digest in previous['source_hashes'].items():
            if name=='design/task4_user_current_model.json' and sha(root/name)!=digest:
                registry=read(root/name);assert registry['version']=='V136' and registry['module']=='task4_user_v136_revision'
            else:assert sha(root/name)==digest,name
        for name,digest in previous['protected_files'].items():
            assert sha(HERE.parent/name)==digest,name
        revision=out/'revision.tex';parts=revision.read_text().split('\n\n');assert len(parts)==4 and parts[2].startswith(('A constructed interior completion','For each target city'))
        parts[2]=witness_paragraph(paths);revision.write_text('\n\n'.join(parts))
        write_vintage(paths,out)
        write_homicide_check(paths,out)
        write_rate_threshold(paths,out)
        write_age_joint(paths,out)
        write_manifest(root,paths,out)
        print('Refreshed V148 validation text and receipts; primary numerical assets not regenerated.')
        return
    base=pd.read_csv(paths['baseline']);fixed=base[base.weight_reference.eq('fixed')].sort_values('decision_rank');assert len(fixed)==16 and fixed.iloc[0].city=='Zurich' and fixed.possible_champion.all()
    summary=read(paths['primary_summary']);assert [summary[x] for x in ['point_cells','partial_cells','fully_missing_cells']]==[112,33,15]
    pref,method,diagnostic,future=map(read,[paths['pref'],paths['method'],paths['diagnostic'],paths['future']]);mc=pd.read_csv(paths['mc']);k100=mc[mc.concentration.eq(100)]
    current=float((fixed.score_upper-fixed.score_lower).mean());original=read(paths['original'])['results']['fixed']['mean_score_interval_width'];reduction=100*(original-current)/original
    profiles={x['profile']:x for x in pref['profiles']};assert [profiles[p]['minimax_choices'] for p in ['baseline','education_priority','independent_living_priority']]==[['Zurich'],['Oslo'],['Zurich']]
    for p in profiles.values():assert len(p['possible_champions'])==16
    # Preserve unchanged indicator definitions and historical-case prose.
    (out/'indicators.tex').write_text((HERE/'task4_v123_assets/indicators.tex').read_text())
    table(out/'baseline.tex','Conservative baseline decision ranks with unchanged weights.','rlrr','Rank & City & Score interval & Maximum regret',[(r.decision_rank,r.city,f'{r.score_lower:.2f}--{r.score_upper:.2f}',f'{r.max_regret:.2f}') for r in fixed.itertuples()],'tab:baseline')
    names={'baseline':'Baseline','education_priority':'Education priority','independent_living_priority':'Independent living'}
    table(out/'preferences.tex',r'Conditional recommendation frequencies (\%) for selected cities at concentration 100.','lrrr','Preference centre & Zurich & Oslo & Singapore',[(label,*[f'{100*k100[(k100.profile==p)&(k100.city==c)].iloc[0].minimax_recommendation_frequency:.2f}' for c in ['Zurich','Oslo','Singapore']]) for p,label in names.items()])
    country=[]
    for row in method['country_pairs']:
        country.extend([(row['country'],row['city_a'],f'{row["a_score_lower"]:.2f}--{row["a_score_upper"]:.2f}'),('',row['city_b'],f'{row["b_score_lower"]:.2f}--{row["b_score_upper"]:.2f}')])
    table(out/'country.tex','Separate historical country cases using the legacy 25-city V117 evidence.','llr','Country & City & Score interval',country)
    macros={}
    for line in (HERE/'task4_v122_generated.tex').read_text().splitlines():
        match=re.fullmatch(r'\\newcommand\{\\(\w+)\}\{(.*)\}',line)
        if match and match[1] in {'EquityCase','AgeCase','CountryInterpretation','CaseReferences'}:macros[match[1]]=match[2].rstrip()
    assert len(macros)==4
    macros.update(CurrentMeanWidth=f'{current:.5f}',TotalWidthReduction=f'{reduction:.2f}')
    before=next(x['mean_width'] for x in summary['results'] if x['scenario']=='before' and x['weight_reference']=='fixed')
    macros['LatestEvidenceChange']=(f'The latest London station/hub subset narrows the preceding fixed-weight mean from {before:.5f} to {current:.5f}, or {100*(before-current)/before:.3f}'+r'\%. '+ 'All static decision ranks remain unchanged. This is an information update, not an observed improvement over time.')
    d={x['weight_reference']:x for x in diagnostic['results']};df,de=d['fixed'],d['equal'];assert df['midpoint_scenario_first']=='Zurich' and len(df['possible_champions'])==16
    macros['RevisionRankChanges']=str(df['changed_city_decision_ranks'])
    b=k100[k100.profile.eq('baseline')].set_index('city');assert b.loc['Oslo','mean_decision_rank']<b.loc['Zurich','mean_decision_rank']
    macros['SummaryWeightMC']=(r'In 10,000 baseline weight perturbations at Dirichlet concentration 100, Zurich is recommended in '+f'{100*b.loc["Zurich","minimax_recommendation_frequency"]:.2f}'+r'\% of draws, compared with '+f'{100*b.loc["Oslo","minimax_recommendation_frequency"]:.2f}'+r'\% for Oslo and '+f'{100*b.loc["Singapore","minimax_recommendation_frequency"]:.2f}'+r'\% for Singapore.')
    cases={x['weight_reference']:x for x in method['method_cases'] if x['evidence_version']=='V136'};case=cases['fixed'];equal=cases['equal'];assert case['vikor_q_winners']==['Dublin'] and case['single_compromise_accepted'] and equal['vikor_q_winners']==['Oslo'] and not equal['single_compromise_accepted']
    macros['MethodComparison']=(r'TOPSIS selects Zurich at the midpoint, whereas VIKOR selects Dublin; Kendall\'s '+rf'$\tau_b={case["kendall_tau_b"]:.3f}$. '+r'Dublin satisfies VIKOR\'s advantage and stability conditions. Under equal weights, '+rf'$\tau_b={equal["kendall_tau_b"]:.3f}$; '+r'Oslo has the lowest VIKOR index but fails those acceptance conditions, so it is not an accepted unique compromise solution.')
    ranks=pd.read_csv(paths['future_ranks'])
    for _,g in ranks.groupby(['evidence_arm','weight_reference','scenario']):assert g.loc[g.decision_rank.eq(1),'city'].tolist()==['Zurich'] and g.possible_champion.all()
    balanced=ranks[ranks.evidence_arm.eq('conditional')&ranks.weight_reference.eq('fixed')&ranks.scenario.eq('balanced_improvement')].sort_values('decision_rank');assert balanced.iloc[1:3].city.tolist()==['Oslo','Singapore']
    macros['FutureDeterministic']=r'All three uniform-change scenarios retain Zurich as the conservative recommendation and all sixteen cities as possible champions under both weight references, including the Singapore-proxy withdrawal arm. Balanced improvement changes the fixed-weight second and third decisions from Singapore--Oslo to Oslo--Singapore.'
    t=pd.read_csv(paths['thresholds']);t=t[t.weight_reference.eq('fixed')].set_index('city')
    macros['FutureThresholds']=('Oslo reaches the tie at approximately '+f'{100*t.loc["Oslo","required_cost_reduction_fraction"]:.3f}'+r'\% reduction, Singapore at '+f'{100*t.loc["Singapore","required_cost_reduction_fraction"]:.3f}'+r'\%, and Stockholm at '+f'{100*t.loc["Stockholm","required_cost_reduction_fraction"]:.3f}'+r'\%. Zurich already minimizes regret at baseline. A slightly greater reduction produces a strict recommendation switch in these calculations.')
    fmc=pd.read_csv(paths['fmc']);fc=fmc[fmc.weight_reference.eq('fixed')&fmc.city.eq('Zurich')];order=['resource_expansion','living_pressure','balanced_improvement']
    def rates(arm):
        f=fc[fc.evidence_arm.eq(arm)].set_index('scenario');return ', '.join(f'{100*f.loc[s,"recommendation_frequency"]:.2f}'+r'\%' for s in order)
    macros['FutureMonteCarlo']=(r'Specifically, $C\sim U[0,1]$ is shared across cities and $I_i\sim U[0,1]$ varies by city, independently; $\delta_i=0.05C+0.05I_i$. The relevant raw multipliers are $1+\delta_i$ or $1-\delta_i$, and affected criteria within a city share that multiplier. With 10,000 draws per scenario, Zurich\'s fixed-weight recommendation frequencies are '+rates('conditional')+r' for resource expansion, living pressure and balanced improvement respectively.')
    macros['ProxyWithdrawalMC']=(r'Repeating the same shocks after withdrawing Singapore\'s historical stage-travel proxy gives '+rates('withdraw_historical_stage_proxy')+r' respectively. These paired calculations isolate dependence on that proxy while retaining the chosen shock distribution.')
    macros['PreferenceResults']=(rf'Education priority changes the conservative recommendation from Zurich to Oslo, with decision-rank $\tau_b={profiles["education_priority"]["kendall_tau_b_vs_baseline"]:.3f}$ relative to baseline. Independent-living priority retains Zurich and gives $\tau_b={profiles["independent_living_priority"]["kendall_tau_b_vs_baseline"]:.3f}$. '+r'All sixteen cities remain possible champions in each profile.')
    oldmc=pd.read_csv(paths['previous_preferences_mc']);oldlondon=oldmc[(oldmc.profile=='baseline')&(oldmc.concentration==100)&(oldmc.city=='London')].iloc[0];newlondon=k100[(k100.profile=='baseline')&(k100.city=='London')].iloc[0]
    macros['PreferenceEvidenceChange']=(f"At concentration 100 around baseline weights, London's mean decision rank changes from {oldlondon.mean_decision_rank:.4f} to {newlondon.mean_decision_rank:.4f} after its inventory supplement. The fixed education-priority recommendation remains Oslo; changes concern the declared evidence bounds and weight distribution.")
    oldt=pd.read_csv(paths['previous_thresholds']);oldt=oldt[oldt.weight_reference.eq('fixed')].set_index('city')
    assert abs(oldt.loc['Berlin','required_cost_reduction_fraction']-t.loc['Berlin','required_cost_reduction_fraction'])<1e-12
    macros['EvidenceThresholdCheck']=("Berlin's hypothetical combined-cost tie threshold remains "+f'{100*t.loc["Berlin","required_cost_reduction_fraction"]:.3f}'+r'\% after the London inventory update. Scenario definitions and weights are unchanged.')
    macros['MonteCarloInterpretation']=(f'At concentration 100, Oslo has a better mean decision rank ({b.loc["Oslo","mean_decision_rank"]:.4f}) than Zurich ({b.loc["Zurich","mean_decision_rank"]:.4f}), although Zurich has the greater recommendation frequency and is the fixed-weight minimax choice. '+r'At concentration 20 under education priority, Singapore is the most frequently recommended city, whereas the fixed education-priority decision is Oslo.')
    (HERE/'task4_v137_generated.tex').write_text('% Generated from V136 evidence and independently audited V137 results.\n'+'\n'.join('\\newcommand{\\'+k+'}{'+v.replace("\\'s","'s")+('' if k in {'CurrentMeanWidth','TotalWidthReduction','RevisionRankChanges'} else ' ')+'}' for k,v in macros.items())+'\n')
    witnesses={x['scenario']:x for x in df['chosen_completion_counterexamples']};interior=witnesses['interior_counterexample'];endpoint=witnesses['adversarial_endpoint_Dublin']
    assert interior['first_city']=='Dublin' and endpoint['first_city']=='Dublin'
    rev=r'''\subsection{A significant revision: retaining uncertain evidence}
A controlled comparison shows why evidence bounds belong in the decision.
On the same 160 utility entries, compare the midpoint completion $z_{ij}=(\ell_{ij}+h_{ij})/2$ with the retained-interval formulation in Equation~\ref{eq:regret}. Both use identical weights, anchors and TOPSIS scores. The midpoint is a declared diagnostic scenario, rather than an estimate of missing observations or a reconstruction of the team's historical first model.

'''
    rev+=f'The revision retains {diagnostic["uncertain_cells_retained"]} non-point entries and selects the city with the smallest worst-case shortfall. Zurich remains the recommendation, but {df["changed_city_decision_ranks"]} cities change decision rank under fixed weights; '+rf'Kendall\'s $\tau_b={df["kendall_tau_b"]:.3f}$. '+f'With equal weights, {de["changed_city_decision_ranks"]} ranks change and '+rf'$\tau_b={de["kendall_tau_b"]:.3f}$.\n\n'
    rev+=witness_paragraph(paths)+'\n\n'
    rev+=r'Retaining intervals changes the decision order while preserving sixteen possible champions. The \TotalWidthReduction\% reduction in interval width comes from admitted data, separately from this formulation comparison.'+'\n'
    # TeX line breaks must be real newlines, not accidental control words.
    rev=rev.replace("\\'s","'s").replace('\\n\\n','\n\n');(out/'revision.tex').write_text(rev)
    plt.rcParams.update({'font.size':12.5,'axes.labelsize':12.5,'xtick.labelsize':12.5,'ytick.labelsize':12.5,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(6.45,4.5));fig.subplots_adjust(left=.25,right=.96,bottom=.16,top=.97);ys=list(range(16));l=fixed.score_lower.to_numpy();u=fixed.score_upper.to_numpy();ax.hlines(ys,l,u,color='#526678',linewidth=2.3);ax.scatter(l,ys,marker='|',s=100,c='#526678');ax.scatter(u,ys,marker='|',s=100,c='#526678');ax.hlines(0,l[0],u[0],color='#006c67',linewidth=4);ax.set_yticks(ys,fixed.city);ax.invert_yaxis();ax.set_xlim(40,75);ax.set_xticks([40,50,60,70]);ax.set_xlabel('TOPSIS score bound (0-100)');ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0)
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
    for suffix in ['pdf','svg','png']:fig.savefig(out/f'score_intervals.{suffix}',dpi=300)
    plt.close(fig);svg=out/'score_intervals.svg';svg.write_text('\n'.join(x.rstrip() for x in svg.read_text().splitlines())+'\n');fixed.to_csv(out/'source_intervals.csv',index=False);k100.to_csv(out/'source_mc_k100.csv',index=False)
    write_vintage(paths,out)
    write_homicide_check(paths,out)
    write_rate_threshold(paths,out)
    write_age_joint(paths,out)
    write_manifest(root,paths,out)
    for path,expected in hashes.items():assert sha(root/path)==expected
    print('Built current V136/V137 full-paper tables, macros, diagnostic and 12.5pt figure; total width reduction:',round(reduction,4))
if __name__=='__main__':main()

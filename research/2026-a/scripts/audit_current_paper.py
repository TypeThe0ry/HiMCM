"""Independent audit of current local V203 paper; does not build or activate it."""
from pathlib import Path
import hashlib,json,re,subprocess,zlib,unicodedata,xml.etree.ElementTree as ET
import numpy as np,pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES,weights
from audit_task4_v193 import values,norm
R=Path(__file__).resolve().parents[1]; H=R.parents[1]; P=R.parents[2]/'HiMCM-Overleaf'; A=R/'results/current_paper_assets'; B=Path('/data/scratch/himcm-current-oslo-spatial-build'); O=R/'results/current_paper_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def frame(p):return pd.read_csv(p,float_precision='round_trip')
def main():
 snapshot=read(R/'design/task4_user_v203_snapshot.json'); assert snapshot['bindings']==len(snapshot['source_sha256']) and snapshot['bindings']>=476
 for n,h in snapshot['source_sha256'].items():assert sha(R/n)==h,n
 old=read(R/'results/task4_v202_transition/protection_snapshot.json'); assert len(old['v200_bindings'])==407
 transition=read(R/'results/task4_v203_transition/protection_snapshot.json'); assert len(transition['v202_bindings'])==476
 for n,h in transition['v202_bindings'].items():assert snapshot['source_sha256'][n]==h
 for n in ['ref.bib','mcmthesis.cls','figures/country_contrasts.pdf']:
  p=P/n;assert sha(p)==old['protected_files'][str(p)],n
 spatial=read(R/'results/current_oslo_spatial_review/verification.json'); assert spatial['status'].startswith('PASS') and spatial['preserved_v203_bindings']==548 and spatial['commute_bound_files_checked']==22
 for name,digest in spatial['sha256'].items():assert sha(R/name)==digest,name
 spatial_pdf=R/'visuals/current_spatial/city_walktime.pdf';assert sha(P/'figures/walktime_context.pdf')==sha(spatial_pdf)
 assert spatial['min_text_size_at_6_5_in_pt']>=9 and spatial['figure_svg_width_pt']==468 and spatial['oslo_nasa_alpha_coverages']==[0,0,0]
 for folder in [R/'data/current_oslo_travel2009',R/'data/current_zurich_fte_bound']:
  assert folder.is_dir()
 tex=(P/'main.tex').read_text(); oldtex=subprocess.check_output(['git','-C',str(P),'show','aeeac9d918f1f97d2045025fdc4079d5ae4f74ff:main.tex'],text=True)
 assert hashlib.sha256(oldtex.encode()).hexdigest()==old['protected_files'][str(P/'main.tex')]
 original=set(re.findall(r'\\bibitem\{([^}]+)\}',oldtex));current=set(re.findall(r'\\bibitem\{([^}]+)\}',tex)); assert len(original)==59 and original<current and len(current)==61 and 'enturstop' in current,(len(original),len(current),current-original)
 prior_tex=subprocess.check_output(['git','-C',str(P),'show','faadd04:main.tex'],text=True)
 prior_refs=set(re.findall(r'\\bibitem\{([^}]+)\}',prior_tex)); assert len(prior_refs)==61 and prior_refs<=current
 assert re.search(r'tcn\s*=\s*18213',tex)
 ai='\\section*{Report on Use of AI Tools}'
 assert tex[tex.index(ai):]==prior_tex[prior_tex.index(ai):].replace('V202 primary','V203 primary').replace('V202 validation','V203 validation')
 from task4_v137_method_country import CASE_FILES
 for name in CASE_FILES:assert sha(R/'results/task4_v203_method'/name)==sha(R/'results/task4_v200_method'/name),name
 manifest=read(A/'manifest.json')
 for n,h in manifest['source_sha256'].items():assert sha(R/n)==h,n
 for n,h in manifest['output_sha256'].items():assert sha(A/n)==h,n
 for n in ['identification_matrix.pdf','score_intervals.pdf']:assert sha(P/'figures'/n)==sha(A/n),n
 for n in ['indicators.tex','preferences.tex','revision.tex','vintage_table.tex']:
  assert norm((A/n).read_text()) in norm(tex),n
 macros={m[1]:m[2] for line in tex.splitlines() if (m:=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line))}
 am={m[1]:m[2] for line in (A/'generated.tex').read_text().splitlines() if (m:=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line))}
 # Historical explanatory case wording is preserved in the manuscript rather than rewritten.
 dynamic=['CurrentMeanWidth','TotalWidthReduction','LatestEvidenceChange','RevisionRankChanges','SummaryWeightMC','MethodComparison','FutureDeterministic','FutureThresholds','PreferenceResults','PreferenceEvidenceChange','EvidenceThresholdCheck','MonteCarloInterpretation','MCBaseMeans','MCSettings','MCPairComparisons','MCCertifiedPairs','MCUnresolvedPairs','MCUniqueMinSettings','MCFrequencyHalfWidthPP','MCRankHalfWidth']
 for key in dynamic:assert macros[key]==am[key],key
 f,l,h=revised_bounds();cities=f.city.tolist();assert [int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())]==[112,37,11]
 ranks=frame(R/'results/task4_user_v203_revision/current_ranks.csv');widths={}
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  a,b,r=values(l,h,w);v=ranks[ranks.weight_reference.eq(ref)].set_index('city').loc[cities]
  for col,arr in [('score_lower',a),('score_upper',b),('max_regret',r)]:np.testing.assert_allclose(v[col],arr,atol=1e-11,rtol=0)
  assert v.index[v.decision_rank.eq(1)].tolist()==(['Oslo'] if ref=='fixed' else ['Zurich']) and v.possible_champion.sum()==16 and v.necessary_champion.sum()==0
  widths[ref]=float(np.mean(b-a))
 assert macros['CurrentMeanWidth']==f"{widths['fixed']:.5f}"
 expected=ranks[ranks.weight_reference.eq('fixed')].set_index(['city','weight_reference']).sort_index();actual=frame(A/'source_intervals.csv').set_index(['city','weight_reference']).sort_index();pd.testing.assert_frame_equal(actual,expected,check_exact=True)
 for r in expected.sort_values('decision_rank').itertuples():assert f'{r.decision_rank} & {r.Index[0]} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f}' in tex,r.Index
 m=frame(A/'matrix.csv').set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
 np.testing.assert_allclose(m.utility_lower.to_numpy().reshape(16,10),l,rtol=0,atol=2e-16);np.testing.assert_allclose(m.utility_upper.to_numpy().reshape(16,10),h,rtol=0,atol=2e-16);assert m.state.value_counts().to_dict()=={'point':112,'partial':37,'unknown':11}
 pref=frame(R/'results/task4_v203_preferences/mc_city_summary.csv');k=pref[pref.concentration.eq(100)]
 for profile,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]:
  cells=[f"{100*float(k[k.profile.eq(profile)&k.city.eq(city)].iloc[0].minimax_recommendation_frequency):.2f}" for city in ['Zurich','Oslo','Singapore']];assert label+' & '+' & '.join(cells) in tex
 for city in ['Zurich','Oslo','Singapore']:
  row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0];assert f'{100*row.minimax_recommendation_frequency:.2f}' in macros['SummaryWeightMC'];assert f'{row.mean_decision_rank:.4f}' in macros['MonteCarloInterpretation']
 for key,val in [('MCBaseMeans','2064'),('MCSettings','37'),('MCPairComparisons','4440'),('MCCertifiedPairs','4271'),('MCUnresolvedPairs','169'),('MCUniqueMinSettings','23')]:assert macros[key].strip()==val
 future=read(R/'results/task4_v203_future/summary.json');thresholds={x['city']:x for x in future['thresholds'] if x['weight_reference']=='fixed'}
 for city in ['Zurich','Singapore','Stockholm']:assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}" in macros['FutureThresholds']
 assert thresholds['Oslo']['required_cost_reduction_fraction']==0 and thresholds['Oslo']['status']=='already_strict_minimax'
 assert thresholds['Berlin']['required_cost_reduction_fraction'] is None
 for scenario in ['resource_expansion','living_pressure']:
  assert next(x for x in future['scenarios'] if x['evidence_arm']=='conditional' and x['scenario']==scenario and x['weight_reference']=='fixed')['minimax_choices']==['Oslo']
 assert 'Fixed weights select Oslo in all three scenarios' in macros['FutureDeterministic']
 mc=frame(R/'results/task4_v203_future/future_mc_city_summary.csv')
 for arm,macro in [('conditional','FutureMonteCarlo'),('withdraw_historical_stage_proxy','ProxyWithdrawalMC')]:
  for scenario in ['resource_expansion','living_pressure','balanced_improvement']:
   row=mc[mc.weight_reference.eq('fixed')&mc.city.eq('Oslo')&mc.evidence_arm.eq(arm)&mc.scenario.eq(scenario)].iloc[0];assert f'{100*row.recommendation_frequency:.2f}' in macros[macro]
 vintage=read(R/'results/task4_v203_diagnostics/summary.json')['vintage_cases'];vintage={(x['scenario'],x['weight_reference']):x for x in vintage}
 for sc,label in [('baseline','Retained input'),('pre2020_points','Before 2020'),('after2025_points','After 2025'),('non_ok_points','Non-ok flags'),('union_points','Union')]:
  assert f"{label} & {vintage[sc,'fixed']['withdrawn_point_cells']} & {'/'.join(vintage[sc,'fixed']['minimax_choices'])} & {'/'.join(vintage[sc,'equal']['minimax_choices'])} & {vintage[sc,'fixed']['mean_interval_width']:.2f}" in tex
 for city in ['Zurich','Oslo']:
  row=ranks[ranks.weight_reference.eq('fixed')].set_index('city').loc[city];assert f"{row.score_lower:.2f}" in tex and f"{row.max_regret:.2f}" in tex
 n=norm(tex)
 for phrase in ['25 Singapore venues','OCBC Aquatic Centre','withholding them leaves 23','withholding OCBC leaves 22','ages 16 and above','for all ages','Tuesday maintenance','5--28 December','2024 population of 6,036,900','inventory date is unstated']:
  assert phrase in n,phrase
 for value in ['15.606','0.648','28.10','40.50','0.14981']:assert value in n,value
 assert 'per entry' in n.lower() or 'per-entry' in n.lower() or 'per visit' in n.lower()
 assert '07:00' in n and '21:30' in n
 fonts=[]
 for name in ['identification_matrix.pdf','score_intervals.pdf']:
  p=P/'figures'/name;sizes=[]
  for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',p.read_bytes(),re.S):
   try:raw=zlib.decompress(stream)
   except zlib.error:continue
   sizes.extend(float(x) for x in re.findall(rb'/\w+\s+([0-9.]+)\s+Tf',raw))
  width=float(re.search(r'Page size:\s+([0-9.]+)',subprocess.check_output(['pdfinfo',str(p)],text=True))[1]);assert sizes and min(sizes)*468/width>=9,(p,sizes,width)
  fonts.append({'figure':name,'minimum_pt_at_6_5in':min(sizes)*468/width})
 # The spatial PDF has 468-pt width and its text is designed for full text width.
 assert re.search(r'\\includegraphics\s*\[\s*width\s*=\s*\\linewidth\s*\]\s*\{figures/walktime_context(?:\.pdf)?\}',tex)
 spatial_info=subprocess.check_output(['pdfinfo',str(spatial_pdf)],text=True);assert abs(float(re.search(r'Page size:\s+([0-9.]+)',spatial_info)[1])-468)<.01
 fonts.append({'figure':'walktime_context.pdf','minimum_pt_at_6_5in':spatial['min_text_size_at_6_5_in_pt']})
 pdf=B/'main.pdf';aux=(B/'main.aux').read_text();log=(B/'main.log').read_text();pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f')[:-1]
 def label(name):return int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 end=label('main-end');assert end==25 and len(pages)==label('LastPage')==27==end+2
 # Inspect rendered text by section, not merely the source macros used to generate it.
 def rendered(x):
  x=unicodedata.normalize('NFKC',x).replace('−','-').replace('–','-')
  x=re.sub(r'-\s*\n\s*','',x)
  return re.sub(r'\s+',' ',x).lower()
 summary=rendered(pages[0]);full=rendered(' '.join(pages));news=rendered(' '.join(pages[label('news-start')-1:label('news-end')]))
 assert 'recommend oslo under baseline weights and zurich under equal weights' in summary
 assert 'oslo is selected in all three scenarios under baseline weights' in summary
 assert 'equal weights select oslo, zurich and oslo' in summary
 assert 'oslo is the cautious recommendation under baseline and education-priority weights' in news
 assert 'zurich is selected when all ten measures receive equal weight' in news
 assert 'baseline weights select oslo in all three scenarios' in news
 assert 'zurich under living pressure' in news
 for phrase in ['626 on-street bus stop groups','replaces the earlier subset of 89 metro stations', 'rather than being added to it','supplied 2025 population', 'restoring the earlier subset selects zurich under both baseline and equal weights', 'largest possible shortfall', 'smallest such shortfall', 'not forecasts']:
  assert phrase in news,phrase
 assert 380 <= len(re.findall(r"[a-z]+(?:['’-][a-z]+)?|\d+", news)) <= 450

 for city in ['Zurich','Oslo','Singapore']:
  row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0];assert f'{100*row.minimax_recommendation_frequency:.2f}%' in summary
 for city in ['Zurich','Singapore','Stockholm']:
  assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}%" in full
 for value in ['4,271','4,440','169','23 of 37','15.606','0.648','28.10','40.50','0.14981']:assert value in full,value
 # An administrative all-mode alternative is distinct from the pure-bus primary.
 alternative=read(R/'results/current_transport_candidate/preview.json')
 for ref in ['fixed','equal']:
  row=next(v for v in alternative['comparisons'] if v['scenario']=='native_registry_roots' and v['weight_reference']==ref)
  assert row['count']==829 and row['recommendation']==['Oslo']
 assert all(x in full for x in ['626','829','89'])
 assert 'enturstop' in tex and '517' not in tex
 for phrase in ['pure on-street bus subset','native parent grouping','tveten bru entry is excluded','without a confirmed closure','2025 population of 727,797','replaces the earlier 89-station metro subset','two replacement bus groups','midtstuen bus group','or both retains oslo under baseline and zurich under equal weights','restoring the earlier 89 metro stations selects zurich under both weight sets']:
  assert phrase in full,phrase
 scenarios=read(R/'results/task4_user_v203_revision/summary.json')['results']
 for case in ['withhold_two_rail_replacement_stops','withhold_no_calls_Midtstuen_bus','withhold_all_three_service_flags']:
  for ref,winner in [('fixed','Oslo'),('equal','Zurich')]:
   row=next(x for x in scenarios if x['scenario']==case and x['weight_reference']==ref)
   assert row['minimax_choices']==[winner]
 for ref in ['fixed','equal']:
  row=next(x for x in scenarios if x['scenario']=='withdraw_Oslo_bus_refinement' and x['weight_reference']==ref)
  assert row['minimax_choices']==['Zurich']
 scope=read(R/'results/current_oslo_commute_scope/verification.json')
 assert scope['status'].startswith('PASS') and scope['science_bindings_unchanged']==548 and scope['independent_scalar_city_weight_cases']==64
 for source in scope['raw_responses']:assert sha(R/source['file'])==source['sha256'] and source['recorded_http_status']==200
 for source,digest in scope['source_sha256'].items():assert sha(R/source)==digest,source
 for source,digest in read(R/'results/current_oslo_commute_scope/summary.json')['source_sha256'].items():assert sha(R/source)==digest,source
 record=read(R/'data/current_oslo_travel2009/eurostat_NO001C_2009.json');indicator=record['dimension']['indic_ur']['category']['index']['TT1019V']
 assert record['value'][str(indicator)]==31 and record['dimension']['cities']['category']['label']['NO001C']=='Oslo (greater city)' and 'status' not in record
 sb=frame(R/'results/current_oslo_commute_scope/bounds.csv');sr=frame(R/'results/current_oslo_commute_scope/ranks.csv')
 for scenario in ['retained_V203','withdraw_Oslo_commute_proxy']:
  bl=sb[sb.scenario.eq(scenario)].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
  ll=bl.lower.to_numpy().reshape(16,10);hh=bl.upper.to_numpy().reshape(16,10);wanted=l.copy()
  if scenario=='withdraw_Oslo_commute_proxy':wanted[cities.index('Oslo'),NAMES.index('travel')]=0
  np.testing.assert_array_equal(ll,wanted);np.testing.assert_array_equal(hh,h)
  for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   aa,bb,rr=values(ll,hh,w);v=sr[sr.scenario.eq(scenario)&sr.weight_reference.eq(ref)].set_index('city').loc[cities]
   for col,arr in [('score_lower',aa),('score_upper',bb),('max_regret',rr)]:np.testing.assert_allclose(v[col],arr,atol=1e-11,rtol=0)
   expected=['Zurich'] if scenario=='withdraw_Oslo_commute_proxy' or ref=='equal' else ['Oslo']
   assert v.index[v.decision_rank.eq(1)].tolist()==expected and v.possible_champion.sum()==16 and v.necessary_champion.sum()==0
   row=next(x for x in scope['comparisons'] if x['scenario']==scenario and x['weight_reference']==ref)
   assert row['recommendation']==expected and row['possible_champions']==16 and row['necessary_champions']==0
 assert '31' in full and '2009' in full and 'greater city' in full
 assert 'commute proxy alone selects zurich under both' in summary
 assert 'work-commute proxy selects zurich under both weight sets' in news
 assert 'commute proxy alone selects zurich under both weights; all sixteen remain possible champions and none is necessary' in full
 assert 'matches establish neither the team' in full and 'nor the historical boundary' in full
 assert 'oslo' in summary and 'zurich' in summary and 'oslo' in news and 'zurich' in news
 # Figure labels and source limitations must survive actual typesetting.
 for phrase in ['99.18','99.97']:
  assert phrase in full,phrase
 figure_source=(R/'visuals/current_spatial/README.md').read_text().lower()
 for phrase in ['residents','not students','cloud','granule','30']:
  assert phrase in figure_source,phrase
 refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux));assert refs==current
 cited={k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',tex) for k in g.split(',')};assert cited<=refs,cited-refs
 nodes=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])).findall('.//{*}page');assert len(nodes)==len(pages)
 for i,node in enumerate(nodes):
  assert (float(node.get('width')),float(node.get('height')))==(612,792);words=node.findall('.//{*}word');assert not any(float(w.get('yMin'))>745 for w in words),(i,'footer')
  if i:
   top=[w for w in words if float(w.get('yMin'))<65];assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top) and any(w.text=='Page' and float(w.get('xMin'))>450 for w in top) and any(w.text=='18213' for w in top);assert f'Page {i+1} of {len(pages)}' in norm(pages[i])
  else:assert '18213' in pages[0]
 assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning'])
 result=dict(status='pass',scope='Independent local numeric, selected text, preservation and PDF geometry audit; excludes online compilation, visual review, source requalification and final team acceptance.',v203_bindings=len(snapshot['source_sha256']),inherited_v202_bindings=476,reference_keys=len(current),figure_minimum_fonts=fonts,mean_score_interval_widths=widths,main_and_reference_pages=end,total_pages=len(pages),actual_registration_verified=False,pdf_sha256=sha(pdf),main_sha256=sha(P/'main.tex'),oslo_source_scope_verification_sha256=sha(R/'results/current_oslo_commute_scope/verification.json'),oslo_source_scope_summary_sha256=sha(R/'results/current_oslo_commute_scope/summary.json'),oslo_eurostat_sha256=sha(R/'data/current_oslo_travel2009/eurostat_NO001C_2009.json'),spatial_audit_sha256=sha(R/'results/current_oslo_spatial_review/verification.json'),spatial_source_sha256={str(p.relative_to(R)):sha(p) for p in [R/'data/current_oslo_spatial/6494_hexes.zip',R/'data/current_oslo_spatial/download.json',R/'data/task4_access/city_index.json',R/'data/task4_access/9808_hexes.zip',R/'visuals/current_spatial/build.py',R/'visuals/current_spatial/render.py',R/'visuals/current_spatial/metrics.json',R/'visuals/current_spatial/imagery_manifest.json',R/'visuals/current_spatial/fallback_manifest.json',R/'visuals/current_spatial/oslo_imagery_manifest.json',R/'visuals/current_spatial/city_walktime.pdf']},assets_sha256={n:sha(P/'figures'/n) for n in ['identification_matrix.pdf','score_intervals.pdf']})
 O.mkdir(exist_ok=True);(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

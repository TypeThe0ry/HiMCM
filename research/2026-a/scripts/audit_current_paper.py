"""Independent audit of current local V202 paper; does not build or activate it."""
from pathlib import Path
import hashlib,json,re,subprocess,zlib,unicodedata,xml.etree.ElementTree as ET
import numpy as np,pandas as pd
from task4_user_v202_revision import revised_bounds
from task4_v5_model import NAMES,weights
from audit_task4_v193 import values,norm
R=Path(__file__).resolve().parents[1]; H=R.parents[1]; P=R.parents[2]/'HiMCM-Overleaf'; A=R/'results/current_paper_assets'; B=Path('/data/scratch/himcm-v202-current-build'); O=R/'results/current_paper_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def frame(p):return pd.read_csv(p,float_precision='round_trip')
def main():
 snapshot=read(R/'design/task4_user_v202_snapshot.json'); assert snapshot['bindings']==len(snapshot['source_sha256'])==476
 for n,h in snapshot['source_sha256'].items():assert sha(R/n)==h,n
 old=read(R/'results/task4_v202_transition/protection_snapshot.json'); assert len(old['v200_bindings'])==407
 for n,h in old['v200_bindings'].items():assert snapshot['source_sha256'][n]==h
 for n in ['ref.bib','mcmthesis.cls','figures/country_contrasts.pdf','figures/walktime_context.pdf']:
  p=P/n;assert sha(p)==old['protected_files'][str(p)],n
 tex=(P/'main.tex').read_text(); oldtex=subprocess.check_output(['git','-C',str(P),'show','HEAD:main.tex'],text=True)
 assert hashlib.sha256(oldtex.encode()).hexdigest()==old['protected_files'][str(P/'main.tex')]
 original=set(re.findall(r'\\bibitem\{([^}]+)\}',oldtex));current=set(re.findall(r'\\bibitem\{([^}]+)\}',tex)); assert len(original)==59 and original<current and len(current)==60,(len(original),len(current),current-original)
 assert re.search(r'tcn\s*=\s*18213',tex)
 ai='\\section*{Report on Use of AI Tools}'
 assert tex[tex.index(ai):]==oldtex[oldtex.index(ai):].replace('V200 primary','V202 primary').replace('V200 validation','V202 validation')
 from task4_v137_method_country import CASE_FILES
 for name in CASE_FILES:assert sha(R/'results/task4_v202_method'/name)==sha(R/'results/task4_v200_method'/name),name
 manifest=read(A/'manifest.json')
 for n,h in manifest['source_sha256'].items():assert sha(R/n)==h,n
 for n,h in manifest['output_sha256'].items():assert sha(A/n)==h,n
 for n in ['identification_matrix.pdf','score_intervals.pdf']:assert sha(P/'figures'/n)==sha(A/n),n
 for n in ['indicators.tex','preferences.tex','revision.tex','vintage_table.tex']:
  assert norm((A/n).read_text()) in norm(tex),n
 macros={m[1]:m[2] for line in tex.splitlines() if (m:=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line))}
 am={m[1]:m[2] for line in (A/'generated.tex').read_text().splitlines() if (m:=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line))}
 # Historical explanatory case wording is preserved in the manuscript rather than rewritten.
 dynamic=['CurrentMeanWidth','TotalWidthReduction','LatestEvidenceChange','RevisionRankChanges','SummaryWeightMC','MethodComparison','FutureDeterministic','FutureThresholds','FutureMonteCarlo','ProxyWithdrawalMC','PreferenceResults','PreferenceEvidenceChange','EvidenceThresholdCheck','MonteCarloInterpretation','MCBaseMeans','MCSettings','MCPairComparisons','MCCertifiedPairs','MCUnresolvedPairs','MCUniqueMinSettings','MCFrequencyHalfWidthPP','MCRankHalfWidth']
 for key in dynamic:assert macros[key]==am[key],key
 f,l,h=revised_bounds();cities=f.city.tolist();assert [int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())]==[112,37,11]
 ranks=frame(R/'results/task4_user_v202_revision/current_ranks.csv');widths={}
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  a,b,r=values(l,h,w);v=ranks[ranks.weight_reference.eq(ref)].set_index('city').loc[cities]
  for col,arr in [('score_lower',a),('score_upper',b),('max_regret',r)]:np.testing.assert_allclose(v[col],arr,atol=1e-11,rtol=0)
  assert v.index[v.decision_rank.eq(1)].tolist()==['Zurich'] and v.possible_champion.sum()==16 and v.necessary_champion.sum()==0
  widths[ref]=float(np.mean(b-a))
 assert macros['CurrentMeanWidth']==f"{widths['fixed']:.5f}"
 expected=ranks[ranks.weight_reference.eq('fixed')].set_index(['city','weight_reference']).sort_index();actual=frame(A/'source_intervals.csv').set_index(['city','weight_reference']).sort_index();pd.testing.assert_frame_equal(actual,expected,check_exact=True)
 for r in expected.sort_values('decision_rank').itertuples():assert f'{r.decision_rank} & {r.Index[0]} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f}' in tex,r.Index
 m=frame(A/'matrix.csv').set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
 np.testing.assert_allclose(m.utility_lower.to_numpy().reshape(16,10),l,rtol=0,atol=2e-16);np.testing.assert_allclose(m.utility_upper.to_numpy().reshape(16,10),h,rtol=0,atol=2e-16);assert m.state.value_counts().to_dict()=={'point':112,'partial':37,'unknown':11}
 pref=frame(R/'results/task4_v202_preferences/mc_city_summary.csv');k=pref[pref.concentration.eq(100)]
 for profile,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]:
  cells=[f"{100*float(k[k.profile.eq(profile)&k.city.eq(city)].iloc[0].minimax_recommendation_frequency):.2f}" for city in ['Zurich','Oslo','Singapore']];assert label+' & '+' & '.join(cells) in tex
 for city in ['Zurich','Oslo','Singapore']:
  row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0];assert f'{100*row.minimax_recommendation_frequency:.2f}' in macros['SummaryWeightMC'];assert f'{row.mean_decision_rank:.4f}' in macros['MonteCarloInterpretation']
 for key,val in [('MCBaseMeans','2064'),('MCSettings','37'),('MCPairComparisons','4440'),('MCCertifiedPairs','4260'),('MCUnresolvedPairs','180'),('MCUniqueMinSettings','18')]:assert macros[key].strip()==val
 future=read(R/'results/task4_v202_future/summary.json');thresholds={x['city']:x for x in future['thresholds'] if x['weight_reference']=='fixed'}
 for city in ['Oslo','Singapore','Stockholm']:assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}" in macros['FutureThresholds']
 assert f"{100*thresholds['Berlin']['required_cost_reduction_fraction']:.3f}" in macros['EvidenceThresholdCheck']
 for scenario in ['resource_expansion','living_pressure']:
  assert next(x for x in future['scenarios'] if x['evidence_arm']=='conditional' and x['scenario']==scenario and x['weight_reference']=='fixed')['minimax_choices']==['Singapore']
 assert 'resource expansion and living pressure select Singapore' in macros['FutureDeterministic']
 mc=frame(R/'results/task4_v202_future/future_mc_city_summary.csv')
 for arm,macro in [('conditional','FutureMonteCarlo'),('withdraw_historical_stage_proxy','ProxyWithdrawalMC')]:
  for scenario in ['resource_expansion','living_pressure','balanced_improvement']:
   row=mc[mc.weight_reference.eq('fixed')&mc.city.eq('Zurich')&mc.evidence_arm.eq(arm)&mc.scenario.eq(scenario)].iloc[0];assert f'{100*row.recommendation_frequency:.2f}' in macros[macro]
 vintage=read(R/'results/task4_v202_diagnostics/summary.json')['vintage_cases'];vintage={(x['scenario'],x['weight_reference']):x for x in vintage}
 for sc,label in [('baseline','Retained input'),('pre2020_points','Before 2020'),('after2025_points','After 2025'),('non_ok_points','Non-ok flags'),('union_points','Union')]:
  assert f"{label} & {vintage[sc,'fixed']['withdrawn_point_cells']} & {'/'.join(vintage[sc,'fixed']['minimax_choices'])} & {'/'.join(vintage[sc,'equal']['minimax_choices'])} & {vintage[sc,'fixed']['mean_interval_width']:.2f}" in tex
 for city in ['Zurich','Oslo']:
  row=ranks[ranks.weight_reference.eq('fixed')].set_index('city').loc[city];assert f"{row.score_lower:.5f}" in tex and f"{row.max_regret:.5f}" in tex
 n=norm(tex)
 for phrase in ['25 Singapore venues','OCBC Aquatic Centre','withholding them leaves 23','withholding OCBC leaves 22','ages 16 and above','for all ages','Tuesday maintenance','5--28 December','2024 population of 6,036,900','inventory date is unstated']:
  assert phrase in n,phrase
 for value in ['0.23330','0.26325','0.23842','0.20848','0.42205','63.44548','40.07 minutes']:assert value in n,value
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
 pdf=B/'main.pdf';aux=(B/'main.aux').read_text();log=(B/'main.log').read_text();pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f')[:-1]
 def label(name):return int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 end=label('main-end');assert end<=25 and len(pages)==label('LastPage')==end+2
 # Inspect rendered text by section, not merely the source macros used to generate it.
 def rendered(x):
  x=unicodedata.normalize('NFKC',x).replace('−','-').replace('–','-')
  x=re.sub(r'-\s*\n\s*','',x)
  return re.sub(r'\s+',' ',x).lower()
 summary=rendered(pages[0]);full=rendered(' '.join(pages));news=rendered(' '.join(pages)[(' '.join(pages)).index('Scenarios for planning'):])
 assert 'resource expansion and living pressure' in summary and 'singapore is selected under baseline weights' in summary and 'balanced improvement retains zurich' in summary
 assert 'resource expansion and living pressure select singapore' in full and 'balanced improvement retains zurich' in full and 'equal weights retain zurich in all three scenarios' in full
 assert 'resource expansion and living pressure select singapore under baseline priorities' in news and 'zurich remains the recommendation for balanced improvement and under equal priorities' in news
 for stale in ['resource expansion selects singapore; living pressure and balanced improvement retain zurich','resource expansion selects singapore under baseline priorities; living pressure and balanced improvement retain zurich']:
  assert stale not in full,stale
 for city in ['Zurich','Oslo','Singapore']:
  row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0];assert f'{100*row.minimax_recommendation_frequency:.2f}%' in summary
 for city in ['Singapore','Oslo','Stockholm']:
  assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}%" in full
 for scenario in ['resource_expansion','living_pressure','balanced_improvement']:
  row=mc[mc.weight_reference.eq('fixed')&mc.city.eq('Zurich')&mc.evidence_arm.eq('conditional')&mc.scenario.eq(scenario)].iloc[0];assert f'{100*row.recommendation_frequency:.2f}%' in full
 for value in ['4,260','4,440','180 unresolved','18 of 37','0.42205%','63.44548%','40.07 minutes']:assert value in full,value
 refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux));assert refs==current
 cited={k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',tex) for k in g.split(',')};assert cited<=refs,cited-refs
 nodes=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])).findall('.//{*}page');assert len(nodes)==len(pages)
 for i,node in enumerate(nodes):
  assert (float(node.get('width')),float(node.get('height')))==(612,792);words=node.findall('.//{*}word');assert not any(float(w.get('yMin'))>745 for w in words),(i,'footer')
  if i:
   top=[w for w in words if float(w.get('yMin'))<65];assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top) and any(w.text=='Page' and float(w.get('xMin'))>450 for w in top) and any(w.text=='18213' for w in top);assert f'Page {i+1} of {len(pages)}' in norm(pages[i])
  else:assert '18213' in pages[0]
 assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning'])
 result=dict(status='pass',scope='Independent local numerical, selected text, preservation, and PDF geometry audit; excludes server compilation, visual review, independent requalification of sources and final team acceptance.',v202_bindings=476,inherited_v200_bindings=407,rendered_summary_method_and_news_scenarios_checked=True,rendered_mc_and_threshold_values_checked=True,reference_keys=len(current),new_reference_keys=sorted(current-original),figure_minimum_fonts=fonts,mean_score_interval_widths=widths,main_and_reference_pages=end,total_pages=len(pages),actual_registration_verified=False,pdf_sha256=sha(pdf),main_sha256=sha(P/'main.tex'),assets_sha256={n:sha(P/'figures'/n) for n in ['identification_matrix.pdf','score_intervals.pdf']})
 O.mkdir(exist_ok=True);(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

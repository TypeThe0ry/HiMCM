"""Independent selected numerical, content, preservation and PDF audit of V201.

Visual review, online compilation, and scientific validity of underlying sources are separate.
"""
from pathlib import Path
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET,zlib
import numpy as np
import pandas as pd
from task4_user_v200_revision import revised_bounds
from task4_v5_model import NAMES,weights
from audit_task4_v193 import graph,norm,values
R=Path(__file__).resolve().parents[1]; P=R.parents[2]/'HiMCM-Overleaf'; D=P/'drafts'; O=R/'results/task4_v201_review'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def frame(p): return pd.read_csv(p,float_precision='round_trip')
def main():
 protected=read(O/'protection_snapshot.json')
 for name,digest in protected.items(): assert sha(P/name)==digest,name
 proof=read(R/'results/task4_v200_transition/verification.json'); assert proof['status']=='pass'
 for group in ('source_sha256','result_sha256'):
  for name,digest in proof[group].items(): assert sha(R/name)==digest,name
 f,l,h=revised_bounds(); assert l.shape==(16,10)
 assert [int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())]==[112,37,11]
 ranks=frame(R/'results/task4_user_v200_revision/current_ranks.csv'); widths={}
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  a,b,r=values(l,h,w); v=ranks[ranks.weight_reference.eq(ref)].set_index('city').loc[f.city.tolist()]
  for col,arr in [('score_lower',a),('score_upper',b),('max_regret',r)]: np.testing.assert_allclose(v[col],arr,atol=1e-11,rtol=0)
  assert v.index[v.decision_rank.eq(1)].tolist()==['Zurich']; assert v.possible_champion.sum()==16 and v.necessary_champion.sum()==0
  widths[ref]=float(np.mean(b-a))
 A=D/'task4_v201_assets'; actual=frame(A/'source_intervals.csv').set_index(['city','weight_reference']).sort_index(); expected=ranks[ranks.weight_reference.eq('fixed')].set_index(['city','weight_reference']).sort_index(); pd.testing.assert_frame_equal(actual,expected,check_exact=True)
 table=(A/'baseline.tex').read_text()
 for r in expected.sort_values('decision_rank').itertuples(): assert f'{r.decision_rank} & {r.Index[0]} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f}' in table,r.Index
 matrix=list(D.glob('task4_v201*assets/matrix.csv')); assert len(matrix)==1,matrix
 m=frame(matrix[0]).set_index(['city','indicator']).loc[pd.MultiIndex.from_product([f.city.tolist(),NAMES])]
 np.testing.assert_allclose(m.utility_lower.to_numpy().reshape(16,10),l,rtol=0,atol=2e-16); np.testing.assert_allclose(m.utility_upper.to_numpy().reshape(16,10),h,rtol=0,atol=2e-16)
 assert m.state.value_counts().to_dict()=={'point':112,'partial':37,'unknown':11}
 fm=read(matrix[0].parent/'figure_manifest.json'); assert fm['matrix_sha256']==sha(matrix[0])
 for ext,digest in fm['output_sha256'].items(): assert sha(matrix[0].parent/('identification_matrix.'+ext))==digest
 fonts=[]
 for pdf in [matrix[0].parent/'identification_matrix.pdf',A/'score_intervals.pdf']:
  sizes=[]
  for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',pdf.read_bytes(),re.S):
   try: raw=zlib.decompress(stream)
   except zlib.error: continue
   sizes.extend(float(x) for x in re.findall(rb'/\w+\s+([0-9.]+)\s+Tf',raw))
  width=float(re.search(r'Page size:\s+([0-9.]+)',subprocess.check_output(['pdfinfo',str(pdf)],text=True))[1]); assert sizes and min(sizes)*468/width>=9,(pdf,sizes,width)
  fonts.append({'asset':str(pdf.relative_to(P)),'minimum_pt_at_6_5_in':min(sizes)*468/width})
 manifest=read(A/'manifest.json')
 for group,base in [('source_sha256',R),('paper_input_sha256',P),('output_sha256',P)]:
  for name,digest in manifest.get(group,{}).items(): assert sha(base/name)==digest,(group,name)
 macros={m[1]:m[2] for line in (D/'task4_v201_generated.tex').read_text().splitlines() if (m:=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line))}
 assert macros['CurrentMeanWidth']==f"{widths['fixed']:.5f}"
 summary=read(R/'results/task4_user_v200_revision/summary.json'); prev=next(x for x in summary['results'] if x['scenario']=='before_V197' and x['weight_reference']=='fixed'); assert f"{prev['mean_width']:.5f}" in macros['LatestEvidenceChange']
 pref=frame(R/'results/task4_v200_preferences/mc_city_summary.csv'); k=pref[pref.concentration.eq(100)]
 for profile,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]:
  cells=[f"{100*float(k[k.profile.eq(profile)&k.city.eq(city)].iloc[0].minimax_recommendation_frequency):.2f}" for city in ['Zurich','Oslo','Singapore']]; assert label+' & '+' & '.join(cells) in (A/'preferences.tex').read_text()
 for city in ['Zurich','Oslo','Singapore']:
  row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0]; assert f'{100*row.minimax_recommendation_frequency:.2f}' in macros['SummaryWeightMC']; assert f'{row.mean_decision_rank:.4f}' in macros['MonteCarloInterpretation']
 for key,val in [('MCBaseMeans','2064'),('MCSettings','37'),('MCPairComparisons','4440'),('MCCertifiedPairs','4259'),('MCUnresolvedPairs','181'),('MCUniqueMinSettings','17')]: assert macros[key].strip()==val
 future=read(R/'results/task4_v200_future/summary.json'); thresholds={x['city']:x for x in future['thresholds'] if x['weight_reference']=='fixed'}
 for city in ['Oslo','Singapore','Stockholm']: assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}" in macros['FutureThresholds']
 assert f"{100*thresholds['Berlin']['required_cost_reduction_fraction']:.3f}" in macros['EvidenceThresholdCheck']
 assert next(x for x in future['scenarios'] if x['evidence_arm']=='conditional' and x['scenario']=='resource_expansion' and x['weight_reference']=='fixed')['minimax_choices']==['Singapore']; assert 'resource expansion selects Singapore' in macros['FutureDeterministic']
 mc=frame(R/'results/task4_v200_future/future_mc_city_summary.csv')
 for arm,macro in [('conditional','FutureMonteCarlo'),('withdraw_historical_stage_proxy','ProxyWithdrawalMC')]:
  for scenario in ['resource_expansion','living_pressure','balanced_improvement']:
   row=mc[mc.weight_reference.eq('fixed')&mc.city.eq('Zurich')&mc.evidence_arm.eq(arm)&mc.scenario.eq(scenario)].iloc[0]; assert f'{100*row.recommendation_frequency:.2f}' in macros[macro]
 vintage=read(R/'results/task4_v200_diagnostics/summary.json')['vintage_cases']; vintage={(x['scenario'],x['weight_reference']):x for x in vintage}; vt=(A/'vintage_table.tex').read_text()
 for sc,label in [('baseline','Retained input'),('pre2020_points','Before 2020'),('after2025_points','After 2025'),('non_ok_points','Non-ok flags'),('union_points','Union')]:
  assert f"{label} & {vintage[sc,'fixed']['withdrawn_point_cells']} & {'/'.join(vintage[sc,'fixed']['minimax_choices'])} & {'/'.join(vintage[sc,'equal']['minimax_choices'])} & {vintage[sc,'fixed']['mean_interval_width']:.2f}" in vt
 sources=graph(D/'task4_v201_paper.tex'); text='\n'.join(p.read_text() for p in sorted(sources)); n=norm(text)
 assert 'tcn=18213' in (D/'task4_v201_paper.tex').read_text()
 for x in ['112 points, 37 partial intervals and 11 fully unknown','1.57080','63.44548'] : assert x in n,x
 assert not any(x in n for x in ['13.01105','education priority selects Oslo'])
 core=norm((D/'task4_v201_core.tex').read_text()); front=norm((D/'task4_v201_front.tex').read_text()); vintage_text=norm((D/'task4_v201_vintage.tex').read_text())
 fixed=ranks[ranks.weight_reference.eq('fixed')].set_index('city')
 for city in ['Zurich','Oslo']:
  assert f"{fixed.loc[city,'score_lower']:.5f}" in core and f"{fixed.loc[city,'max_regret']:.5f}" in core
 for x in ['25 Singapore venues','four pool-specific temporary notices affect three venues','those three venues leaves 22','not currently open pools or teen access']: assert x in core,x
 for x in ['education emphasis selects Singapore','all sixteen remain possible champions','resource expansion selects Singapore']: assert x in front,x
 for x in ['at it Singapore (baseline) or Oslo (equal) can tie','above it a counterexample exists']: assert x in vintage_text,x
 assert 'language fit' in front and 'one main quality score' in front
 assert (D/'task4_v201_ai.tex').read_text()==(D/'task4_v198_ai.tex').read_text().replace('V197 primary','V200 primary').replace('V197 validation','V200 validation')
 old=(D/'task4_v198_references.tex').read_text(); new=(D/'task4_v201_references.tex').read_text(); assert set(re.findall(r'\\bibitem\{([^}]+)\}',new))==set(re.findall(r'\\bibitem\{([^}]+)\}',old))|{'sgpool_directory'}
 pdf=D/'task4_v201_paper.pdf'; pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f')[:-1]; aux=Path('/data/scratch/himcm_v201_build/task4_v201_paper.aux').read_text()
 def label(name): return int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 end=label('main-end'); assert end<=25 and len(pages)==label('LastPage')==end+2
 for heading in ['Introduction and decision scope','Assumptions and their role','Notation','Data collection and comparability','Establishing the baseline evaluation model','Model revision and extension','Comparing cities within the same country','Conclusion and decision use','News article','References','Report on Use of AI Tools']:
  assert heading in norm(pages[1]),heading
 assert re.search(r'5\s+Establishing the baseline evaluation model',pages[1]) and re.search(r'6\s+Model revision and extension',pages[1])
 refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux)); assert len(refs)==57; cited={k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',text) for k in g.split(',')}; assert cited<=refs,cited-refs
 nodes=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])).findall('.//{*}page'); assert len(nodes)==len(pages)
 for i,node in enumerate(nodes):
  assert (float(node.get('width')),float(node.get('height')))==(612,792); words=node.findall('.//{*}word'); assert not any(float(w.get('yMin'))>745 for w in words),('footer',i+1)
  if i:
   top=[w for w in words if float(w.get('yMin'))<65]; assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top) and any(w.text=='Page' and float(w.get('xMin'))>450 for w in top); assert any(w.text=='18213' for w in top) and f'Page {i+1} of {len(pages)}' in norm(pages[i])
  else: assert '18213' in pages[0]
 log=Path('/data/scratch/himcm_v201_build/task4_v201_paper.log').read_text(); assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning'])
 assert pages==subprocess.check_output(['pdftotext','-layout','/data/scratch/himcm_v201_build/task4_v201_paper.pdf','-'],text=True).split('\f')[:-1]
 result=dict(version='V201',status='pass',scope='Independent selected numeric, content, protected-file and PDF geometry audit; not exhaustive prose/source quality, visual review or final team acceptance.',protected_files=len(protected),V200_bound_files=sum(len(proof[x]) for x in ('source_sha256','result_sha256')),point_partial_unknown=[112,37,11],mean_score_interval_widths=widths,figure_minimum_inserted_fonts=fonts,AI_window_frozen=True,reference_keys=57,actual_registration_verified=False,submission_ready=False,server_compile_verified=False,underfull_counts=[log.count('Underfull')],direct_rebuild_text_equal=True,total_pages=len(pages),main_and_references_pages=end,pdf_sha256=sha(pdf),tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(sources)})
 O.mkdir(exist_ok=True); (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__':main()

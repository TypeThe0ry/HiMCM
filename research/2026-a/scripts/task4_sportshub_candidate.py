"""Isolated preview of one deduplicated public venue; active V200 stays unchanged."""
from pathlib import Path
import hashlib,json,re
import numpy as np
import pandas as pd
from task4_user_v200_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT,NAMES,weights
from audit_current_priority import scalar_scores,decision
from audit_current_collection import text
O=ROOT/'results/current_sportshub_candidate';D=ROOT/'data/current_sg_sportshub'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 candidate=json.loads((D/'candidate.json').read_text());assert candidate['candidate_physical_venues']==1
 bindings={n:sha(ROOT/n) for n in ['design/task4_user_current_model.json','design/task4_user_current_extensions.json','design/task4_user_current_review.json','design/task4_user_current_delivery.json']}
 for name in ['venue','swimming']:
  m=json.loads((D/(name+'.html.json')).read_text());p=D/(name+'.html')
  assert m['http_status']==200 and p.stat().st_size==m['bytes'] and sha(p)==m['sha256']
 venue=text(D/'venue.html');swim=text(D/'swimming.html')
 assert all(s in venue for s in ['7 Stadium Drive','397632','general public','competition and training pools open for public swimming'])
 assert all(s in swim for s in ['Per entry rates','Child (under 18 years old)','all ages','16','Tuesdays','5 to 28 December 2026'])
 old=json.loads((ROOT/'data/task4_v199_sgpool/venues.json').read_text())['venues'];assert len(old)==len({x['postal_code'] for x in old})==25
 for x in old:
  assert x['postal_code']!='397632' and 'ocbc' not in x['name'].lower()
  assert '7stadiumdrive' not in re.sub(r'[^a-z0-9]','',x['address'].lower())
 _,lo,hi=revised_bounds();initial=np.stack([lo,hi]).copy();f,_,_=revised_bounds();cities=f.city.tolist();i=cities.index('Singapore');j=NAMES.index('public_pool_density');pop=int(f.iloc[i].population)
 assert pop==6036900 and int(f.iloc[i].population_year)==2024
 rows=[];summaries=[]
 for label,n in [('active_V200_25',25),('candidate_inventory26',26),('withdraw_new_venue25',25),('withhold4_notice_venues22',22)]:
  a=lo.copy();density=n*100000/pop;a[i,j]=density/(1+density)
  mask=np.ones((16,10),bool);mask[i,j]=False;np.testing.assert_array_equal(a[mask],lo[mask])
  if n==25:np.testing.assert_array_equal(a,lo)
  for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   t=evaluate(cities,a,hi,w);L,U=scalar_scores(a,w),scalar_scores(hi,w);regret,risk,possible,choices=decision(L,U)
   for key,x in [('score_lower',L),('score_upper',U),('max_regret',regret)]:np.testing.assert_allclose(t[key],x,rtol=0,atol=3e-13)
   assert t.possible_champion.tolist()==possible.tolist()
   summaries.append(dict(scenario=label,count=n,weight_reference=ref,utility_lower=float(a[i,j]),mean_score_width=float((U-L).mean()),conservative_recommendation=[cities[k] for k in choices],possible_champions=int(possible.sum()),necessary_champions=int(t.necessary_champion.sum()),Singapore_regret_gap_to_best_other=float(regret[i]-np.delete(regret,i).min())))
   rows.append(t.assign(scenario=label,weight_reference=ref))
 _,a,b=revised_bounds();np.testing.assert_array_equal(initial,np.stack([a,b]))
 for n,h in bindings.items():assert sha(ROOT/n)==h,n
 for n,h in json.loads((ROOT/'design/task4_user_v200_snapshot.json').read_text())['source_sha256'].items():assert sha(ROOT/n)==h,n
 O.mkdir(exist_ok=True);pd.concat(rows,ignore_index=True).to_csv(O/'scores.csv',index=False)
 report=dict(status='verified_isolated_preview_not_admitted',active_science='V200 unchanged',candidate_physical_venues=1,candidate_combined_count=26,active_count=25,primary_admissions=0,actual_active_score_width_reduction=0,population=pop,population_year=2024,source_capture_date='2026-11-10',inventory_reference_date=None,semantics='One physical venue includes several basins; public individual-entry prices support a physical public-venue subset, not universal adolescent use or current opening.',restrictions=candidate['restrictions_and_closures'],failed_conditions_pdf_does_not_negate_two_successful_pages=True,withholding_scope='Withhold old3 pool-notice venues plus new OCBC notice venue;22 is not an all-open count or assertion of four complete closures.',other159cells_all_uppers_and_originals_preserved=True,independent_scalar_city_weight_cases=128,summaries=summaries,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),D/'candidate.json',D/'venue.html',D/'venue.html.json',D/'swimming.html',D/'swimming.html.json',D/'conditions.pdf.json',ROOT/'data/task4_v199_sgpool/venues.json',ROOT/'design/task4_user_v200_snapshot.json']})
 (O/'preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()

"""Isolated inventory and notice-withholding previews; no active data admission."""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_user_v197_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT,NAMES,weights
from audit_task4_v199_priority import scalar_scores,decision
O=ROOT/'results/task4_v199_priority'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=ROOT/'data/task4_v199_sgpool';listing=json.loads((source/'venues.json').read_text());counts=json.loads((source/'candidate_count.json').read_text());detail=json.loads((source/'detail_verification.json').read_text())
 rows=listing['venues'];assert len(rows)==len({r['postal_code'] for r in rows})==25
 assert counts['identity_verified_count']==25 and counts['current_open_access_confirmed_count']==0
 withheld={r['provider_id'] for r in counts['nonweekly_closure_record_keys']};assert withheld=={'clementi-swimming-complex','jurong-east-swimming-complex','katong-swimming-complex'}
 assert len(detail['pages'])==25 and all(all(r['identity_check'][k] for k in ['name_matches_catalog','address_matches_catalog','postal_code_matches_catalog']) for r in detail['pages'])
 f,lo,hi=revised_bounds();initial=np.stack([lo,hi]).copy();cities=f.city.tolist();i=cities.index('Singapore');j=NAMES.index('public_pool_density');pop=int(f.iloc[i].population);assert pop==6036900
 assert int(f.iloc[i].population_year)==2024 and pd.isna(f.iloc[i].pools_per_100k)
 out=[];summaries=[]
 for label,n in [('retained_V197',7),('inventory25_partial_closure_flags',25),('withhold3_notice_venues22',22)]:
  a=lo.copy();density=n*100000/pop;a[i,j]=density/(1+density)
  mask=np.ones((16,10),bool);mask[i,j]=False;np.testing.assert_array_equal(a[mask],lo[mask])
  if n==7:np.testing.assert_allclose(a,lo,atol=1e-16,rtol=0)
  for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   t=evaluate(cities,a,hi,w);L,U=scalar_scores(a,w),scalar_scores(hi,w);regret,risk,possible,choices=decision(L,U)
   for k,x in [('score_lower',L),('score_upper',U),('max_regret',regret)]:np.testing.assert_allclose(t[k],x,rtol=0,atol=3e-13)
   assert t.possible_champion.tolist()==possible.tolist()
   r=dict(scenario=label,weight_reference=ref,count=n,utility_lower=float(a[i,j]),mean_score_width=float((U-L).mean()),minimax_regret=risk,Singapore_regret_gap_to_best_other=float(regret[i]-np.delete(regret,i).min()),conservative_recommendation=';'.join(cities[k] for k in choices),possible_count=int(t.possible_champion.sum()),necessary_count=int(t.necessary_champion.sum()))
   summaries.append(r);out.append(t.assign(scenario=label,weight_reference=ref))
 _,a,b=revised_bounds();np.testing.assert_array_equal(initial,np.stack([a,b]))
 pd.concat(out,ignore_index=True).to_csv(O/'candidate_scores.csv',index=False)
 report=dict(status='preview_only_not_admitted',base_science='V197 unchanged',paper='V198 unchanged',population_retained=pop,population_year_retained=2024,source_capture='2026-11-10',source_inventory_reference_date='unstated;8Nov2026isdisplayedpageupdatemetadata',catalog_count=25,withheld_pool_specific_notice_venues=sorted(withheld),summaries=summaries,other159cells_alluppers_and_weights_unchanged=True,primary_admissions=0,actual_active_model_width_reduction=0,scope='Physical public-venue inventory and separate sensitivity withholding three venues with basin-specific notices. Neither arm establishes a current-open/access count; withholding does not label those whole venues closed. No union with historical article, 2025 census, personal accessibility or winner probability.',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),source/'venues.json',source/'candidate_count.json',source/'detail_verification.json',ROOT/'design/task4_user_v197_snapshot.json']})
 (O/'candidate_preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()

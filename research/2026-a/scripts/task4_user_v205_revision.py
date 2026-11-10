"""Staged Prague source-defined bus-node refinement; current V204 stays active."""
from pathlib import Path
from functools import lru_cache
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v204_revision import revised_bounds as previous_bounds
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,SPEC,weights
from task4_ahp_mc_baseline import score_many,interval_metrics,rank_metrics
OUT=ROOT/'results/task4_user_v205_revision'
MANIFEST=ROOT/'design/task4_user_v205_admissions.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@lru_cache(maxsize=1)
def admission():
 m=json.loads(MANIFEST.read_text());assert m['version']=='V205' and m['activation_status']=='staged_not_active'
 assert m['input_sha256']==sha(SOURCE)
 for name,h in m['source_hashes'].items():assert sha(ROOT/name)==h,name
 obs=m['observations'][0];assert len(m['observations'])==1
 for name,v in dict(city='Prague',indicator='public_transport_density',raw_count_before=57,raw_count=942,population=1407084,population_year=2025,anchor=50,service_day='20261110',counts_not_added=True,public_request_stop_condition_retained=True,actual_operation_verified=False).items():assert obs[name]==v,name
 w=pd.read_csv(ROOT/m['public_witnesses'],dtype=str,keep_default_na=False)
 ordinary=pd.read_csv(ROOT/m['ordinary_witnesses'],dtype=str,keep_default_na=False)
 assert len(w)==w.node.nunique()==942 and len(ordinary)==ordinary.node.nunique()==50
 assert set(ordinary.node)<=set(w.node) and set(obs['native_node_ids'])==set(w.node)
 assert w.gtfs_zone_region_type.eq('1').all() and w.gtfs_location_type.eq('0').all()
 assert w.route_type.eq('3').all() and w.route_is_night.eq('0').all() and w.route_is_substitute_transport.eq('0').all() and w.trip_operation_type.eq('1').all()
 access=w[['pickup_type','drop_off_type']].agg(tuple,axis=1)
 assert access.value_counts().to_dict()=={('3','3'):892,('0','0'):50}
 assert set(w.loc[access.map(lambda x:x==('0','0')),'node'])==set(ordinary.node)
 assert set(m['request_only_node_ids'])==set(w.node)-set(ordinary.node)
 return m,w,ordinary

def revised_bounds(include_prague_bus=True,withhold_prague_request_stops=False,**kwargs):
 f,lo,hi=previous_bounds(**kwargs);old=lo.copy();oldhi=hi.copy()
 if withhold_prague_request_stops and not include_prague_bus:raise ValueError('Request withholding requires Prague candidate')
 if include_prague_bus:
  m,w,ordinary=admission();i=f.city.tolist().index('Prague');j=NAMES.index('public_transport_density')
  assert f.iloc[i].population==1407084 and f.iloc[i].population_year==2025 and SPEC[j][2]==50 and hi[i,j]==1
  # The retained independent metro subset remains available. Never add the two.
  count=max(57,len(ordinary)) if withhold_prague_request_stops else len(w)
  density=count*100000/1407084;lo[i,j]=density/(50+density)
  mask=np.ones(lo.shape,bool);mask[i,j]=False
  np.testing.assert_array_equal(lo[mask],old[mask]);assert lo[i,j]>=old[i,j]
 np.testing.assert_array_equal(hi,oldhi)
 return f,lo,hi

def controlled_cases():
 f,old,hi=previous_bounds();_,lo,newhi=revised_bounds();cities=f.city.tolist();i=cities.index('Prague');j=NAMES.index('public_transport_density')
 np.testing.assert_array_equal(hi,newhi)
 cases=[('before_V204',old,hi),('after_conditional',lo,hi),('withdraw_Prague_bus_refinement',*revised_bounds(include_prague_bus=False)[1:]),('withhold_Prague_request_stop_witnesses',*revised_bounds(withhold_prague_request_stops=True)[1:])]
 prior=pd.read_csv(ROOT/'results/task4_user_v204_revision/utility_bounds.csv')
 for label in prior.scenario.unique():
  if label in ('before_V203','after_conditional'):continue
  a=prior.loc[prior.scenario.eq(label)].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
  lower=a.lower.to_numpy().reshape(16,10).copy();upper=a.upper.to_numpy().reshape(16,10).copy()
  lower[i,j]=lo[i,j];cases.append((label,lower,upper))
 assert len(cases)==len({x[0] for x in cases})==31
 return f,cases

def main():
 if OUT.exists():raise ValueError('Preserve staged output; use a fresh scratch checkout')
 m,w,ordinary=admission();f,cases=controlled_cases();cities=f.city.tolist();ranks=[];bounds=[];mc=[];summaries=[]
 for label,a,b in cases:
  for ref,weight in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   t=evaluate(cities,a,b,weight);ranks.append(t.assign(scenario=label,weight_reference=ref));summaries.append(dict(scenario=label,weight_reference=ref,choices=t.loc[t.decision_rank.eq(1),'city'].tolist(),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),mean_width=float((t.score_upper-t.score_lower).mean())))
  bounds.extend(dict(scenario=label,city=c,indicator=n,lower=a[i,j],upper=b[i,j]) for i,c in enumerate(cities) for j,n in enumerate(NAMES))
 for ref,center in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  for concentration in [20,100,500]:
   draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*center,10000)
   for label,a,b in cases:
    regret,possible,_,_,_=interval_metrics(score_many(a,draws),score_many(b,draws));rank,recommended,_=rank_metrics(regret,descending=False)
    mc.extend(dict(scenario=label,weight_reference=ref,concentration=concentration,city=c,minimax_recommendation_frequency=float(recommended[:,i].mean()),mean_decision_rank=float(rank[:,i].mean()),possible_champion_frequency=float(possible[:,i].mean())) for i,c in enumerate(cities))
   print('V205 primary',ref,concentration,'complete',flush=True)
 OUT.mkdir(parents=True);table=pd.concat(ranks,ignore_index=True);table.to_csv(OUT/'all_ranks.csv',index=False);table.loc[table.scenario.eq('after_conditional')].to_csv(OUT/'current_ranks.csv',index=False);pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False);pd.DataFrame(mc).to_csv(OUT/'mc_city_summary.csv',index=False)
 _,lo,hi=revised_bounds()
 report=dict(version='V205',activation_status='staged_not_active',current_active_primary='V204',results=summaries,primary_cases=len(cases),primary_mc_settings=len(cases)*6,draws_per_setting=10000,mc_seed=20261108,changed_cells=1,other159_lower_and_all160_upper_preserved=True,point_cells=int((lo==hi).sum()),partial_cells=int(((hi>lo)&(hi-lo<1)).sum()),fully_missing_cells=int(((hi-lo)==1).sum()),input_sha256=sha(SOURCE),admissions_sha256=sha(MANIFEST),source_defined_nodes=942,ordinary_nodes=50,additional_request_nodes=892,request_withhold_retained_lower_count=57,primary_admissions=0,actual_primary_width_reduction=0,changes_current_primary=False,changes_manuscript=False,scope='Qualified scheduled source-defined bus nodes, service day20261110, 2025 submitted population. Driver-request public-stop policy remains a condition, not universal or actual operation. Request-withdrawal arm retains the independent57metro lower bound; counts never added. Frozen V204 controls carried forward with only Prague lower refined;31cases/186pairedweightMCsettings. Conditional simulation frequencies are not empirical win probabilities. Scientific staging is not activation or paper delivery.')
 (OUT/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print('V205 primary staging complete',len(cases),'cases',flush=True)
if __name__=='__main__':main()

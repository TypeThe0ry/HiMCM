"""Isolated source-defined Oslo bus-stop subset; original values/rules unchanged."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v202_revision import revised_bounds as previous_bounds
from task4_user_v136_revision import without_historical_proxy
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,SPEC,weights
from task4_ahp_mc_baseline import score_many,interval_metrics,rank_metrics
OUT=ROOT/'results/task4_user_v203_revision';MANIFEST=ROOT/'design/task4_user_v203_admissions.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def revised_bounds(include_oslo_bus=True,include_sportshub=True,include_sg_pool=True,include_zurich_pool=True,include_tokyo=True,include_warsaw=True,withhold_notice_venues=False,withhold_existing_notice_venues=False,withhold_rail_replacement=False,withhold_no_calls_bus=False,include_questioned_stop=False):
 f,lo,hi=previous_bounds(include_sportshub=include_sportshub,include_sg_pool=include_sg_pool,include_zurich_pool=include_zurich_pool,include_tokyo=include_tokyo,include_warsaw=include_warsaw,withhold_notice_venues=withhold_notice_venues,withhold_existing_notice_venues=withhold_existing_notice_venues)
 before=np.stack([lo,hi]).copy();m=json.loads(MANIFEST.read_text());assert sha(SOURCE)==m['input_sha256']
 for n,h in m['source_hashes'].items():assert sha(ROOT/n)==h,n
 row=m['observations'][0];i=f.city.tolist().index('Oslo');j=NAMES.index('public_transport_density')
 assert row['raw_count_before']==89 and row['raw_count']==len(set(row['native_root_ids']))==626
 assert f.iloc[i].population==row['population']==727797 and f.iloc[i].population_year==row['population_year']==2025
 assert hi[i,j]==1 and SPEC[j][2]==50
 if any([withhold_rail_replacement,withhold_no_calls_bus,include_questioned_stop]):assert include_oslo_bus
 if include_oslo_bus:
  n=626-2*int(withhold_rail_replacement)-int(withhold_no_calls_bus)+int(include_questioned_stop)
  density=n*100000/row['population'];lo[i,j]=density/(SPEC[j][2]+density)
 mask=np.ones((16,10),bool);mask[i,j]=False
 np.testing.assert_array_equal(np.stack([lo,hi])[:,mask],before[:,mask]);np.testing.assert_array_equal(hi,before[1])
 return f,lo,hi

def main():
 OUT.mkdir(exist_ok=True);f,l0,h0=previous_bounds();_,lo,hi=revised_bounds();cities=f.city.tolist()
 _,without_new,_=revised_bounds(False);np.testing.assert_array_equal(without_new,l0)
 def lower(**kwargs):return revised_bounds(**kwargs)[1]
 amsterdam=lo.copy();amsterdam[cities.index('Amsterdam'),NAMES.index('public_transport_density')]=0
 cases=[('before_V202',l0,h0),('after_conditional',lo,hi),('withdraw_Oslo_bus_refinement',without_new,hi),('withdraw_OCBC_venue',lower(include_sportshub=False),hi),('withdraw_Singapore_directory_refinement',lower(include_sg_pool=False),hi),('withdraw_all_Singapore_pool_supplements',lower(include_sportshub=False,include_sg_pool=False),hi),('withhold_existing_three_notice_venues',lower(withhold_existing_notice_venues=True),hi),('withhold_all_four_notice_venues',lower(withhold_notice_venues=True),hi),('withdraw_Zurich_pool_refinement',lower(include_zurich_pool=False),hi),('withdraw_Tokyo_inventory',lower(include_tokyo=False),hi),('withdraw_Warsaw_inventory',lower(include_warsaw=False),hi),('withdraw_both_inventory',lower(include_tokyo=False,include_warsaw=False),hi),('withdraw_historical_stage_proxy',*without_historical_proxy(f,lo,hi)),('withdraw_Amsterdam_mapped_inventory',amsterdam,hi),('withhold_two_rail_replacement_stops',lower(withhold_rail_replacement=True),hi),('withhold_no_calls_Midtstuen_bus',lower(withhold_no_calls_bus=True),hi),('withhold_all_three_service_flags',lower(withhold_rail_replacement=True,withhold_no_calls_bus=True),hi),('include_questioned_Tveten_bru',lower(include_questioned_stop=True),hi)]
 assert len(cases)==18
 ranks=[];bounds=[];reports=[];mc=[]
 for label,a,b in cases:
  for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   t=evaluate(cities,a,b,w);ranks.append(t.assign(scenario=label,weight_reference=ref));reports.append(dict(scenario=label,weight_reference=ref,possible_champions=t.loc[t.possible_champion,'city'].tolist(),necessary_champions=t.loc[t.necessary_champion,'city'].tolist(),minimax_choices=t.loc[t.decision_rank.eq(1),'city'].tolist(),mean_width=float((t.score_upper-t.score_lower).mean())))
  bounds.extend(dict(scenario=label,city=c,indicator=n,lower=a[i,j],upper=b[i,j]) for i,c in enumerate(cities) for j,n in enumerate(NAMES))
 for ref,center in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  for concentration in [20,100,500]:
   draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*center,10000)
   for label,a,b in cases:
    lower_scores,upper=score_many(a,draws),score_many(b,draws);regret,possible,_,_,_=interval_metrics(lower_scores,upper);rank,recommended,_=rank_metrics(regret,descending=False)
    for i,c in enumerate(cities):mc.append(dict(scenario=label,weight_reference=ref,concentration=concentration,city=c,minimax_recommendation_frequency=float(recommended[:,i].mean()),mean_decision_rank=float(rank[:,i].mean()),possible_champion_frequency=float(possible[:,i].mean())))
 table=pd.concat(ranks,ignore_index=True);table.to_csv(OUT/'all_ranks.csv',index=False);table[table.scenario.eq('after_conditional')].to_csv(OUT/'current_ranks.csv',index=False);pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False);pd.DataFrame(mc).to_csv(OUT/'mc_city_summary.csv',index=False)
 summary=dict(version='V203',activation_status='staged_not_active',baseline='V202 user16',results=reports,changed_cells=1,unchanged_cells=159,all_upper_bounds_unchanged=True,point_cells=112,partial_cells=37,fully_missing_cells=11,cumulative_supplements=25,newly_filled_cells=0,refined_existing_partial_cells=1,input_sha256=sha(SOURCE),admissions_sha256=sha(MANIFEST),mc_seed=20261108,mc_draws_per_setting=10000,primary_mc_settings=len(cases)*6,scope='626purebusonstreet source-defined stop groups; no addition of89metro;627questionedstop,624railreplacement/625no-querycalls/623allflags sensitivity;notallserved/access; originalvaluesandrulesretained')
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('V203 isolated primary complete;18cases108MCsettings')
if __name__=='__main__':main()

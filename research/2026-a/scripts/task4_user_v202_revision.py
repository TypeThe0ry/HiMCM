"""Isolated one-venue public inventory refinement; unchanged original data and rules."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v200_revision import revised_bounds as previous_bounds
from task4_user_v136_revision import without_historical_proxy
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,SPEC,weights
from task4_ahp_mc_baseline import score_many,interval_metrics,rank_metrics
OUT=ROOT/'results/task4_user_v202_revision';MANIFEST=ROOT/'design/task4_user_v202_admissions.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def revised_bounds(include_sportshub=True,include_sg_pool=True,include_zurich_pool=True,include_tokyo=True,include_warsaw=True,withhold_notice_venues=False,withhold_existing_notice_venues=False):
 f,lo,hi=previous_bounds(include_sg_pool,include_zurich_pool,include_tokyo,include_warsaw);before=np.stack([lo,hi]).copy();m=json.loads(MANIFEST.read_text());assert sha(SOURCE)==m['input_sha256']
 for n,h in m['source_hashes'].items():assert sha(ROOT/n)==h,n
 row=m['observations'][0];i=f.city.tolist().index('Singapore');j=NAMES.index('public_pool_density')
 assert row['raw_count_before']==25 and row['raw_count']==len(set(row['venues']))==26
 assert f.iloc[i].population==row['population']==6036900 and f.iloc[i].population_year==row['population_year']==2024
 assert pd.isna(f.iloc[i].pools_per_100k) and hi[i,j]==1
 assert not (withhold_notice_venues and withhold_existing_notice_venues)
 if withhold_notice_venues or withhold_existing_notice_venues:assert include_sg_pool
 n=(25 if include_sg_pool else 7)+int(include_sportshub)
 if withhold_notice_venues:n-=3+int(include_sportshub)
 elif withhold_existing_notice_venues:n-=3
 if include_sportshub or withhold_notice_venues or withhold_existing_notice_venues:
  density=n*100000/row['population'];lo[i,j]=density/(SPEC[j][2]+density)
 mask=np.ones((16,10),bool);mask[i,j]=False
 np.testing.assert_array_equal(np.stack([lo,hi])[:,mask],before[:,mask]);np.testing.assert_array_equal(hi,before[1])
 if include_sportshub and include_sg_pool and not (withhold_notice_venues or withhold_existing_notice_venues):np.testing.assert_allclose([lo[i,j],hi[i,j]],row['utility_after'],rtol=0,atol=1e-16)
 return f,lo,hi

def main():
 OUT.mkdir(exist_ok=True);f,l0,h0=previous_bounds();_,lo,hi=revised_bounds();cities=f.city.tolist()
 _,without_new,_=revised_bounds(False);np.testing.assert_array_equal(without_new,l0)
 _,without_dir,_=revised_bounds(include_sg_pool=False);_,without_all,_=revised_bounds(False,False)
 _,notice23,_=revised_bounds(withhold_existing_notice_venues=True);_,notice22,_=revised_bounds(withhold_notice_venues=True)
 _,without_zh,_=revised_bounds(include_zurich_pool=False);_,without_tokyo,_=revised_bounds(include_tokyo=False);_,without_warsaw,_=revised_bounds(include_warsaw=False);_,without_both,_=revised_bounds(include_tokyo=False,include_warsaw=False)
 amsterdam=lo.copy();amsterdam[cities.index('Amsterdam'),NAMES.index('public_transport_density')]=0
 cases=[('before_V200',l0,h0),('after_conditional',lo,hi),('withdraw_OCBC_venue',without_new,hi),('withdraw_Singapore_directory_refinement',without_dir,hi),('withdraw_all_Singapore_pool_supplements',without_all,hi),('withhold_existing_three_notice_venues',notice23,hi),('withhold_all_four_notice_venues',notice22,hi),('withdraw_Zurich_pool_refinement',without_zh,hi),('withdraw_Tokyo_inventory',without_tokyo,hi),('withdraw_Warsaw_inventory',without_warsaw,hi),('withdraw_both_inventory',without_both,hi),('withdraw_historical_stage_proxy',*without_historical_proxy(f,lo,hi)),('withdraw_Amsterdam_mapped_inventory',amsterdam,hi)]
 ranks=[];bounds=[];reports=[];mc=[]
 for label,a,b in cases:
  for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   t=evaluate(cities,a,b,w);ranks.append(t.assign(scenario=label,weight_reference=ref));reports.append(dict(scenario=label,weight_reference=ref,possible_champions=t.loc[t.possible_champion,'city'].tolist(),necessary_champions=t.loc[t.necessary_champion,'city'].tolist(),minimax_choices=t.loc[t.decision_rank.eq(1),'city'].tolist(),mean_width=float((t.score_upper-t.score_lower).mean())))
  bounds.extend(dict(scenario=label,city=c,indicator=n,lower=a[i,j],upper=b[i,j]) for i,c in enumerate(cities) for j,n in enumerate(NAMES))
 for ref,center in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  for concentration in [20,100,500]:
   draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*center,10000)
   for label,a,b in cases:
    lower,upper=score_many(a,draws),score_many(b,draws);regret,possible,_,_,_=interval_metrics(lower,upper);rank,recommended,_=rank_metrics(regret,descending=False)
    for i,c in enumerate(cities):mc.append(dict(scenario=label,weight_reference=ref,concentration=concentration,city=c,minimax_recommendation_frequency=float(recommended[:,i].mean()),mean_decision_rank=float(rank[:,i].mean()),possible_champion_frequency=float(possible[:,i].mean())))
 table=pd.concat(ranks,ignore_index=True);table.to_csv(OUT/'all_ranks.csv',index=False);table[table.scenario.eq('after_conditional')].to_csv(OUT/'current_ranks.csv',index=False);pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False);pd.DataFrame(mc).to_csv(OUT/'mc_city_summary.csv',index=False)
 summary=dict(version='V202',activation_status='staged_not_active',baseline='V200 user16',results=reports,changed_cells=1,unchanged_cells=159,all_upper_bounds_unchanged=True,point_cells=112,partial_cells=37,fully_missing_cells=11,cumulative_supplements=25,newly_filled_cells=0,refined_existing_partial_cells=1,input_sha256=sha(SOURCE),admissions_sha256=sha(MANIFEST),mc_seed=20261108,mc_draws_per_setting=10000,primary_mc_settings=len(cases)*6,scope='26physicalpublicvenues;23old-notices-only and22all-notices withholding cases;notopenoruniversalaccess; originalvaluesandscientificrulesretained')
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('V202 isolated primary complete;13cases78MCsettings')
if __name__=='__main__':main()

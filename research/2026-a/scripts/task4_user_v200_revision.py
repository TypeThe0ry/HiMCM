"""Staged Singapore pool inventory refinement with explicit notice withholding."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v197_revision import revised_bounds as previous_bounds
from task4_user_v136_revision import without_historical_proxy
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,SPEC,weights
from task4_ahp_mc_baseline import score_many,interval_metrics,rank_metrics
OUT=ROOT/'results/task4_user_v200_revision';MANIFEST=ROOT/'design/task4_user_v200_admissions.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def revised_bounds(include_sg_pool=True,include_zurich_pool=True,include_tokyo=True,include_warsaw=True,withhold_notice_venues=False):
 f,lo,hi=previous_bounds(include_zurich_pool,include_tokyo,include_warsaw);before=np.stack([lo,hi]).copy();m=json.loads(MANIFEST.read_text());assert sha(SOURCE)==m['input_sha256']
 for n,h in m['source_hashes'].items():assert sha(ROOT/n)==h,n
 row=m['observations'][0];i=f.city.tolist().index('Singapore');j=NAMES.index('public_pool_density')
 assert row['raw_count']==len(set(row['venues']))==len(set(row['provider_page_ids']))==25
 assert row['notice_withholding_count']==25-len(row['withheld_notice_venues'])==22
 assert f.iloc[i].population==row['population']==6036900 and f.iloc[i].population_year==row['population_year']==2024
 assert pd.isna(f.iloc[i].pools_per_100k) and hi[i,j]==1
 n=row['notice_withholding_count'] if withhold_notice_venues else row['raw_count'];d=n*100000/row['population'];u=d/(SPEC[j][2]+d)
 np.testing.assert_allclose(row['utility_after'],[2500000/(6036900+2500000),1],rtol=0,atol=1e-16)
 assert u>lo[i,j]
 if include_sg_pool:lo[i,j]=u
 mask=np.ones((16,10),bool);mask[i,j]=False
 np.testing.assert_array_equal(np.stack([lo,hi])[:,mask],before[:,mask]);np.testing.assert_array_equal(hi,before[1])
 return f,lo,hi

def main():
 OUT.mkdir(exist_ok=True);f,l0,h0=previous_bounds();_,lo,hi=revised_bounds();cities=f.city.tolist()
 _,without_sg,_=revised_bounds(False);np.testing.assert_array_equal(without_sg,l0)
 _,notice22,_=revised_bounds(withhold_notice_venues=True)
 _,without_zh,_=revised_bounds(True,False);_,without_tokyo,_=revised_bounds(True,True,False);_,without_warsaw,_=revised_bounds(True,True,True,False);_,without_both,_=revised_bounds(True,True,False,False)
 amsterdam=lo.copy();amsterdam[cities.index('Amsterdam'),NAMES.index('public_transport_density')]=0
 cases=[('before_V197',l0,h0),('after_conditional',lo,hi),('withdraw_Singapore_pool_refinement',without_sg,hi),('withhold_three_pool_notice_venues',notice22,hi),('withdraw_Zurich_pool_refinement',without_zh,hi),('withdraw_Tokyo_inventory',without_tokyo,hi),('withdraw_Warsaw_inventory',without_warsaw,hi),('withdraw_both_inventory',without_both,hi),('withdraw_historical_stage_proxy',*without_historical_proxy(f,lo,hi)),('withdraw_Amsterdam_mapped_inventory',amsterdam,hi)]
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
 summary=dict(version='V200',activation_status='staged_not_active',baseline='V197 user16',results=reports,changed_cells=1,unchanged_cells=159,all_upper_bounds_unchanged=True,point_cells=112,partial_cells=37,fully_missing_cells=11,cumulative_supplements=25,newly_filled_cells=0,refined_existing_partial_cells=1,input_sha256=sha(SOURCE),admissions_sha256=sha(MANIFEST),mc_seed=20261108,mc_draws_per_setting=10000,primary_mc_settings=len(cases)*6,scope='25namedphysicalpublicvenuesnotopen/accesscount;22noticewithholdingcase;nouservalues,weights,anchors,intervalrules,currentregistriesorpaperchanged')
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('V200 stagedprimary complete;10cases60MCsettings;112point37partial11unknown;25unique supplementedkeys')
if __name__=='__main__':main()

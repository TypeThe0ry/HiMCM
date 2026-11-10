"""Retain Oslo's supplied2009 mean; separately withdraw its commute-proxy bounds."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate,SOURCE
from task4_v5_model import ROOT,NAMES,weights
O=ROOT/'results/current_oslo_commute_scope'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 snapshot=ROOT/'design/task4_user_v203_snapshot.json';bound=json.loads(snapshot.read_text())['source_sha256']
 assert len(bound)==548
 for n,h in bound.items():assert sha(ROOT/n)==h,n
 nav=[ROOT/'design'/f'task4_user_current_{n}.json' for n in ['model','extensions','review','delivery']]
 P=ROOT.parents[2]/'HiMCM-Overleaf';deps=json.loads((ROOT/'results/current_paper_review/current_verification.json').read_text())['current_files_sha256']
 protect={str(p):sha(p) for p in [*nav,*[P/n for n in deps]]}
 f,lo,hi=revised_bounds();old=np.stack([lo,hi]).copy();cities=f.city.tolist();i=cities.index('Oslo');j=NAMES.index('travel')
 assert f.iloc[i].commute_min==31 and int(f.iloc[i].commute_min_year)==2009 and f.iloc[i].commute_min_flag=='STALE'
 a,b=lo.copy(),hi.copy();a[i,j]=0;b[i,j]=1
 mask=np.ones((16,10),bool);mask[i,j]=False;np.testing.assert_array_equal(np.stack([a,b])[:,mask],old[:,mask]);np.testing.assert_array_equal(b,hi)
 tables=[];reports=[]
 for label,l,h in [('retained_V203',lo,hi),('withdraw_Oslo_commute_proxy',a,b)]:
  for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
   t=evaluate(cities,l,h,w);tables.append(t.assign(scenario=label,weight_reference=ref));reports.append(dict(scenario=label,weight_reference=ref,recommendation=t.loc[t.decision_rank.eq(1),'city'].tolist(),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),mean_score_width=float((t.score_upper-t.score_lower).mean())))
 _,x,y=revised_bounds();np.testing.assert_array_equal(np.stack([x,y]),old)
 for n,h in bound.items():assert sha(ROOT/n)==h,n
 for n,h in protect.items():assert sha(Path(n))==h,n
 O.mkdir(exist_ok=True);pd.concat(tables,ignore_index=True).to_csv(O/'ranks.csv',index=False)
 pd.DataFrame([dict(scenario=s,city=c,indicator=n,lower=l[z,k],upper=h[z,k]) for s,l,h in [('retained_V203',lo,hi),('withdraw_Oslo_commute_proxy',a,b)] for z,c in enumerate(cities) for k,n in enumerate(NAMES)]).to_csv(O/'bounds.csv',index=False)
 source_files=[]
 for directory in ['current_oslo_travel2009','current_zurich_fte_bound']:
  source_files.extend(p for p in (ROOT/'data'/directory).iterdir() if p.is_file())
 report=dict(status='controlled_source_scope_check_primary_unchanged',primary_model='V203',original_mean=31,original_mean_year=2009,original_mean_flag='STALE',original_CSV_sha256=sha(SOURCE),source_lineage='Eurostatvalue/yearmatch is a source lead, not proof of original CSV lineage or historical boundary. Independent TOI2009mean26 is not substituted.',comparisons=reports,changed_lower_cells=1,all_other_bounds_preserved=True,primary_admissions=0,actual_active_width_reduction=0,MC_replayed=False,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),snapshot,*source_files]},protected_at_run=protect,scope='Deterministic withdrawal of only Oslo travel information; not a correction, new observation, duration distribution, calibrated error or forecast.')
 (O/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(reports,indent=2))
if __name__=='__main__':main()

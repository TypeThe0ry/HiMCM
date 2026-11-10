"""Isolated preview of12 named Zurich venues, never active model admission."""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_user_v192_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,score,weights
from task4_interval_decision import interval_decision
O=ROOT/'results/task4_v196_candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=ROOT/'data/task4_v196_zurichpool/school_candidates.json';c=json.loads(source.read_text())
 assert c['status']=='pass' and c['all_thirteen_addresses_unique'] and c['candidate_count_not_admitted']
 q=c['conservative_candidate'];assert q['proposed_count']==12 and len(q['new_school_names'])==5
 f,lo,hi=revised_bounds();before=np.stack([lo,hi]).copy();i=f.city.tolist().index('Zurich');j=NAMES.index('public_pool_density')
 population=int(f.iloc[i]['population']);assert population==q['population']==440935
 density=12*100000/population;x=density/(1+density);a=lo.copy();a[i,j]=x;assert x>lo[i,j]
 mask=np.ones((16,10),bool);mask[i,j]=False;np.testing.assert_array_equal(a[mask],lo[mask])
 rows=[];summ=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  widths=[]
  for label,l in [('baseline_V192',lo),('candidate12_not_admitted',a)]:
   L,U=score(l,w),score(hi,w);d=interval_decision(L,U);widths.append(float(np.mean(U-L)))
   summ.append(dict(weight_reference=ref,scenario=label,mean_score_width=widths[-1],minimax_regret=float(d['minimax_regret']),possible_count=int(d['possible_champion'].sum()),necessary_count=int(d['necessary_champion'].sum()),conservative_recommendation=';'.join(f.city.iloc[k] for k in d['minimax_choices'])))
   for k,city in enumerate(f.city):rows.append(dict(weight_reference=ref,scenario=label,city=city,score_lower=L[k],score_upper=U[k],max_regret=d['max_regret'][k]))
  assert widths[1]<widths[0]
 _,l,u=revised_bounds();np.testing.assert_array_equal(before,np.stack([l,u]))
 O.mkdir(exist_ok=True);pd.DataFrame(rows).to_csv(O/'scores.csv',index=False)
 report=dict(status='preview_only_not_admitted',base_science='V192',old_count=7,candidate_count=12,population_retained=population,population_year_retained=2025,old_utility_lower=float(lo[i,j]),candidate_utility_lower=x,upper_retained=1.,other159cells_and_alluppers_unchanged=True,baseline_partial_unknown_counts_unchanged=[37,11],summary=summ,primary_admissions=0,actual_active_model_width_reduction=0,scope='Conditionalfacilitysupplysubset;restrictedpublicsessions,holidayclosuresandindividualaccessunknown. Kügelilooadult-onlyexcluded. Noforecastoruniversalteenaccessclaim.',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [source,Path(__file__),ROOT/'design/task4_user_v192_snapshot.json']})
 (O/'preview.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

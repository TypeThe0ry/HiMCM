"""Recompute endpoint exclusion acquisition after V113, using saved audited bounds."""
from pathlib import Path
import itertools,json
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
b=pd.read_csv(ROOT/'results/task4_v113_ahp_mc/utility_bounds.csv',float_precision='round_trip');lo=b.lower.to_numpy().reshape(25,10);hi=b.upper.to_numpy().reshape(25,10);cities=b.city.drop_duplicates().tolist();names=b.indicator.drop_duplicates().tolist();aux=np.array([False,False,False,False,False,False,True,False,False,True]);rows=[];bundles=[];single=[]
for name,w in [('inherited',np.where(aux,.05,.9/8)),('equal',np.ones(10)/10)]:
 def score(z):return 100/(1+np.sqrt(np.sum(w*(1-z)**2,axis=-1)/np.sum(w*z*z,axis=-1)))
 lower,upper=score(lo),score(hi)
 for i,c in enumerate(cities):
  target=max(np.delete(lower,i));ratio=(target/(100-target))**2;unknown=np.flatnonzero(hi[i]-lo[i]>1e-12);success=[]
  for count in range(1,len(unknown)+1):
   for chosen in itertools.combinations(unknown,count):
    z=hi[i].copy();z[list(chosen)]=lo[i,list(chosen)]
    if np.sum(w*z*z)<ratio*np.sum(w*(1-z)**2)-1e-10:success.append(chosen)
   if success:break
  rows.append(dict(scenario=name,city=c,minimum_hypothetical_cells=count if success else None,minimal_bundle_count=len(success)))
  for chosen in success:bundles.append(dict(scenario=name,city=c,indicators='|'.join(names[j] for j in chosen),cell_count=len(chosen)))
  for j in unknown:
   z=hi[i].copy();z[j]=lo[i,j];minimum=score(z)
   z=lo[i].copy();z[j]=hi[i,j];maximum=score(z)
   single.append(dict(scenario=name,city=c,indicator=names[j],own_exclusion=bool(minimum<target-1e-12),other_exclusion_count=int(np.sum(np.delete(upper,i)<maximum-1e-12))))
old=pd.read_csv(ROOT/'results/task4_v113_exclusion_priority/city_requirements.csv')[['scenario','city','minimum_hypothetical_cells','minimal_bundle_count']]
new=pd.DataFrame(rows);compare=old.merge(new,on=['scenario','city'],suffixes=('_v108','_v113'));compare.to_csv(OUT/'post_revision_city_requirements.csv',index=False);pd.DataFrame(bundles).to_csv(OUT/'post_revision_minimum_bundles.csv',index=False)
changed=compare[(compare.minimum_hypothetical_cells_v108.fillna(-1)!=compare.minimum_hypothetical_cells_v113.fillna(-1))|(compare.minimal_bundle_count_v108!=compare.minimal_bundle_count_v113)]
result=dict(model_version='V113',single_self_exclusion_count=int(sum(r['own_exclusion'] for r in single)),single_max_other_exclusion=max(r['other_exclusion_count'] for r in single),changed_city_requirements=changed.fillna('none').to_dict('records'),scope='Hypothetical exact endpoint revelations, not observed data or plausible outcomes. Bounds unchanged.')
(OUT/'post_revision_priority.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

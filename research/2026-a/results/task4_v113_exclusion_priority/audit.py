import sys,itertools,json
import numpy as np,pandas as pd
from pathlib import Path
sys.path.insert(0,'research/2026-a/scripts')
from task4_mexico_sampling_revision import mexico_sampling_bounds
from task4_v5_model import CITIES,NAMES,weights
lo,hi=mexico_sampling_bounds();out=Path('research/2026-a/results/task4_v113_exclusion_priority')
f=pd.read_csv(out/'city_requirements.csv');cells=pd.read_csv(out/'single_cell_thresholds.csv');checked=0
for name,w in [('inherited',weights(.1)),('equal',np.full(10,.1))]:
 L=100/(1+np.sqrt(np.sum(w*(1-lo)**2,axis=1)/np.sum(w*lo**2,axis=1)))
 for i,c in enumerate(CITIES):
  threshold=np.max(np.delete(L,i));ratio=(threshold/(100-threshold))**2
  unknown=np.flatnonzero(hi[i]-lo[i]>1e-12);best=11
  for bits in itertools.product([0,1],repeat=len(unknown)):
   z=hi[i].copy();chosen=unknown[np.array(bits,dtype=bool)];z[chosen]=lo[i,chosen]
   excluded=np.sum(w*z*z)<ratio*np.sum(w*(1-z)**2)-1e-10
   if excluded:best=min(best,len(chosen))
   checked+=1
  recorded=f[(f.scenario==name)&(f.city==c)].minimum_hypothetical_cells.iloc[0]
  assert (best==11 and pd.isna(recorded)) or best==recorded
result=dict(status='passed',independent_squared_distance_comparison=True,endpoint_subsets_checked=checked,city_scenarios_verified=50,no_single_cell_exclusion_in_both_scenarios=True,source='current_bounds V108 unchanged',scope='Numerical exhaustive endpoint check, not physical joint attainability or empirical observation')
(out/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

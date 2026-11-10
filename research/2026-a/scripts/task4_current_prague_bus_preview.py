"""Compare a source-backed conditional Prague candidate; no primary admission."""
from pathlib import Path
import csv,hashlib,json,math,sys
import numpy as np
import pandas as pd
from task4_user_v204_revision import revised_bounds
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import NAMES,weights
R=Path(__file__).resolve().parents[1];O=R/'results/current_prague_bus_candidate_preview'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def scalar(a,w):
 result=[]
 for row in a:
  A=math.sqrt(sum(float(v)*float(x)**2 for v,x in zip(w,row)))
  B=math.sqrt(sum(float(v)*(1-float(x))**2 for v,x in zip(w,row)))
  result.append(100*A/(A+B))
 return np.array(result)
def main():
 if O.exists():raise ValueError('Frozen output exists; replay in a scratch checkout')
 H=R/'results/current_prague_bus_crosswalk';receipt=json.loads((H/'receipt.json').read_text())
 for p,h in receipt['source_sha256'].items():assert sha(R/p)==h,p
 witness=list(csv.DictReader((H/'witness.csv').open()))
 assert len(witness)==len({r['node'] for r in witness})==receipt['conditional_candidate_distinct_nodes']==942
 assert all(r['classification']=='qualifying' and r['current_types']=='bus' and r['inprague']=='1' and not r['flags'] and r['current_night_values']=='absent' and r['current_group_municipality']=='Praha' for r in witness)
 metro=list(csv.DictReader((R/'data/task4_v127_prague/station_complexes.csv').open()))
 overlap=len({r['node'] for r in witness}&{r['pid_node_id'] for r in metro});assert overlap==47
 f,lo,hi=revised_bounds();cities=f.city.tolist();i=cities.index('Prague');j=NAMES.index('public_transport_density')
 assert int(f.iloc[i].population)==1407084 and int(f.iloc[i].population_year)==2025
 density=942*100000/1407084;candidate=density/(50+density)
 assert abs(lo[i,j]-(57*100000/1407084)/(50+57*100000/1407084))<1e-15
 a=lo.copy();a[i,j]=candidate;mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
 np.testing.assert_array_equal(a[mask],lo[mask]);assert hi[i,j]==1
 rows=[];summary=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  baseline_width=None
  for label,b in [('retained_V204',lo),('conditional_cross_snapshot_942_nodes',a)]:
   t=evaluate(cities,b,hi,w);low=scalar(b,w);up=scalar(hi,w)
   regret=np.array([max(0,max(up[k]-low[ii] for k in range(16) if k!=ii)) for ii in range(16)])
   np.testing.assert_allclose(t.score_lower,low,atol=1e-12,rtol=0);np.testing.assert_allclose(t.score_upper,up,atol=1e-12,rtol=0);np.testing.assert_allclose(t.max_regret,regret,atol=1e-12,rtol=0)
   width=float((up-low).mean())
   if baseline_width is None:baseline_width=width
   summary.append(dict(weight_reference=ref,scenario=label,mean_width=width,hypothetical_width_reduction=baseline_width-width,choices=t.loc[t.decision_rank.eq(1),'city'].tolist(),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),Prague_decision_rank=int(t.iloc[i].decision_rank)))
   rows.append(t.assign(weight_reference=ref,scenario=label))
 np.testing.assert_array_equal(lo,revised_bounds()[1]);np.testing.assert_array_equal(hi,revised_bounds()[2])
 paths=[Path(__file__),SOURCE,H/'receipt.json',H/'extract.py',H/'README.md',H/'witness.csv',H/'link_diagnostics.csv',R/'data/task4_v127_prague/station_complexes.csv',R/'design/task4_user_v204_snapshot.json']
 paths += [Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().parent==R/'scripts']
 O.mkdir(parents=True);pd.concat(rows,ignore_index=True).to_csv(O/'city_cases.csv',index=False)
 report=dict(status='pass conditional candidate preview',source_sha256={str(p.relative_to(R)):sha(p) for p in sorted(set(paths))},output_sha256={'city_cases.csv':sha(O/'city_cases.csv')},summary=summary,scalar_city_cases=64,conditional_count=942,retained_count=57,counts_not_added=True,overlapping_native_metro_nodes=overlap,candidate_utility_lower=candidate,other159_lower_and_all160_upper_preserved=True,primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,scope='A conditional source-defined bus-node inventory diagnostic, not an admitted physical-site lower bound, confirmed day service or historical census. Old city-list2026-11-09 and newer JSON2026-11-10 are separate snapshots; missingisNight remainsunknown. The candidate replaces57 for this comparison, never adds57. Numeric changes are hypothetical until identity/count-unit,date/public-service/geography qualification and controlled scientific integration. No MC replay or paper update.')
 (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'summary':summary},indent=2))
if __name__=='__main__':main()

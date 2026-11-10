"""Controlled V202 Oslo count-definition diagnostics; no source admission.

The native NSR unit and distance/name clusters are distinct counting experiments.
Neither is silently added to the 89-station subset or labelled a 2025 observation.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v202_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,SPEC,weights
from task4_user_city_indicators import evaluate
from audit_current_priority import scalar_scores,decision
D=ROOT/'data/current_oslo_transport';O=ROOT/'results/current_transport_candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 summary=json.loads((D/'summary.json').read_text());candidate=json.loads((D/'candidate.json').read_text());snap=ROOT/'design/task4_user_v202_snapshot.json'
 science=json.loads(snap.read_text())['source_sha256']
 for n,h in science.items():assert sha(ROOT/n)==h,n
 nav=[ROOT/'design'/('task4_user_current_'+n+'.json') for n in ['model','extensions','review','delivery']]
 paper=ROOT.parents[1].parent/'HiMCM-Overleaf';deps=json.loads((ROOT/'results/current_paper_review/current_verification.json').read_text())['current_files_sha256']
 protect={str(p):sha(p) for p in nav+[paper/n for n in deps]}
 f,lo,hi=revised_bounds();original=np.stack([lo,hi]).copy();cities=f.city.tolist();i=cities.index('Oslo');j=NAMES.index('public_transport_density');pop=int(f.iloc[i].population)
 assert pop==727797 and SPEC[j][2]==50
 assert candidate['population']==pop and summary['population']==pop
 native=int(summary['eligible_root_groups']);clusters=int(summary['conservative_basin_count'])
 assert native==829 and clusters==candidate['candidate_count']==517
 inventory=pd.read_csv(D/'conservative_basins.csv');assert len(inventory)==native and inventory.id.nunique()==native and inventory.basin.nunique()==clusters
 def altered(n):
  a=lo.copy();density=n*100000/pop;a[i,j]=density/(50+density);return a
 np.testing.assert_allclose(altered(89),lo,atol=1e-16,rtol=0)
 scenarios=[('active_metro_subset89',89),('distance_name_clusters_unvalidated',clusters),('native_registry_roots',native),('withdraw_new_inventory',89),('below_fixed_integer_switch',226),('above_fixed_integer_switch',227),('below_equal_integer_switch',639),('above_equal_integer_switch',640)]
 tables=[];reports=[];thresholds=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  for label,n in scenarios:
   a=altered(n);mask=np.ones((16,10),bool);mask[i,j]=False
   np.testing.assert_array_equal(a[mask],lo[mask])
   t=evaluate(cities,a,hi,w);L,U=scalar_scores(a,w),scalar_scores(hi,w);regret,risk,possible,choices=decision(L,U)
   for key,v in [('score_lower',L),('score_upper',U),('max_regret',regret)]:np.testing.assert_allclose(t[key],v,atol=3e-13,rtol=0)
   assert t.possible_champion.tolist()==possible.tolist()
   reports.append(dict(scenario=label,count=n,weight_reference=ref,utility_lower=float(a[i,j]),mean_score_width=float((U-L).mean()),recommendation=[cities[k] for k in choices],possible_champions=int(possible.sum()),necessary_champions=int(t.necessary_champion.sum()),Oslo_regret_gap_to_best_other=float(regret[i]-np.delete(regret,i).min())))
   tables.append(t.assign(scenario=label,weight_reference=ref))
  def gap(n):
   L=scalar_scores(altered(n),w);U=scalar_scores(hi,w);r=decision(L,U)[0]
   return r[i]-np.delete(r,i).min()
  tie=float(brentq(gap,89,10000,xtol=1e-10));first=math.floor(tie)+1
  assert gap(first)<0<gap(first-1)
  thresholds.append(dict(weight_reference=ref,tie_count_equivalent=tie,first_strict_integer_count=first,scope='Only Oslo transport lower bound changes; conditional on treating count as comparable stop units. Not an observed inventory or collection target probability.'))
 _,a,b=revised_bounds();np.testing.assert_array_equal(original,np.stack([a,b]))
 for n,h in science.items():assert sha(ROOT/n)==h,n
 for n,h in protect.items():assert sha(Path(n))==h,n
 O.mkdir(parents=True,exist_ok=True);pd.concat(tables,ignore_index=True).to_csv(O/'scores.csv',index=False)
 out=dict(status='isolated_definition_sensitivity_not_admitted',active_science='V202 unchanged',primary_admissions=0,actual_active_width_reduction=0,source_capture_date=candidate['source_capture_date_utc'],population=pop,retained_active_metro_count=89,native_root_count=native,unvalidated_cluster_count=clusters,unit_warning='Native root groups are administrative registry units; 250m/name clusters are a separate heuristic and not certified physical-stop lower bounds. No new count is summed with89.',comparisons=reports,thresholds=thresholds,independent_scalar_city_weight_cases=16*len(reports),science_bindings_verified=len(science),other159lower_all160uppers_originalCSV_and_paper_preserved=True,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),D/'03_Oslo_latest.zip',D/'download.json',D/'candidate.json',D/'summary.json',D/'conservative_basins.csv',D/'native_stopplaces.csv',snap,*nav]})
 (O/'preview.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(comparisons=reports[:4],thresholds=thresholds),indent=2))
if __name__=='__main__':main()

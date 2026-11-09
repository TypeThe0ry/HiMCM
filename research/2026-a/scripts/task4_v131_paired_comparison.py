"""Pair actual frozen V128/V127 and V131/V130 results, without relabelling old data."""
from pathlib import Path
import json,hashlib
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/task4_v131_revision'
CASES={
 'preference_ranks':('preferences','ranks.csv',['profile','city']),
 'preference_MC':('preferences','mc_city_summary.csv',['profile','city','concentration','draws']),
 'future_ranks':('future','ranks.csv',['evidence_arm','scenario','weight_reference','city']),
 'future_thresholds':('future','thresholds.csv',['city','weight_reference']),
 'future_shock_MC':('future','future_mc_city_summary.csv',['evidence_arm','scenario','weight_reference','city']),
 'future_weight_MC':('future','weight_mc_city_summary.csv',['evidence_arm','scenario','weight_reference','city']),
 'methods':('method_country','method_ranks.csv',['weight_reference','city']),
 'diagnostic':('revision_diagnostic','rank_comparison.csv',['weight_reference','city'])}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 OUT.mkdir(exist_ok=True)
 protected={}
 reports={}
 for name,(module,file,keys) in CASES.items():
  old=ROOT/f'results/task4_v128_{module}'/file;new=ROOT/f'results/task4_v131_{module}'/file
  protected.update({str(p.relative_to(ROOT)):sha(p) for p in [old,new]})
  a,b=pd.read_csv(old,float_precision='round_trip'),pd.read_csv(new,float_precision='round_trip')
  if name=='methods':
   a=a[a.evidence_version=='V127'];b=b[b.evidence_version=='V130']
  joined=a.merge(b,on=keys,how='outer',suffixes=('_V128','_V131'),indicator=True,validate='one_to_one')
  assert (joined['_merge']=='both').all()
  metrics={}
  for col in a.columns.intersection(b.columns):
   if col in keys:continue
   if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]):
    delta=joined[col+'_V131'].astype(float)-joined[col+'_V128'].astype(float)
    joined[col+'_change']=delta
    metrics[col]=dict(changed_rows=int((delta.abs()>1e-12).sum()),maximum_absolute_change=float(delta.abs().max()))
  joined.to_csv(OUT/(name+'_V128_V131.csv'),index=False)
  reports[name]=dict(rows=len(joined),keys=keys,metrics=metrics)
 for p,h in protected.items():assert sha(ROOT/p)==h
 (OUT/'paired_comparison.json').write_text(json.dumps(dict(status='pass',before='V128 on V127',after='V131 on staged V130',comparisons=reports,input_sha256=protected),indent=2)+'\n')
 print(json.dumps(reports,indent=2))
if __name__=='__main__':main()

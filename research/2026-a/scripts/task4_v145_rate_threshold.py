"""Numerical point-rate tie thresholds, not inferred/observed replacement rates."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v136_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT,weights
OUT=ROOT/'results/task4_v145_rate_threshold'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    frozen={}
    for n,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256'),('results/task4_v144_homicide_sensitivity/verification.json','result_sha256')]:frozen.update(read(ROOT/n)[key]);frozen[n]=sha(ROOT/n)
    data=ROOT/'data/task4_v145_zurich_scope';v=read(data/'verification.json');assert v['status']=='pass'
    for n,h in v['source_sha256'].items():assert sha(data/n)==h;frozen[str((data/n).relative_to(ROOT))]=h
    assert sha(data/'extract.py')==v['extractor_sha256']
    for p in [Path(__file__),data/'extract.py',data/'verification.json',ROOT/'design/task4_user_current_model.json']:frozen[str(p.relative_to(ROOT))]=sha(p)
    for n,h in frozen.items():assert sha(ROOT/n)==h,n
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();i=cities.index('Zurich');assert lo[i,0]==hi[i,0]==2/(2+.14)
    threshold=[];probes=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        def table_at(r):
            lower=lo.copy();upper=hi.copy();lower[i,0]=upper[i,0]=2/(2+r)
            mask=np.ones((16,10),bool);mask[i,0]=False
            np.testing.assert_array_equal(lower[mask],lo[mask]);np.testing.assert_array_equal(upper[mask],hi[mask])
            return evaluate(cities,lower,upper,w)
        def gap(r):
            t=table_at(r);return float(t.iloc[i].max_regret-t.drop(i).max_regret.min())
        assert gap(0)<0<gap(5)
        root=float(brentq(gap,0,5,xtol=1e-14));left=root-1e-8;right=root+1e-8;assert gap(left)<0<gap(right)
        at=table_at(root);other=at.drop(i).sort_values('max_regret');alternative=other.iloc[0].city
        assert float(other.iloc[1].max_regret-other.iloc[0].max_regret)>1e-6
        threshold.append(dict(weight_reference=ref,rate_per100000=root,utility=2/(2+root),numerical_bracket_lower=left,numerical_bracket_upper=right,gap_lower=gap(left),gap_upper=gap(right),zurich_max_regret=float(at.iloc[i].max_regret),alternative=alternative,alternative_max_regret=float(other.iloc[0].max_regret),other_best_margin=float(other.iloc[1].max_regret-other.iloc[0].max_regret),positive_zurich_regret_at_rate0=float(table_at(0).iloc[i].max_regret)))
        for label,r in [('zero',0),('low_neighbor',.135),('retained_point',.14),('high_neighbor',.145),('bracket_below',left),('bracket_above',right),('high_probe',5)]:
            t=table_at(r);probes.append(t.assign(weight_reference=ref,probe=label,hypothetical_rate=r))
    OUT.mkdir(exist_ok=True);pd.concat(probes,ignore_index=True).to_csv(OUT/'probes.csv',index=False)
    summary=dict(version='V145 hypothetical Zurich homicide-point tie thresholds on V136',thresholds=threshold,unchanged_other_utility_entries=159,primary_data_admissions=0,changes_primary_data=False,changes_primary_model=False,uniqueness_argument='With r>=0 and u=2/(2+r), Zurich score bounds strictly decrease. Its positive maximum regret strictly increases; every other city regret is nonincreasing. Their minimum is nonincreasing, so the continuous difference strictly increases. Opposite signs at r=0 and r=5 give exactly one crossing on the nonnegative domain.',interpretation='Hypothetical POINT-rate changes with all other 159 entries fixed. Cutoffs are not observed rates, data corrections, confidence limits or forecasts. These differ from V144 full-information withdrawal to [0,1].',source_sha256=frozen)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for n,h in frozen.items():assert sha(ROOT/n)==h,n
    print(json.dumps(threshold,indent=2))
if __name__=='__main__':main()

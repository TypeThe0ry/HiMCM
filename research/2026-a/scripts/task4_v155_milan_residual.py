"""Residual partial transport information and matched teacher complementarity."""
from pathlib import Path
import hashlib,json
from itertools import product
import numpy as np
import pandas as pd
from task4_user_v154_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,weights,score
from task4_interval_decision import interval_decision,voi_1d
from task4_v124_priority import independent_scores

OUT=ROOT/'results/task4_v155_priority'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    f,lo,hi=revised_bounds();cities=f.city.tolist();i=cities.index('Milan')
    t=NAMES.index('public_transport_density');p=NAMES.index('upper_secondary_ptr')
    xmin=float(lo[i,t]);assert 0<xmin<hi[i,t]==1 and lo[i,p]==0 and hi[i,p]==1
    hashes={n:sha(ROOT/n) for n in json.loads((ROOT/'design/task4_user_v154_snapshot.json').read_text())['source_sha256']}
    rows=[];reports=[];checks=0
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        base=interval_decision(score(lo,w),score(hi,w));risk=base['minimax_regret']
        def trial(x,y=None,exact=True):
            nonlocal checks
            a,b=lo.copy(),hi.copy();a[i,t]=x
            if exact:b[i,t]=x
            if y is not None:
                a[i,p]=y
                if exact:b[i,p]=y
            mask=np.ones((16,10),bool);mask[i,t]=False
            if y is not None:mask[i,p]=False
            np.testing.assert_array_equal(a[mask],lo[mask]);np.testing.assert_array_equal(b[mask],hi[mask])
            assert np.all(a>=lo) and np.all(b<=hi)
            L,U=score(a,w),score(b,w)
            np.testing.assert_allclose(L,independent_scores(a,w),atol=1e-12,rtol=0)
            np.testing.assert_allclose(U,independent_scores(b,w),atol=1e-12,rtol=0)
            d=interval_decision(L,U)
            rr=np.array([max(0,np.delete(U,k).max()-L[k]) for k in range(16)])
            np.testing.assert_allclose(d['max_regret'],rr,atol=1e-12,rtol=0)
            checks+=1
            return L,U,d
        def callback(x):return trial(x)[:2]
        value=voi_1d(callback,baseline=(score(lo,w),score(hi,w)),k=i,xlo=xmin,xhi=1)
        for exact in [True,False]:
            mode='exact' if exact else 'lower_only'
            for y in [None,*np.linspace(0,1,21)]:
                for x in np.linspace(xmin,1,21):
                    L,U,d=trial(float(x),None if y is None else float(y),exact)
                    rows.append(dict(weight_reference=ref,mode=mode,
                                     group='transport_only' if y is None else 'transport_and_PTR',
                                     transport_utility=float(x),teacher_utility=y,
                                     minimax_regret=float(d['minimax_regret']),
                                     regret_reduction=float(risk-d['minimax_regret']),
                                     possible_count=int(d['possible_champion'].sum()),
                                     excluded_cities=';'.join(cities[k] for k in range(16) if not d['possible_champion'][k]),
                                     minimax_choices=';'.join(cities[k] for k in d['minimax_choices']),
                                     milan_score_lower=float(L[i]),milan_score_upper=float(U[i])))
        corners=[trial(x,y)[2] for x,y in product([xmin,1],[0,1])]
        reports.append(dict(weight_reference=ref,transport_utility_domain=[xmin,1],
                            exact_transport_VOI=value,
                            joint_endpoint_best_risk_reduction=max(risk-d['minimax_regret'] for d in corners),
                            joint_optimistic_champion_exclusions=max(16-int(d['possible_champion'].sum()) for d in corners)))
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT/'milan_residual_grid.csv',index=False)
    for n,h in hashes.items():assert sha(ROOT/n)==h,n
    (OUT/'milan_residual_summary.json').write_text(json.dumps(dict(version='V155',primary='V154',
        source_sha256=hashes,city='Milan',new_data_admissions=0,changes_primary_model=False,
        scope='Only Milan residual transport interval and its fully missing PTR vary; all other158 entries retained. Exact information and lower-bound-only information are separate hypothetical acquisition modes.',
        endpoint_scope='Closed rectangle limits, not guaranteed physical counts or positive finite pupil-teacher ratios; no sampling or source availability probabilities.',
        grid_rows=len(rows),independent_evaluations=checks,cases=reports,generator_sha256=sha(Path(__file__)),
        result_sha256={'milan_residual_grid.csv':sha(OUT/'milan_residual_grid.csv')}),indent=2)+'\n')
    print('Milan residual',len(rows),'grid cases;',checks,'independent checks')

if __name__=='__main__':main()

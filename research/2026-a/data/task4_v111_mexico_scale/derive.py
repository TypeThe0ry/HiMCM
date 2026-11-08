"""Re-evaluate V108 Mexico ratios and fixed-weight Taylor envelopes at new scales."""
from pathlib import Path
import hashlib,importlib.util,json,math
import numpy as np
from scipy.stats import t
P=Path(__file__).resolve().parent
SOURCE=P.parent/'task4_v108_mexico_design'

def derive(tau):
    if not np.isfinite(tau) or tau<=0:raise ValueError('Positive finite time scale required')
    spec=importlib.util.spec_from_file_location('mexico_scale_design',SOURCE/'derive_design.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    # Fresh isolated module instance; historical source files remain unchanged.
    m.ENDS=[(math.exp(-b/tau) if b is not None else 0.,math.exp(-a/tau)) for a,b in zip([0,15,30,60,120],[15,30,60,120,None])]+[(0.,1.)]*3
    data=m.derive_from_moments();d=data['diagnostics'];df=d['psu_n']-d['strata_n'];critical=float(t.ppf(.975,df))
    sides=data['scenarios']['boundary3_optional'];bounds=[];prefixes=[]
    for side,sign in [('lower',-1),('upper',1)]:
        cs=sides[side]['candidates'];values=[r['ratio']+sign*critical*r['taylor_se'] for r in cs]
        k=int(np.argmin(values) if sign<0 else np.argmax(values));bounds.append(float(np.clip(values[k],0,1)));prefixes.append(k)
    return dict(city='Mexico City',tau_minutes=tau,utility_lower=bounds[0],utility_upper=bounds[1],point_lower=sides['lower']['estimate'],point_upper=sides['upper']['estimate'],selected_prefixes=prefixes,df=df,critical=critical,candidates=sides,input_moments_sha256=data['input_moments_sha256'])

def main():
    rows=[derive(tau) for tau in [15,20,30,45,60]]
    baseline=json.loads((P.parents[1]/'results/task4_v108_mexico_sampling/inference.json').read_text())['scenarios']['boundary3_optional']['outer']
    np.testing.assert_allclose([rows[2]['utility_lower'],rows[2]['utility_upper']],baseline,rtol=0,atol=1e-14)
    result=dict(source='EIC2025 conditional resident age14-18; V108 optional completed-secondary transition',method='Actual original time-bin utility coefficients and fixed-weight design moments; same candidate family and approximate Taylor outer envelope; no FPC',main_admitted=False,new_observations=0,source_script_sha256=hashlib.sha256((SOURCE/'derive_design.py').read_bytes()).hexdigest(),scenarios=rows)
    (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print([(r['tau_minutes'],r['utility_lower'],r['utility_upper']) for r in rows])
if __name__=='__main__':main()

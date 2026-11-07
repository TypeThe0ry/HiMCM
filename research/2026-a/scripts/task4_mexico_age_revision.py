"""Align Mexican census travel to ages14–18; retain conditional stage inference."""
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_population_role_revision import revised_bounds
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def mexico_bounds():
    lo,hi=revised_bounds()
    path=ROOT/'data/task4_v72_mexico'
    spec=importlib.util.spec_from_file_location('mexico72_extract',path/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    r=module.derive()
    assert r==json.loads((path/'summary.json').read_text())
    old,new=[r['scopes'][s] for s in ('age3_17','age14_18')]
    i,j=CITIES.index('Mexico City'),NAMES.index('travel')
    np.testing.assert_allclose([lo[i,j],hi[i,j]],[old['utility_lower'],old['utility_upper']],rtol=0,atol=1e-14)
    lo[i,j],hi[i,j]=new['utility_lower'],new['utility_upper']
    return lo,hi


def main():
    old=revised_bounds();new=mexico_bounds();base,_=summarize(*old,weights())
    mask=np.ones(old[0].shape,bool);mask[CITIES.index('Mexico City'),NAMES.index('travel')]=False
    for a,b in zip(old,new):np.testing.assert_array_equal(a[mask],b[mask])
    frames=[];bounds=[];reports=[];certificates=[]
    for label,(lo,hi) in [('v70_before',old),('v72_age14_18',new)]:
        f,d=summarize(lo,hi,weights());f['scenario']=label;frames.append(f)
        cert=certify(lo,hi)
        for r in cert:r.update(scenario=label,city=None if r['winner'] is None else CITIES[r['winner']])
        certificates.extend(cert)
        reports.append(dict(scenario=label,changed_cells=int(((lo!=old[0])|(hi!=old[1])).sum()),changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=f.loc[f.possible_champion,'city'].tolist(),continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(lo))!=k])['possible']],continuous_recommendation=dict(unresolved_leaves=sum(not r['certified'] for r in cert),winners=sorted({r['city'] for r in cert if r['certified']})),selected_cities=f[f.city.isin(['Mexico City','Singapore','Tokyo','Phoenix'])].to_dict('records')))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(lo[i,j]),upper=float(hi[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    out=ROOT/'results/task4_v72_mexico_age';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version='V72',baseline='V70',main_admitted=False,unchanged_cells=249,scenarios=reports)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

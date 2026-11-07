"""Extend Tokyo upper-secondary coverage while retaining geography/staff allocation bounds."""
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_singapore_stage_revision import singapore_stage_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify

SOURCE = ROOT / 'data/task4_v69_tokyo'


def evidence():
    spec = importlib.util.spec_from_file_location('tokyo_special_extract', SOURCE/'extract.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    record = module.extract()
    assert record == json.loads((SOURCE/'summary.json').read_text()), 'Refresh source extraction'
    n0,n1 = record['expanded_students_interval']; t0,t1 = record['expanded_teachers_interval']
    assert 0 < n0 <= n1 and 0 <= t0 <= t1
    np.testing.assert_allclose(record['expanded_utility_interval'],
        [15*t0/(n1+15*t0),15*t1/(n0+15*t1)],rtol=0,atol=1e-15)
    return record


def tokyo_special_bounds():
    lo,hi = singapore_stage_bounds()
    i,j = CITIES.index('Tokyo'),NAMES.index('upper_secondary_ptr')
    lo[i,j],hi[i,j] = evidence()['expanded_utility_interval']
    return lo,hi


def main():
    old = singapore_stage_bounds(); new = tokyo_special_bounds()
    i,j = CITIES.index('Tokyo'),NAMES.index('upper_secondary_ptr')
    keep = np.ones(old[0].shape,bool); keep[i,j] = False
    for a,b in zip(old,new): np.testing.assert_array_equal(a[keep],b[keep])
    withdrawn = tuple(x.copy() for x in new)
    withdrawn[0][i,j],withdrawn[1][i,j] = 0,1
    base,_ = summarize(*old,weights())
    frames=[]; rows=[]; reports=[]; leaves=[]
    for label,(lo,hi) in [('v68_before',old),('v69_special_upper_secondary',new),('tokyo_education_withdrawn',withdrawn)]:
        assert np.all((0 <= lo)&(lo <= hi)&(hi <= 1))
        frame,decision=summarize(lo,hi,weights());frame['scenario']=label;frames.append(frame)
        cert=certify(lo,hi)
        for leaf in cert: leaf.update(scenario=label,city=None if leaf['winner'] is None else CITIES[leaf['winner']])
        leaves.extend(cert)
        reports.append(dict(scenario=label,tokyo_education=[float(lo[i,j]),float(hi[i,j])],
            tokyo=frame.iloc[i][['score_lower','score_upper','decision_rank','max_regret']].to_dict(),
            choice=[CITIES[k] for k in decision['minimax_choices']],
            changed_ranks=int((frame.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v68=float(kendalltau(frame.decision_rank,base.decision_rank).statistic),
            possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(lo))!=k])['possible']],
            continuous_recommendation=dict(unresolved_leaves=sum(not r['certified'] for r in cert),winners=sorted({r['city'] for r in cert if r['certified']}))))
        rows.extend(dict(scenario=label,city=c,indicator=n,lower=float(lo[k,m]),upper=float(hi[k,m])) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    out=ROOT/'results/task4_v69_tokyo';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(rows).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(leaves).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version='V69',current_scenario='v69_special_upper_secondary',main_admitted=False,
        updated_cells=1,other_unchanged_cells=int(keep.sum()),scenarios=reports,
        alpha_fixed=.1,alpha_range=[.05,.2],numerical_certificate_not_formal_interval_arithmetic=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

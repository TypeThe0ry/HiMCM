"""Replace 2020 Mexican travel with verified 2025 bins and optional transition."""
import hashlib,importlib.util,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_copenhagen_institution_revision import copenhagen_bounds
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def source_2025():
    path=ROOT/'data/task4_v107_mexico'
    spec=importlib.util.spec_from_file_location('mexico107_aggregate',path/'derive_from_aggregates.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    r=module.derive_from_aggregates();s=json.loads((path/'summary.json').read_text())
    assert s['survey_year']==2025 and s['borough_count']==16 and s['person_rows']==442778
    return r


def mexico_2025_bounds(withdraw=False):
    lo,hi=copenhagen_bounds();i,j=CITIES.index('Mexico City'),NAMES.index('travel')
    previous=json.loads((ROOT/'data/task4_v72_mexico/summary.json').read_text())['scopes']['age14_18']
    np.testing.assert_allclose([lo[i,j],hi[i,j]],[previous['utility_lower'],previous['utility_upper']],rtol=0,atol=1e-14)
    if not withdraw:lo[i,j],hi[i,j]=source_2025()['boundary3_optional']
    return lo,hi


def main():
    baseline=copenhagen_bounds();current=mexico_2025_bounds();back=mexico_2025_bounds(True)
    i,j=CITIES.index('Mexico City'),NAMES.index('travel');mask=np.ones(baseline[0].shape,bool);mask[i,j]=False
    for a,b,c in zip(baseline,current,back):np.testing.assert_array_equal(a[mask],b[mask]);np.testing.assert_array_equal(a,c)
    historical=json.loads((ROOT/'data/task4_v107_mexico_membership/summary.json').read_text())
    np.testing.assert_allclose(historical['old_utility'],[baseline[0][i,j],baseline[1][i,j]],rtol=0,atol=1e-14)
    legacy25=source_2025()['legacy_progression']
    cases=[('v102_2020_progression',baseline)]
    for name,interval in [('2020_transition_optional',historical['revised_utility']),('2025_progression',legacy25)]:
        l,h=[a.copy() for a in baseline];l[i,j],h[i,j]=interval;cases.append((name,(l,h)))
    cases.extend([('v107_2025_transition_optional',current),('v107_withdrawn',back)])
    base,_=summarize(*baseline,weights());frames=[];bounds=[];certs=[];reports=[]
    for label,(l,h) in cases:
        f,d=summarize(l,h,weights());frames.append(f.assign(scenario=label))
        cert=certify(l,h);certs.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,mexico_travel_interval=[l[i,j],h[i,j]],mexico=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            changed_ranks_vs_v102=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau_vs_v102=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(CITIES))!=k])['possible']],
            continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=l[k,m],upper=h[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    digest=hashlib.sha256(np.stack(current).astype('<f8').tobytes()).hexdigest()
    out=ROOT/'results/task4_v107_mexico_revision'
    if (out/'summary.json').exists():
        old=json.loads((out/'summary.json').read_text());assert old['input_bounds_sha256']==digest and old['model_version']=='V107'
    out.mkdir(exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False);pd.DataFrame(certs).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version='V107',baseline_model='V102',main_admitted=True,primary_scenario='v107_2025_transition_optional',changed_cells=1,unchanged_other_cells=249,withdrawal_restores_v102=True,input_bounds_sha256=digest,
        source_2025_summary_sha256=hashlib.sha256((ROOT/'data/task4_v107_mexico/summary.json').read_bytes()).hexdigest(),source_2020_revision_sha256=hashlib.sha256((ROOT/'data/task4_v107_mexico_membership/summary.json').read_bytes()).hexdigest(),
        fixed_alpha=.1,alpha_range=[.05,.2],scenarios=reports,
        scope='2025 CDMX resident age14-18 weighted sample; current high-school stage remains conditional, completed-secondary transition membership is optional. Time-bin/membership identification envelope, not sampling CI. New period may shift either endpoint; no unsupported intersection of years. Original raw local-only; published sufficient aggregates reproduce numerical results.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([dict(scenario=r['scenario'],bounds=r['mexico_travel_interval'],mexico=r['mexico'],changed_ranks=r['changed_ranks_vs_v102']) for r in reports],indent=2))

if __name__=='__main__':main()

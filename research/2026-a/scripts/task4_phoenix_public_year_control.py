"""Matched public-school coverage controls; never replace all-city education."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_current_model import current_bounds
from task4_joint_uncertainty_stress import protect_output
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def public_utility(row):
    nlo=row['grade9_12_lower'];nhi=row['including_possible_ungraded_upper']
    tlo=row['known_strict_teacher_fte_lower'];thi=row['teacher_fte_upper']
    if not np.isfinite([nlo,tlo]).all() or nlo<=0 or tlo<0:
        raise ValueError('Positive known enrollment and nonnegative teacher lower bound required')
    if nhi is not None and (not np.isfinite(nhi) or nhi<nlo):raise ValueError('Invalid enrollment upper')
    if thi is not None and (not np.isfinite(thi) or thi<tlo):raise ValueError('Invalid teacher upper')
    return [0. if nhi is None else 15*tlo/(nhi+15*tlo),1. if thi is None else 15*thi/(nlo+15*thi)]


def main():
    source=ROOT/'data/task4_v105_phoenix';data=json.loads((source/'summary.json').read_text())
    for r in json.loads((source/'reused_sources.json').read_text()):
        b=(source.parent/r['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha256'] and len(b)==r['bytes']
    lo,hi,config=current_bounds();saved=np.stack([lo,hi]).copy();i,j=CITIES.index('Phoenix'),NAMES.index('upper_secondary_ptr');mask=np.ones(lo.shape,bool);mask[i,j]=False
    assert (lo[i,j],hi[i,j])==(0.,1.)
    scenarios=[('current_all_city',lo.copy(),hi.copy())]
    for r in data['years']:
        l,h=lo.copy(),hi.copy();l[i,j],h[i,j]=public_utility(r)
        scenarios.append(('public_only_'+r['year'],l,h))
    frames=[];bounds=[];certs=[];reports=[]
    baseline,_=summarize(lo,hi,weights(config['fixed_alpha']))
    for label,l,h in scenarios:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        f,d=summarize(l,h,weights(config['fixed_alpha']));frames.append(f.assign(scenario=label))
        cert=certify(l,h,*config['alpha_range']);certs.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,phoenix_public_or_main_utility=[l[i,j],h[i,j]],phoenix=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            changed_ranks_vs_main=int((f.decision_rank!=baseline.decision_rank).sum()),kendall_tau_vs_main=float(kendalltau(f.decision_rank,baseline.decision_rank).statistic),
            choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(CITIES))!=k],*config['alpha_range'])['possible']],
            continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=l[k,m],upper=h[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    np.testing.assert_array_equal(saved,np.stack([lo,hi]))
    out=ROOT/'results/task4_v105_phoenix_public_control';protect_output(out,lo,hi,config);out.mkdir(exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False);pd.DataFrame(certs).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version=config['model_version'],main_admitted=False,actual_changed_cells=0,unchanged_other_cells_per_control=249,
        input_bounds_sha256=hashlib.sha256(saved.astype('<f8').tobytes()).hexdigest(),source_summary_sha256=hashlib.sha256((source/'summary.json').read_bytes()).hexdigest(),
        fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],scenarios=reports,
        interpretation='Phoenix public-only diagnostic substituted into one slot, not a comparable all-city ranking. Same coverage rules, different years and released records; not a causal year effect. Private coverage is unresolved and never mixed across years. Missing enrollment or teacher upper bounds remain unbounded.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([dict(scenario=r['scenario'],utility=r['phoenix_public_or_main_utility'],phoenix=r['phoenix'],changed_ranks=r['changed_ranks_vs_main']) for r in reports],indent=2))

if __name__=='__main__':main()

"""Replace Singapore Pre-U proxy with an explicitly conditional ISCED-3 pool bound."""
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_cape_2025_revision import cape_2025_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify
from task4_acquisition_limits import certificate

SOURCE = ROOT / 'data/task4_v68_singapore'


def evidence():
    spec = importlib.util.spec_from_file_location('singapore_stage_extract', SOURCE / 'extract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    record = module.extract()
    assert record == json.loads((SOURCE / 'observation.json').read_text()), 'Refresh source extraction'
    return record


def singapore_stage_bounds():
    r = evidence()
    lo, hi = cape_2025_bounds()
    i, j = CITIES.index('Singapore'), NAMES.index('upper_secondary_ptr')
    lo[i, j], hi[i, j] = r['utility_interval']
    return lo, hi


def main():
    old = cape_2025_bounds()
    new = singapore_stage_bounds()
    i, j = CITIES.index('Singapore'), NAMES.index('upper_secondary_ptr')
    mask = np.ones(old[0].shape, bool); mask[i, j] = False
    for a, b in zip(old, new):
        np.testing.assert_array_equal(a[mask], b[mask])
    assert np.all((0 <= new[0]) & (new[0] <= new[1]) & (new[1] <= 1))
    classified = tuple(x.copy() for x in new)
    classified[0][i, j], classified[1][i, j] = evidence()['secondary_classified_utility_interval']
    broader = tuple(x.copy() for x in new)
    broader[0][i, j], broader[1][i, j] = evidence()['broader_utility_interval']
    withdrawn = tuple(x.copy() for x in new)
    withdrawn[0][i, j], withdrawn[1][i, j] = 0, 1
    base, _ = summarize(*old, weights())
    rows, bounds, summaries, certificates = [], [], [], []
    for label, (lo, hi) in [('v63_preuniversity_proxy', old), ('v68_isced3_conditional', new),
                           ('secondary_classification_assumption', classified),
                           ('all_normal_technical_unresolved', broader),
                           ('singapore_education_withdrawn', withdrawn)]:
        frame, decision = summarize(lo, hi, weights())
        frame['scenario'] = label; rows.append(frame)
        possible = [c for k, c in enumerate(CITIES) if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']]
        leaves = certify(lo, hi)
        for leaf in leaves:
            leaf.update(scenario=label, city=None if leaf['winner'] is None else CITIES[leaf['winner']])
        certificates.extend(leaves)
        summaries.append(dict(scenario=label, singapore_education=[float(lo[i,j]),float(hi[i,j])],
            singapore=frame.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in decision['minimax_choices']],
            changed_ranks=int((frame.decision_rank != base.decision_rank).sum()),
            kendall_tau_vs_v63=float(kendalltau(frame.decision_rank, base.decision_rank).statistic),
            possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
            continuous_possible_champions=possible,
            continuous_recommendation=dict(unresolved_leaves=sum(not r['certified'] for r in leaves),
                winners=sorted({r['city'] for r in leaves if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(lo[k,m]),upper=float(hi[k,m]))
                      for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    # Reuse the existing universal-completion proof, rather than inventing observations.
    measured = np.zeros_like(new[0], bool)
    measured[:, [NAMES.index('upper_secondary_ptr'), NAMES.index('travel')]] = True
    acquisition = certificate(*new, measured)
    for r in acquisition: r['city'] = CITIES[r['index']]
    out = ROOT / 'results/task4_v68_singapore_stage'; out.mkdir(parents=True,exist_ok=True)
    pd.concat(rows).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    pd.DataFrame(acquisition).to_csv(out/'acquisition_limits.csv',index=False)
    result = dict(model_version='V68',main_admitted=False,current_scenario='v68_isced3_conditional',
        baseline='V63; selected through V67',updated_cells=1,other_unchanged_cells=int(mask.sum()),
        scenarios=summaries,all_city_exact_education_travel=dict(
            selected_cells=int(measured.sum()),
            fixed_unavoidable_cities=[r['city'] for r in acquisition if r['fixed_unavoidable']],
            continuous_unavoidable_cities=[r['city'] for r in acquisition if r['continuous_unavoidable']],
            interpretation='Universal bound over exact observations within the current box, all other cells fixed. Not actual observations; not generally an attainable joint minimum.'),
        source_scope='MOE-reported secondary course counts and all-school reported teacher pool; international schools and actual teaching allocation remain unresolved.',
        alpha_fixed=.1,alpha_range=[.05,.2],numerical_certificate_not_formal_interval_arithmetic=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()

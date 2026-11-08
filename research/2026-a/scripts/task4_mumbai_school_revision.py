"""Use grade-specific Mumbai enrolment and retain shared-teacher allocation bounds."""
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_mexico_age_revision import mexico_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def source():
    path = ROOT / 'data/task4_v78_mumbai_school'
    spec = importlib.util.spec_from_file_location('mumbai78_extract', path / 'extract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.extract()
    assert result == json.loads((path / 'summary.json').read_text())
    return result


def mumbai_bounds():
    lo, hi = mexico_bounds()
    result = source()
    i, j = CITIES.index('Mumbai'), NAMES.index('upper_secondary_ptr')
    assert lo[i, j] == 0 and hi[i, j] == 1
    lo[i, j], hi[i, j] = result['utility_lower'], result['utility_upper']
    return lo, hi


def main():
    old, new = mexico_bounds(), mumbai_bounds()
    i, j = CITIES.index('Mumbai'), NAMES.index('upper_secondary_ptr')
    mask = np.ones(old[0].shape, bool)
    mask[i, j] = False
    for a, b in zip(old, new):
        np.testing.assert_array_equal(a[mask], b[mask])
    base, _ = summarize(*old, weights())
    scenarios = [('v72_before', old), ('v78_school_allocation', new)]
    # Reporting-precision diagnostics only; neither supplies main-model bounds.
    for delta in (0., .5, 1.):
        lo, hi = (a.copy() for a in old)
        lo[i, j], hi[i, j] = 15 / (56 + delta), 15 / (56 - delta)
        scenarios.append((f'reported_41_plusminus_{delta:g}', (lo, hi)))
    frames, bounds, reports, certificates = [], [], [], []
    for label, (lo, hi) in scenarios:
        f, decision = summarize(lo, hi, weights())
        f['scenario'] = label
        frames.append(f)
        cert = certify(lo, hi)
        for r in cert:
            r.update(scenario=label, city=None if r['winner'] is None else CITIES[r['winner']])
        certificates.extend(cert)
        reports.append(dict(
            scenario=label, scenario_only=label.startswith('reported_'),
            changed_cells=int(((lo != old[0]) | (hi != old[1])).sum()),
            changed_ranks=int((f.decision_rank != base.decision_rank).sum()),
            kendall_tau=float(kendalltau(f.decision_rank, base.decision_rank).statistic),
            choice=[CITIES[k] for k in decision['minimax_choices']],
            possible_champions=f.loc[f.possible_champion, 'city'].tolist(),
            continuous_possible_champions=[c for k, c in enumerate(CITIES)
                if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']],
            continuous_recommendation=dict(unresolved_leaves=sum(not r['certified'] for r in cert),
                winners=sorted({r['city'] for r in cert if r['certified']})),
            selected_cities=f[f.city.isin(['Mumbai', 'Dhaka', 'Singapore', 'Tokyo', 'Phoenix'])].to_dict('records')))
        bounds.extend(dict(scenario=label, city=c, indicator=n, lower=float(lo[k, q]), upper=float(hi[k, q]))
            for k, c in enumerate(CITIES) for q, n in enumerate(NAMES))
    out = ROOT / 'results/task4_v78_mumbai_school'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out / 'ranks.csv', index=False)
    pd.DataFrame(bounds).to_csv(out / 'utility_bounds.csv', index=False)
    pd.DataFrame(certificates).to_csv(out / 'recommendation_certificate.csv', index=False)
    result = dict(model_version='V78', baseline='V72', main_admitted=False,
        unchanged_cells=249, source='data/task4_v78_mumbai_school/summary.json', scenarios=reports)
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([dict(scenario=r['scenario'], changed_ranks=r['changed_ranks'],
        possible_champions=len(r['possible_champions']), choice=r['choice']) for r in reports], indent=2))


if __name__ == '__main__':
    main()

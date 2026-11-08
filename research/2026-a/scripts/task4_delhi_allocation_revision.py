"""Align Delhi and Mumbai's same-source nominal teaching-resource allocation."""
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_mumbai_school_revision import mumbai_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def source():
    path = ROOT / 'data/task4_v79_delhi'
    spec = importlib.util.spec_from_file_location('delhi79_extract', path / 'extract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.extract()
    assert result == json.loads((path / 'summary.json').read_text())
    return result


def delhi_bounds():
    lo, hi = mumbai_bounds()
    r = source()
    i, j = CITIES.index('Delhi'), NAMES.index('upper_secondary_ptr')
    old = json.loads((ROOT / 'data/task4_v34_education/observation.json').read_text())
    np.testing.assert_allclose([lo[i, j], hi[i, j]], old['utility_headcount'], rtol=0, atol=1e-14)
    lo[i, j], hi[i, j] = r['utility_lower'], r['utility_upper']
    return lo, hi


def main():
    old, new = mumbai_bounds(), delhi_bounds()
    i, j = CITIES.index('Delhi'), NAMES.index('upper_secondary_ptr')
    mask = np.ones(old[0].shape, bool)
    mask[i, j] = False
    for a, b in zip(old, new):
        np.testing.assert_array_equal(a[mask], b[mask])
    # Same old aggregates, revised shared-allocation rule, before school-level Z.
    aggregate = [a.copy() for a in old]
    earlier = json.loads((ROOT / 'data/task4_v34_education/observation.json').read_text())
    aggregate[0][i, j] = earlier['allocation_utility_lower']
    aggregate[1][i, j] = earlier['allocation_utility_upper']
    scenarios = [('v78_before', old), ('aggregate_allocation_only', aggregate),
                 ('v79_school_allocation', new)]
    base, _ = summarize(*old, weights())
    frames, bounds, reports, certificates = [], [], [], []
    for label, (lo, hi) in scenarios:
        f, d = summarize(lo, hi, weights())
        f['scenario'] = label
        frames.append(f)
        cert = certify(lo, hi)
        for r in cert:
            r.update(scenario=label, city=None if r['winner'] is None else CITIES[r['winner']])
        certificates.extend(cert)
        reports.append(dict(scenario=label,
            changed_cells=int(((lo != old[0]) | (hi != old[1])).sum()),
            changed_ranks=int((f.decision_rank != base.decision_rank).sum()),
            kendall_tau=float(kendalltau(f.decision_rank, base.decision_rank).statistic),
            choice=[CITIES[k] for k in d['minimax_choices']],
            possible_champions=f.loc[f.possible_champion, 'city'].tolist(),
            continuous_possible_champions=[c for k, c in enumerate(CITIES)
                if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']],
            continuous_recommendation=dict(unresolved_leaves=sum(not r['certified'] for r in cert),
                winners=sorted({r['city'] for r in cert if r['certified']})),
            selected_cities=f[f.city.isin(['Delhi', 'Santiago', 'Mumbai', 'Phoenix', 'Singapore'])].to_dict('records')))
        bounds.extend(dict(scenario=label, city=c, indicator=n, lower=float(lo[k, q]), upper=float(hi[k, q]))
            for k, c in enumerate(CITIES) for q, n in enumerate(NAMES))
    out = ROOT / 'results/task4_v79_delhi_allocation'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out / 'ranks.csv', index=False)
    pd.DataFrame(bounds).to_csv(out / 'utility_bounds.csv', index=False)
    pd.DataFrame(certificates).to_csv(out / 'recommendation_certificate.csv', index=False)
    result = dict(model_version='V79', baseline='V78', main_admitted=False,
        unchanged_cells=249, source='data/task4_v79_delhi/summary.json', scenarios=reports)
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([dict(scenario=r['scenario'], changed_ranks=r['changed_ranks'],
        possible_champions=len(r['possible_champions']), choice=r['choice']) for r in reports], indent=2))


if __name__ == '__main__':
    main()

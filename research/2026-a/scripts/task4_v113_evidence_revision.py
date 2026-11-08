"""Source-only revision: verified Singapore inventory and conditional Tokyo bound."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_mexico_sampling_revision import mexico_sampling_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize

OUT = ROOT/'results/task4_v113_evidence_revision'

def evidence_bounds(singapore=True, tokyo=True):
    lo, hi = mexico_sampling_bounds()
    for enabled, folder in [(singapore, 'singapore'), (tokyo, 'tokyo')]:
        if not enabled:
            continue
        p = ROOT/f'data/task4_v113_{folder}'
        for item in json.loads((p/'manifest.json').read_text()):
            assert hashlib.sha256((p/item['file']).read_bytes()).hexdigest() == item['sha256']
        r = json.loads((p/'observation.json').read_text())
        i, j = CITIES.index(r['city']), NAMES.index(r['indicator'])
        np.testing.assert_allclose([lo[i,j], hi[i,j]], r['utility_before'], atol=1e-15, rtol=0)
        a, b = r['utility_after']
        assert lo[i,j] <= a <= b <= hi[i,j]
        lo[i,j], hi[i,j] = a, b
    return lo, hi

def run():
    OUT.mkdir(exist_ok=True)
    base = mexico_sampling_bounds()
    frames, bounds, reports = [], [], []
    cases = [('v108', base), ('singapore_only_strict_tokyo', evidence_bounds(tokyo=False)),
             ('tokyo_only_conditional', evidence_bounds(singapore=False)),
             ('v113_conditional', evidence_bounds())]
    for name, (lo, hi) in cases:
        for weight_name, w in [('inherited', weights(.1)), ('equal', np.ones(10)/10)]:
            old, _ = summarize(*base, w)
            frame, d = summarize(lo, hi, w)
            frame['previous_decision_rank'] = old.decision_rank
            frame['rank_change_positive_improves'] = old.decision_rank-frame.decision_rank
            frames.append(frame.assign(scenario=name, weight_reference=weight_name))
            reports.append(dict(scenario=name, weight_reference=weight_name,
                changed_cells=int(np.count_nonzero((lo!=base[0]) | (hi!=base[1]))),
                choice=[CITIES[k] for k in d['minimax_choices']],
                possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
                necessary_champions=frame.loc[frame.necessary_champion,'city'].tolist(),
                changed_ranks=int((frame.decision_rank!=old.decision_rank).sum()),
                kendall=float(kendalltau(frame.decision_rank, old.decision_rank).statistic),
                mean_score_width=float((frame.score_upper-frame.score_lower).mean()),
                minimax_regret=d['minimax_regret'],
                total_utility_width=float((hi-lo).sum())))
        bounds.extend(dict(scenario=name, city=c, indicator=n, lower=lo[i,j], upper=hi[i,j])
                      for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    all_ranks = pd.concat(frames, ignore_index=True)
    all_ranks.to_csv(OUT/'ranks.csv', index=False)
    all_ranks[all_ranks.weight_reference=='inherited'].to_csv(OUT/'baseline_ranks.csv', index=False)
    pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv', index=False)
    lo, hi = evidence_bounds()
    result = dict(model_version='V113', baseline_model='V108', scenarios=reports,
        bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),
        unchanged_cells=248, weights_unchanged=True, transforms_unchanged=True,
        new_highschool_travel_observations=0,
        source_observations={k:hashlib.sha256((ROOT/f'data/task4_v113_{k}/observation.json').read_bytes()).hexdigest()
                             for k in ['singapore','tokyo']},
        scope='Tokyo is a national recorded-criminal-death superset bound, not observed city homicide or unreported/resident mortality. Strict Tokyo arm retains [0,1]. Singapore is a partial recognized-HE inventory, not quality or access.')
    (OUT/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(reports, indent=2))
    return result

def compare_monte_carlo():
    old = pd.read_csv(ROOT/'results/task4_v112_ahp_mc/monte_carlo_city_summary.csv')
    new = pd.read_csv(ROOT/'results/task4_v113_ahp_mc/monte_carlo_city_summary.csv')
    merged = old.merge(new, on=['center','concentration','city'], suffixes=('_before','_after'), validate='one_to_one')
    assert len(merged) == 150
    merged.to_csv(ROOT/'results/task4_v113_ahp_mc/comparison_v112.csv', index=False)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare-mc', action='store_true')
    args = parser.parse_args()
    if args.compare_mc:
        compare_monte_carlo()
    else:
        run()

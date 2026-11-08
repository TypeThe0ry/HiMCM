"""Istanbul verified facility subsets; unchanged weights and missing travel."""
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v113_evidence_revision import evidence_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize

OUT = ROOT/'results/task4_v114_istanbul_revision'
DATA = ROOT/'data/task4_v114_istanbul_facilities'

def istanbul_bounds(transit=True, pools=True):
    lo, hi = evidence_bounds()
    for item in json.loads((DATA/'manifest.json').read_text()):
        assert hashlib.sha256((DATA/item['file']).read_bytes()).hexdigest() == item['sha256']
    enabled = {'public_transport_density': transit, 'public_pool_density': pools}
    rows = json.loads((DATA/'observations.json').read_text())
    assert len(rows) == 2 and {r['indicator'] for r in rows} == set(enabled)
    for r in rows:
        if not enabled[r['indicator']]:
            continue
        assert r['city'] == 'Istanbul' and r['lower_bound_only']
        i, j = CITIES.index(r['city']), NAMES.index(r['indicator'])
        np.testing.assert_array_equal([lo[i,j],hi[i,j]], r['utility_before'])
        density = r['raw_count']*100000/r['population']
        expected = density/(r['utility_anchor']+density)
        np.testing.assert_allclose(r['utility_after'], [expected,1], rtol=0, atol=1e-15)
        lo[i,j], hi[i,j] = r['utility_after']
    return lo, hi

def run():
    OUT.mkdir(exist_ok=True)
    base = evidence_bounds()
    frames, bounds, reports = [], [], []
    cases = [('v113',base),('transit_only',istanbul_bounds(pools=False)),
             ('pools_only',istanbul_bounds(transit=False)),('v114',istanbul_bounds())]
    for label,(lo,hi) in cases:
        assert np.all(lo>=base[0]) and np.array_equal(hi,base[1])
        for ref,w in [('inherited',weights(.1)),('equal',np.ones(10)/10)]:
            old,_ = summarize(*base,w)
            frame,d = summarize(lo,hi,w)
            frame['previous_decision_rank'] = old.decision_rank
            frame['rank_change_positive_improves'] = old.decision_rank-frame.decision_rank
            frames.append(frame.assign(scenario=label,weight_reference=ref))
            reports.append(dict(scenario=label,weight_reference=ref,
                changed_cells=int(np.count_nonzero(lo!=base[0])),
                changed_ranks=int(np.count_nonzero(old.decision_rank!=frame.decision_rank)),
                kendall=float(kendalltau(old.decision_rank,frame.decision_rank).statistic),
                choice=[CITIES[k] for k in d['minimax_choices']],
                possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
                necessary_champions=frame.loc[frame.necessary_champion,'city'].tolist(),
                minimax_regret=d['minimax_regret'],
                mean_score_width=float((frame.score_upper-frame.score_lower).mean()),
                istanbul=frame[frame.city=='Istanbul'].iloc[0].to_dict()))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=lo[i,j],upper=hi[i,j])
            for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    all_ranks = pd.concat(frames,ignore_index=True)
    all_ranks.to_csv(OUT/'ranks.csv',index=False)
    all_ranks[all_ranks.weight_reference=='inherited'].to_csv(OUT/'baseline_ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False)
    result=dict(model_version='V114',baseline_model='V113',scenarios=reports,
        unchanged_cells=248,all_upper_bounds_unchanged=True,weights_and_transforms_unchanged=True,
        new_highschool_travel_observations=0,safety_and_education_unchanged=True,
        input_bounds_sha256=hashlib.sha256(np.stack(base).astype('<f8').tobytes()).hexdigest(),
        observation_sha256=hashlib.sha256((DATA/'observations.json').read_bytes()).hexdigest(),
        source_scope='2025 partial physical-stop and public-swimming-venue inventories. Upper bounds stay unknown. Facility supply is not actual student accessibility.')
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(reports,indent=2))

def compare_mc():
    old=pd.read_csv(ROOT/'results/task4_v113_ahp_mc/monte_carlo_city_summary.csv')
    new=pd.read_csv(ROOT/'results/task4_v114_ahp_mc/monte_carlo_city_summary.csv')
    out=old.merge(new,on=['center','concentration','city'],suffixes=('_before','_after'),validate='one_to_one')
    assert len(out)==150
    out.to_csv(ROOT/'results/task4_v114_ahp_mc/comparison_v113.csv',index=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compare-mc',action='store_true');args=parser.parse_args()
    compare_mc() if args.compare_mc else run()

"""Joint predeclared source-block information withdrawal, conditional on V204."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from task4_user_v204_revision import revised_bounds
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import NAMES, weights

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/current_v204_source_block_stress'
GROUPS = {
    'cost_housing': ('cost_living_index', 'price_income_ratio'),
    'broadband': ('fixed_broadband_mbps',),
    'pm': ('pm25',),
}
FIELDS = {'cost_living_index': 'cli', 'price_income_ratio': 'pir',
          'fixed_broadband_mbps': 'broadband_mbps', 'pm25': 'pm25_ugm3'}
EVIDENCE = {
    'cost_housing': 'results/current_cost_edition_review/edition_values.csv',
    'broadband': 'data/current_all16_broadband_fields/comparison.csv',
    'pm': 'data/task4_v117_team_intake/city_indicators.csv',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise RuntimeError('Output directory must be absent or empty')
    f, lo, hi = revised_bounds()
    cities = f.city.tolist()
    assert len(cities) == len(set(cities)) == 16 and lo.shape == hi.shape == (16, 10)
    # Bind to the saved current V204 case, including the Vienna refinement.
    saved = pd.read_csv(ROOT / 'results/task4_user_v204_revision/utility_bounds.csv')
    saved = saved[saved.scenario.eq('after_conditional')].set_index(['city', 'indicator'])
    assert len(saved) == 160 and saved.index.is_unique
    for i, city in enumerate(cities):
        for j, name in enumerate(NAMES):
            assert np.isclose(saved.loc[(city, name), 'lower'], lo[i, j], atol=1e-14, rtol=0)
            assert np.isclose(saved.loc[(city, name), 'upper'], hi[i, j], atol=1e-14, rtol=0)
    assert (f.pm25_ugm3_year == 2024).all() and (f.pm25_ugm3_flag == 'MODELLED').all()
    for group, cols in GROUPS.items():
        for name in cols:
            j = NAMES.index(name)
            assert np.array_equal(lo[:, j], hi[:, j]), (group, name)
    names = list(GROUPS)
    blocks = [tuple(c) for k in range(4) for c in combinations(names, k)]
    assert len(blocks) == 8
    ranks, bounds, cases, source_map = [], [], [], []
    bb = pd.read_csv(ROOT / EVIDENCE['broadband']).set_index('city')
    assert bb.index.is_unique and set(bb.index) == set(cities)
    for group, cols in GROUPS.items():
        for name in cols:
            j = NAMES.index(name); field = FIELDS[name]
            for i, city in enumerate(cities):
                row = dict(group=group, city=city, indicator=name, raw_column=field,
                           raw_value=float(f.iloc[i][field]), raw_year=str(f.iloc[i][field+'_year']),
                           raw_flag=str(f.iloc[i][field+'_flag']), retained_lower=float(lo[i,j]),
                           retained_upper=float(hi[i,j]), evidence_file=EVIDENCE[group],
                           source_interpretation=('Numbeo candidate publication series; original extraction lineage unconfirmed' if group == 'cost_housing' else
                                'Ookla four-field comparison; original extraction lineage unconfirmed' if group == 'broadband' else
                                'Original 2024 MODELLED PM column; publisher lineage unconfirmed'))
                if group == 'broadband':
                    row['field_match'] = bb.loc[city, 'exact_match_fields']
                source_map.append(row)
    assert len(source_map) == 64
    for block in blocks:
        label = '+'.join(block) if block else 'retained_V204'
        ll, hh = lo.copy(), hi.copy()
        mask = np.zeros(lo.shape, dtype=bool)
        for group in block:
            for name in GROUPS[group]: mask[:, NAMES.index(name)] = True
        ll[mask] = 0.; hh[mask] = 1.
        assert mask.sum() == sum(16 * len(GROUPS[g]) for g in block)
        assert np.array_equal(ll[~mask], lo[~mask]) and np.array_equal(hh[~mask], hi[~mask])
        bounds.extend(dict(case=label, city=c, indicator=n, lower=float(ll[i,j]), upper=float(hh[i,j]), withdrawn=bool(mask[i,j]))
                      for i,c in enumerate(cities) for j,n in enumerate(NAMES))
        for ref, w in [('fixed', weights(.1)), ('equal', np.full(10, .1))]:
            t = evaluate(cities, ll, hh, w).drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank'])
            ranks.append(t.assign(case=label, weight_reference=ref))
            choices = t.loc[t.decision_rank.eq(1), 'city'].tolist()
            cases.append(dict(case=label, groups=list(block), withdrawn_points=int(mask.sum()), weight_reference=ref,
                              choices=choices, choice_max_regret=float(t.loc[t.decision_rank.eq(1), 'max_regret'].iloc[0]),
                              mean_width=float((t.score_upper-t.score_lower).mean()),
                              possible_champions=int(t.possible_champion.sum()), necessary_champions=int(t.necessary_champion.sum())))
    minimal = {}
    for ref in ('fixed','equal'):
        relevant = [c for c in cases if c['weight_reference'] == ref]
        baseline = relevant[0]['choices']
        changed = [c for c in relevant if c['choices'] != baseline]
        minimal[ref] = [c['groups'] for c in changed if not any(set(d['groups']) < set(c['groups']) for d in changed)]
        for c in relevant: c['choice_changed_from_retained'] = c['choices'] != baseline
    OUT.mkdir(parents=True, exist_ok=True)
    pd.concat(ranks, ignore_index=True).to_csv(OUT/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(OUT/'bounds.csv',index=False)
    pd.DataFrame(source_map).to_csv(OUT/'source_map.csv',index=False)
    manifest = dict(version='V204', group_definitions={g:dict(indicators=list(v), point_count=16*len(v), evidence=EVIDENCE[g]) for g,v in GROUPS.items()},
                    combinations=[dict(case='+'.join(b) if b else 'retained_V204', groups=list(b), indicators=[n for g in b for n in GROUPS[g]], withdrawn_points=sum(16*len(GROUPS[g]) for g in b), weight_references=['fixed','equal']) for b in blocks],
                    weight_references={ref:dict(zip(NAMES, map(float,w))) for ref,w in [('fixed', weights(.1)), ('equal', np.full(10,.1))]},
                    construction='Selected point utility intervals replaced with [0,1]; all other V204 bounds, anchors, weights, and decision rules unchanged.',
                    evidence_qualification='Candidate source groupings only: original CSV extraction lineage is unconfirmed. No verified shared source, common error, joint physical plausibility, error tolerance, or failure probability is assumed.',
                    prior_single_group_work='PM block withdrawal, broadband field alternative and cost edition alternatives were V203 analyses; this is a V204 joint information-withdrawal analysis, not a rerun of V203.')
    (OUT/'case_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    paths=[SOURCE,Path(__file__),ROOT/'results/task4_user_v204_revision/utility_bounds.csv',ROOT/'design/task4_user_v204_admissions.json']+[ROOT/p for p in EVIDENCE.values()]
    summary=dict(version='V204', cases=cases, inclusion_minimal_choice_changing_group_sets=minimal,
                 rank_rows=256, bounds_rows=1280, source_map_rows=64, primary_admissions=0, actual_primary_width_reduction=0,
                 interpretation='Stress of complete information withdrawal over predefined blocks. [0,1] is the anchored utility domain; rectangular cross-city extremes are not assumed physically joint or probable. Inclusion-minimal sets are defined among these three blocks, not an error tolerance or real-world failure probability. No new data, primary change, manuscript edit, or primary interval narrowing.',
                 input_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths},
                 output_sha256={n:sha(OUT/n) for n in ('ranks.csv','bounds.csv','source_map.csv','case_manifest.json')})
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(dict(cases=cases,minimal=minimal),indent=2))

if __name__ == '__main__': main()

"""Verified cross-city evidence, keeping V114 weights and missing rules fixed."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v114_istanbul_revision import istanbul_bounds
from task4_v5_model import ROOT, CITIES, NAMES, SPEC, weights, summarize

OUT = ROOT / 'results/task4_v117_city_revision'
ADMISSIONS = ROOT / 'design/task4_v117_admissions.json'

def revised_bounds(selected=None, baseline=None):
    lo, hi = (a.copy() for a in (istanbul_bounds() if baseline is None else baseline))
    base = np.stack([lo, hi]).copy()
    used = set()
    for record in json.loads(ADMISSIONS.read_text()):
        source = ROOT / record['observations']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256']
        for path, digest in record['source_hashes'].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest
        for r in json.loads(source.read_text()):
            if selected is not None and r['city'] not in selected and (r['city'],r['indicator']) not in selected:
                continue
            i, j = CITIES.index(r['city']), NAMES.index(r['indicator'])
            assert r['city'] != 'Istanbul' and (i,j) not in used
            used.add((i,j))
            np.testing.assert_allclose([lo[i,j],hi[i,j]], r['utility_before'], rtol=0, atol=1e-12)
            x = r['raw_count'] * 100000 / r['population']
            _, benefit, anchor, _ = SPEC[j]
            if benefit:
                assert r['lower_bound_only']
                expected = [x/(anchor+x),hi[i,j]]
            elif r.get('upper_bound_only',False) or r.get('raw_rate_upper_bound_only',False):
                expected = [anchor/(anchor+x),hi[i,j]]
            else:
                assert r.get('point_observation',False)
                expected = [anchor/(anchor+x)]*2
            np.testing.assert_allclose(expected,r['utility_after'],rtol=0,atol=1e-12)
            lo[i,j],hi[i,j] = expected
    assert np.all(lo >= base[0]) and np.all(hi <= base[1]) and np.all(lo <= hi)
    np.testing.assert_array_equal(np.stack([lo,hi])[:,CITIES.index('Istanbul')],base[:,CITIES.index('Istanbul')])
    return lo,hi

def run():
    OUT.mkdir(exist_ok=True)
    base=istanbul_bounds()
    cities=sorted({r['city'] for item in json.loads(ADMISSIONS.read_text()) for r in json.loads((ROOT/item['observations']).read_text())})
    cells=[(r['city'],r['indicator']) for item in json.loads(ADMISSIONS.read_text()) for r in json.loads((ROOT/item['observations']).read_text())]
    cases=[('v114',base)]+[(':'.join(cell),revised_bounds({cell},base)) for cell in cells]+[('v117',revised_bounds(baseline=base)),('withdrawal',revised_bounds(set(),base))]
    frames=[];reports=[];bounds=[]
    for label,(lo,hi) in cases:
        changed=(lo!=base[0])|(hi!=base[1])
        if label=='withdrawal':np.testing.assert_array_equal(np.stack([lo,hi]),np.stack(base))
        for ref,w in [('inherited',weights(.1)),('equal',np.ones(10)/10)]:
            old,_=summarize(*base,w);frame,d=summarize(lo,hi,w)
            frame['previous_decision_rank']=old.decision_rank
            frame['rank_change_positive_improves']=old.decision_rank-frame.decision_rank
            frame['score_width_before']=old.score_upper-old.score_lower
            frame['score_width']=frame.score_upper-frame.score_lower
            frames.append(frame.assign(scenario=label,weight_reference=ref))
            reports.append(dict(scenario=label,weight_reference=ref,changed_cells=int(changed.sum()),
                kendall_tau_b=float(kendalltau(old.decision_rank,frame.decision_rank).statistic),
                possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
                choice=[CITIES[k] for k in d['minimax_choices']],
                mean_score_width=float(frame.score_width.mean()),
                changed_city_rows=frame.loc[frame.city.isin(cities)].to_dict('records')))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=lo[i,j],upper=hi[i,j]) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    allr=pd.concat(frames,ignore_index=True)
    allr.to_csv(OUT/'ranks.csv',index=False)
    allr[allr.weight_reference=='inherited'].to_csv(OUT/'baseline_ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False)
    result=dict(model_version='V117',baseline='V114',weights_and_rules_unchanged=True,istanbul_unchanged=True,
        scope='Conditional administrative evidence; facility inventories are supply, not teenage access. Toronto crime-classification superset is a conditional reported-crime bound.',scenarios=reports)
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([r for r in reports if r['scenario']=='v117'],indent=2))

if __name__=='__main__':run()

"""Controlled Singapore mean-to-median alternative; original user16 V203 retained."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES, weights

R = Path(__file__).resolve().parents[1]
O = R / 'results/current_all16_broadband_review'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    source = R / 'data/task4_v5_resources/ookla_global_index.html'
    raw = source.read_text(); data = json.JSONDecoder().raw_decode(raw.split('var results = ', 1)[1])[0]
    median = next(x for x in data['fixedMedian'] if x['country']['country_code'] == 'SG')
    mean = next(x for x in data['fixedMean'] if x['country']['country_code'] == 'SG')
    assert median['download_mbps'] == '476.02' and mean['download_mbps'] == '667.71'
    f, low, high = revised_bounds(); cities = f.city.tolist(); assert len(cities) == 16
    i = cities.index('Singapore'); j = NAMES.index('fixed_broadband_mbps')
    changed_low = low.copy(); changed_high = high.copy()
    changed_low[i,j] = changed_high[i,j] = float(median['download_mbps']) / (100 + float(median['download_mbps']))
    mask = np.ones(low.shape, dtype=bool); mask[i,j] = False
    assert np.array_equal(changed_low[mask], low[mask]) and np.array_equal(changed_high[mask], high[mask])
    cases = []; tables = []; bounds = []
    for scenario, ll, hh in [('retained_V203', low, high), ('Singapore_median_alternative', changed_low, changed_high)]:
        bounds.extend(dict(scenario=scenario,city=city,indicator=name,lower=float(ll[a,b]),upper=float(hh[a,b]))
                      for a,city in enumerate(cities) for b,name in enumerate(NAMES))
        for reference, w in [('fixed', weights(.1)), ('equal', np.full(10,.1))]:
            t = evaluate(cities,ll,hh,w)
            tables.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(scenario=scenario,weight_reference=reference))
            sg = t[t.city.eq('Singapore')].iloc[0]
            cases.append(dict(scenario=scenario,weight_reference=reference,
                recommendations=t.loc[t.decision_rank.eq(1),'city'].tolist(),
                possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),
                mean_width=float((t.score_upper-t.score_lower).mean()),
                Singapore=dict(score_lower=float(sg.score_lower),score_upper=float(sg.score_upper),max_regret=float(sg.max_regret),decision_rank=int(sg.decision_rank))))
    contrasts = []
    for reference in ['fixed','equal']:
        before = next(x for x in cases if x['scenario']=='retained_V203' and x['weight_reference']==reference)
        after = next(x for x in cases if x['scenario']=='Singapore_median_alternative' and x['weight_reference']==reference)
        ranks = [t.set_index('city').decision_rank for t in tables if t.weight_reference.iloc[0]==reference]
        contrasts.append(dict(weight_reference=reference,decision_rank_changes=int((ranks[0]!=ranks[1]).sum()),
            Singapore_lower_change=after['Singapore']['score_lower']-before['Singapore']['score_lower'],
            Singapore_upper_change=after['Singapore']['score_upper']-before['Singapore']['score_upper'],
            mean_width_change=after['mean_width']-before['mean_width'],recommendation_changed=before['recommendations']!=after['recommendations']))
    O.mkdir(exist_ok=True)
    pd.concat(tables,ignore_index=True).to_csv(O/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(O/'bounds.csv',index=False)
    summary = dict(primary_model='V203 unchanged',scenario='Only Singapore broadband point uses the matching fixed-median field in a temporary copy',
        original_value=667.71,alternative_value=476.02,original_utility=float(low[i,j]),alternative_utility=float(changed_low[i,j]),
        changed_cells=1,other159cells_unchanged=True,rank_rows=64,bound_rows=320,cases=cases,contrasts=contrasts,
        primary_admissions=0,actual_primary_width_reduction=0,
        source_sha256={str(p.relative_to(R)):sha(p) for p in [source,R/'data/task4_v5_resources/manifest.json',R/'data/task4_v117_team_intake/city_indicators.csv',R/'data/current_all16_broadband_fields/comparison.csv',R/'data/current_all16_broadband_fields/summary.json',Path(__file__)]},
        output_sha256={name:sha(O/name) for name in ['bounds.csv','ranks.csv']},
        scope='Statistic-definition sensitivity, not a primary correction, new observation, missing-data admission, uncertainty reduction, original extraction lineage or geographic harmonization. Same fixed ideal points, weights and all other ranges retained. No Monte Carlo replay or future forecast.')
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'rank_rows':64,'bound_rows':320,'contrasts':contrasts}))

if __name__ == '__main__': main()

"""User-supplied 16-city scenario; offline, original values and missing bounds retained."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import SPEC, NAMES, weights, score
from task4_interval_decision import interval_decision

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/task4_v117_team_intake/city_indicators.csv'
OUT = ROOT/'results/task4_user_city_indicators'
FIELDS = ['homicide_per_100k', 'pm25_ugm3', 'cli', 'pir',
          'pupil_teacher_ratio', 'he_per_million', None, 'commute_min',
          'broadband_mbps', 'pools_per_100k']


def build(frame):
    """Map submitted measurements without filtering flags or imputing missing cells."""
    lo = np.zeros((len(frame), len(SPEC)))
    hi = np.ones_like(lo)
    audit = []
    for i, row in frame.reset_index(drop=True).iterrows():
        for j, (name, benefit, anchor, _) in enumerate(SPEC):
            field = FIELDS[j]
            raw = row[field] if field else np.nan
            mapped = np.nan
            rule = 'missing retained as [0,1]'
            if field is None:
                rule = 'transit share is not stop density; retained as [0,1]'
            elif pd.notna(raw):
                x = float(raw)
                if not np.isfinite(x) or x < 0:
                    raise ValueError(f'Invalid nonnegative value: {row.city}, {field}')
                mapped = x / 10 if field == 'he_per_million' else x
                if field == 'commute_min':
                    lo[i,j] = np.exp(-x/30)
                    rule = 'submitted commute mean: Jensen lower exp(-mean/30), upper 1'
                else:
                    lo[i,j] = hi[i,j] = mapped/(anchor+mapped) if benefit else anchor/(anchor+mapped)
                    rule = 'benefit x/(a+x)' if benefit else 'cost a/(a+x)'
                    if field == 'he_per_million':
                        rule = 'per-million / 10 to per-100000; ' + rule
            audit.append(dict(city=row.city, indicator=name, input_field=field,
                              submitted_value=raw, mapped_value=mapped,
                              submitted_flag=row.get(f'{field}_flag') if field else None,
                              submitted_year=row.get(f'{field}_year') if field else None,
                              utility_lower=lo[i,j], utility_upper=hi[i,j], rule=rule))
    assert np.all((0 <= lo) & (lo <= hi) & (hi <= 1))
    return lo, hi, pd.DataFrame(audit)


def evaluate(cities, lo, hi, w):
    lower, upper = score(lo,w), score(hi,w)
    d = interval_decision(lower, upper)
    frame = pd.DataFrame(dict(city=cities, score_lower=lower, score_upper=upper,
        best_rank=d['best_rank'], worst_rank=d['worst_rank'],
        possible_champion=d['possible_champion'], necessary_champion=d['necessary_champion'],
        max_regret=d['max_regret']))
    frame['decision_rank'] = frame.max_regret.rank(method='min').astype(int)
    frame['midpoint_illustrative_score'] = score((lo+hi)/2,w)
    frame['midpoint_illustrative_rank'] = frame.midpoint_illustrative_score.rank(ascending=False,method='min').astype(int)
    assert np.all(frame.midpoint_illustrative_score >= lower-1e-10)
    assert np.all(frame.midpoint_illustrative_score <= upper+1e-10)
    return frame


def main():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    source = pd.read_csv(SOURCE)
    assert source.city.is_unique and len(source) >= 2
    lo,hi,audit = build(source)
    OUT.mkdir(parents=True,exist_ok=True)
    audit.to_csv(OUT/'utility_bounds.csv',index=False)
    summaries = {}
    all_results = []
    ws = {'fixed': weights(.1), 'equal': np.ones(len(SPEC))/len(SPEC)}
    for reference,w in ws.items():
        assert np.isclose(w.sum(),1)
        frame = evaluate(source.city.tolist(),lo,hi,w)
        frame.to_csv(OUT/f'{reference}_ranks.csv',index=False)
        all_results.append(frame.assign(weight_reference=reference))
        summaries[reference] = dict(
            possible_champions=frame.loc[frame.possible_champion,'city'].tolist(),
            necessary_champions=frame.loc[frame.necessary_champion,'city'].tolist(),
            minimax_choices=frame.loc[frame.decision_rank==1,'city'].tolist(),
            midpoint_illustrative_first=frame.loc[frame.midpoint_illustrative_rank==1,'city'].tolist(),
            mean_score_interval_width=float((frame.score_upper-frame.score_lower).mean()))
    pd.concat(all_results,ignore_index=True).to_csv(OUT/'all_ranks.csv',index=False)
    pd.DataFrame(dict(indicator=NAMES, fixed=ws['fixed'], equal=ws['equal'])).to_csv(OUT/'weights.csv',index=False)
    summary = dict(input=str(SOURCE.relative_to(ROOT)), input_sha256=digest, cities=len(source),
        criteria=len(SPEC), uninformative_cells=int(np.sum((hi-lo)==1)),
        point_cells=int(np.sum(lo==hi)), partial_interval_cells=int(np.sum((hi>lo)&(hi-lo<1))),
        flags_used_for_exclusion=False, original_25_city_registry_changed=False, results=summaries)
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    assert digest == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()

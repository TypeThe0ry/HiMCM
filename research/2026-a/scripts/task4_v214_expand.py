"""V214: extend the V207/V208 model from 16 to 43 cities (27 new cities from public sources).

New-city utilities follow the same rules as task4_user_city_indicators.build; a gap
left after the targeted search takes the median utility of the cities that have the
value (flag 'median_fill'). Cities with two or more gaps after the search are excluded.
"""
import json
import os
import numpy as np
import pandas as pd
import task4_v207_ahp as V
from task4_v5_model import ROOT, NAMES, SPEC

DATA = ROOT / 'data/task4_v214_expand'
MIN_POP = float(os.environ.get('HIMCM_MIN_POP', '0'))  # TT 15 Nov: UN Degree of Urbanisation 'city' definition; all candidates qualify
DROP = [c for c in os.environ.get('HIMCM_DROP', '').split(',') if c]
KEEP = ['Shanghai']  # TT 15 Nov: keep Shanghai, fill remaining gaps
OUT = ROOT / os.environ.get('HIMCM_OUT', 'results/task4_v214_final')
FIELD = {'homicide_rate': 'homicide_per_100k', 'pm25': 'pm25_ugm3', 'cost_living_index': 'cli',
         'price_income_ratio': 'pir', 'upper_secondary_ptr': 'pupil_teacher_ratio', 'research_he_density': 'he_per_million',
         'public_transport_density': 'public_transport_density_per_100k', 'travel': 'commute_min',
         'fixed_broadband_mbps': 'broadband_mbps', 'public_pool_density': 'pools_per_100k'}
_bounds16 = V.bounds


def new_frame():
    m = pd.read_csv(DATA / 'new_cities_filled.csv')
    gaps = m[[FIELD[n] for n in NAMES]].isna().sum(1)
    small = m.population.astype(float) < MIN_POP
    out = ((gaps >= 2) & ~m.city.isin(KEEP)) | small | m.city.isin(DROP)
    return m[~out].reset_index(drop=True), m.loc[out, 'city'].tolist(), dict(zip(m.city, gaps))


def bounds_all(override=True, fill=True):
    f16, lo16, hi16 = _bounds16(override=override, fill=fill)
    m, _, _ = new_frame()
    n = len(m); lo = np.zeros((n, 10)); hi = np.ones((n, 10)); filled = []
    for j, (name, benefit, anchor, _) in enumerate(SPEC):
        col = FIELD[name]
        for i, row in m.iterrows():
            x = row[col]
            if pd.isna(x):
                continue
            x = float(x)
            if name == 'travel':
                lo[i, j], hi[i, j] = np.exp(-x / 30), 1.0
                continue
            if name == 'research_he_density':
                x = x / 10  # per million -> per 100,000
            u = x / (anchor + x) if benefit else anchor / (anchor + x)
            lo[i, j] = u
            hi[i, j] = 1.0 if (name == 'public_transport_density' and str(row.get(col + '_flag')) == 'lower_bound') else u
    all_lo, all_hi = np.vstack([lo16, lo]), np.vstack([hi16, hi])
    for j in range(10):  # median fill for remaining single gaps
        col = FIELD[SPEC[j][0]]
        miss = m[col].isna().to_numpy()
        if miss.any():
            known = np.r_[np.ones(len(lo16), bool), ~miss]
            med = float(np.median((all_lo[known, j] + all_hi[known, j]) / 2))
            for i in np.where(miss)[0]:
                all_lo[len(lo16) + i, j] = all_hi[len(lo16) + i, j] = med; filled.append((m.city[i], SPEC[j][0]))
    keep = [c for c in f16.columns if c in m.columns]
    f = pd.concat([f16, m[keep]], ignore_index=True)
    bounds_all.median_filled = filled
    return f, all_lo, all_hi


def cases_all():
    f16, cases = V.controlled_cases_orig()
    _, lo, hi = bounds_all()
    out = []
    for label, a, b in cases:
        out.append((label, np.vstack([a, lo[len(a):]]), np.vstack([b, hi[len(b):]])))
    return f16, out


if __name__ == '__main__':
    V.controlled_cases_orig = V.controlled_cases
    V.bounds = bounds_all
    V.controlled_cases = cases_all
    V.OUT = OUT
    OUT.mkdir(parents=True, exist_ok=True)
    V.main()
    _, excl, gaps = new_frame()
    s = json.loads((OUT / 'summary.json').read_text())
    s['expansion'] = dict(excluded=excl, gaps_after_search=gaps, median_filled=bounds_all.median_filled)
    (OUT / 'summary.json').write_text(json.dumps(s, indent=1, default=float))
    print('excluded', excl); print('median filled', bounds_all.median_filled)

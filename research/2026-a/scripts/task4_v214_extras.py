"""V214 extras on 43 cities: family profiles, must-have thresholds, Mercer comparison."""
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import task4_v207_ahp as V
import task4_v214_expand as E
from task4_v5_model import NAMES, score

OUT = E.OUT
f, lo, hi = E.bounds_all(); w, _ = V.ahp_weights(); mid = (lo + hi) / 2; cities = f.city.tolist()
PROFILES = {'safety-first': {(0, 1): 5, (0, 2): 3, (0, 3): 5, (0, 4): 7, (1, 2): 1, (1, 3): 1, (1, 4): 2, (2, 3): 1, (2, 4): 2, (3, 4): 2},
            'budget-first': {(0, 1): 1 / 2, (0, 2): 1, (0, 3): 2, (0, 4): 3, (1, 2): 2, (1, 3): 3, (1, 4): 5, (2, 3): 2, (2, 4): 3, (3, 4): 2},
            'independent-mobility': {(0, 1): 1, (0, 2): 1, (0, 3): 1 / 2, (0, 4): 2, (1, 2): 1, (1, 3): 1 / 2, (1, 4): 2, (2, 3): 1 / 2, (2, 4): 2, (3, 4): 4}}
prof = {}
for n, j in PROFILES.items():
    cw, lam, ci, cr = V.ahp(V.matrix(5, j)); ww = np.zeros(10)
    for k, (name, ms) in enumerate(V.CATEGORIES):
        lw, *_ = V.ahp(V.matrix(2, {(0, 1): V.WITHIN[name]}))
        for m_, v in zip(ms, lw):
            ww[NAMES.index(m_)] = cw[k] * v
    s = score(mid, ww); o = np.argsort(-s)
    prof[n] = dict(category_weights=dict(zip([x for x, _ in V.CATEGORIES], np.round(cw, 3).tolist())), CR=round(float(cr), 4),
                   top5=[(cities[i], round(float(s[i]), 1)) for i in o[:5]])
(OUT / 'profiles.json').write_text(json.dumps(prof, indent=1))
raw = f.set_index('city')
hom = raw.homicide_per_100k.astype(float).copy(); hom['Zurich'] = V.ZURICH_HOMICIDE; hom['Amsterdam'] = V.AMSTERDAM_HOMICIDE
vals = {'homicide': hom, 'pm25': raw.pm25_ugm3.astype(float), 'pir': raw.pir.astype(float)}
gates = [('homicide', 3.0), ('pm25', 25.0), ('pir', 20.0)]
fail = {c: [k for k, t in gates if pd.notna(vals[k][c]) and vals[k][c] > t] for c in cities}
s = score(mid, w); order = [cities[i] for i in np.argsort(-s)]
feas = [c for c in order if not fail[c]]
(OUT / 'gate_revision.json').write_text(json.dumps(dict(gates=gates, excluded={c: v for c, v in fail.items() if v}, feasible_order=feas), indent=1))
mer = json.loads((V.OUT.parent / 'task4_v207_ahp/external_mercer.json').read_text())['mercer_rank']
rank = {c: i + 1 for i, c in enumerate(order)}
cc = [c for c in mer if c in rank]
r = spearmanr([rank[c] for c in cc], [mer[c] for c in cc])
(OUT / 'external_mercer.json').write_text(json.dumps(dict(mercer_rank=mer, our_rank={c: rank[c] for c in cc}, spearman=r.statistic, p=r.pvalue), indent=1))
print(json.dumps(prof, indent=0)[:900]); print('excluded', {c: v for c, v in fail.items() if v}); print('feasible top5', feas[:5]); print('mercer', r)

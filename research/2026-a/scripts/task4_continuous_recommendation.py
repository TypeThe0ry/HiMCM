"""Bound minimax regret throughout an alpha interval, retaining unresolved leaves.

For fixed utility, squared positive/negative distances are affine in alpha.
Their ratio is monotone (or constant), so score extrema occur at endpoints.
This supplies interval bounds, rather than a grid-only stability assertion.
"""
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, CITIES, score, weights, summarize
from task4_saopaulo_age_revision import saopaulo_age_bounds


def regret_enclosure(lo, hi, a, b, padding=1e-9):
    ls = np.array([score(lo, weights(x)) for x in (a, b)])
    us = np.array([score(hi, weights(x)) for x in (a, b)])
    lmin, lmax = ls.min(axis=0)-padding, ls.max(axis=0)+padding
    umin, umax = us.min(axis=0)-padding, us.max(axis=0)+padding
    low = np.array([max(0., np.delete(umin, i).max()-lmax[i]) for i in range(len(lo))])
    high = np.array([max(0., np.delete(umax, i).max()-lmin[i]) for i in range(len(lo))])
    return low, high


def certify(lo, hi, alpha_min=.05, alpha_max=.2, max_depth=16):
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    if (lo.ndim != 2 or lo.shape != hi.shape or lo.shape[1] != 10 or len(lo) < 2
        or not np.isfinite(lo).all() or not np.isfinite(hi).all()
        or not np.all((0 <= lo) & (lo <= hi) & (hi <= 1))):
        raise ValueError('Ordered finite city-by-ten utility bounds required')
    if not 0 < alpha_min <= alpha_max < 1 or not 0 <= max_depth <= 20:
        raise ValueError('Interior alpha range and depth 0..20 required')
    pending = [(alpha_min, alpha_max, 0)]
    leaves = []
    while pending:
        a, b, depth = pending.pop()
        low, high = regret_enclosure(lo, hi, a, b)
        margins = np.array([np.delete(low, i).min()-high[i] for i in range(len(lo))])
        winner = int(np.argmax(margins))
        if margins[winner] > 1e-8:
            leaves.append(dict(alpha_lower=a, alpha_upper=b, certified=True,
                               winner=winner, regret_gap_lower=float(margins[winner]), depth=depth))
        elif depth == max_depth or a == b:
            leaves.append(dict(alpha_lower=a, alpha_upper=b, certified=False,
                               winner=None, regret_gap_lower=None, depth=depth))
        else:
            m = (a+b)/2
            pending.extend([(m,b,depth+1), (a,m,depth+1)])
    return sorted(leaves, key=lambda r:r['alpha_lower'])


def checks():
    rng = np.random.default_rng(501)
    for _ in range(20):
        lo = rng.uniform(0, .5, (4,10)); hi = lo+rng.uniform(0,.5,(4,10))
        lower, upper = regret_enclosure(lo,hi,.05,.2)
        for a in rng.uniform(.05,.2,30):
            ls,us=score(lo,weights(a)),score(hi,weights(a))
            actual=np.array([max(0,np.delete(us,i).max()-ls[i]) for i in range(4)])
            assert np.all(lower <= actual) and np.all(actual <= upper)
    # Ties and unresolved crossings must not be called unique recommendations.
    tied=np.full((2,10),.5)
    assert not any(r['certified'] for r in certify(tied,tied,max_depth=2))
    switching=np.array([[.9]*10,[.1]*10])
    switching[0,[6,9]]=.1; switching[1,[6,9]]=.9
    leaves=certify(switching,switching,.1,.9,max_depth=8)
    assert {r['winner'] for r in leaves if r['certified']} == {0,1}
    assert any(not r['certified'] for r in leaves)
    dominant=np.array([[.8]*10,[.2]*10])
    assert certify(dominant,dominant)[0]['winner']==0


def main():
    checks()
    lo,hi=saopaulo_age_bounds()
    leaves=certify(lo,hi)
    for row in leaves:
        row['city']=None if row['winner'] is None else CITIES[row['winner']]
    out=ROOT/'results/task4_v50_continuous_recommendation';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(leaves).to_csv(out/'certified_intervals.csv',index=False)
    rank,decision=summarize(lo,hi,weights())
    old=pd.read_csv(ROOT/'results/task4_v49_evidence_audit/ranks.csv')
    for col in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(rank[col],old[col],rtol=0,atol=1e-12)
    rank.to_csv(out/'ranks.csv',index=False)
    summary=dict(baseline='V48; V49 evidence retained',admitted_cells_changed=0,
        alpha_range=[.05,.2],certified_leaves=sum(r['certified'] for r in leaves),
        unresolved_leaves=sum(not r['certified'] for r in leaves),
        certified_winners=sorted({r['city'] for r in leaves if r['certified']}),
        minimum_certified_regret_gap=min((r['regret_gap_lower'] for r in leaves if r['certified']),default=None),
        score_roundoff_padding=1e-9,strict_gap_tolerance=1e-8,
        numerical_certificate_not_formal_interval_arithmetic=True,
        fixed_possible_champions=int(rank.possible_champion.sum()),main_admitted=False)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()

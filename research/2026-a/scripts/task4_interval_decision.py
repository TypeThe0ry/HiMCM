"""Exact fixed-preference decisions under independent city score intervals.

Ranks use competition ranking (1 + number strictly above), allowing tied winners.
Indicators need not have probability distributions. The single-indicator acquisition
calculation is deterministic value of perfect information, not expected utility.
"""
import numpy as np


def _arrays(lower, upper):
    lo, hi = np.asarray(lower, float), np.asarray(upper, float)
    if lo.ndim != 1 or lo.shape != hi.shape or len(lo) < 2:
        raise ValueError('Need matching 1D arrays for at least two cities')
    if not np.all(np.isfinite(lo)) or not np.all(np.isfinite(hi)) or np.any(lo > hi):
        raise ValueError('Score endpoints must be finite and ordered')
    return lo, hi


def interval_decision(lower, upper, tol=1e-12):
    """Sharp bounds when each city can independently attain its score interval.

    Closed intervals assumed. If an upper endpoint is only a supremum, the
    reported sets are conservative closures; boundary-only ties need care.
    """
    lo, hi = _arrays(lower, upper)
    n = len(lo)
    best, worst, possible, necessary, unique, regret = [], [], [], [], [], []
    for i in range(n):
        others = np.arange(n) != i
        best.append(1 + np.count_nonzero(lo[others] > hi[i]+tol))
        worst.append(1 + np.count_nonzero(hi[others] > lo[i]+tol))
        possible.append(hi[i] >= np.max(lo[others])-tol)
        necessary.append(lo[i] >= np.max(hi[others])-tol)
        unique.append(lo[i] > np.max(hi[others])+tol)
        regret.append(max(0., float(np.max(hi[others])-lo[i])))
    regret = np.asarray(regret)
    return dict(best_rank=np.asarray(best), worst_rank=np.asarray(worst),
                possible_champion=np.asarray(possible),
                necessary_champion=np.asarray(necessary),
                unique_necessary_champion=np.asarray(unique),
                max_regret=regret, minimax_regret=float(regret.min()),
                minimax_choices=np.flatnonzero(regret <= regret.min()+tol))


def voi_1d(callback, k, xlo, xhi, baseline=None, max_iterations=60):
    """Guaranteed/best-possible regret reduction from exactly observing one x.

    callback(x) -> (lower_scores, upper_scores), full city arrays after observing x.
    Only city k may change; both its score endpoints must be nondecreasing in x.
    This structural requirement is the caller's responsibility; finite probes catch
    obvious misuse but are not a monotonicity proof. Remaining indicators retain
    uncertainty. baseline=(lo,hi) may be supplied; otherwise infer the full envelope
    from endpoint callbacks. Values use the same score units as callback.

    Given monotonicity, choosing k has decreasing regret A(x); the best other action
    has increasing regret B(x). Post-information minimax regret min(A(x),B(x)) has
    its maximum at their crossing (or an endpoint), found by bisection. Its minimum
    lies at an endpoint. No assumed distribution of the missing x is introduced.
    """
    if not np.isfinite(xlo) or not np.isfinite(xhi) or xlo > xhi:
        raise ValueError('Invalid indicator interval')
    l0, h0 = _arrays(*callback(xlo))
    l1, h1 = _arrays(*callback(xhi))
    if not 0 <= k < len(l0):
        raise ValueError('Invalid city index')
    other = np.arange(len(l0)) != k
    if (not np.allclose(l0[other], l1[other], atol=1e-12, rtol=0) or
            not np.allclose(h0[other], h1[other], atol=1e-12, rtol=0) or
            l0[k] > l1[k]+1e-12 or h0[k] > h1[k]+1e-12):
        raise ValueError('Expected only city k to change monotonically')
    blo, bhi = _arrays(*(baseline if baseline is not None else (l0, h1)))
    before = interval_decision(blo, bhi)['minimax_regret']

    def components(x):
        lo, hi = _arrays(*callback(x))
        if (np.any(lo < blo-1e-10) or np.any(hi > bhi+1e-10) or
                not np.allclose(lo[other], l0[other], atol=1e-12, rtol=0) or
                not np.allclose(hi[other], h0[other], atol=1e-12, rtol=0)):
            raise ValueError('Post-observation set must be nested and other cities unchanged')
        rr = interval_decision(lo, hi)['max_regret']
        return float(rr[k]), float(np.min(rr[other]))

    def f(x):
        a, b = components(x)
        return a-b

    left, right = float(xlo), float(xhi)
    candidates = [left, right]
    iterations = 0
    if xlo != xhi and f(left) >= 0 >= f(right):
        for iterations in range(1, max_iterations+1):
            mid = (left+right)/2
            if mid == left or mid == right:
                break
            if f(mid) > 0:
                left = mid
            else:
                right = mid
        candidates.extend([left, right])
    post = np.asarray([min(components(x)) for x in candidates])
    worst = float(post.max())
    best = min(min(components(xlo)), min(components(xhi)))
    if worst > before+1e-9:
        raise AssertionError('Observing nested information cannot increase minimax regret')
    return dict(current_minimax_regret=float(before),
                worst_post_regret=worst, best_post_regret=float(best),
                guaranteed_gain=max(0., float(before-worst)),
                best_possible_gain=max(0., float(before-best)),
                worst_x=float(candidates[int(np.argmax(post))]),
                iterations=iterations, crossing_bracket_width=float(right-left))


def selfcheck():
    """Independent enumeration and grid tests, including ties and open-tail logic."""
    from itertools import product
    rng = np.random.default_rng(20261107)
    # Every extremal rank/regret can be witnessed at a corner of a rectangle.
    for _ in range(20):
        lo = rng.uniform(0, .7, 5)
        hi = lo+rng.uniform(0, 1-lo)
        dec = interval_decision(lo, hi)
        rankings, regrets = [], []
        for bits in product([0, 1], repeat=len(lo)):
            s = np.where(bits, hi, lo)
            rankings.append([1+np.sum(s > v+1e-12) for v in s])
            regrets.append(s.max()-s)
        ranks = np.asarray(rankings)
        assert np.array_equal(dec['best_rank'], ranks.min(axis=0))
        assert np.array_equal(dec['worst_rank'], ranks.max(axis=0))
        assert np.allclose(dec['max_regret'], np.max(regrets, axis=0))
    tied = interval_decision([.5,.5], [.5,.5])
    assert tied['necessary_champion'].all() and not tied['unique_necessary_champion'].any()
    assert np.array_equal(tied['best_rank'], [1,1])
    assert np.allclose(interval_decision([.9,.1], [1.,.2])['max_regret'], [0,.9])
    # Nonlinear score response with residual uncertainty after learning x.
    for _ in range(20):
        lo = rng.uniform(0, .7, 5)
        hi = lo+rng.uniform(0, 1-lo)
        k = int(rng.integers(len(lo)))
        def callback(x):
            ll, hh = lo.copy(), hi.copy()
            ll[k] = lo[k]+.35*(hi[k]-lo[k])*x*x
            hh[k] = lo[k]+(hi[k]-lo[k])*(.65+.35*x*x)
            return ll, hh
        result = voi_1d(callback, k, 0., 1.)
        brute = [interval_decision(*callback(x))['minimax_regret']
                 for x in np.linspace(0, 1, 501)]
        assert result['worst_post_regret'] >= max(brute)-1e-10
        assert result['worst_post_regret']-max(brute) < .002
        assert abs(result['best_post_regret']-min(brute)) < 1e-10
    print('PASS: 20 interval corner enumerations, tie/self checks, 20 nonlinear VOI grid checks')


if __name__ == '__main__':
    selfcheck()

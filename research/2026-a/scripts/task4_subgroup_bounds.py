"""Bound a latent subgroup's mean using histogram capacities, not parent means.

The subgroup may select any mass within each parent bin. Known subgroup mass
in [m0,m1] implies extremal trimmed means at m0. With no positive lower mass,
return support endpoint infimum/supremum. No distribution within bins assumed.
"""
import numpy as np


def subgroup_bounds(counts, utility_lower, utility_upper, mass_interval):
    counts, low, high = (np.asarray(x, dtype=float) for x in (counts, utility_lower, utility_upper))
    if (counts.ndim != 1 or not len(counts) or low.shape != counts.shape or high.shape != counts.shape
        or not np.isfinite([counts, low, high]).all() or np.any(counts < 0)
        or not np.all((0 <= low) & (low <= high) & (high <= 1))):
        raise ValueError('Nonnegative bin capacities and ordered utility endpoints required')
    mass = np.asarray(mass_interval, dtype=float)
    total = float(counts.sum())
    if (mass.shape != (2,) or not np.isfinite(mass).all()
        or not 0 <= mass[0] <= mass[1] <= total or mass[1] <= 0):
        raise ValueError('Nonempty feasible subgroup mass interval required')
    present = counts > 0
    if mass[0] == 0:
        return float(low[present].min()), float(high[present].max())

    def trim(values, maximize):
        order = np.argsort(values)
        if maximize: order = order[::-1]
        remaining = float(mass[0]); numerator = 0.
        for k in order:
            take = min(float(counts[k]), remaining)
            numerator += take * values[k]; remaining -= take
            if remaining <= 0: break
        assert remaining <= 1e-10 * max(1., total)
        return float(numerator / mass[0])

    return trim(low, False), trim(high, True)

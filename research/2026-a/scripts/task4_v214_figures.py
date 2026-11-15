"""V214 paper figures for the expanded (about 40-city) model.

Wraps task4_v207_figures (F): its bounds and result folder are pointed at the
expanded city set (task4_v214_expand, E) and the figures that cannot hold ~40
rows are redesigned here.  Output PDFs keep the V207 file names in
HiMCM-Overleaf/figures.  Run:  python task4_v214_figures.py [name ...]
"""
import json
import sys
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Ellipse
import task4_v207_ahp as V
import task4_v214_expand as E
import task4_v207_figures as F
from task4_v207_figures import INK, MUTED, GRID, SERIES, SPECTRUM, SHORT, CAT_SHORT, FIG
from task4_v207_flags import flag, COUNTRY
from task4_v5_model import ROOT, NAMES, score
from task4_v207_ahp import ahp_weights, CATEGORIES
from audit_task4_v203 import raw_map

# --- point the V207 figure code at the expanded model ---
V.bounds = E.bounds_all
F.bounds = E.bounds_all
F.RES = E.OUT
RES = E.OUT
bounds = E.bounds_all

# City colour convention for highlighted cities (TT 11-15).
CITY_COL = {'Luxembourg': '#00a3e0', 'Zurich': '#d52b1e', 'Macao SAR': '#1a9e5c', 'Reykjavik': '#6250d6', 'Madrid': '#e0a800'}
HL = ['Luxembourg', 'Zurich', 'Macao SAR', 'Reykjavik']  # weight-sensitivity highlights
GREY = '#c4c3bd'
TAGS = {'Luxembourg': 'Best all-round', 'Zurich': 'Close second', 'Macao SAR': 'Shortest trips', 'Reykjavik': 'Best mobility',
        'Madrid': 'Best value', 'Dubai': 'Best schools', 'Singapore': 'Safest streets'}


def top3(main):
    return main.city[:3].tolist()

COORDS = dict(F.COORDS)
COORDS.update({'New York': (40.71, -74.01), 'Los Angeles': (34.05, -118.24), 'Chicago': (41.88, -87.63),
               'San Francisco': (37.77, -122.42), 'Beijing': (39.90, 116.40), 'Shenzhen': (22.54, 114.06),
               'Guangzhou': (23.13, 113.26), 'Hong Kong SAR': (22.32, 114.17), 'Macao SAR': (22.20, 113.54),
               'New Delhi': (28.61, 77.21), 'Mumbai': (19.08, 72.88), 'Toronto': (43.65, -79.38),
               'Sao Paulo': (-23.55, -46.63), 'Mexico City': (19.43, -99.13), 'Buenos Aires': (-34.60, -58.38),
               'Copenhagen': (55.68, 12.57), 'Luxembourg': (49.61, 6.13), 'Reykjavik': (64.15, -21.94),
               'Dubai': (25.20, 55.27), 'Abu Dhabi': (24.45, 54.38), 'Istanbul': (41.01, 28.98),
               'Cairo': (30.04, 31.24), 'Johannesburg': (-26.20, 28.05), 'Nairobi': (-1.29, 36.82),
               'Seoul': (37.57, 126.98), 'Sydney': (-33.87, 151.21), 'Kuala Lumpur': (3.14, 101.69),
               'Shanghai': (31.23, 121.47)})


def data():
    return F.data()


# ----------------------------------------------------------------------------- city map
EU = (-13, 30, 35.5, 62.5)  # lon0, lon1, lat0, lat1 of the Europe inset


def _land(ax, shp, x0, x1, y0, y1):
    ax.set_facecolor('#d9e7f4')
    for s in shp.shapes():
        bx = s.bbox
        if bx[2] < x0 - 5 or bx[0] > x1 + 5 or bx[3] < y0 - 5 or bx[1] > y1 + 5:
            continue
        pts = np.array(s.points); parts = list(s.parts) + [len(pts)]
        for a, b in zip(parts[:-1], parts[1:]):
            ax.fill(pts[a:b, 0], pts[a:b, 1], color='#f8f7f3', ec='#b9b7ae', lw=.3)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect(1 / np.cos(np.radians((y0 + y1) / 2)))
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color('#c9c7bf'); sp.set_linewidth(.6)


def _label(ax, c, r, lon, lat, dx, dy, kx, ky, flagged=True, bold=False, col=INK, text=None):
    """Flag + 'City (rank)' (or `text`) next to a dot; dx, dy in inches, kx/ky degrees per inch."""
    ha = 'left' if dx > 0 else 'right'
    if text is None:
        text = f'{c} ({r})'
    fw, fh = .22 * kx, .15 * ky
    x = lon + dx * kx; y = lat + dy * ky
    if flagged:
        fx = x if dx > 0 else x - fw
        flag(ax, COUNTRY[c], fx, y - fh / 2, fw, fh)
        tx = fx + fw + .04 * kx if dx > 0 else fx - .04 * kx
    else:
        tx = x
    ax.text(tx, y, text, ha=ha, va='center', fontsize=9, color=col, weight='bold' if bold else 'normal', zorder=11)


def city_map(main):
    import shapefile
    shp = shapefile.Reader(str(ROOT / 'visuals/cartography/vector_data/ne_10m_land/ne_10m_land.shp'))
    rank = main.set_index('city')['rank']
    top10 = set(main.city[:10])
    W, H = 6.5, 5.3
    fig = plt.figure(figsize=(W, H))
    # world: equirectangular crop of the inhabited world
    axW = fig.add_axes([0, .485, 1, .515]); wx0, wx1, wy0, wy1 = -128, 158, -42, 70
    _land(axW, shp, wx0, wx1, wy0, wy1)
    fig.canvas.draw(); pos = axW.get_position()
    kx = (wx1 - wx0) / (pos.width * W); ky = (wy1 - wy0) / (pos.height * H)
    axW.add_patch(Rectangle((EU[0], EU[2]), EU[1] - EU[0], EU[3] - EU[2], fill=False, ec=INK, lw=.8, ls=(0, (3, 2)), zorder=12))
    n_eu = sum(EU[0] < lon < EU[1] and EU[2] < lat < EU[3] for c, (lat, lon) in COORDS.items() if c in rank.index)
    axW.text(EU[1] + .3 * kx, EU[2] + 2, f'Europe inset\n({n_eu} cities)', fontsize=9, color=INK, va='bottom', ha='left', zorder=12, linespacing=.95)
    offs = {'Reykjavik': (-.08, -.1), 'Macao SAR': (-.1, -.22), 'Singapore': (.1, -.08), 'Dubai': (-.1, .16), 'Abu Dhabi': (-.1, -.2)}
    noffs = {'Hong Kong SAR': (.06, -.06), 'Shenzhen': (.06, .06), 'Guangzhou': (-.06, .06), 'Toronto': (.04, .07), 'New York': (.06, -.04),
             'Chicago': (-.07, .0), 'San Francisco': (.05, .05), 'Los Angeles': (.05, -.06), 'Mexico City': (-.06, -.02),
             'Sao Paulo': (.06, 0), 'Buenos Aires': (-.06, -.02), 'Cairo': (-.06, .03), 'Istanbul': (-.06, .04), 'Johannesburg': (.06, 0),
             'Nairobi': (.06, 0), 'New Delhi': (.05, .0), 'Mumbai': (-.06, -.02), 'Beijing': (-.06, .04), 'Shanghai': (.06, .02),
             'Seoul': (.06, .04), 'Tokyo': (.06, -.02), 'Sydney': (-.06, 0), 'Kuala Lumpur': (-.06, .02)}
    for c, (lat, lon) in COORDS.items():
        if c not in rank.index:
            continue
        r = int(rank[c]); in_eu = EU[0] < lon < EU[1] and EU[2] < lat < EU[3]
        hot = c in top10
        axW.scatter(lon, lat, s=24 if hot else 11, color=SERIES[0] if hot else '#6e6d68', ec='white', lw=.6, zorder=10)
        if in_eu:
            continue
        if hot:
            dx, dy = offs[c]; _label(axW, c, r, lon, lat, dx, dy, kx, ky, bold=r <= 3)
            axW.plot([lon, lon + dx * kx * .85], [lat, lat + dy * ky * .85], color=MUTED, lw=.6, zorder=9)
        else:
            dx, dy = noffs.get(c, (.06, 0)); _label(axW, c, r, lon, lat, dx, dy, kx, ky, flagged=False, col=MUTED, text=str(r))
    axW.text(.008, .975, f'All {len(main)} cities', transform=axW.transAxes, va='top', fontsize=10, weight='bold', color=INK)
    axW.scatter([.012], [.885], transform=axW.transAxes, s=24, color=SERIES[0], ec='white', lw=.6, clip_on=False)
    axW.text(.03, .885, 'top 10: name and rank', transform=axW.transAxes, va='center', fontsize=9, color=INK)
    axW.scatter([.012], [.815], transform=axW.transAxes, s=11, color='#6e6d68', ec='white', lw=.6, clip_on=False)
    axW.text(.03, .815, f'ranks 11-{len(main)}: rank only, names below', transform=axW.transAxes, va='center', fontsize=9, color=INK)
    # Europe inset
    axE = fig.add_axes([0, 0, .38, .465]); ex0, ex1, ey0, ey1 = EU
    _land(axE, shp, ex0, ex1, ey0, ey1)
    fig.canvas.draw(); pos = axE.get_position()
    kx = (ex1 - ex0) / (pos.width * W); ky = (ey1 - ey0) / (pos.height * H)
    axE.text(.02, .975, 'Europe', transform=axE.transAxes, va='top', fontsize=10, weight='bold', color=INK)
    eoffs = {'London': (-.06, -.04), 'Amsterdam': (-.03, .07), 'Paris': (-.06, -.04), 'Zurich': (.09, -.1), 'Milan': (.09, -.1),
             'Berlin': (.06, .03), 'Prague': (.06, -.02), 'Vienna': (.06, -.03), 'Warsaw': (.06, .0), 'Dublin': (.08, .1),
             'Oslo': (-.06, .02), 'Stockholm': (.06, .0), 'Helsinki': (-.08, .1), 'Madrid': (.09, -.1),
             'Copenhagen': (.08, .1), 'Luxembourg': (.08, -.08), 'Istanbul': (-.06, .02), 'Reykjavik': (.08, 0)}
    for c, (lat, lon) in COORDS.items():
        if c not in rank.index or not (ex0 < lon < ex1 and ey0 < lat < ey1):
            continue
        r = int(rank[c]); hot = c in top10
        axE.scatter(lon, lat, s=24 if hot else 11, color=SERIES[0] if hot else '#6e6d68', ec='white', lw=.6, zorder=10)
        dx, dy = eoffs[c]
        _label(axE, c, r, lon, lat, dx, dy, kx, ky, flagged=hot, bold=r <= 3, col=INK if hot else MUTED, text=None if hot else str(r))
    # ranks 11-43 as a flagged list in three columns
    axL = fig.add_axes([.395, 0, .605, .465]); axL.set_xlim(0, .605 * W); axL.set_ylim(.465 * H, 0); axL.axis('off')
    axL.text(0, .12, f'Ranks 11-{len(main)}', fontsize=10, weight='bold', color=INK, va='center')
    rest = main.iloc[10:]
    rows = int(np.ceil(len(rest) / 3)); dy = (.465 * H - .35) / rows
    for k, (c, r) in enumerate(zip(rest.city, rest['rank'])):
        col, row = divmod(k, rows); x = col * 1.31; y = .38 + row * dy
        axL.text(x + .17, y, str(r), ha='right', va='center', fontsize=9, color=MUTED)
        flag(axL, COUNTRY[c], x + .21, y - .055, .17, .11)
        axL.text(x + .42, y, c, va='center', fontsize=9, color=INK)
    fig.savefig(FIG / 'city_map.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- heat map
def heatmap(f, lo, hi, main):
    cities = f.city.tolist()
    order = [cities.index(c) for c in main.city]
    cols = [m for _, ms in CATEGORIES for m in ms]
    J = [NAMES.index(m) for m in cols]
    L, H = lo[np.ix_(order, J)], hi[np.ix_(order, J)]
    M = (L + H) / 2
    n, m = M.shape
    W, Hh = 6.5, 7.7
    fig, ax = plt.subplots(figsize=(W, Hh))
    fig.subplots_adjust(left=.215, right=.99, top=.905, bottom=.055)
    for i in range(n):
        for j in range(m):
            v = M[i, j]
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=SPECTRUM(v), lw=0))
            col = 'white' if (v > .80 or v < .15) else INK
            ax.text(j + .5, i + .5, f'{v:.2f}', ha='center', va='center', fontsize=9, color=col)
    for j in range(m + 1):
        ax.axvline(j, color='white', lw=2 if j % 2 == 0 else .8)
    for i in range(n + 1):
        ax.axhline(i, color='white', lw=.6)
    ax.set_xlim(0, m); ax.set_ylim(n, 0)
    ax.set_yticks(np.arange(n) + .5)
    ax.set_yticklabels([f'{r}  {c}' for r, c in zip(main['rank'], main.city)], fontsize=9)
    ax.set_xticks(np.arange(m) + .5); ax.set_xticklabels([SHORT[c] for c in cols], linespacing=.95, fontsize=9.5)
    ax.xaxis.tick_top(); ax.tick_params(length=0, pad=3)
    ax.tick_params(axis='y', pad=22)
    for i, c in enumerate(main.city):
        flag(ax, COUNTRY[c], -.50, i + .5 + .38, .36, -.76, clip=False)  # y axis is inverted; 0.18 x 0.12 in
    for s in ax.spines.values():
        s.set_visible(False)
    for k, (name, _) in enumerate(CATEGORIES):
        ax.annotate('', xy=(2 * k + .08, -2.2), xytext=(2 * k + 1.92, -2.2), annotation_clip=False,
                    arrowprops=dict(arrowstyle='-', color=MUTED, lw=.8))
        ax.text(2 * k + 1, -2.45, CAT_SHORT[name], ha='center', va='bottom', fontsize=10, weight='bold', clip_on=False)
    cax = fig.add_axes([.215, .018, .33, .012])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=SPECTRUM, norm=plt.Normalize(0, 1)), cax=cax, orientation='horizontal')
    cb.outline.set_visible(False); cb.set_ticks([0, .5, 1]); cb.ax.set_xticklabels(['0 worst', '0.5 at anchor', '1 best'], fontsize=9)
    cb.ax.tick_params(length=0, pad=2)
    fig.text(.985, .024, 'Cells: midpoint utility; single gaps median-filled', fontsize=9, color=MUTED, va='center', ha='right')
    fig.savefig(FIG / 'indicator_compare.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- raw values
def raw_multiples(f):
    df = f.set_index('city').copy()
    df.loc['Zurich', 'homicide_per_100k'] = round(V.ZURICH_HOMICIDE, 2); df.loc['Amsterdam', 'homicide_per_100k'] = round(V.AMSTERDAM_HOMICIDE, 2)
    best, worst = 8, 4
    fig, axes = plt.subplots(2, 3, figsize=(6.5, 5.2))
    fig.subplots_adjust(left=.01, right=.99, top=.947, bottom=.015, wspace=.06, hspace=.14)
    fig.text(.01, .978, 'Best eight and worst four cities per indicator (rank among the cities with a record). Green: best three   Red: worst four',
             fontsize=9, color=MUTED, va='center')
    for ax, (col, title, benefit, fmt) in zip(axes.ravel(), F.RAW):
        v = df[col].astype(float).dropna().sort_values(ascending=not benefit)  # best first
        n = len(v)
        show = [(i + 1, c, x) for i, (c, x) in enumerate(v.items()) if i < best or i >= n - worst]
        xs = np.array([x for _, _, x in show]); srt = np.sort(xs)
        vmax = srt[-1] if srt[-1] < 3 * srt[-2] else 1.25 * srt[-2]  # cap one extreme outlier
        Wd = 1.6 * vmax; x0 = -Wd * .6 / .4  # bars start 60% across the panel, after rank, flag and name
        for k, (r, c, x) in enumerate(show):
            y = k if k < best else k + 1  # one empty row marks the gap
            colr = '#1baf7a' if r <= 3 else ('#e34948' if r > n - worst else GREY)
            ax.barh(y, min(x, vmax), left=0, height=.7, color=colr)
            ax.text(min(x, vmax) + .02 * vmax, y, fmt.format(x) + ('»' if x > vmax else ''), ha='left', va='center', fontsize=9, color=MUTED)
            ax.text(-.03 * Wd, y, c, ha='right', va='center', fontsize=9, color=INK)
            ax.text(x0 + .17 * Wd, y, str(r), ha='right', va='center', fontsize=9, color=MUTED)
            flag(ax, COUNTRY[c], x0 + .21 * Wd, y + .3, .17 * Wd, -.6)
        gap_y = best
        ax.text(-.03 * Wd, gap_y, f'{n - best - worst} other cities', ha='right', va='center', fontsize=9, color=MUTED, style='italic')
        ax.plot([x0 + .08 * Wd, x0 + .17 * Wd], [gap_y, gap_y], color=MUTED, lw=.6)
        ax.plot([.0, .3 * vmax], [gap_y, gap_y], color='#d9d8d3', lw=.8, ls=(0, (1, 2)))
        ax.set_xlim(x0, Wd); ax.set_ylim(best + worst + .6, -1.5); ax.axis('off')
        ax.text(x0, -1.15, title, fontsize=10, weight='bold', color=INK, va='center')
    fig.savefig(FIG / 'raw_compare.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- radar tiers
def radars(main):
    cats = [c for c, _ in CATEGORIES]
    labels = ['Safety &\nenvironment', 'Cost of\nliving', 'Education', 'Mobility', 'Daily\nlife']
    raw = main.set_index('city')[cats].astype(float)
    scaled = .12 + .88 * (raw - raw.min()) / (raw.max() - raw.min())  # stretch to the 43-city range
    avg = scaled.mean()
    order = main.sort_values('rank').city.tolist(); n = len(order)
    m0 = n // 2 - 1  # three ranks around the middle of the list
    panels = [('Top: ranks 1-3', order[:3]), (f'Middle: ranks {m0 + 1}-{m0 + 3}', order[m0:m0 + 3]),
              (f'Bottom: ranks {n - 2}-{n}', order[n - 3:])]
    ang = np.linspace(0, 2 * np.pi, len(cats), endpoint=False)
    loop = np.r_[ang, ang[0]]
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 3.3), subplot_kw=dict(polar=True))
    fig.subplots_adjust(left=.08, right=.92, top=.78, bottom=.27, wspace=.75)
    for ax, (title, cs) in zip(axes, panels):
        ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
        ax.set_ylim(0, 1.04); ax.set_yticks([.12, .56, 1.0]); ax.set_yticklabels([])
        ax.set_xticks(ang); ax.set_xticklabels(labels, fontsize=9, linespacing=.9)
        ax.tick_params(axis='x', pad=7)
        ax.grid(color=GRID, lw=.6); ax.spines['polar'].set_color(GRID)
        ax.plot(loop, np.r_[avg.values, avg.values[0]], color=MUTED, lw=1, ls=(0, (3, 2)))
        for k, c in enumerate(cs):
            v = scaled.loc[c].values; col = CITY_COL.get(c, SERIES[k])
            ax.fill(loop, np.r_[v, v[0]], color=col, alpha=.22, lw=0)
            ax.plot(loop, np.r_[v, v[0]], color=col, lw=2.2, marker='o', ms=4.5, markeredgecolor='white', markeredgewidth=.8)
        ax.set_title(title, pad=28, weight='bold')
        handles = [plt.Line2D([], [], color=CITY_COL.get(c, SERIES[k]), lw=2) for k, c in enumerate(cs)]
        names = [f"{int(main.set_index('city').loc[c, 'rank'])}. {c}" for c in cs]
        ax.legend(handles + [plt.Line2D([], [], color=MUTED, lw=1, ls=(0, (3, 2)))], names + [f'{n}-city mean'],
                  loc='upper center', bbox_to_anchor=(.5, -.18), frameon=False, fontsize=9, handlelength=1.4, ncol=1, labelspacing=.25)
    fig.savefig(FIG / 'radar_tiers.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- 2035
def future(f, lo, hi, w, main):
    fut = pd.read_csv(RES / 'future_2035.csv')
    p = fut.pivot(index='city', columns='scenario', values='score').loc[main.city]
    rk = fut.pivot(index='city', columns='scenario', values='rank').loc[main.city]
    scen = [('resource_expansion', 'S1'), ('living_pressure', 'S2'), ('balanced_improvement', 'S3')]
    # Catch-up threshold: one city cuts pupils/teacher, PM2.5 and travel time while others stay put; leader = rank 1.
    cities = f.city.tolist(); means = f.commute_min.to_numpy(float); zi = cities.index(main.city[0])
    idx = [NAMES.index(n) for n in ['upper_secondary_ptr', 'pm25', 'travel']]
    need = {}
    for c in main.city[1:]:
        i = cities.index(c); need[c] = None
        for cut in np.arange(0, .951, .005):
            Fm = np.ones((len(cities), 10)); Fm[i, idx] = 1 - cut
            a, b = raw_map(lo, hi, Fm, means); s = score((a + b) / 2, w)
            if s[i] >= s[zi]:
                need[c] = cut; break
    pd.Series(need).to_csv(RES / 'catchup_cut.csv', header=['cut'])
    top = 6
    extra = iter(['#eb6834', '#2a78d6', '#e87ba4', '#008300', '#0e8c9c', '#8a5a2b', '#c47a00', '#5b6770', '#b5651d', '#7a9a01'])
    pal = dict(CITY_COL)
    boards = [('today', 'Today', 'current data'),
              ('resource_expansion', '2035 · S1', 'more schools, stops, pools'),
              ('living_pressure', '2035 · S2', 'higher costs, longer trips'),
              ('balanced_improvement', '2035 · S3', 'smaller classes, cleaner air')]
    for k, _, _ in boards:
        for c in p[k].sort_values(ascending=False).head(top).index:
            if c not in pal:
                pal[c] = next(extra)
    fig, axes = plt.subplots(2, 2, figsize=(5.4, 4.0), sharex=True)
    axes = axes.ravel()
    fig.subplots_adjust(left=.01, right=.99, top=.90, bottom=.07, wspace=.10, hspace=.42)
    same = all((rk.loc[main.city[top:], k] == rk.loc[main.city[top:], 'today']).all() for k, _ in scen)
    fig.text(.01, .012, (f'Ranks {top + 1}-{len(p)} keep their order in every scenario. ' if same else '') + 'Box: rank changed.', fontsize=9, color=MUTED)
    for ax, (k, title, sub) in zip(axes, boards):
        b6 = p[k].sort_values(ascending=False).head(top)
        O = 42
        for y_, (c, v) in enumerate(b6.items()):
            ax.text(36.5, y_, f'{y_ + 1}', va='center', ha='right', fontsize=10, color=INK, weight='bold')
            flag(ax, COUNTRY[c], 37.5, y_ + .27, 3.3, -.54)
            ax.barh(y_, v - 40, left=O, height=.72, color=pal[c])
            ax.text(O + .8, y_, c, va='center', ha='left', fontsize=9, color='white', weight='bold')
            ax.text(O + v - 40 + .5, y_, f'{v:.1f}', va='center', ha='left', fontsize=9.5, color=INK, weight='bold')
            if k != 'today':
                d = v - p.loc[c, 'today']
                ax.text(84, y_, f'{d:+.1f}', va='center', ha='right', fontsize=9, color='#0b7a2b' if d > 0 else '#c0392b')
            if rk.loc[c, k] != rk.loc[c, 'today']:
                ax.barh(y_, v - 40, left=O, height=.72, fill=False, edgecolor=INK, lw=1.4)
        ax.set_xlim(33, 84.5); ax.set_ylim(top - .4, -.6)
        ax.axis('off')
        ax.set_title(f'{title}\n', fontsize=10.5, weight='bold', loc='left', pad=5)
        ax.text(0, 1.025, sub, transform=ax.transAxes, fontsize=9, color=MUTED, va='bottom')
    fig.savefig(FIG / 'future_2035.pdf'); plt.close(fig)
    return need


# ----------------------------------------------------------------------------- weight sensitivity
def weight_sensitivity():
    f, lo, hi = bounds(); w, _ = ahp_weights(); mid = (lo + hi) / 2; cities = f.city.tolist()
    ms = np.exp(np.linspace(np.log(.25), np.log(4), 41))
    hl = {c: CITY_COL[c] for c in HL}
    y0, y1 = 45, 75
    fig, axes = plt.subplots(1, 5, figsize=(6.5, 2.7), sharey=True)
    fig.subplots_adjust(left=.075, right=.99, top=.80, bottom=.26, wspace=.10)
    rows = []
    for ax, (name, members) in zip(axes, CATEGORIES):
        idx = [NAMES.index(m) for m in members]
        S = []
        for m in ms:
            ww = w.copy(); ww[idx] *= m; ww /= ww.sum(); S.append(score(mid, ww))
        S = np.array(S)
        for k, c in enumerate(cities):
            if c not in hl:
                ax.plot(ms, S[:, k], color='#d6d5cf', lw=.8)
        for c, col in hl.items():
            ax.plot(ms, S[:, cities.index(c)], color=col, lw=1.8)
        lead = [cities[i] for i in S.argmax(1)]
        sw = [m for m, a, b in zip(ms[1:], lead[:-1], lead[1:]) if a != b]
        for m in sw:
            ax.axvline(m, color=MUTED, lw=.7, ls=(0, (2, 2)))
            ax.text(m / 1.06, y1 - .6, f'×{m:.1f}', fontsize=9, color=MUTED, va='top', ha='right')
        rows.append(dict(category=name, leader_switch=[round(float(m), 2) for m in sw], leaders=sorted(set(lead))))
        ax.axvline(1, color=INK, lw=.6)
        ax.set_xscale('log'); ax.set_xticks([.25, 1, 4]); ax.set_xticklabels(['¼', '1', '4'])
        ax.minorticks_off(); ax.set_ylim(y0, y1); ax.tick_params(length=0)
        ax.grid(axis='y', color=GRID, lw=.5); ax.set_axisbelow(True)
        for sp in ['top', 'right']:
            ax.spines[sp].set_visible(False)
        ax.set_title(CAT_SHORT[name], fontsize=9.5, weight='bold')
    axes[0].set_ylabel('TOPSIS score')
    fig.text(.53, .115, f'Multiplier on one category weight (others rescaled; 1 = AHP weights). Grey: other cities, axis cut at {y0}.',
             ha='center', fontsize=9, color=MUTED)
    lg = fig.add_axes([.12, 0, .82, .075]); lg.axis('off')
    fw_, fh_ = fig.get_size_inches(); pos = lg.get_position(); lw_in, lh_in = pos.width * fw_, pos.height * fh_
    lg.set_xlim(0, lw_in); lg.set_ylim(0, lh_in)
    for k, (c, col) in enumerate(hl.items()):
        x = k * lw_in / 4
        lg.plot([x + .1, x + .32], [lh_in / 2] * 2, color=col, lw=1.8)
        flag(lg, COUNTRY[c], x + .4, lh_in / 2 - .06, .18, .12)
        lg.text(x + .64, lh_in / 2, c, va='center', fontsize=9, color=INK)
    fig.savefig(FIG / 'weight_sensitivity.pdf'); plt.close(fig)
    (RES / 'weight_sensitivity.json').write_text(json.dumps(rows, indent=1))
    return rows


# ----------------------------------------------------------------------------- robustness
def robustness_fig(main):
    s = json.loads((RES / 'summary.json').read_text())
    top = 20
    sub = main.head(top)
    iv = pd.DataFrame(s['interval_ahp']).set_index('city').loc[sub.city]
    fig = plt.figure(figsize=(6.5, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1], left=.19, right=.975, top=.88, bottom=.25, wspace=.30)
    ax = fig.add_subplot(gs[0]); y = np.arange(len(iv))
    for i, (c, r) in enumerate(iv.iterrows()):
        col = CITY_COL.get(c, SERIES[0]) if c in top3(main) else '#9c9b95'
        ax.plot([r.score_lower, r.score_upper], [i, i], color=col, lw=3.2, alpha=.45, solid_capstyle='round')
        ax.scatter(r.score, i, s=24, color=col, zorder=3, edgecolor='white', lw=.6)
    lead = main.city[0]; g = iv.score_lower.max()
    ax.axvline(g, color='#e34948', lw=.8, ls=(0, (3, 2)))
    ax.text(g + .3, 8.2, f'best guaranteed\nscore ({lead})', fontsize=9, color='#e34948', va='top')
    ax.set_yticks(y); ax.set_yticklabels([f'{r}  {c}' for r, c in zip(sub['rank'], sub.city)], fontsize=9)
    ax.set_ylim(len(iv) - .4, -.6); ax.tick_params(length=0)
    ax.grid(axis='x', color=GRID, lw=.5); ax.set_axisbelow(True)
    for sp in ['top', 'right', 'left']:
        ax.spines[sp].set_visible(False)
    ax.set_xlabel('TOPSIS score: range and representative value')
    ax.set_title(f'A   Score ranges, top {top} of {len(main)}', loc='left', fontsize=10.5, weight='bold')
    ax = fig.add_subplot(gs[1])
    ks = ['20', '100', '500']
    names = [c for c, _ in sorted(s['dirichlet']['20']['first'].items(), key=lambda kv: -kv[1])[:3]]
    names = [c for c in main.city if c in names]  # rank order
    cols = {c: CITY_COL.get(c, ['#eb6834', '#2a78d6', '#0e8c9c'][i]) for i, c in enumerate(names)}
    import matplotlib.patheffects as pe
    ax.set_yticks(range(3)); ax.set_yticklabels([f'κ = {k}' for k in ks]); ax.set_ylim(2.5, -.5)
    ax.set_xlim(0, 100); ax.set_xticks([0, 50, 100]); ax.set_xticklabels(['0', '50%', '100%'])
    Hb = .6
    left = np.zeros(3)
    for c in names + ['Other']:
        vals = np.array([100 * (s['dirichlet'][kk]['first'].get(c, 0) if c != 'Other' else
                                1 - sum(s['dirichlet'][kk]['first'].get(n, 0) for n in names)) for kk in ks])
        for j, v in enumerate(vals):
            if v > 0:
                ax.add_patch(Rectangle((left[j], j - Hb / 2), v, Hb, facecolor=cols.get(c, GREY), edgecolor='white', lw=.8, zorder=3))
            if v > 8:
                t = ax.text(left[j] + v / 2, j, f'{v:.0f}%', ha='center', va='center', fontsize=9, color='white', weight='bold', zorder=6)
                t.set_path_effects([pe.withStroke(linewidth=2.2, foreground='#333333')])
        left += vals
    small = [(c, 100 * s['dirichlet']['20']['first'].get(c, 0)) for c in names[1:]]
    ax.text(50, -.45, '   '.join(f'{c} {v:.0f}%' for c, v in small) + ' at κ = 20', ha='center', va='bottom', fontsize=9, color=MUTED)
    ax.set_ylim(2.5, -.9)
    ax.tick_params(length=0)
    for sp in ['top', 'right', 'left']:
        ax.spines[sp].set_visible(False)
    ax.set_xlabel('Share of weight draws ranked first')
    ax.set_title('B   Random AHP weights', loc='left', fontsize=10.5, weight='bold')
    handles = [plt.Rectangle((0, 0), 1, 1, color=cols[c]) for c in names] + [plt.Rectangle((0, 0), 1, 1, color=GREY)]
    ax.legend(handles, names + ['Other'], loc='upper left', bbox_to_anchor=(-.02, -.2), ncol=2, frameon=False, fontsize=9,
              handlelength=1, columnspacing=.8, handletextpad=.3)
    fig.savefig(FIG / 'robustness.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- gate revision
GATE_LAB = {'homicide': ('Homicide > 3 per 100,000', 'homicide_per_100k', '{:.1f}'),
            'pm25': ('PM2.5 > 25 µg/m³', 'pm25_ugm3', '{:.0f}'),
            'pir': ('House price / income > 20', 'pir', '{:.0f}')}


def gate_revision(f, main):
    g = json.loads((RES / 'gate_revision.json').read_text())
    excluded, feas = g['excluded'], g['feasible_order']
    raw = f.set_index('city').copy()
    raw.loc['Zurich', 'homicide_per_100k'] = V.ZURICH_HOMICIDE; raw.loc['Amsterdam', 'homicide_per_100k'] = V.AMSTERDAM_HOMICIDE
    rank = main.set_index('city')['rank']; sc = main.set_index('city')['score']
    show = 12
    W, Hh = 6.5, 3.6
    fig = plt.figure(figsize=(W, Hh))
    # left: feasible ranking
    ax = fig.add_axes([0, 0, .5, 1]); ax.set_xlim(0, .5 * W); ax.set_ylim(Hh, 0); ax.axis('off')
    ax.text(.05, .17, f'Feasible ranking after thresholds: top {show} of {len(feas)}', fontsize=10, weight='bold', color=INK, va='center')
    ax.text(.05, .42, 'new', fontsize=9, color=MUTED, va='center'); ax.text(.42, .42, 'was', fontsize=9, color=MUTED, va='center')
    ax.text(1.98, .42, 'representative score', fontsize=9, color=MUTED, va='center')
    y0, dy = .62, .22; smin, smax = 50, 70; x0, x1 = 1.98, 2.95
    for j, c in enumerate(feas[:show]):
        y = y0 + j * dy
        if j % 2 == 0:
            ax.add_patch(Rectangle((0, y - dy / 2), .5 * W - .05, dy, color='#f6f5f2', lw=0, zorder=0))
        col = CITY_COL.get(c, '#3f88c0')
        ax.add_patch(Ellipse((.15, y), .17, .17, color=col)); ax.text(.15, y, str(j + 1), ha='center', va='center', fontsize=9, color='white', weight='bold')
        mv = int(rank[c]) - (j + 1)
        ax.text(.52, y, f'{int(rank[c])}', ha='right', va='center', fontsize=9, color=MUTED)
        ax.text(.56, y, '' if mv == 0 else f'↑{mv}', va='center', fontsize=9, color='#0b7a2b')
        flag(ax, COUNTRY[c], .78, y - .055, .18, .11)
        ax.text(1.02, y, c, va='center', fontsize=9.5, color=INK, weight='bold' if c in top3(main) else 'normal')
        bw = (sc[c] - smin) / (smax - smin) * (x1 - x0)
        ax.add_patch(Rectangle((x0, y - .075), bw, .15, color=col, lw=0))
        ax.text(x0 + bw + .04, y, f'{sc[c]:.1f}', va='center', fontsize=9, color=INK)
    first_out = min(int(rank[c]) for c in excluded)
    ax.text(.05, y0 + show * dy + .02, f'Baseline ranks 1-{first_out - 1} unchanged; the highest excluded city was rank {first_out}.',
            fontsize=9, color=MUTED, va='center', style='italic')
    # right: excluded cities grouped by failed threshold
    ax = fig.add_axes([.52, 0, .48, 1]); ax.set_xlim(0, .48 * W); ax.set_ylim(Hh, 0); ax.axis('off')
    ax.text(.05, .17, f'Excluded by a must-have threshold: {len(excluded)} cities', fontsize=10, weight='bold', color=INK, va='center')
    y = .45
    for key, (lab, col, fmt) in GATE_LAB.items():
        cs = [c for c in main.city if key in excluded.get(c, [])]
        ax.add_patch(FancyBboxPatch((.05, y - .09), 2.95, .19, boxstyle='round,pad=0,rounding_size=.04', fc='#fbe3e1', ec='none'))
        ax.text(.12, y + .005, f'{lab}  ·  {len(cs)} cities', va='center', fontsize=9.5, weight='bold', color='#a5281f')
        items = ', '.join(f'{c} {fmt.format(float(raw.loc[c, col]))}' for c in cs)
        lines = textwrap.wrap(items, 50)
        for k, ln in enumerate(lines):
            ax.text(.12, y + .23 + k * .165, ln, va='center', fontsize=9, color=INK)
        y += .23 + len(lines) * .165 + .13
    both = [c for c, v in excluded.items() if len(v) > 1]
    note = ('Values after each city; ' + ', '.join(both) + ' fail two thresholds.') if both else 'Values after each city.'
    for k, ln in enumerate(textwrap.wrap(note, 52)):
        ax.text(.12, y + .02 + k * .165, ln, va='center', fontsize=9, color=MUTED, style='italic')
    fig.savefig(FIG / 'gate_revision.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- news
def news_podium(main):
    t3 = top3(main); sc_ = main.set_index('city')['score']
    podium = [(t3[1], 2, .62), (t3[0], 1, .8), (t3[2], 3, .5)]
    W, H = 3.14, 1.42
    fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    for k, (c, r, h) in enumerate(podium):
        sc = float(sc_[c]); tag = TAGS.get(c, '')
        col = CITY_COL.get(c, SERIES[0]); w = .94; x = .06 + k * (w + .09); cx = x + w / 2
        ax.add_patch(FancyBboxPatch((x, .05), w, h, boxstyle='round,pad=0,rounding_size=.05', fc=col, ec='none'))
        ax.text(cx, .05 + h - .17, str(r), ha='center', va='center', fontsize=14, weight='bold', color='white')
        ax.text(cx, .05 + h - .37, f'{sc:.1f} points', ha='center', va='center', fontsize=9, color='white', weight='bold')
        flag(ax, COUNTRY[c], cx - .18, .05 + h + .06, .36, .24)
        ax.text(cx, .05 + h + .42, c, ha='center', va='center', fontsize=11, weight='bold', color=INK)
        if h > .6:
            ax.text(cx, .15, tag, ha='center', va='center', fontsize=9, color='white', style='italic')
        else:
            ax.text(cx, .05 + h + .62, tag, ha='center', va='center', fontsize=9, color=MUTED, style='italic')
    fig.savefig(FIG / 'news_podium.pdf'); plt.close(fig)


def news_glance(main):
    cats = [c for c, _ in CATEGORIES]
    m = main.set_index('city')
    cities = [(c, CITY_COL.get(c, SERIES[0])) for c in top3(main)]
    W, H = 6.5, 1.8
    fig, axes = plt.subplots(1, 5, figsize=(W, H), sharey=True)
    fig.subplots_adjust(left=.2, right=.985, top=.8, bottom=.05, wspace=.16)
    for ax, cat in zip(axes, cats):
        for i, (c, col) in enumerate(cities):
            v = float(m.loc[c, cat])
            ax.barh(i, v, height=.62, color=col, alpha=.95)
            ax.text(v + .02, i, f'{v:.2f}', va='center', fontsize=10, color=INK)
        ax.set_xlim(0, 1.22); ax.set_ylim(2.5, -.5); ax.set_xticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.axvline(0, color=MUTED, lw=.8); ax.tick_params(axis='y', length=0)
        ax.set_title(CAT_SHORT[cat], fontsize=10.5, weight='bold', color=INK)
    axes[0].set_yticks(range(3)); axes[0].set_yticklabels([c for c, _ in cities], fontsize=10.5)
    axes[0].tick_params(axis='y', length=0, pad=24)
    pos = axes[0].get_position()
    for i, (c, _) in enumerate(cities):
        ya = pos.y0 + pos.height * (2.5 - i) / 3.0
        fa = fig.add_axes([pos.x0 - .045, ya - .045, .035, .09]); fa.set_xlim(0, 1); fa.set_ylim(0, 1); fa.axis('off')
        flag(fa, COUNTRY[c], 0, .2, 1, .6)
    fig.savefig(FIG / 'news_glance.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- category champions
def category_champions(main):
    cats = [c for c, _ in CATEGORIES]
    W, H = 6.5, 2.35
    fig, axes = plt.subplots(1, 5, figsize=(W, H))
    fig.subplots_adjust(left=.005, right=.995, top=.98, bottom=.02, wspace=.04)
    medal = ['#d4a017', '#9ea3a8', '#b87333']
    for ax, cat, col in zip(axes, cats, ['#2a78d6', '#eda100', '#1baf7a', '#6250d6', '#eb6834']):
        pos = ax.get_position(); aw, ah = pos.width * W, pos.height * H
        ax.set_xlim(0, aw); ax.set_ylim(0, ah); ax.axis('off')  # 1 data unit = 1 inch
        ax.add_patch(Rectangle((0, ah - .27), aw, .27, color=col, lw=0))
        ax.text(aw / 2, ah - .135, CAT_SHORT[cat], ha='center', va='center', fontsize=9.5, weight='bold', color='white')
        top = main.set_index('city')[cat].sort_values(ascending=False).head(3)
        for k, (c, v) in enumerate(top.items()):
            y = ah - .62 - k * .62
            ax.add_patch(plt.Circle((.1, y), .085, color=medal[k]))
            ax.text(.1, y, str(k + 1), ha='center', va='center', fontsize=9, color='white', weight='bold')
            flag(ax, COUNTRY[c], .22, y - .08, .24, .16)
            ax.text(.5, y + .07, c, va='center', fontsize=9, color=INK, weight='bold' if k == 0 else 'normal')
            ax.text(.5, y - .1, f'score {v:.2f}', va='center', fontsize=9, color=MUTED)
    fig.savefig(FIG / 'category_champions.pdf'); plt.close(fig)


# ----------------------------------------------------------------------------- workflow
def workflow():
    f, *_ = bounds()
    steps = [('1  Data', f'{len(f)} cities\n10 indicators\nofficial records\nand proxies', '#2a78d6'),
             ('2  Utilities', 'every value\nmapped to 0-1\nwith a fixed\nreference level', '#1baf7a'),
             ('3  AHP', 'five categories\ncompared from a\nstudent view\nCR = 0.006', '#eda100'),
             ('4  TOPSIS', 'distance to the\nbest and worst\nprofile, 0-100\nLuxembourg first', '#eb6834'),
             ('5  Checks', 'score ranges\nwithdrawals\nrandom weights\nVIKOR, 2035', '#6250d6')]
    fig, ax = plt.subplots(figsize=(6.5, 1.5))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, 100); ax.set_ylim(0, 24); ax.axis('off')
    w, gap = 17.6, 2.9
    for k, (title, body, col) in enumerate(steps):
        x = .4 + k * (w + gap)
        ax.add_patch(FancyBboxPatch((x, .5), w, 23, boxstyle='round,pad=0,rounding_size=1.6', fc='white', ec=col, lw=1.4))
        ax.add_patch(FancyBboxPatch((x, 18), w, 5.5, boxstyle='round,pad=0,rounding_size=1.6', fc=col, ec=col, lw=1.4))
        ax.add_patch(Rectangle((x, 18), w, 2, color=col, lw=0))
        ax.text(x + w / 2, 20.7, title, ha='center', va='center', fontsize=9.5, weight='bold', color='white')
        ax.text(x + w / 2, 9.2, body, ha='center', va='center', fontsize=9, color=INK, linespacing=1.15)
        if k < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x + w + .3, 11), (x + w + gap - .3, 11), arrowstyle='-|>', mutation_scale=9, color=MUTED, lw=1.1))
    fig.savefig(FIG / 'workflow.pdf'); plt.close(fig)


ALL = ['city_map', 'indicator_compare', 'raw_compare', 'radar_tiers', 'future_2035', 'weight_sensitivity', 'robustness',
       'gate_revision', 'category_champions', 'ahp_weights', 'workflow', 'news_podium', 'news_glance']


def run(names):
    f, lo, hi, w, main = data()
    for name in names:
        if name == 'city_map': city_map(main)
        elif name == 'indicator_compare': heatmap(f, lo, hi, main)
        elif name == 'raw_compare': raw_multiples(f)
        elif name == 'radar_tiers': radars(main)
        elif name == 'future_2035': print('catch-up cuts', future(f, lo, hi, w, main))
        elif name == 'weight_sensitivity': print(weight_sensitivity())
        elif name == 'robustness': robustness_fig(main)
        elif name == 'gate_revision': gate_revision(f, main)
        elif name == 'category_champions': category_champions(main)
        elif name == 'ahp_weights': F.weight_donut()
        elif name == 'workflow': workflow()
        elif name == 'news_podium': news_podium(main)
        elif name == 'news_glance': news_glance(main)
        else: raise SystemExit(f'unknown figure {name}')
        print('wrote', FIG / f'{name}.pdf')


if __name__ == '__main__':
    run(sys.argv[1:] or ALL)

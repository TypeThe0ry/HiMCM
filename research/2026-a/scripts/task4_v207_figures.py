"""V207 paper figures: indicator heat map, tier radar charts, 2035 scenarios."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from task4_v5_model import ROOT, NAMES, score
from task4_user_v205_revision import revised_bounds
from task4_v207_ahp import ahp_weights, CATEGORIES, OUT as RES, bounds, PTR_FILL, PTR_MEDIAN_FILL, TRAVEL_FILL
from matplotlib.patches import Polygon
from audit_task4_v203 import raw_map
from task4_v207_flags import flag, COUNTRY

FIG = ROOT.parents[2] / 'HiMCM-Overleaf/figures'
PROXY = {(c, 'upper_secondary_ptr') for c in list(PTR_FILL) + PTR_MEDIAN_FILL} | {(c, 'travel') for c in TRAVEL_FILL}
# Figures kept out of the paper for now (TT 11-14), ready to re-insert.
SPARE = ROOT / 'results/task4_v207_ahp/spare_figures'
for f in font_manager.findSystemFonts():
    if 'Lato' in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({'font.family': 'Lato', 'font.size': 9.5, 'axes.titlesize': 11,
                     'axes.labelsize': 10, 'xtick.labelsize': 9.5, 'ytick.labelsize': 9.5,
                     'legend.fontsize': 9.5, 'pdf.fonttype': 42, 'axes.edgecolor': '#52514e',
                     'axes.linewidth': .6, 'text.color': '#0b0b0b', 'axes.labelcolor': '#0b0b0b',
                     'xtick.color': '#52514e', 'ytick.color': '#52514e'})
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#d9d8d3'
SERIES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100']
BLUE = LinearSegmentedColormap.from_list('blue', ['#f4f8fd', '#b7d3f6', '#6da7ec', '#2a78d6', '#184f95', '#0d366b'])
SPECTRUM = LinearSegmentedColormap.from_list('spectrum', ['#a50026', '#e0533a', '#f9a65a', '#fee597', '#e3f1e8', '#8cc5d6', '#3f88c0', '#253f94'])
SHORT = {'homicide_rate': 'Homicide', 'pm25': 'PM2.5', 'cost_living_index': 'Living\ncost',
         'price_income_ratio': 'Housing', 'upper_secondary_ptr': 'Pupils/\nteacher',
         'research_he_density': 'Higher\nedu.', 'travel': 'Travel\ntime',
         'public_transport_density': 'Transit\nstops', 'fixed_broadband_mbps': 'Broad-\nband',
         'public_pool_density': 'Pools'}
CAT_SHORT = {'Safety and environment': 'Safety & env.', 'Cost of living': 'Cost of living',
             'Education': 'Education', 'Mobility': 'Mobility', 'Daily life': 'Daily life'}


def data():
    f, lo, hi = bounds()
    w, _ = ahp_weights()
    main = pd.read_csv(RES / 'main_ranking.csv')
    return f, lo, hi, w, main


def heatmap(f, lo, hi, main):
    cities = f.city.tolist()
    order = [cities.index(c) for c in main.city]
    cols = [m for _, ms in CATEGORIES for m in ms]
    J = [NAMES.index(m) for m in cols]
    L, H = lo[np.ix_(order, J)], hi[np.ix_(order, J)]
    M = (L + H) / 2
    fig, ax = plt.subplots(figsize=(6.5, 5.6))
    fig.subplots_adjust(left=.20, right=.985, top=.80, bottom=.12)
    n, m = M.shape
    for i in range(n):
        for j in range(m):
            unknown = H[i, j] - L[i, j] >= 1 - 1e-12
            if unknown:
                ax.add_patch(Rectangle((j, i), 1, 1, facecolor='#f0efec', edgecolor='#b9b8b2', hatch='////', lw=0))
                ax.text(j + .5, i + .5, 'no data', ha='center', va='center', fontsize=9, color=MUTED)
                continue
            v = M[i, j]
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=SPECTRUM(v), lw=0))
            txt = f'{v:.2f}'
            col = 'white' if (v > .80 or v < .15) else INK
            ax.text(j + .5, i + .5, txt, ha='center', va='center', fontsize=9, color=col)
            if H[i, j] - L[i, j] > 1e-12:  # utility range: corner triangle
                ax.add_patch(Polygon([(j + .72, i + .04), (j + .96, i + .04), (j + .96, i + .38)], color=INK, lw=0))
            if (main.city.iloc[i], cols[j]) in PROXY:  # proxy value: dashed outline
                ax.add_patch(Rectangle((j + .06, i + .08), .88, .84, fill=False, edgecolor=INK, lw=1.0, ls=(0, (2, 1.5))))
    for j in range(m + 1):
        ax.axvline(j, color='white', lw=2 if j % 2 == 0 else .8)
    for i in range(n + 1):
        ax.axhline(i, color='white', lw=.8)
    ax.set_xlim(0, m); ax.set_ylim(n, 0)
    ax.set_yticks(np.arange(n) + .5)
    ax.set_yticklabels([f'{r}  {c}' for r, c in zip(main['rank'], main.city)])
    ax.set_xticks(np.arange(m) + .5); ax.set_xticklabels([SHORT[c] for c in cols], linespacing=.95)
    ax.xaxis.tick_top(); ax.tick_params(length=0, pad=3)
    ax.tick_params(axis='y', pad=25)
    for i, c in enumerate(main.city):
        flag(ax, COUNTRY[c], -.46, i + .5 + .26, .36, -.52, clip=False)  # y axis is inverted
    for s in ax.spines.values():
        s.set_visible(False)
    for k, (name, _) in enumerate(CATEGORIES):
        ax.annotate('', xy=(2 * k + .08, -1.55), xytext=(2 * k + 1.92, -1.55), annotation_clip=False,
                    arrowprops=dict(arrowstyle='-', color=MUTED, lw=.8))
        ax.text(2 * k + 1, -1.75, CAT_SHORT[name], ha='center', va='bottom', fontsize=10, weight='bold', clip_on=False)
    cax = fig.add_axes([.20, .05, .36, .018])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=SPECTRUM, norm=plt.Normalize(0, 1)), cax=cax, orientation='horizontal')
    cb.outline.set_visible(False); cb.set_ticks([0, .5, 1]); cb.ax.set_xticklabels(['0 worst', '0.5 at anchor', '1 best'])
    lg = fig.add_axes([.60, .02, .38, .07]); lg.set_xlim(0, 10); lg.set_ylim(0, 2); lg.axis('off')
    lg.add_patch(Rectangle((0, 1.1), .9, .8, facecolor='#e3f1e8', lw=0))
    lg.add_patch(Polygon([(.65, 1.15), (.88, 1.15), (.88, 1.45)], color=INK, lw=0))
    lg.text(1.2, 1.5, 'utility range (midpoint shown)', va='center', fontsize=9, color=MUTED)
    lg.add_patch(Rectangle((0, .1), .9, .8, facecolor='#e3f1e8', edgecolor=INK, lw=1.0, ls=(0, (2, 1.5))))
    lg.text(1.2, .5, 'proxy value (national or survey)', va='center', fontsize=9, color=MUTED)
    fig.savefig(FIG / 'indicator_compare.pdf'); plt.close(fig)


def radars(main):
    cats = [c for c, _ in CATEGORIES]
    labels = ['Safety &\nenvironment', 'Cost of\nliving', 'Education', 'Mobility', 'Daily\nlife']
    raw = main.set_index('city')[cats].astype(float)
    # Stretch each category to the 16-city range so differences between cities stand out.
    scaled = .12 + .88 * (raw - raw.min()) / (raw.max() - raw.min())
    avg = scaled.mean()
    order = main.sort_values('rank').city.tolist()
    panels = [('Top: ranks 1-3', order[:3]), ('Middle: ranks 7-9', order[6:9]),
              ('Bottom: ranks 14-16', order[13:16])]
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
            v = scaled.loc[c].values
            ax.fill(loop, np.r_[v, v[0]], color=SERIES[k], alpha=.22, lw=0)
            ax.plot(loop, np.r_[v, v[0]], color=SERIES[k], lw=2.2, marker='o', ms=4.5,
                    markeredgecolor='white', markeredgewidth=.8)
        ax.set_title(title, pad=28, weight='bold')
        handles = [plt.Line2D([], [], color=SERIES[k], lw=2) for k in range(len(cs))]
        names = [f"{int(main.set_index('city').loc[c, 'rank'])}. {c}" for c in cs]
        ax.legend(handles + [plt.Line2D([], [], color=MUTED, lw=1, ls=(0, (3, 2)))], names + ['16-city mean'],
                  loc='upper center', bbox_to_anchor=(.5, -.18), frameon=False, fontsize=9, handlelength=1.4,
                  ncol=1, labelspacing=.25)
    fig.savefig(FIG / 'radar_tiers.pdf'); plt.close(fig)


def future(f, lo, hi, w, main):
    fut = pd.read_csv(RES / 'future_2035.csv')
    p = fut.pivot(index='city', columns='scenario', values='score').loc[main.city]
    rk = fut.pivot(index='city', columns='scenario', values='rank').loc[main.city]
    scen = [('resource_expansion', 'S1 More\nfacilities'),
            ('living_pressure', 'S2 Higher\ncosts'),
            ('balanced_improvement', 'S3 Better\nschools, air')]
    # Catch-up threshold: one city cuts pupils/teacher, PM2.5 and travel time while others stay put.
    cities = f.city.tolist(); means = f.commute_min.to_numpy(float); zi = cities.index('Zurich')
    idx = [NAMES.index(n) for n in ['upper_secondary_ptr', 'pm25', 'travel']]
    need = {}
    for c in main.city[1:]:
        i = cities.index(c); need[c] = None
        for cut in np.arange(0, .951, .005):
            F = np.ones((16, 10)); F[i, idx] = 1 - cut
            a, b = raw_map(lo, hi, F, means); s = score((a + b) / 2, w)
            if s[i] >= s[zi]:
                need[c] = cut; break
    pd.Series(need).to_csv(RES / 'catchup_cut.csv', header=['cut'])
    # Four leaderboards: today and the three 2035 scenarios, top six cities each.
    top = 6
    pal = dict(zip(main.city[:top], ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#6250d6', '#008300', '#e34948', '#0e8c9c', '#8a5a2b']))
    boards = [('today', 'Today', 'current data')] + [
        ('resource_expansion', '2035 · S1', 'more schools, stops, pools'),
        ('living_pressure', '2035 · S2', 'higher costs, longer trips'),
        ('balanced_improvement', '2035 · S3', 'smaller classes, cleaner air')]
    fig, axes = plt.subplots(2, 2, figsize=(5.4, 4.0), sharex=True)
    axes = axes.ravel()
    fig.subplots_adjust(left=.01, right=.99, top=.90, bottom=.07, wspace=.10, hspace=.42)
    same = all((rk.loc[main.city[top:], k] == rk.loc[main.city[top:], 'today']).all() for k, _ in scen)
    fig.text(.01, .012, (f'Ranks {top + 1}-16 keep their order in every scenario. ' if same else '') + 'Box: rank changed.', fontsize=9, color=MUTED)
    for ax, (k, title, sub) in zip(axes, boards):
        b6 = p[k].sort_values(ascending=False).head(top)
        O = 42  # bars start here; a bar of length v-40 encodes the score
        for y_, (c, v) in enumerate(b6.items()):
            ax.text(36.5, y_, f'{y_ + 1}', va='center', ha='right', fontsize=10, color=INK, weight='bold')
            flag(ax, COUNTRY[c], 37.5, y_ + .27, 3.3, -.54)  # y axis is inverted
            ax.barh(y_, v - 40, left=O, height=.72, color=pal.get(c, '#c4c3bd'))
            ax.text(O + .8, y_, c, va='center', ha='left', fontsize=9, color='white', weight='bold')
            ax.text(O + v - 40 + .5, y_, f'{v:.1f}', va='center', ha='left', fontsize=9.5, color=INK, weight='bold')
            if k != 'today':
                d = v - p.loc[c, 'today']
                ax.text(80, y_, f'{d:+.1f}', va='center', ha='right', fontsize=9,
                        color='#0b7a2b' if d > 0 else '#c0392b')
            if rk.loc[c, k] != rk.loc[c, 'today']:
                ax.barh(y_, v - 40, left=O, height=.72, fill=False, edgecolor=INK, lw=1.4)
        ax.set_xlim(33, 80.5); ax.set_ylim(top - .4, -.6)
        ax.axis('off')
        ax.set_title(f'{title}\n', fontsize=10.5, weight='bold', loc='left', pad=5)
        ax.text(0, 1.025, sub, transform=ax.transAxes, fontsize=9, color=MUTED, va='bottom')
    fig.savefig(FIG / 'future_2035.pdf'); plt.close(fig)
    return need


if __name__ == '__main__':
    f, lo, hi, w, main = data()
    heatmap(f, lo, hi, main)
    radars(main)
    need = future(f, lo, hi, w, main)
    print(json.dumps({k: v for k, v in need.items()}, indent=0))


COORDS = {'Vienna': (48.21, 16.37), 'Zurich': (47.37, 8.54), 'Helsinki': (60.17, 24.94), 'Berlin': (52.52, 13.40),
          'London': (51.51, -0.13), 'Amsterdam': (52.37, 4.90), 'Stockholm': (59.33, 18.07), 'Paris': (48.86, 2.35),
          'Madrid': (40.42, -3.70), 'Milan': (45.46, 9.19), 'Dublin': (53.35, -6.26), 'Oslo': (59.91, 10.75),
          'Prague': (50.08, 14.44), 'Warsaw': (52.23, 21.01), 'Singapore': (1.35, 103.82), 'Tokyo': (35.68, 139.69)}
# label offsets in degrees (dx, dy) to keep names clear of each other
OFFS = {'London': (-.6, .0), 'Amsterdam': (.5, 1.3), 'Paris': (-.6, -.5), 'Zurich': (-.6, -.8), 'Milan': (.6, -.8),
        'Berlin': (.6, -.8), 'Prague': (.6, -.6), 'Vienna': (.6, -.7), 'Warsaw': (.6, .7), 'Dublin': (-.6, .5),
        'Oslo': (-.6, .5), 'Stockholm': (.6, -.8), 'Helsinki': (.6, .6), 'Madrid': (.6, -.7),
        'Singapore': (.7, .0), 'Tokyo': (-.7, -.9)}


def city_map(main):
    import shapefile
    shp = shapefile.Reader(str(ROOT / 'visuals/cartography/vector_data/ne_10m_land/ne_10m_land.shp'))
    rank = main.set_index('city')['rank']
    fig = plt.figure(figsize=(6.5, 4.1))
    axE = fig.add_axes([.0, .0, .70, 1.0]); axA = fig.add_axes([.71, .30, .29, .62])
    views = [(axE, (-12, 32), (35, 64.5), 'Europe: 14 cities'), (axA, (96, 146), (-4, 44), 'Asia: 2 cities')]
    for ax, (x0, x1), (y0, y1), title in views:
        ax.set_facecolor('#eaf2fb')
        for s in shp.shapes():
            bx = s.bbox
            if bx[2] < x0 - 5 or bx[0] > x1 + 5 or bx[3] < y0 - 5 or bx[1] > y1 + 5:
                continue
            pts = np.array(s.points); parts = list(s.parts) + [len(pts)]
            for a, b in zip(parts[:-1], parts[1:]):
                ax.fill(pts[a:b, 0], pts[a:b, 1], color='#f4f3ef', ec='#c9c7bf', lw=.4)
        ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
        ax.set_aspect(1 / np.cos(np.radians((y0 + y1) / 2)))
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color('#c9c7bf'); sp.set_linewidth(.6)
        ax.text(.02, .98, title, transform=ax.transAxes, va='top', fontsize=10, weight='bold', color=INK)
        k = (x1 - x0) / (ax.get_position().width * 6.5) / (44 / (.70 * 6.5))  # degrees per inch, Europe = 1
        for c, (lat, lon) in COORDS.items():
            if not (x0 < lon < x1 and y0 < lat < y1):
                continue
            r = int(rank[c]); col = SERIES[0] if r <= 3 else MUTED
            ax.scatter(lon, lat, s=34 if r <= 3 else 20, color=col, ec='white', lw=.8, zorder=10)
            dx, dy = OFFS[c]; dx *= k; dy *= k
            ha = 'left' if dx > 0 else 'right'
            fw, fh = 1.55 * k, .78 * k
            fx = lon + dx if dx > 0 else lon + dx - fw
            flag(ax, COUNTRY[c], fx, lat + dy - fh / 2, fw, fh)
            tx = fx + fw + .35 * k if dx > 0 else fx - .35 * k
            ax.text(tx, lat + dy, f'{c} ({r})', ha=ha, va='center', fontsize=9, color=INK,
                    weight='bold' if r <= 3 else 'normal', zorder=11)
    fig.text(.715, .22, 'Number in brackets: final rank', fontsize=9, color=MUTED)
    fig.text(.715, .15, 'Blue dot: top three', fontsize=9, color=SERIES[0])
    fig.savefig(FIG / 'city_map.pdf'); plt.close(fig)


if __name__ == '__main__' and 'map' in __import__('sys').argv:
    city_map(data()[4])


def weight_donut():
    w, info = ahp_weights()
    cat_names = [c for c, _ in CATEGORIES]
    cw = [info['category_weights'][c] for c in cat_names]
    base = ['#2a78d6', '#eda100', '#1baf7a', '#6250d6', '#eb6834']
    from matplotlib.colors import to_rgb
    def tint(c, t):
        r = np.array(to_rgb(c)); return tuple(r + (1 - r) * t)
    inner_cols, outer, outer_cols, outer_lab = [], [], [], []
    for (name, ms), col in zip(CATEGORIES, base):
        inner_cols.append(col)
        for k, m in enumerate(ms):
            outer.append(w[NAMES.index(m)]); outer_cols.append(tint(col, .35 + .3 * k))
            outer_lab.append((SHORT[m].replace('/\n', '/').replace('\n', ' ').replace('- ', ''), w[NAMES.index(m)]))
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    fig.subplots_adjust(left=.0, right=1, top=1, bottom=0)
    wo, _ = ax.pie(outer, radius=1.0, colors=outer_cols, startangle=90, counterclock=False,
                   wedgeprops=dict(width=.32, edgecolor='white', linewidth=1.5))
    ax.pie(cw, radius=.68, colors=inner_cols, startangle=90, counterclock=False,
           wedgeprops=dict(width=.3, edgecolor='white', linewidth=1.5))
    # category weights printed inside the inner ring
    ang0 = 90
    for c, v in zip(cat_names, cw):
        mid = np.radians(ang0 - v * 180); ang0 -= v * 360
        ax.text(.53 * np.cos(mid), .53 * np.sin(mid), f'{v:.2f}', ha='center', va='center', fontsize=9.5,
                color='white', weight='bold')
    items = []
    for wedge, (lab, v) in zip(wo, outer_lab):
        a = np.radians((wedge.theta1 + wedge.theta2) / 2)
        items.append([np.cos(a), np.sin(a), 1.15 * np.sin(a), lab, v])
    for side in (1, -1):
        grp = sorted([it for it in items if np.sign(it[0]) == side], key=lambda it: it[2])
        for i in range(1, len(grp)):  # keep labels at least 0.2 apart vertically
            grp[i][2] = max(grp[i][2], grp[i - 1][2] + .2)
    for x, y, ty, lab, v in items:
        ax.annotate(f'{lab} {v:.3f}', xy=(x, y), xytext=(1.3 * np.sign(x), ty),
                    ha='left' if x > 0 else 'right', va='center', fontsize=9, color=INK,
                    arrowprops=dict(arrowstyle='-', color='#b9b8b2', lw=.6, shrinkA=0, shrinkB=2))
    ax.text(0, 0, 'AHP\nweights', ha='center', va='center', fontsize=10, weight='bold', color=INK, linespacing=1)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in base]
    ax.legend(handles, [CAT_SHORT[c] for c in cat_names], loc='lower left', bbox_to_anchor=(.0, .0),
              frameon=False, fontsize=9, handlelength=1, title='Category (inner ring)', title_fontsize=9)
    ax.set_aspect('equal'); ax.set_xlim(-3.9, 2.7); ax.set_ylim(-1.25, 1.35)
    fig.savefig(FIG / 'ahp_weights.pdf'); plt.close(fig)


if __name__ == '__main__' and 'donut' in __import__('sys').argv:
    weight_donut()


RAW = [('homicide_per_100k', 'Homicides per 100,000', False, '{:.2f}'),
       ('pm25_ugm3', 'PM2.5 (µg/m³)', False, '{:.1f}'),
       ('cli', 'Living-cost index', False, '{:.0f}'),
       ('pir', 'House price / income', False, '{:.1f}'),
       ('broadband_mbps', 'Broadband (Mbps)', True, '{:.0f}'),
       ('he_per_million', 'Higher-ed. per million', True, '{:.0f}')]


def raw_multiples(f):
    from task4_v207_ahp import ZURICH_HOMICIDE
    df = f.set_index('city').copy()
    df.loc['Zurich', 'homicide_per_100k'] = round(ZURICH_HOMICIDE, 2)
    fig, axes = plt.subplots(2, 3, figsize=(6.5, 7.6))
    fig.subplots_adjust(left=.01, right=.99, top=.93, bottom=.02, wspace=.06, hspace=.10)
    fig.text(.01, .975, 'Green: best three   Red: worst three   (cities sorted best to worst)', fontsize=9, color=MUTED, va='center')
    for ax, (col, title, benefit, fmt) in zip(axes.ravel(), RAW):
        v = df[col].astype(float).sort_values(ascending=not benefit)  # best first
        n = len(v); srt = np.sort(v.values)
        vmax = srt[-1] if srt[-1] < 3 * srt[-2] else 1.25 * srt[-2]  # cap one extreme outlier
        W = 1.3 * vmax; x0 = -W * .47 / .53  # bars start 47% across the panel, after flag and name
        for i, (c, x) in enumerate(v.items()):
            colr = '#1baf7a' if i < 3 else ('#e34948' if i >= n - 3 else '#c4c3bd')
            ax.barh(i, min(x, vmax), left=0, height=.7, color=colr)
            lab = fmt.format(x) + ('»' if x > vmax else '')
            ax.text(min(x, vmax) + .02 * vmax, i, lab, ha='left', va='center', fontsize=9, color=MUTED)
            ax.text(-.03 * W, i, c, ha='right', va='center', fontsize=9, color=INK)
            flag(ax, COUNTRY[c], x0 + .005 * W, i + .3, .12 * W, -.6)
        ax.set_xlim(x0, W); ax.set_ylim(n - .4, -1.6); ax.axis('off')
        ax.text(x0, -1.25, title, fontsize=10, weight='bold', color=INK, va='center')
    fig.savefig(FIG / 'raw_compare.pdf'); plt.close(fig)


def robustness_fig(main):
    s = json.loads((RES / 'summary.json').read_text())
    iv = pd.DataFrame(s['interval_ahp']).set_index('city').loc[main.city]
    fig = plt.figure(figsize=(6.5, 4.3))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1], left=.15, right=.97, top=.88, bottom=.24, wspace=.32)
    ax = fig.add_subplot(gs[0]); y = np.arange(len(iv))
    top3 = set(main.city[:3])
    for i, (c, r) in enumerate(iv.iterrows()):
        col = SERIES[0] if c in top3 else '#9c9b95'
        ax.plot([r.score_lower, r.score_upper], [i, i], color=col, lw=3.2, alpha=.45, solid_capstyle='round')
        ax.scatter(r.score, i, s=26, color=col, zorder=3, edgecolor='white', lw=.6)
    ax.axvline(iv.score_lower.max(), color='#e34948', lw=.8, ls=(0, (3, 2)))
    ax.text(iv.score_lower.max() + .3, len(iv) - .6, 'best guaranteed\nscore (Zurich)', fontsize=9, color='#e34948', va='bottom')
    ax.set_yticks(y); ax.set_yticklabels([f'{r}  {c}' for r, c in zip(main['rank'], main.city)])
    ax.set_ylim(len(iv) - .4, -.6); ax.tick_params(length=0)
    ax.grid(axis='x', color=GRID, lw=.5); ax.set_axisbelow(True)
    for sp in ['top', 'right', 'left']:
        ax.spines[sp].set_visible(False)
    ax.set_xlabel('TOPSIS score: range and representative value')
    ax.set_title('A   Score ranges', loc='left', fontsize=10.5, weight='bold')
    ax = fig.add_subplot(gs[1])
    ks = ['20', '100', '500']
    names = ['Zurich', 'Madrid', 'Singapore']
    left = np.zeros(3)
    for k, c in enumerate(names + ['Other']):
        vals = np.array([100 * (s['dirichlet'][kk]['first'].get(c, 0) if c != 'Other' else
                                1 - sum(s['dirichlet'][kk]['first'].get(n, 0) for n in names)) for kk in ks])
        ax.barh(range(3), vals, left=left, height=.6, color=(SERIES + ['#c4c3bd'])[k] if k < 3 else '#c4c3bd', label=c)
        for j, v in enumerate(vals):
            if v > 8:
                ax.text(left[j] + v / 2, j, f'{v:.0f}%', ha='center', va='center', fontsize=9, color='white', weight='bold')
        left += vals
    ax.set_yticks(range(3)); ax.set_yticklabels([f'κ = {k}' for k in ks]); ax.set_ylim(2.5, -.5)
    ax.set_xlim(0, 100); ax.set_xticks([0, 50, 100]); ax.set_xticklabels(['0', '50%', '100%'])
    ax.tick_params(length=0)
    for sp in ['top', 'right', 'left']:
        ax.spines[sp].set_visible(False)
    ax.set_xlabel('Share of weight draws ranked first')
    ax.set_title('B   Random AHP weights', loc='left', fontsize=10.5, weight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(-.02, -.2), ncol=2, frameon=False, fontsize=9, handlelength=1, columnspacing=.8, handletextpad=.3)
    fig.savefig(FIG / 'robustness.pdf'); plt.close(fig)


if __name__ == '__main__' and 'extra' in __import__('sys').argv:
    d = data()
    raw_multiples(d[0]); robustness_fig(d[4])

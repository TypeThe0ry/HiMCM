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
from task4_v207_ahp import ahp_weights, CATEGORIES, OUT as RES, bounds
from audit_task4_v203 import raw_map
from task4_v207_flags import flag, COUNTRY

FIG = ROOT.parents[2] / 'HiMCM-Overleaf/figures'
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

"""V216 figures: method workflow with result podium (figures/workflow.pdf) and the
strengths/limits panel (figures/strengths.pdf). Drawn in inch coordinates."""
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle
from task4_v207_figures import INK, MUTED, FIG
from task4_v207_flags import flag, COUNTRY
from task4_v5_model import ROOT

RES = ROOT / 'results/task4_v214_final'
MEDAL = ['#c9a227', '#9aa0a6', '#b0703a']
STEP_COL = ['#2a78d6', '#1baf7a', '#eda100', '#eb6834', '#6250d6']


def canvas(W, H):
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    return fig, ax


def workflow():
    m = pd.read_csv(RES / 'main_ranking.csv')
    s = json.load(open(RES / 'summary.json'))
    import ast
    di = ast.literal_eval(s['dirichlet']) if isinstance(s['dirichlet'], str) else s['dirichlet']
    lead = m.city[0]
    share = 100 * di['100']['first'][lead]
    steps = [('Collect', f'{len(m)} cities', 'UN city definition;\n10 indicators from\npublic statistics'),
             ('Normalise', 'utility 0 to 1', 'each value compared\nwith a fixed anchor;\n1 is always better'),
             ('Weight', 'AHP, CR 0.006', 'pairwise judgements\nfrom a high-school\nstudent\'s view'),
             ('Score', 'TOPSIS 0-100', 'distance to the ideal\nand the worst city\nprofile'),
             ('Stress-test', f'1st in {share:.2f}%', 'of random weightings;\n31 source variants,\nVIKOR, 2035')]
    W, H = 6.5, 2.62
    fig, ax = canvas(W, H)
    n = len(steps); gap = .07; cw = (W - gap * (n - 1)) / n; top = H - .02; hh = .34
    for k, (title, key, body) in enumerate(steps):
        x = k * (cw + gap); col = STEP_COL[k]
        tip = .13 if k < n - 1 else 0
        notch = .13 if k > 0 else 0
        ax.add_patch(Polygon([(x, top), (x + cw, top), (x + cw + tip, top - hh / 2), (x + cw, top - hh), (x, top - hh),
                              (x + notch, top - hh / 2)], closed=True, fc=col, ec='none'))
        ax.text(x + notch + .07, top - hh / 2, f'{k + 1}', fontsize=11, weight='bold', color='white', va='center', alpha=.75)
        ax.text(x + notch + .25, top - hh / 2, title, fontsize=9.5, weight='bold', color='white', va='center')
        ax.text(x + cw / 2, top - hh - .2, key, fontsize=9.5, weight='bold', color=col, ha='center', va='center')
        ax.text(x + cw / 2, top - hh - .56, body, fontsize=8.6, color=INK, ha='center', va='center', linespacing=1.1)
    # result banner
    by, bh = .04, 1.12
    ax.add_patch(FancyBboxPatch((0, by), W, bh, boxstyle='round,pad=0,rounding_size=.08', fc='#f4f3ef', ec='none'))
    ax.annotate('', xy=(1.2, by + bh + .02), xytext=(1.2, top - hh - .86),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1, mutation_scale=9))
    ax.text(.14, by + bh - .2, 'RESULT', fontsize=9, weight='bold', color=MUTED, va='center')
    ax.text(.14, by + bh - .46, f'{lead} ranks first,', fontsize=10.5, weight='bold', color=INK, va='center')
    ax.text(.14, by + bh - .68, f'{m.city[1]} a clear second', fontsize=10.5, weight='bold', color=INK, va='center')
    ax.text(.14, by + .2, f'Shortlist for families: top five,\nthen check admission and cost', fontsize=8.6, color=MUTED, va='center', linespacing=1.1)
    # podium: 2 1 3
    order = [1, 0, 2]; heights = [.42, .62, .3]; pw = 1.12; px0 = 2.75
    for slot, i in enumerate(order):
        x = px0 + slot * (pw + .06); h = heights[slot]
        ax.add_patch(FancyBboxPatch((x, by + .06), pw, h, boxstyle='round,pad=0,rounding_size=.05', fc=MEDAL[i], ec='none'))
        ax.text(x + pw / 2, by + .06 + h / 2, f'{i + 1}', fontsize=12, weight='bold', color='white', ha='center', va='center')
        c = m.city[i]
        yy = by + .06 + h + .1
        flag(ax, COUNTRY[c], x + pw / 2 - .15, yy, .3, .2)
        ax.text(x + pw / 2, yy + .33, c, fontsize=9.5, weight='bold', color=INK, ha='center', va='center')
        ax.text(x + pw + .0 - .06, by + .06 + h - .12, f'{m.score[i]:.1f}', fontsize=8.6, color='white', ha='right', va='center')
    fig.savefig(FIG / 'workflow.pdf'); plt.close(fig)
    print('wrote workflow.pdf')


def strengths():
    S = [('Weights from a student\'s view', 'Two-level AHP over five categories, CR 0.006.'),
         ('One yardstick for 44 cities', 'Ten public indicators and the UN city definition.'),
         ('Stress-tested', '31 variants, withdrawals, random weights, VIKOR.'),
         ('Ready for families', 'Three priority profiles and 2035 scenarios.')]
    L = [('Small cities, national data', 'Some Luxembourg indicators exist only nationally.'),
         ('Ten indicators only', 'Language, admission and culture stay outside.'),
         ('Judgement in the weights', 'Equal weights put Reykjavik first.'),
         ('A snapshot in time', 'Data from 2022-2026; 2035 runs are scenarios.')]
    W, H = 6.5, 2.05
    fig, ax = canvas(W, H)
    cw = (W - .14) / 2
    for col_i, (items, title, col, sym) in enumerate([(S, 'Strengths', '#1baf7a', '+'), (L, 'Limits', '#e34948', '–')]):
        x0 = col_i * (cw + .14)
        ax.add_patch(FancyBboxPatch((x0, H - .3), cw, .28, boxstyle='round,pad=0,rounding_size=.06', fc=col, ec='none'))
        ax.text(x0 + .12, H - .16, title, fontsize=10, weight='bold', color='white', va='center')
        rh = (H - .36) / 4
        for k, (head, body) in enumerate(items):
            y = H - .36 - (k + .5) * rh
            ax.add_patch(FancyBboxPatch((x0, y - rh / 2 + .03), cw, rh - .06, boxstyle='round,pad=0,rounding_size=.05', fc='#f4f3ef', ec='none'))
            ax.add_patch(Circle((x0 + .2, y), .11, color=col))
            ax.text(x0 + .2, y + .005, sym, fontsize=11, weight='bold', color='white', ha='center', va='center')
            ax.text(x0 + .4, y + .09, head, fontsize=9.3, weight='bold', color=INK, va='center')
            ax.text(x0 + .4, y - .1, body, fontsize=8.6, color=MUTED, va='center')
    fig.savefig(FIG / 'strengths.pdf'); plt.close(fig)
    print('wrote strengths.pdf')


if __name__ == '__main__':
    workflow(); strengths()

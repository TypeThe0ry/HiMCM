"""V215 regional figure (figures/regions.pdf): score strips by region + mean category utilities."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from task4_v207_figures import INK, MUTED, GRID, SPECTRUM, CAT_SHORT, FIG
from task4_v207_flags import flag, COUNTRY
from task4_v215_regions import regions, CATS

SHORTREG = {'Southeast Asia and Oceania': 'SE Asia & Oceania', 'Gulf and Türkiye': 'Gulf & Türkiye'}


def main():
    m, reg = regions()
    order = list(reg.index)
    fig = plt.figure(figsize=(6.5, 3.35))
    ax = fig.add_axes([.005, .1, .64, .80])
    hx = fig.add_axes([.665, .1, .33, .80])
    n = len(order)
    for i, r in enumerate(order):
        d = m[m.region == r].sort_values('score')
        y = i
        ax.plot([d.score.min(), d.score.max()], [y, y], color=GRID, lw=5, solid_capstyle='round', zorder=1)
        ax.scatter(d.score, [y] * len(d), s=26, color='#2a78d6', edgecolor='white', lw=.8, zorder=3)
        med = d.score.median()
        ax.plot([med, med], [y - .3, y + .3], color=INK, lw=2.2, zorder=4)
        b, w = d.iloc[-1], d.iloc[0]
        flag(ax, COUNTRY[b.city], b.score + 1.3, y + .16, 2.2, -.32, clip=False)
        ax.text(b.score + 4.0, y, f'{b.city} ({b["rank"]})', va='center', ha='left', fontsize=9, color=INK, weight='bold', clip_on=False)
        if len(d) > 1:
            ax.text(w.score - 4.0, y, f'{w.city} ({w["rank"]})', va='center', ha='right', fontsize=9, color=MUTED)
            flag(ax, COUNTRY[w.city], w.score - 3.5, y + .16, 2.2, -.32, clip=False)
    ax.set_ylim(n - .45, -.75)
    ax.set_xlim(11, 87)
    ax.set_yticks(range(n))
    ax.set_yticklabels([])
    for i, r in enumerate(order):
        ax.text(11.5, i - .42, f'{r}  ·  {int(reg.loc[r, "n"])} cities', fontsize=9, color=MUTED, weight='bold', va='center')
    ax.set_xticks([40, 50, 60, 70])
    ax.tick_params(length=0, labelsize=9)
    ax.grid(axis='x', color=GRID, lw=.6, zorder=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel('Representative score (0-100)', fontsize=9, color=MUTED, labelpad=2)
    ax.set_title('A   Scores by region (rank in brackets)', loc='left', fontsize=10, weight='bold', pad=6)

    M = reg[CATS].to_numpy()
    for i in range(n):
        for j in range(len(CATS)):
            v = M[i, j]
            hx.add_patch(Rectangle((j, i - .5), 1, 1, facecolor=SPECTRUM(v), edgecolor='white', lw=1.2))
            hx.text(j + .5, i, f'{v:.2f}', ha='center', va='center', fontsize=9, color='white' if (v > .8 or v < .15) else INK)
    hx.set_xlim(0, len(CATS)); hx.set_ylim(n - .45, -.75)
    hx.set_yticks([]); hx.set_xticks(np.arange(len(CATS)) + .5)
    hx.set_xticklabels(['Safety\n& env.', 'Cost of\nliving', 'Educ-\nation', 'Mobility\n', 'Daily\nlife'], fontsize=9, linespacing=.9)
    hx.xaxis.tick_bottom(); hx.tick_params(length=0, pad=2)
    for s in hx.spines.values():
        s.set_visible(False)
    hx.set_title('B   Mean category utility', loc='left', fontsize=10, weight='bold', pad=6)
    fig.savefig(FIG / 'regions.pdf'); plt.close(fig)
    print('wrote', FIG / 'regions.pdf')


if __name__ == '__main__':
    main()

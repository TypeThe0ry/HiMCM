"""V215 regional figure (figures/regions.pdf), redesigned twice on 15 Nov after TT feedback.

Panel A: one row per region; each city a dot on a wide score axis, the median a diamond,
the region's best city named on the right. Panel B: mean category utility per region as
solid bars in the category colours used elsewhere in the paper.
Drawn in inch coordinates so flags keep their shape.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from task4_v207_figures import INK, MUTED, GRID, FIG
from task4_v207_flags import flag, COUNTRY
from task4_v215_regions import regions, CATS

CAT_COL = ['#2a78d6', '#eda100', '#1baf7a', '#6250d6', '#eb6834']
CAT_HEAD = ['Safety & env.', 'Cost of living', 'Education', 'Mobility', 'Daily life']
ACCENT = '#2a78d6'
W = 6.5
LAB = 1.28                                   # region-label column width
X0, X1, S0, S1 = LAB + .08, 4.62, 35, 71     # score axis in inches
XB = 4.78                                    # best-city column
RA, RB = .255, .185                          # row heights, panels A and B
SHORT = {'Southeast Asia and Oceania': 'SE Asia & Oceania', 'Gulf and Türkiye': 'Gulf & Türkiye'}


def sx(s):
    return X0 + (s - S0) / (S1 - S0) * (X1 - X0)


def main():
    m, reg = regions()
    order = list(reg.index)
    n = len(order)
    hA = .3 + n * RA + .36
    hB = .45 + n * RB + .05
    H = hA + .12 + hB
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    rend = fig.canvas.get_renderer()

    # ---------------- panel A
    top = H
    ax.text(0, top - .13, 'A', fontsize=10.5, weight='bold', color=INK, va='center')
    ax.text(.2, top - .13, 'City scores by region', fontsize=10, weight='bold', color=INK, va='center')
    ax.scatter([X1 - 1.62], [top - .13], s=19, color=ACCENT, edgecolor='white', lw=.6)
    ax.text(X1 - 1.55, top - .13, 'city', fontsize=9, color=MUTED, va='center')
    ax.scatter([X1 - 1.12], [top - .13], marker='D', s=30, color=INK, edgecolor='white', lw=.9)
    ax.text(X1 - 1.04, top - .13, 'regional median', fontsize=9, color=MUTED, va='center')
    ax.text(XB, top - .13, 'Best city (overall rank)', fontsize=9.5, weight='bold', color=INK, va='center')
    y0 = top - .3
    for s in (40, 45, 50, 55, 60, 65, 70):
        ax.plot([sx(s), sx(s)], [y0 - n * RA, y0], color=GRID, lw=.6 if s % 10 else .9, zorder=0)
        if s % 10 == 0:
            ax.text(sx(s), y0 - n * RA - .1, str(s), fontsize=9, color=MUTED, ha='center', va='center')
    ax.text(sx(53), y0 - n * RA - .27, 'representative score (0-100)', fontsize=9, color=MUTED, ha='center', va='center')
    for i, r in enumerate(order):
        yc = y0 - (i + .5) * RA
        if i % 2 == 0:
            ax.add_patch(Rectangle((0, yc - RA / 2), W, RA, color='#f4f3ef', lw=0, zorder=-1))
        d = m[m.region == r]
        t = ax.text(.02, yc, SHORT.get(r, r), fontsize=9.5, weight='bold', color=INK, va='center')
        bb = t.get_window_extent(rend).transformed(ax.transData.inverted())
        ax.text(bb.x1 + .06, yc, f'{len(d)}', fontsize=9, color=MUTED, va='center')
        lo, hi, med = d.score.min(), d.score.max(), d.score.median()
        ax.plot([sx(lo), sx(hi)], [yc, yc], color='#c9d9ee', lw=4.5, solid_capstyle='round', zorder=1)
        ax.scatter([sx(s) for s in d.score], [yc] * len(d), s=19, color=ACCENT, edgecolor='white', lw=.6, zorder=2)
        ax.scatter([sx(med)], [yc], marker='D', s=30, color=INK, edgecolor='white', lw=.9, zorder=3)
        b = d.loc[d.score.idxmax()]
        flag(ax, COUNTRY[b.city], XB, yc - .068, .2, .136)
        t = ax.text(XB + .26, yc, b.city, fontsize=9.5, weight='bold', color=INK, va='center')
        bb = t.get_window_extent(rend).transformed(ax.transData.inverted())
        ax.text(bb.x1 + .05, yc, f'({int(b["rank"])})', fontsize=9, color=MUTED, va='center')

    # ---------------- panel B
    top = hB
    ax.plot([0, W], [top + .06, top + .06], color=INK, lw=.6)
    ax.text(0, top - .14, 'B', fontsize=10.5, weight='bold', color=INK, va='center')
    ax.text(.2, top - .14, 'Mean category utility', fontsize=10, weight='bold', color=INK, va='center')
    cw = (W - LAB) / 5
    bmax = cw - .36
    y0 = top - .45
    for i, r in enumerate(order):
        yc = y0 - (i + .5) * RB
        if i % 2 == 0:
            ax.add_patch(Rectangle((0, yc - RB / 2), W, RB, color='#f4f3ef', lw=0, zorder=-1))
        ax.text(.02, yc, SHORT.get(r, r), fontsize=9, color=INK, va='center')
    for j, (c, col, h) in enumerate(zip(CATS, CAT_COL, CAT_HEAD)):
        x = LAB + j * cw + .04
        ax.text(x, y0 + .08, h, fontsize=9, weight='bold', color=col, va='center')
        vals = reg[c]
        best = vals.max()
        for i, r in enumerate(order):
            yc = y0 - (i + .5) * RB
            v = vals[r]
            ax.add_patch(Rectangle((x, yc - .06), bmax * v, .12, color=col, lw=0, zorder=2))
            ax.text(x + bmax * v + .04, yc, f'{v:.2f}', fontsize=9, color=INK, va='center',
                    weight='bold' if v == best else 'normal')
        ax.plot([x, x], [y0 - n * RB, y0], color=MUTED, lw=.6, zorder=1)
    fig.savefig(FIG / 'regions.pdf'); plt.close(fig)
    print('wrote', FIG / 'regions.pdf', f'{W} x {H:.2f} in')


if __name__ == '__main__':
    main()

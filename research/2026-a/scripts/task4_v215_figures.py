"""V215 regional figure (figures/regions.pdf), redesigned 15 Nov after TT feedback.

One row per region: score range of its cities (ticks) with the median, the region's best city,
and mean category utilities as tiles in the category colours used elsewhere in the paper.
Drawn in inch coordinates so flags and tiles keep their shape.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from task4_v207_figures import INK, MUTED, GRID, FIG
from task4_v207_flags import flag, COUNTRY
from task4_v215_regions import regions, CATS

CAT_COL = ['#2a78d6', '#eda100', '#1baf7a', '#6250d6', '#eb6834']
CAT_HEAD = ['Safety', 'Cost', 'Educ.', 'Mobility', 'Daily']
ACCENT = '#2a78d6'
W, ROW, TOP, BOT = 6.5, .37, .5, .42
X0, X1, S0, S1 = 1.3, 2.86, 35, 71          # score track: inches <-> score
XB = 3.0                                      # best-city column
XC, CW = 4.34, .432                           # category tiles


def sx(s):
    return X0 + (s - S0) / (S1 - S0) * (X1 - X0)


def main():
    m, reg = regions()
    order = list(reg.index)
    n = len(order)
    H = TOP + n * ROW + BOT
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

    yh = H - .2
    ax.text(0, yh, 'Region', fontsize=9.5, weight='bold', color=INK, va='center')
    ax.text((X0 + X1) / 2, yh, 'City scores, median', fontsize=9.5, weight='bold', color=INK, va='center', ha='center')
    ax.text(XB, yh, 'Best city (rank)', fontsize=9.5, weight='bold', color=INK, va='center')
    for j, (h, c) in enumerate(zip(CAT_HEAD, CAT_COL)):
        cx = XC + j * CW + CW / 2
        ax.text(cx, yh, h, fontsize=9, weight='bold', color=c, va='center', ha='center')
    ax.plot([0, W], [H - .38, H - .38], color=INK, lw=.8)

    for s in (40, 50, 60, 70):
        ax.plot([sx(s), sx(s)], [BOT, H - TOP + .02], color=GRID, lw=.6, zorder=0)
        ax.text(sx(s), BOT - .1, str(s), fontsize=9, color=MUTED, ha='center', va='center')
    ax.text(sx(55), BOT - .29, 'representative score', fontsize=9, color=MUTED, ha='center', va='center')

    for i, r in enumerate(order):
        yc = H - TOP - (i + .5) * ROW
        if i % 2 == 0:
            ax.add_patch(Rectangle((0, yc - ROW / 2), W, ROW, color='#f4f3ef', lw=0, zorder=-1))
        d = m[m.region == r]
        ax.text(0.04, yc + .065, r.replace('Southeast Asia and Oceania', 'SE Asia & Oceania').replace(' and ', ' & '),
                fontsize=9.5, weight='bold', color=INK, va='center')
        ax.text(0.04, yc - .095, f'{len(d)} {"city" if len(d) == 1 else "cities"}', fontsize=9, color=MUTED, va='center')
        lo, hi, med = d.score.min(), d.score.max(), d.score.median()
        ax.add_patch(FancyBboxPatch((sx(lo), yc - .055), sx(hi) - sx(lo), .11, boxstyle='round,pad=0,rounding_size=.055',
                                    color=ACCENT, alpha=.18, lw=0, zorder=1))
        for s in d.score:
            ax.plot([sx(s), sx(s)], [yc - .075, yc + .075], color=ACCENT, lw=1.3, zorder=2, solid_capstyle='round')
        ax.scatter([sx(med)], [yc], marker='D', s=34, color=INK, edgecolor='white', lw=1, zorder=3)
        b = d.loc[d.score.idxmax()]
        flag(ax, COUNTRY[b.city], XB, yc - .075, .225, .15)
        ax.text(XB + .29, yc, b.city, fontsize=9.5, weight='bold', color=INK, va='center')
        t = ax.text(XB + .29, yc, b.city, fontsize=9.5, weight='bold', color=INK, va='center', alpha=0)
        bb = t.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted()); t.remove()
        ax.text(bb.x1 + .05, yc, f'({int(b["rank"])})', fontsize=9, color=MUTED, va='center')
        for j, (c, col) in enumerate(zip(CATS, CAT_COL)):
            v = reg.loc[r, c]
            a = min(1, max(.12, (v - .3) / .45))
            x = XC + j * CW + .03
            ax.add_patch(FancyBboxPatch((x, yc - .12), CW - .06, .24, boxstyle='round,pad=0,rounding_size=.04', color=col, alpha=a, lw=0))
            ax.text(x + (CW - .06) / 2, yc, f'{v:.2f}', fontsize=9, ha='center', va='center', color='white' if a > .55 else INK,
                    weight='bold' if a > .55 else 'normal')
    ax.text(W, BOT - .2, 'Tiles: mean utility in safety & environment, cost of living,\neducation, mobility, daily life (darker = better)', fontsize=9, color=MUTED, ha='right', va='center')
    fig.savefig(FIG / 'regions.pdf'); plt.close(fig)
    print('wrote', FIG / 'regions.pdf', f'{W} x {H:.2f} in')


if __name__ == '__main__':
    main()

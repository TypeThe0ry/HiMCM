"""Vector national flags drawn with matplotlib patches (simplified, no downloads)."""
import numpy as np
from matplotlib.patches import Rectangle, Polygon

COUNTRY = {'Vienna': 'AT', 'Zurich': 'CH', 'Helsinki': 'FI', 'Berlin': 'DE', 'London': 'GB',
           'Amsterdam': 'NL', 'Stockholm': 'SE', 'Paris': 'FR', 'Madrid': 'ES', 'Milan': 'IT',
           'Dublin': 'IE', 'Oslo': 'NO', 'Prague': 'CZ', 'Warsaw': 'PL', 'Singapore': 'SG', 'Tokyo': 'JP',
           # V214 expansion (27 cities)
           'New York': 'US', 'Los Angeles': 'US', 'Chicago': 'US', 'San Francisco': 'US',
           'Beijing': 'CN', 'Shanghai': 'CN', 'Shenzhen': 'CN', 'Guangzhou': 'CN', 'Hong Kong SAR': 'HK', 'Macao SAR': 'MO',
           'New Delhi': 'IN', 'Mumbai': 'IN', 'Toronto': 'CA', 'Sao Paulo': 'BR', 'Mexico City': 'MX',
           'Buenos Aires': 'AR', 'Copenhagen': 'DK', 'Luxembourg': 'LU', 'Reykjavik': 'IS', 'Dubai': 'AE',
           'Abu Dhabi': 'AE', 'Istanbul': 'TR', 'Cairo': 'EG', 'Johannesburg': 'ZA', 'Nairobi': 'KE',
           'Seoul': 'KR', 'Sydney': 'AU', 'Kuala Lumpur': 'MY'}


def _rect(ax, x, y, w, h, c, z=6):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=c, edgecolor='none', lw=0, zorder=z))


def _h(ax, x, y, w, h, cols):
    k = len(cols)
    for i, c in enumerate(cols):
        _rect(ax, x, y + h * (k - 1 - i) / k, w, h / k, c)


def _v(ax, x, y, w, h, cols):
    k = len(cols)
    for i, c in enumerate(cols):
        _rect(ax, x + w * i / k, y, w / k, h, c)


def _nordic(ax, x, y, w, h, bg, cross, inner=None):
    _rect(ax, x, y, w, h, bg)
    cx = x + w * .36
    bands = [(cross, h * (.3 if inner else .22))] + ([(inner, h * .13)] if inner else [])
    for col, th in bands:
        _rect(ax, x, y + h / 2 - th / 2, w, th, col, 7)
        _rect(ax, cx - th * w / h / 1.5 / 2, y, th * w / h / 1.5, h, col, 7)


def _ellipse(cx, cy, rx, ry, n=48):
    t = np.linspace(0, 2 * np.pi, n)
    return np.c_[cx + rx * np.cos(t), cy + ry * np.sin(t)]


def _star(cx, cy, rx, ry, n=5, inner=.4, rot=np.pi / 2):
    """Vertices of an n-pointed star with horizontal/vertical radii rx, ry (data units)."""
    t = rot + np.arange(2 * n) * np.pi / n
    r = np.where(np.arange(2 * n) % 2 == 0, 1.0, inner)
    return np.c_[cx + rx * r * np.cos(t), cy + ry * r * np.sin(t)]


def _poly(ax, pts, col, z=7):
    ax.add_patch(Polygon(pts, facecolor=col, edgecolor='none', zorder=z))


def _band(ax, x0, y0, x1, y1, th, col):
    # th is a thickness in data y-units; approximate in mixed units.
    p0, p1 = np.array([x0, y0]), np.array([x1, y1])
    off = np.array([0, th / 2])
    ax.add_patch(Polygon([p0 + off, p1 + off, p1 - off, p0 - off], facecolor=col, edgecolor='none', zorder=7))


def flag(ax, code, x, y, w, h, clip=True):
    """Draw flag `code` with lower-left corner (x, y) and size (w, h) in data units."""
    n0 = len(ax.patches)
    if h > 0 and ax.yaxis_inverted():  # keep flags upright on inverted y axes
        y, h = y + h, -h
    _draw(ax, code, x, y, w, h)
    if not clip:
        for patch in ax.patches[n0:]:
            patch.set_clip_on(False)


def _draw(ax, code, x, y, w, h):
    if code == 'AT': _h(ax, x, y, w, h, ['#c8102e', 'white', '#c8102e'])
    elif code == 'DE': _h(ax, x, y, w, h, ['#000000', '#dd0000', '#ffce00'])
    elif code == 'NL': _h(ax, x, y, w, h, ['#ae1c28', 'white', '#21468b'])
    elif code == 'PL': _h(ax, x, y, w, h, ['white', '#dc143c'])
    elif code == 'ES':
        _rect(ax, x, y, w, h, '#aa151b'); _rect(ax, x, y + h / 4, w, h / 2, '#f1bf00', 7)
    elif code == 'FR': _v(ax, x, y, w, h, ['#002395', 'white', '#ed2939'])
    elif code == 'IT': _v(ax, x, y, w, h, ['#009246', 'white', '#ce2b37'])
    elif code == 'IE': _v(ax, x, y, w, h, ['#169b62', 'white', '#ff883e'])
    elif code == 'FI': _nordic(ax, x, y, w, h, 'white', '#003580')
    elif code == 'SE': _nordic(ax, x, y, w, h, '#006aa7', '#fecc00')
    elif code == 'NO': _nordic(ax, x, y, w, h, '#ba0c2f', 'white', '#00205b')
    elif code == 'CH':
        _rect(ax, x, y, w, h, '#da291c')
        a, b = .62, .2  # arm length and width as fractions of height
        sx = w / h / 1.5  # aspect correction when w/h is not 1.5 in display units
        _rect(ax, x + w / 2 - b * h * sx / 2, y + h / 2 - a * h / 2, b * h * sx, a * h, 'white', 7)
        _rect(ax, x + w / 2 - a * h * sx / 2, y + h / 2 - b * h / 2, a * h * sx, b * h, 'white', 7)
    elif code == 'CZ':
        _h(ax, x, y, w, h, ['white', '#d7141a'])
        ax.add_patch(Polygon([(x, y), (x, y + h), (x + w / 2, y + h / 2)], facecolor='#11457e', edgecolor='none', zorder=7))
    elif code == 'JP':
        _rect(ax, x, y, w, h, 'white')
        ax.add_patch(Polygon(_ellipse(x + w / 2, y + h / 2, w * .2, h * .3), facecolor='#bc002d', edgecolor='none', zorder=7))
    elif code == 'SG':
        _h(ax, x, y, w, h, ['#ef3340', 'white'])
        ax.add_patch(Polygon(_ellipse(x + w * .2, y + h * .75, w * .1, h * .17), facecolor='white', edgecolor='none', zorder=7))
        ax.add_patch(Polygon(_ellipse(x + w * .245, y + h * .75, w * .1, h * .17), facecolor='#ef3340', edgecolor='none', zorder=8))
        for k in range(5):
            t = np.pi / 2 + 2 * np.pi * k / 5
            ax.add_patch(Polygon(_ellipse(x + w * (.33 + .07 * np.cos(t)), y + h * (.75 + .1 * np.sin(t)), w * .018, h * .03, 12),
                                 facecolor='white', edgecolor='none', zorder=8))
    elif code == 'GB':
        _rect(ax, x, y, w, h, '#012169')
        for th, col in [(h * .2, 'white'), (h * .08, '#c8102e')]:
            _band(ax, x, y, x + w, y + h, th, col); _band(ax, x, y + h, x + w, y, th, col)
        for th, col in [(h * .34, 'white'), (h * .2, '#c8102e')]:
            _rect(ax, x, y + h / 2 - th / 2, w, th, col, 8)
            _rect(ax, x + w / 2 - th * w / h / 1.5 / 2, y, th * w / h / 1.5, h, col, 8)
    # --- V214 expansion ---
    elif code == 'US':
        _h(ax, x, y, w, h, ['#b22234', 'white'] * 6 + ['#b22234'])
        cw, ch = w * .4, h * 7 / 13
        _rect(ax, x, y + h - ch, cw, ch, '#3c3b6e', 7)
        for i in range(3):
            for j in range(3):
                _poly(ax, _ellipse(x + cw * (.2 + .3 * i), y + h - ch * (.2 + .3 * j), w * .02, h * .03, 10), 'white', 8)
    elif code == 'CN':
        _rect(ax, x, y, w, h, '#de2910')
        _poly(ax, _star(x + w * .17, y + h * .7, w * .1, h * .15), '#ffde00')
        for k, (sx, sy) in enumerate([(.33, .9), (.4, .78), (.4, .62), (.33, .5)]):
            _poly(ax, _star(x + w * sx, y + h * sy, w * .033, h * .05), '#ffde00')
    elif code == 'HK':
        _rect(ax, x, y, w, h, '#de2910')
        for k in range(5):
            t = np.pi / 2 + 2 * np.pi * k / 5
            _poly(ax, _ellipse(x + w / 2 + w * .09 * np.cos(t), y + h / 2 + h * .135 * np.sin(t), w * .075, h * .11), 'white')
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .03, h * .045), '#de2910', 8)
    elif code == 'MO':
        _rect(ax, x, y, w, h, '#00785e')
        _poly(ax, _ellipse(x + w / 2, y + h * .42, w * .13, h * .19), 'white')
        _rect(ax, x + w * .33, y + h * .3, w * .34, h * .035, 'white', 8)
        _poly(ax, _star(x + w / 2, y + h * .8, w * .05, h * .075), '#fbd116')
        for sx in (.37, .63):
            _poly(ax, _star(x + w * sx, y + h * .72, w * .03, h * .045), '#fbd116')
    elif code == 'IN':
        _h(ax, x, y, w, h, ['#ff9933', 'white', '#138808'])
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .09, h * .135), '#000080')
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .065, h * .1), 'white', 8)
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .015, h * .022), '#000080', 8)
    elif code == 'CA':
        _rect(ax, x, y, w, h, 'white'); _rect(ax, x, y, w / 4, h, '#d80621', 7); _rect(ax, x + 3 * w / 4, y, w / 4, h, '#d80621', 7)
        leaf = np.array([(0, .95), (.18, .62), (.4, .68), (.3, .3), (.62, .45), (.55, .2), (.08, .02), (.08, -.3), (0, -.3),
                         (-.08, -.3), (-.08, .02), (-.55, .2), (-.62, .45), (-.3, .3), (-.4, .68), (-.18, .62)]) * .42
        _poly(ax, np.c_[x + w / 2 + leaf[:, 0] * w / 1.5, y + h / 2 + (leaf[:, 1] - .3) * h], '#d80621')
    elif code == 'BR':
        _rect(ax, x, y, w, h, '#009c3b')
        _poly(ax, [(x + w * .08, y + h / 2), (x + w / 2, y + h * .92), (x + w * .92, y + h / 2), (x + w / 2, y + h * .08)], '#ffdf00')
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .17, h * .26), '#002776', 8)
        _band(ax, x + w * .33, y + h * .42, x + w * .67, y + h * .52, h * .06, 'white'); ax.patches[-1].set_zorder(9)
    elif code == 'MX':
        _v(ax, x, y, w, h, ['#006847', 'white', '#ce1126'])
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .06, h * .1), '#8c6a3a')
    elif code == 'AR':
        _h(ax, x, y, w, h, ['#74acdf', 'white', '#74acdf'])
        _poly(ax, _star(x + w / 2, y + h / 2, w * .07, h * .105, 12, .7), '#f6b40e')
    elif code == 'DK': _nordic(ax, x, y, w, h, '#c8102e', 'white')
    elif code == 'LU': _h(ax, x, y, w, h, ['#ed2939', 'white', '#00a1de'])
    elif code == 'IS': _nordic(ax, x, y, w, h, '#02529c', 'white', '#dc1e35')
    elif code == 'AE':
        _rect(ax, x, y, w, h, 'white'); _rect(ax, x + w / 4, y + 2 * h / 3, 3 * w / 4, h / 3, '#00732f', 7)
        _rect(ax, x + w / 4, y, 3 * w / 4, h / 3, 'black', 7); _rect(ax, x, y, w / 4, h, '#ff0000', 7)
    elif code == 'TR':
        _rect(ax, x, y, w, h, '#e30a17')
        _poly(ax, _ellipse(x + w * .33, y + h / 2, w * .17, h * .25), 'white')
        _poly(ax, _ellipse(x + w * .37, y + h / 2, w * .135, h * .2), '#e30a17', 8)
        _poly(ax, _star(x + w * .56, y + h / 2, w * .07, h * .105, rot=0), 'white', 8)
    elif code == 'EG':
        _h(ax, x, y, w, h, ['#ce1126', 'white', 'black'])
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .05, h * .09), '#c09300')
    elif code == 'ZA':
        _rect(ax, x, y + h / 2, w, h / 2, '#de3831'); _rect(ax, x, y, w, h / 2, '#002395')
        for col, t, z in [('white', .17, 7), ('#007a4d', .10, 8)]:
            _poly(ax, [(x, y + h * (1 - t * .6)), (x + w * (.5 - t * .4), y + h * (.5 + t / 2)), (x + w, y + h * (.5 + t / 2)),
                       (x + w, y + h * (.5 - t / 2)), (x + w * (.5 - t * .4), y + h * (.5 - t / 2)), (x, y + h * t * .6)], col, z)
        _poly(ax, [(x, y + h * .9), (x + w * .36, y + h / 2), (x, y + h * .1)], '#ffb612', 9)
        _poly(ax, [(x, y + h * .78), (x + w * .26, y + h / 2), (x, y + h * .22)], 'black', 10)
    elif code == 'KE':
        _h(ax, x, y, w, h, ['black', '#bb0000', '#006600'])
        for yy in (h / 3, 2 * h / 3):
            _rect(ax, x, y + yy - h * .025, w, h * .05, 'white', 7)
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .07, h * .3), 'white', 8)
        _poly(ax, _ellipse(x + w / 2, y + h / 2, w * .05, h * .25), '#bb0000', 9)
    elif code == 'KR':
        _rect(ax, x, y, w, h, 'white')
        cx, cy, rx, ry = x + w / 2, y + h / 2, w * .17, h * .25
        _poly(ax, _ellipse(cx, cy, rx, ry), '#cd2e3a')
        t = np.linspace(np.pi, 2 * np.pi, 30)
        lower = np.c_[cx + rx * np.cos(t), cy + ry * np.sin(t)]
        _poly(ax, lower, '#0047a0', 8)
        _poly(ax, _ellipse(cx - rx / 2, cy, rx / 2, ry / 2), '#cd2e3a', 9)
        _poly(ax, _ellipse(cx + rx / 2, cy, rx / 2, ry / 2), '#0047a0', 9)
        for sx in (.12, .88):
            for dy in (-.1, 0, .1):
                _rect(ax, x + w * sx - w * .05, y + h * (.5 + dy) - h * .02, w * .1, h * .04, 'black', 8)
    elif code == 'AU':
        _rect(ax, x, y, w, h, '#012169')
        cw, ch = w / 2, h / 2
        for th, col in [(ch * .2, 'white'), (ch * .08, '#c8102e')]:
            _band(ax, x, y + h - ch, x + cw, y + h, th, col); _band(ax, x, y + h, x + cw, y + h - ch, th, col)
        for th, col in [(ch * .34, 'white'), (ch * .2, '#c8102e')]:
            _rect(ax, x, y + h - ch / 2 - th / 2, cw, th, col, 8)
            _rect(ax, x + cw / 2 - th * w / h / 1.5 / 2, y + h - ch, th * w / h / 1.5, ch, col, 8)
        _poly(ax, _star(x + w / 4, y + h / 4, w * .06, h * .09, 7, .5), 'white', 8)
        for sx, sy, r in [(.75, .85, .04), (.65, .55, .04), (.86, .6, .04), (.75, .3, .04), (.83, .45, .025)]:
            _poly(ax, _star(x + w * sx, y + h * sy, w * r, h * r * 1.5, 7, .5), 'white', 8)
    elif code == 'MY':
        _h(ax, x, y, w, h, ['#cc0001', 'white'] * 7)
        _rect(ax, x, y + h / 2, w / 2, h / 2, '#010066', 7)
        _poly(ax, _ellipse(x + w * .17, y + h * .75, w * .085, h * .13), '#ffcc00', 8)
        _poly(ax, _ellipse(x + w * .2, y + h * .75, w * .07, h * .11), '#010066', 9)
        _poly(ax, _star(x + w * .31, y + h * .75, w * .055, h * .085, 14, .6), '#ffcc00', 8)
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor='#9c9b95', lw=.4, zorder=9))


def flag_bar(ax, code, x0, w, y_top, h, ux, uy):
    """Fill a bar (data coords, y_top = visually upper edge on an inverted axis) with a flag pattern.

    ux, uy are inches per data unit, so crosses and crescents keep their shape on long bars.
    """
    from matplotlib.patches import Ellipse
    R = lambda xx, yy, ww, hh, col, z=3: ax.add_patch(Rectangle((xx, yy), ww, hh, facecolor=col, edgecolor='none', zorder=z))
    third = lambda cols: [R(x0 + w * i / 3, y_top, w / 3, h, c) for i, c in enumerate(cols)]
    hin = abs(h) * uy
    if code == 'CH':
        R(x0, y_top, w, h, '#d52b1e'); arm, bar = .55 * hin, .18 * hin
        cx, cy = x0 + .9 * hin / ux, y_top + h / 2
        R(cx - bar / ux / 2, cy - arm / uy / 2, bar / ux, arm / uy, 'white', 4)
        R(cx - arm / ux / 2, cy - bar / uy / 2, arm / ux, bar / uy, 'white', 4)
    elif code == 'ES':
        R(x0, y_top, w, h, '#aa151b'); R(x0, y_top + h / 4, w, h / 2, '#f1bf00', 4)
    elif code == 'SG':
        R(x0, y_top, w, h / 2, '#ef3340'); R(x0, y_top + h / 2, w, h / 2, 'white')
        ax.add_patch(Rectangle((x0, y_top), w, h, fill=False, edgecolor='#ef3340', lw=.6, zorder=5))
        r = .17 * hin; cx, cy = x0 + 1.6 * r / ux, y_top + h / 4
        ax.add_patch(Ellipse((cx, cy), 2 * r / ux, 2 * r / uy, color='white', zorder=4))
        ax.add_patch(Ellipse((cx + .45 * r / ux, cy), 2 * r / ux, 2 * r / uy, color='#ef3340', zorder=4))
    elif code == 'IT': third(['#009246', '#f4f5f0', '#ce2b37'])
    elif code == 'IE': third(['#169b62', '#f4f5f0', '#ff883e'])
    elif code == 'FR': third(['#002395', '#f4f5f0', '#ed2939'])
    else:
        R(x0, y_top, w, h, '#c4c3bd')
    ax.add_patch(Rectangle((x0, y_top), w, h, fill=False, edgecolor='#9c9b95', lw=.5, zorder=6))

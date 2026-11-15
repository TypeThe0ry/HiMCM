"""Vector national flags drawn with matplotlib patches (simplified, no downloads)."""
import numpy as np
from matplotlib.patches import Rectangle, Polygon

COUNTRY = {'Vienna': 'AT', 'Zurich': 'CH', 'Helsinki': 'FI', 'Berlin': 'DE', 'London': 'GB',
           'Amsterdam': 'NL', 'Stockholm': 'SE', 'Paris': 'FR', 'Madrid': 'ES', 'Milan': 'IT',
           'Dublin': 'IE', 'Oslo': 'NO', 'Prague': 'CZ', 'Warsaw': 'PL', 'Singapore': 'SG', 'Tokyo': 'JP'}


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


def _band(ax, x0, y0, x1, y1, th, col):
    # th is a thickness in data y-units; approximate in mixed units.
    p0, p1 = np.array([x0, y0]), np.array([x1, y1])
    off = np.array([0, th / 2])
    ax.add_patch(Polygon([p0 + off, p1 + off, p1 - off, p0 - off], facecolor=col, edgecolor='none', zorder=7))


def flag(ax, code, x, y, w, h, clip=True):
    """Draw flag `code` with lower-left corner (x, y) and size (w, h) in data units."""
    n0 = len(ax.patches)
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

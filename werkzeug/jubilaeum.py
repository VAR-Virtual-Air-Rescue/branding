# -*- coding: utf-8 -*-
"""Das Jubilaeums-Profilbild: der Hubschrauber ist die Kerze.

Der erste Anlauf stellte eine Ziffernkerze links auf die Kante -- gross und
lesbar, aber sie verdeckte den Heckausleger. Der Hubschrauber ist das Zeichen;
was ihn anschneidet, ist die Kante, und sonst nichts. Also steht jetzt nichts
mehr davor.

Stattdessen sitzt der **Docht auf dem Rotorkopf**, die Flamme brennt zwischen
den beiden Blaettern, und der Hubschrauber wird damit selbst zur Kerze. Die
Ziffer kommt dazu, sobald die Flamme steht -- links oben im Himmel, hinter
allem, so gross, wie der Kreis dort zulaesst.

**Welche Zwei.** Das Anniversary-Banner (werkzeug/overload.py in var-v3) hat
zwei: die Linien-2 aus fuenf parallelen Baendern, und als Alternative die
Block-2 in Uniform Black. Auf dem Banner traegt die Linien-2 -- bei 640 px
Hoehe. Im Profilbild ist die Ziffer bei 128 px rund 22 px hoch; fuenf Linien
mit vier Luecken sind dann je ein Pixel, und die Zwei wird zur Schraffur.
Gemessen, nicht geschaetzt: `zweien_probe.png`. Deshalb die Block-2 -- sie ist
Teil desselben Satzes, nur die Fassung, die in klein traegt.

Die Linien-2 steht trotzdem hier, portiert aus overload.py: fuer den Fall, dass
das Motiv einmal gross gebraucht wird (Banner, Videowand, Kanalbild).
"""
import math, random

from tpl import txt, tw, uid, BLK, STRATOS, GALLIANO, IVORY
from mark import ANG

WARM = "#FFE9A8"
GLUT = "#F5A623"
DOCHT = "#8F6C04"
DAUER = 9.0


# =========================================================================
#  Die Linien-2 -- portiert aus overload.py (var-v3), unveraendert im Aufbau
# =========================================================================
def zwei_pfad(kante=False):
    """Skelett der 2 in einem 1000er-Kasten (760 breit). Liefert (d, bandbreite)."""
    W = 180
    Cx, Cy, R = 380, 380, 290
    r0, th0 = 100, 25
    K = (180, 900)
    pts = []
    th = th0
    while th <= th0 + 360:
        r = r0 + (R - r0) * (th - th0) / 360
        a = math.radians(th)
        pts.append((Cx + r * math.cos(a), Cy + r * math.sin(a)))
        th += 1
    th = th0 + 360
    while th <= th0 + 520:
        a = math.radians(th)
        J = (Cx + R * math.cos(a), Cy + R * math.sin(a))
        tang = (-math.sin(a), math.cos(a))
        toK = (K[0] - J[0], K[1] - J[1])
        n = math.hypot(*toK)
        if th > th0 + 380 and tang[0] * toK[1] / n - tang[1] * toK[0] / n > 0:
            break
        pts.append(J)
        th += 1
    pts.append(K)
    L = 760 - K[0]
    pts.append((760, K[1] - L * math.tan(math.radians(abs(ANG)))) if kante else (760, K[1]))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), W


def linien_zwei(h, farbe=GALLIANO, linien=5, cid=None):
    """Die Linien-2, `h` hoch, Ursprung links oben. Liefert (svg, breite)."""
    cid = cid or uid("zw")
    d, W = zwei_pfad()
    sc = h / 1000
    t = W / (2 * linien - 1)
    masken, w = [], W
    for i in range(2 * linien - 1):
        masken.append(f'<path d="{d}" fill="none" stroke="{"white" if i % 2 == 0 else "black"}" '
                      f'stroke-width="{w:.2f}" stroke-linecap="butt" stroke-linejoin="miter" '
                      f'stroke-miterlimit="4"/>')
        w -= 2 * t
    return (f'<defs><mask id="{cid}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1400" '
            f'height="1400">{"".join(masken)}</mask></defs>'
            f'<g transform="scale({sc:.5f})"><rect x="-100" y="-100" width="1100" height="1200" '
            f'fill="{farbe}" mask="url(#{cid})"/></g>'), 760 * sc


def block_zwei(h, farbe=GALLIANO, jahr="2"):
    """Die Block-2 aus Uniform Black, Versalhoehe `h`, Ursprung links oben."""
    gr = h / 0.72
    t, b = txt(jahr, gr, farbe, 0, h, BLK, 0)
    return t, b


# =========================================================================
#  Docht und Flamme
# =========================================================================
def _kt(*paare):
    zs = ";".join(str(v) for _, v in paare)
    ts = ";".join(f"{min(1.0, max(0.0, t / DAUER)):.4f}" for t, _ in paare)
    return zs, ts


def _anim(attr, paare, typ=None, additiv=False):
    zs, ts = _kt(*paare)
    if typ:
        return (f'<animateTransform attributeName="transform" type="{typ}" '
                f'values="{zs}" keyTimes="{ts}" dur="{DAUER}s" repeatCount="indefinite"'
                f'{" additive=\"sum\"" if additiv else ""}/>')
    return (f'<animate attributeName="{attr}" values="{zs}" keyTimes="{ts}" '
            f'dur="{DAUER}s" repeatCount="indefinite"/>')


def _flackern(t0, t1, ruhe=1.0, hub=0.09, schritt=0.11, seed=3):
    r = random.Random(seed)
    out, t = [], t0
    while t < t1:
        out.append((t, round(ruhe + r.uniform(-hub, hub), 3)))
        t += schritt * r.uniform(0.7, 1.3)
    return out


def _flamme(h, w):
    aussen = (f'M0,{-h:.1f} C{w:.1f},{-h*.55:.1f} {w:.1f},{-h*.12:.1f} 0,0 '
              f'C{-w:.1f},{-h*.12:.1f} {-w:.1f},{-h*.55:.1f} 0,{-h:.1f}Z')
    hi, wi = h * .55, w * .5
    innen = (f'M0,{-hi:.1f} C{wi:.1f},{-hi*.5:.1f} {wi:.1f},{-hi*.1:.1f} 0,0 '
             f'C{-wi:.1f},{-hi*.1:.1f} {-wi:.1f},{-hi*.5:.1f} 0,{-hi:.1f}Z')
    return (f'<path d="{aussen}" fill="{GLUT}"/><path d="{innen}" fill="{WARM}"/>'
            f'<circle cy="{-hi*.35:.1f}" r="{wi*.55:.1f}" fill="{IVORY}"/>')


# Der Rotorkopf, am gerenderten Zeichen gemessen: die Nabe liegt bei y=150,
# der Mast darunter bei x 261..270. Der Docht steht auf der Nabe.
ROTORKOPF = (268, 149)


def docht_und_flamme(bewegt=False, x=ROTORKOPF[0], y=ROTORKOPF[1]):
    """Docht auf dem Rotorkopf, Flamme darueber. Ursprung: Fuss des Dochts."""
    dh = 16                    # Dochthoehe
    fh, fw = 46, 12            # Flamme
    docht = (f'<line x1="0" y1="0" x2="0" y2="{-dh}" stroke="{DOCHT}" '
             f'stroke-width="3.2" stroke-linecap="round"/>')
    if not bewegt:
        return (f'<g transform="translate({x},{y})">{docht}'
                f'<g transform="translate(0,{-dh})"><circle r="30" fill="{GLUT}" opacity=".16"/>'
                f'{_flamme(fh, fw)}</g></g>')

    # Docht waechst aus der Nabe, dann Zuendblitz, dann Flackern, am Ende aus.
    docht_a = _anim(None, [(0, "1 0"), (0.15, "1 0"), (0.65, "1 1"), (8.7, "1 1"),
                           (8.95, "1 0"), (DAUER, "1 0")], typ="scale")
    fl = ([(0, 0), (0.95, 0), (1.12, 1.35), (1.26, 0.9)]
          + _flackern(1.35, 8.55, 1.0, 0.09, 0.13, seed=5)
          + [(8.6, 1), (8.85, 0), (DAUER, 0)])
    fl_scale = _anim(None, [(t, f"{v} {v}") for t, v in fl], typ="scale")
    neig = ([(0, 0), (1.3, 0)] + _flackern(1.35, 8.55, 0, 6, 0.17, seed=9)
            + [(8.6, 0), (DAUER, 0)])
    fl_skew = _anim(None, [(t, f"{v}") for t, v in neig], typ="skewX", additiv=True)
    blitz = _anim("opacity", [(0, 0), (0.92, 0), (1.0, .6), (1.26, 0), (DAUER, 0)])
    blitz_r = _anim("r", [(0, 2), (0.92, 2), (1.26, 52), (DAUER, 52)])
    schein = _anim("opacity", [(0, 0), (1.05, 0), (1.35, .16)]
                   + [(t, round(.16 + (v - 1) * .5, 3)) for t, v in _flackern(1.45, 8.5, 1, .06, .19, seed=2)]
                   + [(8.6, .16), (8.85, 0), (DAUER, 0)])
    return (f'<g transform="translate({x},{y})"><g>{docht_a}{docht}</g>'
            f'<g transform="translate(0,{-dh})">'
            f'<circle r="30" fill="{GLUT}" opacity="0">{schein}</circle>'
            f'<circle r="2" fill="{WARM}" opacity="0">{blitz}{blitz_r}</circle>'
            f'<g>{fl_scale}{fl_skew}{_flamme(fh, fw)}</g></g></g>')


# =========================================================================
#  Die Ziffer im Himmel
# =========================================================================
# Links oben, ueber dem linken Rotorblatt. Der Kreis laesst dort ein Feld von
# rund 90 Einheiten Hoehe zu, bevor die Zeichnung ihn oben beschneidet.
# Bei x=84 lag die obere linke Ecke der Ziffer bei y=42 -- der Kreis beginnt
# dort erst bei y=66, die Rundung schnitt die Zwei an. Bei x=102 ist oben
# Platz ab y=50; die rechte untere Ecke bleibt ueber dem linken Rotorblatt.
ZIFFER_X, ZIFFER_Y, ZIFFER_H = 102, 50, 90


def ziffer(jahr="2", bewegt=False):
    z, b = block_zwei(ZIFFER_H, GALLIANO, jahr)
    # Ursprung der Skalierung: die Mitte der Ziffer, damit sie aus sich selbst
    # heraus aufploppt und nicht aus einer Ecke.
    mx, my = ZIFFER_X + b / 2, ZIFFER_Y + ZIFFER_H / 2
    if not bewegt:
        return f'<g transform="translate({ZIFFER_X},{ZIFFER_Y})">{z}</g>'
    pop = _anim(None, [(0, "0 0"), (2.0, "0 0"), (2.35, "1.16 1.16"), (2.5, "0.95 0.95"),
                       (2.65, "1 1"), (8.6, "1 1"), (8.95, "0 0"), (DAUER, "0 0")], typ="scale")
    return (f'<g transform="translate({mx:.1f},{my:.1f})"><g>{pop}'
            f'<g transform="translate({-b/2:.1f},{-ZIFFER_H/2:.1f})">{z}</g></g></g>')

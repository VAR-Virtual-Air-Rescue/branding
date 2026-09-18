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

**Welche Zwei.** Die Linien-2 des Anniversary-Banners -- mit drei Linien statt
fuenf und in Ivory statt Gold. Beides ist gemessen, nicht gewaehlt
(linien2_probe.png, k3_farbe.png): bei 128 px, in denen Discord ein Servericon
zeigt, ist die Ziffer 50 px hoch und ihr Band neun Pixel breit. Fuenf Linien
mit vier Luecken sind dann je ein Pixel, eine Flaeche mit Textur; drei bleiben
Linien. Und Gold hinter dem goldenen Hubschrauber wird zum Knaeuel -- Ivory
loest die Ziffer vom Zeichen.

So gross passt sie nur hinter den Hubschrauber. Das geht, weil die Linien-2
offen ist: das Zeichen liegt davor und bleibt lesbar, die Spirale steht frei im
Himmel, Ausleger und Rotorblatt laufen durch den Fuss.
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


def _pfadlaenge(d):
    pts = [tuple(map(float, q.split(","))) for q in d[1:].split(" L")]
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def linien_zwei(h, farbe=GALLIANO, linien=5, cid=None, zeichnen=None):
    """Die Linien-2, `h` hoch, Ursprung links oben. Liefert (svg, breite).

    `zeichnen=(t0, t1)` laesst die Zwei sich zwischen t0 und t1 zeichnen -- von
    der Spiralmitte nach aussen bis zum Fuss. Das geht ueber `stroke-dashoffset`
    auf den Maskenlinien: alle teilen sich denselben Pfad, also zieht dieselbe
    Animation alle Baender gleichzeitig nach, mit ihren Luecken.
    """
    cid = cid or uid("zw")
    d, W = zwei_pfad()
    sc = h / 1000
    t = W / (2 * linien - 1)
    L = _pfadlaenge(d) + 2 * W        # etwas Reserve fuer die Kappen
    masken, w = [], W
    for i in range(2 * linien - 1):
        strich = ""
        if zeichnen:
            t0, t1 = zeichnen
            strich = (f' stroke-dasharray="{L:.0f}"><animate attributeName="stroke-dashoffset" '
                      f'values="{L:.0f};{L:.0f};0;0" keyTimes="0;{t0/DAUER:.4f};{t1/DAUER:.4f};1" '
                      f'dur="{DAUER}s" repeatCount="indefinite" calcMode="spline" '
                      f'keySplines="0 0 1 1;0.3 0 0.4 1;0 0 1 1"/></path')
        masken.append(f'<path d="{d}" fill="none" stroke="{"white" if i % 2 == 0 else "black"}" '
                      f'stroke-width="{w:.2f}" stroke-linecap="butt" stroke-linejoin="miter" '
                      f'stroke-miterlimit="4"' + (strich + ">" if strich else "/>"))
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
    dh = 20                    # Dochthoehe
    # Die Flamme ist das, woran man die Kerze erkennt -- bei 46 Einheiten war
    # sie im 128-px-Servericon elf Pixel hoch und ging unter. Jetzt doppelt.
    fh, fw = 84, 21            # Flamme
    docht = (f'<line x1="0" y1="0" x2="0" y2="{-dh}" stroke="{DOCHT}" '
             f'stroke-width="4.2" stroke-linecap="round"/>')
    if not bewegt:
        return (f'<g transform="translate({x},{y})">{docht}'
                f'<g transform="translate(0,{-dh})"><circle r="52" fill="{GLUT}" opacity=".16"/>'
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
    blitz_r = _anim("r", [(0, 2), (0.92, 2), (1.26, 80), (DAUER, 80)])
    schein = _anim("opacity", [(0, 0), (1.05, 0), (1.35, .16)]
                   + [(t, round(.16 + (v - 1) * .5, 3)) for t, v in _flackern(1.45, 8.5, 1, .06, .19, seed=2)]
                   + [(8.6, .16), (8.85, 0), (DAUER, 0)])
    return (f'<g transform="translate({x},{y})"><g>{docht_a}{docht}</g>'
            f'<g transform="translate(0,{-dh})">'
            f'<circle r="52" fill="{GLUT}" opacity="0">{schein}</circle>'
            f'<circle r="2" fill="{WARM}" opacity="0">{blitz}{blitz_r}</circle>'
            f'<g>{fl_scale}{fl_skew}{_flamme(fh, fw)}</g></g></g>')


# =========================================================================
#  Die Ziffer im Himmel -- die Linien-2, gross, hinter dem Hubschrauber
# =========================================================================
# Drei Linien statt fuenf. Bei 128 px, in denen Discord ein Servericon zeigt,
# ist eine Ziffer von 200 Einheiten 50 px hoch; das Band ist dann 9 px breit.
# Mit fuenf Linien sind das je ein Pixel Linie und Luecke -- eine Flaeche mit
# Textur. Mit dreien bleiben die Linien Linien. Angesehen in linien2_probe.png.
#
# So gross passt sie nur hinter den Hubschrauber. Das geht, weil die Linien-2
# offen ist: das Zeichen liegt davor und bleibt lesbar, die Spirale steht frei
# im Himmel, und Ausleger und Rotorblatt laufen durch den Fuss.
ZIFFER_X, ZIFFER_Y, ZIFFER_H, ZIFFER_LINIEN = 82, 46, 200, 3
ZIFFER_FARBE = IVORY


def ziffer(jahr="2", bewegt=False):
    if not bewegt:
        z, b = linien_zwei(ZIFFER_H, ZIFFER_FARBE, ZIFFER_LINIEN)
        return f'<g transform="translate({ZIFFER_X},{ZIFFER_Y})">{z}</g>'
    # Sobald die Flamme steht, zeichnet sich die Zwei: 2,0 bis 3,8 s von der
    # Spiralmitte nach aussen. Am Ende blendet sie aus statt sich zurueckzuziehen.
    z, b = linien_zwei(ZIFFER_H, ZIFFER_FARBE, ZIFFER_LINIEN, zeichnen=(2.0, 3.8))
    aus = _anim("opacity", [(0, 1), (8.55, 1), (8.9, 0), (DAUER, 0)])
    return f'<g transform="translate({ZIFFER_X},{ZIFFER_Y})">{aus}{z}</g>' 


# =========================================================================
#  Konfetti -- ein Ausbruch aus der Kerze, sobald die Zwei steht
# =========================================================================
KONFETTI_FARBEN = [GALLIANO, IVORY, WARM, GLUT]


def _flugbahn(vx, vy, dauer, g=300.0, n=8):
    """Wurfparabel als Stuetzpunkte: (t, 'x y'). Schwerkraft in Einheiten/s^2."""
    out = []
    for i in range(n + 1):
        t = dauer * i / n
        out.append((t, f"{vx * t:.1f} {vy * t + 0.5 * g * t * t:.1f}"))
    return out


def konfetti(bewegt=False, x=ROTORKOPF[0], y=ROTORKOPF[1] - 30, n=56, seed=11):
    """Konfetti aus der Kerze. Ursprung knapp ueber dem Rotorkopf.

    Stehend: ein paar Teile, die in der Luft haengen -- damit die stehende
    Fassung zur bewegten passt, aber ohne den Himmel zuzustellen.

    Bewegt: bei 3,9 s, gleich nachdem sich die Zwei gezeichnet hat, platzt der
    Ausbruch. Jedes Teil hat seine eigene Wurfparabel, dreht sich dabei und
    verblasst im letzten Drittel -- sonst laege am Ende Konfetti auf der
    Wortmarke. Ein zweiter, kleinerer Ausbruch bei 6,4 s haelt die Schleife
    lebendig, bis alles bei 8,6 s abbaut.
    """
    r = random.Random(seed)
    teile = []

    def teil(i):
        farbe = KONFETTI_FARBEN[i % len(KONFETTI_FARBEN)]
        if i % 3 == 0:
            return f'<circle r="{r.uniform(3.0, 4.6):.1f}" fill="{farbe}"/>'
        w, h = r.uniform(7, 11), r.uniform(4, 6)
        return f'<rect x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{farbe}"/>'

    if not bewegt:
        for i in range(10):
            a = math.radians(r.uniform(-150, -30))
            d = r.uniform(70, 150)
            px, py = x + math.cos(a) * d, y + math.sin(a) * d * 0.8
            teile.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate({r.uniform(0,360):.0f})" '
                         f'opacity=".85">{teil(i)}</g>')
        return "".join(teile)

    def ausbruch(t0, anzahl, kraft, seed2):
        rr = random.Random(seed2)
        out = []
        for i in range(anzahl):
            # Faecher nach oben: Winkel zwischen 200 und 340 Grad (SVG-y zeigt
            # nach unten, also sind negative Sinuswerte "oben").
            a = math.radians(rr.uniform(190, 350))
            v = rr.uniform(0.55, 1.0) * kraft
            vx, vy = math.cos(a) * v, math.sin(a) * v
            flug = rr.uniform(2.2, 3.0)
            bahn = [(0, "0 0"), (t0, "0 0")] + [(t0 + t, p) for t, p in _flugbahn(vx, vy, flug)]
            bahn += [(DAUER, bahn[-1][1])]
            lauf = _anim(None, bahn, typ="translate")
            dreh = _anim(None, [(0, "0"), (t0, "0"), (t0 + flug, f"{rr.uniform(-720, 720):.0f}"),
                                (DAUER, f"{rr.uniform(-720, 720):.0f}")], typ="rotate", additiv=True)
            sicht = _anim("opacity", [(0, 0), (t0, 0), (t0 + .04, 1), (t0 + flug * .65, 1),
                                      (t0 + flug, 0), (DAUER, 0)])
            # Beim Abschuss kurz groesser -- der Knall.
            pop = _anim(None, [(0, "1 1"), (t0, "1.6 1.6"), (t0 + .25, "1 1"), (DAUER, "1 1")],
                        typ="scale", additiv=True)
            out.append(f'<g opacity="0">{sicht}<g>{lauf}{dreh}{pop}{teil(i)}</g></g>')
        return "".join(out)

    return (f'<g transform="translate({x},{y})">'
            # Mit 560 Einheiten/s war das Konfetti nach vier Zehnteln oben aus dem
            # Kreis heraus; bei 230 steigt es rund neunzig Einheiten, treibt seitlich
            # durch den Himmel und faellt am Hubschrauber vorbei.
            f'{ausbruch(3.9, n, 230, seed)}{ausbruch(6.3, n // 2, 190, seed + 1)}</g>')

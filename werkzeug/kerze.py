# -*- coding: utf-8 -*-
"""Die Jubilaeumskerze: eine Ziffer als Kerze, die aufploppt, angezuendet wird,
brennt und tropft.

Sie steht oben in der Mitte des Himmels, auf dem Rotor. Das ist der einzige
Platz, an dem sie gross genug werden kann: der Hubschrauber beginnt bei y=126
und nimmt darunter die ganze Breite ein, und der Kreis wird nach oben hin
schmal -- bei y=20 sind es noch 200 Einheiten Breite, bei y=60 schon 330.

**Die Ziffer kommt aus Uniform Black**, nicht aus einer Kerzenschrift. Bei 128
Pixeln, in denen Discord ein Serverbild zeigt, ist die Ziffer rund 30 Pixel
hoch; eine verspielte Form zerfiele dort. Kerze wird sie durch Docht, Flamme
und Tropfen, nicht durch die Buchstabenform.

Der Rand um die Ziffer ist ein zweiter, breiter gezeichneter Pfad darunter --
kein `stroke` auf dem Buchstabenpfad. Der Buchstabenpfad traegt `scale(g/1000)`,
und ein Strich darauf wuerde mitskaliert (siehe signatur.py: aus 4,6 wurden
0,28).

Die Bewegung ist SMIL in **einer** Schleife von neun Sekunden; jede Phase sitzt
ueber keyTimes an ihrer Stelle. Getrennte Animationen mit `begin` liefen beim
Neustart der Schleife weiter oder gar nicht -- dieselbe Lehre wie beim
Silvester-Feuerwerk.

    0,0 - 0,8 s   die Kerze ploppt auf (ueberschwingend, wie aus dem Kuchen)
    1,1 - 1,5 s   der Docht faengt, kurzer Blitz, die Flamme steht
    1,5 - 8,5 s   sie brennt und flackert
    3,0 s / 5,3 s zwei Tropfen wachsen und laufen ein Stueck herab
    8,6 - 9,0 s   alles zieht sich zurueck, die Schleife beginnt von vorn
"""
import math, random

from tpl import txt, tw, uid, BLK, STRATOS, GALLIANO, IVORY

WARM = "#FFE9A8"      # Flammenkern, wie im Silvester-Feuerwerk
GLUT = "#F5A623"      # Flammenrand -- waermer als Galliano, sonst ist sie ein Blatt
DOCHT = "#8F6C04"     # die dunkle Goldstufe des Brandbooks

DAUER = 9.0


def _kt(*paare):
    """[(sekunde, wert), ...] -> (values, keyTimes) fuer eine 9-s-Schleife."""
    zs = ";".join(str(v) for _, v in paare)
    ts = ";".join(f"{min(1.0, max(0.0, t / DAUER)):.4f}" for t, _ in paare)
    return zs, ts


def _anim(attr, paare, typ=None, additiv=False):
    zs, ts = _kt(*paare)
    if typ:
        return (f'<animateTransform attributeName="transform" type="{typ}" '
                f'values="{zs}" keyTimes="{ts}" dur="{DAUER}s" '
                f'repeatCount="indefinite"{" additive=\"sum\"" if additiv else ""}/>')
    return (f'<animate attributeName="{attr}" values="{zs}" keyTimes="{ts}" '
            f'dur="{DAUER}s" repeatCount="indefinite"/>')


def _flackern(t0, t1, ruhe=1.0, hub=0.09, schritt=0.11, seed=3):
    """Flackerwerte zwischen t0 und t1 -- kleine, unregelmaessige Ausschlaege."""
    r = random.Random(seed)
    out, t = [], t0
    while t < t1:
        out.append((t, round(ruhe + r.uniform(-hub, hub), 3)))
        t += schritt * r.uniform(0.7, 1.3)
    return out


# =========================================================================
#  Bauteile -- alle relativ zum Fusspunkt der Kerze (0,0), Grundlinie y=0
# =========================================================================
def _ziffer(jahr, gr):
    """Ziffer mit goldenem Rand: erst breit in Gold, dann Ivory darueber."""
    rand = max(3.0, gr * .055)
    # Zwei Lagen statt eines Strichs auf dem Buchstabenpfad -- der Strich
    # wuerde vom inneren scale(g/1000) mitskaliert.
    unten, _ = txt(jahr, gr, GALLIANO, 0, 0, BLK, 0, "middle")
    unten = unten.replace('<g fill=', f'<g stroke="{GALLIANO}" stroke-linejoin="round" '
                          f'stroke-width="{rand * 2 * 1000 / gr:.1f}" fill=', 1)
    oben, _ = txt(jahr, gr, IVORY, 0, 0, BLK, 0, "middle")
    # Drei Punkte im Wachs -- die Tupfen der Vorlage, sparsam. Bei 128 px sind
    # sie ein Hauch, nicht ein Muster.
    punkte = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{gr*.028:.1f}" fill="{STRATOS}" opacity=".35"/>'
        for x, y in ((-gr * .08, -gr * .52), (gr * .12, -gr * .30), (-gr * .02, -gr * .12)))
    return unten + oben + punkte


def _flamme(gr):
    """Teardrop mit warmem Kern. Der Ursprung liegt an der Dochtspitze."""
    h, w = gr * .30, gr * .15
    aussen = (f'M0,{-h:.1f} C{w:.1f},{-h*.55:.1f} {w:.1f},{-h*.12:.1f} 0,0 '
              f'C{-w:.1f},{-h*.12:.1f} {-w:.1f},{-h*.55:.1f} 0,{-h:.1f}Z')
    hi, wi = h * .55, w * .5
    innen = (f'M0,{-hi:.1f} C{wi:.1f},{-hi*.5:.1f} {wi:.1f},{-hi*.1:.1f} 0,0 '
             f'C{-wi:.1f},{-hi*.1:.1f} {-wi:.1f},{-hi*.5:.1f} 0,{-hi:.1f}Z')
    return (f'<path d="{aussen}" fill="{GLUT}"/>'
            f'<path d="{innen}" fill="{WARM}"/>'
            f'<circle cy="{-hi*.35:.1f}" r="{wi*.55:.1f}" fill="{IVORY}"/>')


def _tropfen(gr):
    """Ein Wachstropfen, Ursprung an seiner Oberkante."""
    h, w = gr * .16, gr * .075
    return (f'<path d="M0,0 C{w:.1f},{h*.3:.1f} {w:.1f},{h*.75:.1f} 0,{h:.1f} '
            f'C{-w:.1f},{h*.75:.1f} {-w:.1f},{h*.3:.1f} 0,0Z" '
            f'fill="{IVORY}" stroke="{GALLIANO}" stroke-width="{max(1.2, gr*.014):.1f}"/>')


# =========================================================================
#  Die Kerze -- stehend und bewegt
# =========================================================================
def kerze(jahr="2", gr=118, x=256, y=122, bewegt=False):
    """Kerze mit Fusspunkt bei (x, y). `gr` ist die Schriftgroesse der Ziffer.

    Docht und Flamme sitzen am hoechsten Punkt der Ziffer; bei einer "2" liegt
    der links der Mitte, bei einer "1" rechts. Gemessen wird das nicht, sondern
    aus der Ziffer geschaetzt -- fuer die Ziffern 1 bis 9 stimmen die Werte.
    """
    hoehe = gr * .72                          # Versalhoehe Uniform Black
    breite = tw(jahr, gr, BLK, 0)
    dx_docht = {"1": .18, "2": -.10, "3": .04, "4": .10, "5": -.02,
                "6": .06, "7": .12, "8": 0, "9": .02}.get(jahr[-1], 0) * breite
    docht_y = -hoehe - gr * .02
    docht_h = gr * .10

    docht = (f'<line x1="{dx_docht:.1f}" y1="{docht_y:.1f}" x2="{dx_docht:.1f}" '
             f'y2="{docht_y - docht_h:.1f}" stroke="{DOCHT}" '
             f'stroke-width="{max(2, gr*.03):.1f}" stroke-linecap="round"/>')

    if not bewegt:
        flamme = (f'<g transform="translate({dx_docht:.1f},{docht_y - docht_h:.1f})">'
                  f'<circle r="{gr*.26:.1f}" fill="{GLUT}" opacity=".16"/>{_flamme(gr)}</g>')
        tropfen = (f'<g transform="translate({breite*.36:.1f},{-hoehe*.78:.1f})">{_tropfen(gr)}</g>'
                   f'<g transform="translate({-breite*.30:.1f},{-hoehe*.28:.1f}) scale(.8)">{_tropfen(gr)}</g>')
        return (f'<g transform="translate({x},{y})">{_ziffer(jahr, gr)}{docht}'
                f'{tropfen}{flamme}</g>')

    # --- bewegt --------------------------------------------------------------
    # Kerze: ploppt auf, steht, zieht sich am Ende zurueck.
    pop = _anim(None, [(0, "0 0"), (0.05, "0 0"), (0.45, "1.18 1.18"),
                       (0.62, "0.94 0.94"), (0.78, "1 1"),
                       (8.6, "1 1"), (8.95, "0 0"), (DAUER, "0 0")], typ="scale")

    # Flamme: nichts, dann Zuendblitz, dann Flackern, am Ende aus.
    fl = ([(0, 0), (1.10, 0), (1.28, 1.35), (1.42, 0.9)]
          + _flackern(1.50, 8.55, 1.0, 0.09, 0.13, seed=5)
          + [(8.6, 1), (8.85, 0), (DAUER, 0)])
    flamme_scale = _anim(None, [(t, f"{v} {v}") for t, v in fl], typ="scale")
    # Ein leichtes Neigen dazu -- eine Flamme, die nur pumpt, sieht aus wie ein
    # Herzschlag.
    neig = ([(0, 0), (1.45, 0)] + _flackern(1.5, 8.55, 0, 6, 0.17, seed=9)
            + [(8.6, 0), (DAUER, 0)])
    flamme_skew = _anim(None, [(t, f"{v}") for t, v in neig], typ="skewX", additiv=True)

    # Zuendblitz: ein kurzer heller Kreis, der gleich wieder verschwindet.
    blitz = _anim("opacity", [(0, 0), (1.08, 0), (1.16, .55), (1.42, 0), (DAUER, 0)])
    blitz_r = _anim("r", [(0, 2), (1.08, 2), (1.42, gr * .42), (DAUER, gr * .42)])

    # Schein: erst mit der Flamme da, dann leise mitflackernd.
    schein_op = ([(0, 0), (1.2, 0), (1.5, .16)]
                 + [(t, round(.16 + (v - 1) * .5, 3)) for t, v in _flackern(1.6, 8.5, 1, .06, .19, seed=2)]
                 + [(8.6, .16), (8.85, 0), (DAUER, 0)])
    schein = _anim("opacity", schein_op)

    # Tropfen: wachsen, rutschen, verblassen.
    def tropfen_anim(t_start, weg):
        wachs = _anim(None, [(0, "1 0"), (t_start, "1 0"), (t_start + .8, "1 1"),
                             (8.6, "1 1"), (8.9, "1 0"), (DAUER, "1 0")], typ="scale")
        lauf = _anim(None, [(0, "0 0"), (t_start + .8, "0 0"),
                            (t_start + 3.0, f"0 {weg:.1f}"), (8.6, f"0 {weg:.1f}"),
                            (DAUER, f"0 {weg:.1f}")], typ="translate", additiv=True)
        op = _anim("opacity", [(0, 1), (t_start + 2.4, 1), (t_start + 3.0, 0), (DAUER, 0)])
        return wachs + lauf + op

    t1 = (f'<g transform="translate({breite*.36:.1f},{-hoehe*.78:.1f})">'
          f'<g>{tropfen_anim(3.0, gr*.20)}{_tropfen(gr)}</g></g>')
    t2 = (f'<g transform="translate({-breite*.30:.1f},{-hoehe*.28:.1f})">'
          f'<g>{tropfen_anim(5.3, gr*.14)}<g transform="scale(.8)">{_tropfen(gr)}</g></g></g>')

    fx, fy = dx_docht, docht_y - docht_h
    flamme = (f'<g transform="translate({fx:.1f},{fy:.1f})">'
              f'<circle r="{gr*.26:.1f}" fill="{GLUT}" opacity="0">{schein}</circle>'
              f'<circle r="2" fill="{WARM}" opacity="0">{blitz}{blitz_r}</circle>'
              f'<g>{flamme_scale}{flamme_skew}{_flamme(gr)}</g></g>')

    return (f'<g transform="translate({x},{y})"><g>{pop}'
            f'{_ziffer(jahr, gr)}{docht}{t1}{t2}{flamme}</g></g>')

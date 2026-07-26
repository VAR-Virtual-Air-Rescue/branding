# -*- coding: utf-8 -*-
"""Halloween als Kuerbis und animierte Fassungen der Editionen.

Bewegt wird nur der Hintergrund -- Hubschrauber, Kante und Wortmarke bleiben
still. Die Animationen sind SMIL und laufen damit direkt im Browser; fuer
Discord wird daraus ein APNG exportiert.
"""
import math, os
from mark import (STRATOS, GALLIANO, IVORY, C, R, S, ANG, svg, disc,
                  heli_on_edge, word_max, uid, EDGE, CUT, BAR)
from editions import (feld, oben, flaeche, streifen, muster, E,
                      STERN, KUERBIS, FLEDER, KNOCHEN, RAKETE, PRIDE)

KANTE_Y = EDGE + CUT
NACHT   = "#1A0E22"
ORANGE  = "#E5720A"
ORANGE2 = "#C25A05"
GLUT    = "#FFB020"

# ---------------------------------------------------------------- Kuerbis
KUERBIS_HELL = "#F07C10"
KUERBIS_TIEF = "#B14E04"
SCHNITT      = "#14090E"
GLIMM        = "#FFC24A"
FADEN        = "#E8E2D4"

def rippen(farbe=KUERBIS_TIEF, opa=".5", breite=11):
    """Kuerbisrippen: Boegen ueber die ganze Scheibe."""
    out = []
    for i in range(1, 7):
        t = i / 7
        x = S * t
        bow = (t - .5) * 2
        rx = abs(bow) * S * 0.46 + 8
        out.append(f'<path d="M{x:.0f},-10 C{x - bow*rx:.0f},{S*.3:.0f} '
                   f'{x - bow*rx:.0f},{S*.7:.0f} {x:.0f},{S+10:.0f}" '
                   f'fill="none" stroke="{farbe}" stroke-width="{breite}" '
                   f'opacity="{opa}" stroke-linecap="round"/>')
    return "".join(out)

def stiel():
    return (f'<g transform="translate({C},22)">'
            f'<path d="M-15,30 C-13,4 -6,-10 0,-17 C7,-8 13,4 15,30 Z" fill="#3E6B34"/>'
            f'<path d="M0,-16 C12,-28 26,-26 31,-13" fill="none" stroke="#3E6B34" '
            f'stroke-width="8" stroke-linecap="round"/></g>')

def netz(ecke, r, speichen, boegen, opa=".72"):
    """Spinnennetz -- links und rechts bewusst unterschiedlich gross."""
    x0, y0 = (0, 0) if ecke == "lo" else (S, 0)
    a0, a1 = (0, 90) if ecke == "lo" else (90, 180)
    d = []
    for k in range(speichen + 1):
        w = math.radians(a0 + (a1 - a0) * k / speichen)
        d.append(f'M{x0},{y0} L{x0+math.cos(w)*r:.1f},{y0+math.sin(w)*r:.1f}')
    for j in range(1, boegen + 1):
        rr = r * j / boegen
        pts = []
        for k in range(speichen + 1):
            w = math.radians(a0 + (a1 - a0) * k / speichen)
            pts.append(f'{x0+math.cos(w)*rr:.1f},{y0+math.sin(w)*rr:.1f}')
        d.append("M" + " L".join(pts))
    return (f'<g stroke="{FADEN}" stroke-width="2.2" fill="none" opacity="{opa}">'
            f'<path d="{" ".join(d)}"/></g>')

def faeden():
    """Spinnfaeden vom Kreisrand zum Hubschrauber -- er haengt selbst im Netz."""
    ziele  = [(150, 216), (272, 196), (378, 210)]
    aussen = [(22, 40),   (198, -8),  (486, 58)]
    out = []
    for (ax, ay), (zx, zy) in zip(aussen, ziele):
        mx, my = (ax + zx) / 2, (ay + zy) / 2 + 22
        out.append(f'<path d="M{ax},{ay} Q{mx:.0f},{my:.0f} {zx},{zy}" fill="none" '
                   f'stroke="{FADEN}" stroke-width="2" opacity=".62"/>')
        for t in (.34, .64):
            px = ax + (zx - ax) * t
            py = ay + (zy - ay) * t + 15
            out.append(f'<path d="M{px-14:.0f},{py-6:.0f} Q{px:.0f},{py+7:.0f} '
                       f'{px+14:.0f},{py-6:.0f}" fill="none" stroke="{FADEN}" '
                       f'stroke-width="1.6" opacity=".45"/>')
    return "".join(out)

SPINNE_KOERPER = (
    '<ellipse cx="0" cy="4" rx="17" ry="21" fill="#0E0710"/>'
    '<circle cx="0" cy="-19" r="11.5" fill="#0E0710"/>'
    '<g stroke="#0E0710" stroke-width="4.6" stroke-linecap="round" fill="none">'
    '<path d="M-13,-6 C-27,-14 -34,-24 -33,-33"/>'
    '<path d="M-15,2 C-31,-1 -40,-6 -42,-14"/>'
    '<path d="M-15,11 C-31,14 -38,21 -39,30"/>'
    '<path d="M-11,19 C-22,28 -26,38 -24,47"/>'
    '<path d="M13,-6 C27,-14 34,-24 33,-33"/>'
    '<path d="M15,2 C31,-1 40,-6 42,-14"/>'
    '<path d="M15,11 C31,14 38,21 39,30"/>'
    '<path d="M11,19 C22,28 26,38 24,47"/></g>'
    '<circle cx="-4.6" cy="-21" r="3.4" fill="#FF9A1E"/>'
    '<circle cx="4.6" cy="-21" r="3.4" fill="#FF9A1E"/>'
    '<circle cx="-4.6" cy="-21" r="1.4" fill="#14090E"/>'
    '<circle cx="4.6" cy="-21" r="1.4" fill="#14090E"/>')

def spinne(x, faden, animiert=False):
    """Haengende Spinne. Der Schwung dreht um den Aufhaengepunkt, nicht um sie selbst."""
    schwung = ('<animateTransform attributeName="transform" type="rotate" '
               'values="-15 0 0;15 0 0;-15 0 0" dur="3.4s" repeatCount="indefinite" '
               'calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>'
               ) if animiert else ""
    ab = ('<animateTransform attributeName="transform" type="translate" '
          'values="0 0;0 18;0 0" dur="5.1s" repeatCount="indefinite" '
          'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" '
          'additive="sum"/>') if animiert else ""
    # Aeussere Gruppe traegt die Position, die innere die Bewegung. Ein
    # animateTransform ohne additive ersetzt sonst das transform der Gruppe --
    # die Spinne landet dann am linken Bildrand.
    return (f'<g transform="translate({x},0)"><g>{schwung}{ab}'
            f'<line x1="0" y1="0" x2="0" y2="{faden}" stroke="{FADEN}" '
            f'stroke-width="2.2" opacity=".8"/>'
            f'<g transform="translate(0,{faden+22})">{SPINNE_KOERPER}</g></g></g>')

def fledermaus(x0, y0, x1, y1, dauer, verzug, gross=1.0):
    """Fledermaus fliegt durchs Bild, Fluegel schlagen."""
    fl = ('<path d="M-26,0 C-17,-13 -9,-9 0,0 C9,-9 17,-13 26,0 '
          'C17,5 9,3 0,9 C-9,3 -17,5 -26,0 Z" fill="#160A14">'
          '<animate attributeName="d" dur="0.42s" repeatCount="indefinite" '
          'values="M-26,0 C-17,-13 -9,-9 0,0 C9,-9 17,-13 26,0 C17,5 9,3 0,9 '
          'C-9,3 -17,5 -26,0 Z;'
          'M-22,-9 C-15,-20 -8,-13 0,-3 C8,-13 15,-20 22,-9 C15,-1 8,-1 0,6 '
          'C-8,-1 -15,-1 -22,-9 Z;'
          'M-26,0 C-17,-13 -9,-9 0,0 C9,-9 17,-13 26,0 C17,5 9,3 0,9 '
          'C-9,3 -17,5 -26,0 Z"/></path>')
    return (f'<g opacity="0"><g transform="scale({gross})">{fl}</g>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="{x0} {y0};{x1} {y1}" dur="{dauer}s" begin="{verzug}s" '
            f'repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;0.12;0.85;1" dur="{dauer}s" begin="{verzug}s" '
            f'repeatCount="indefinite"/></g>')

def halloween(animiert=False):
    """Das Icon selbst ist der Kuerbis: Rippen, Stiel, Glimmkern, ausgeschnittene Marke."""
    heli, bar, _ = heli_on_edge(418, C, KANTE_Y, SCHNITT, CUT, BAR, "#6B3402")
    puls = ('<animate attributeName="opacity" values=".22;.62;.22" dur="2.4s" '
            'repeatCount="indefinite"/>') if animiert else ""
    tiere = (fledermaus(-60, 96, S + 60, 62, 7.5, 0.0, 1.0)
             + fledermaus(S + 60, 168, -60, 132, 9.5, 3.2, 0.72)) if animiert else \
            muster([FLEDER], 5, 3)
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{KUERBIS_HELL}"/>'
            + rippen()
            # Glimmkern direkt hinter der Marke, damit der Schnitt beleuchtet wirkt
            + f'<ellipse cx="{C}" cy="{S*.40:.0f}" rx="{R*.86:.0f}" ry="{R*.52:.0f}" '
              f'fill="{GLIMM}" opacity=".22">{puls}</ellipse>'
            + stiel()
            + oben(netz("lo", 206, 6, 4) + netz("ru", 132, 4, 3, ".52")
                   + faeden()
                   + muster([KUERBIS, KNOCHEN], 7, 9)
                   + tiere
                   + spinne(int(S * .74), 118, animiert))
            + feld(flaeche(KUERBIS_TIEF) + rippen("#7E3603", ".42"))
            + heli + bar
            + word_max(KANTE_Y + BAR + 6, SCHNITT))
    return svg(disc(body, uid("h")))

# ---------------------------------------------------------------- Animiert
def bewegt(bg, heli_col, bar_col, wort_col, obenteil, unten):
    heli, bar, _ = heli_on_edge(418, C, KANTE_Y, heli_col, CUT, BAR, bar_col)
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{bg}"/>'
            + (oben(obenteil) if obenteil else "")
            + unten + heli + bar
            + word_max(KANTE_Y + BAR + 6, wort_col))
    return svg(disc(body, uid("a")))

A = {}
A["pb_halloween_anim"] = halloween(True)

# Pride -- die Fahne schwingt, die Welle laeuft von links nach rechts
def pride_welle(spalten=22):
    """Senkrechte Streifen der Flaeche, jede Spalte mit eigener Phase."""
    br = S / spalten
    st = streifen(PRIDE)
    teile = []
    for i in range(spalten):
        cid = uid("pw")
        teile.append(
            f'<defs><clipPath id="{cid}"><rect x="{i*br-0.4:.2f}" y="-60" '
            f'width="{br+0.8:.2f}" height="{S*2}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><g>{st}'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 -8;0 8;0 -8" dur="2.6s" begin="{-(i/spalten)*2.6:.2f}s" '
            f'repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/></g></g>')
    return "".join(teile)

A["pb_pride_anim"] = bewegt(
    STRATOS, GALLIANO, "#2B6EFF", STRATOS, "", feld(pride_welle()))

# Weihnachten -- Schnee faellt
_flocken = "".join(
    f'<circle cx="{(i*67)%S}" cy="{-((i*29)%330)}" r="{3.6+(i%4)*1.6:.1f}" '
    f'fill="#FFFFFC" opacity="{.45+.14*(i%4):.2f}">'
    f'<animate attributeName="cy" from="{-((i*29)%330)-40}" to="{KANTE_Y+30}" '
    f'dur="{7+(i%5)*1.7:.1f}s" repeatCount="indefinite"/></circle>' for i in range(26))
A["pb_weihnachten_anim"] = bewegt(
    "#0E2E2B", GALLIANO, "#F08A80", IVORY, _flocken, feld(flaeche("#C0392B")))

# Jahreswechsel -- die Rakete steigt, explodiert, die Jahreszahl bleibt stehen
from text2path import text_path
import random as _rd

def feuerwerk(jahr="2027", dauer=6.0):
    """Rakete steigt, explodiert, die Funken lassen die Jahreszahl stehen.

    Eine einzige Schleife von `dauer` Sekunden; jede Phase sitzt ueber keyTimes
    an ihrer Stelle. Grosszuegig dimensioniert -- als Discord-Icon ist das Ganze
    nur rund 128 px gross.
    """
    D = f"{dauer}s"
    teile = []

    def kt(*paare):
        """(zeitpunkt_in_sekunden, wert) -> values/keyTimes fuer eine Schleife."""
        zs = ";".join(f"{v}" for _, v in paare)
        ts = ";".join(f"{min(1, max(0, t / dauer)):.4f}" for t, _ in paare)
        return zs, ts

    def rakete(bx, by, t0, r_auf=7.0, farbe="#FFE9A8"):
        """Aufsteigender Leuchtkoerper mit Schweif."""
        t1 = t0 + 1.25
        cy_v, cy_t = kt((0, KANTE_Y + 40), (t0, KANTE_Y + 40), (t1, by),
                        (t1 + .01, by), (dauer, by))
        op_v, op_t = kt((0, 0), (t0, 0), (t0 + .12, 1), (t1 - .08, 1),
                        (t1, 0), (dauer, 0))
        return (
            # Schweif
            f'<rect x="{bx-2.6:.1f}" y="0" width="5.2" height="34" rx="2.6" '
            f'fill="{farbe}" opacity="0">'
            f'<animate attributeName="y" values="{cy_v}" keyTimes="{cy_t}" '
            f'dur="{D}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op_v}" keyTimes="{op_t}" '
            f'dur="{D}" repeatCount="indefinite"/></rect>'
            # Kopf
            f'<circle cx="{bx}" r="{r_auf}" fill="{farbe}" opacity="0">'
            f'<animate attributeName="cy" values="{cy_v}" keyTimes="{cy_t}" '
            f'dur="{D}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op_v}" keyTimes="{op_t}" '
            f'dur="{D}" repeatCount="indefinite"/></circle>')

    def explosion(bx, by, t0, n=26, weite=104, farbe="#F5D76E", r_funke=5.0):
        out = []
        for k in range(n):
            w = k / n * 6.2832
            zx = bx + math.cos(w) * weite * (0.82 + 0.3 * (k % 3) / 2)
            zy = by + math.sin(w) * weite * 0.66 + 34
            t1 = t0 + 1.15
            x_v, x_t = kt((0, bx), (t0, bx), (t1, f"{zx:.0f}"), (dauer, f"{zx:.0f}"))
            y_v, y_t = kt((0, by), (t0, by), (t1, f"{zy:.0f}"), (dauer, f"{zy:.0f}"))
            o_v, o_t = kt((0, 0), (t0, 0), (t0 + .06, 1), (t0 + .7, 1),
                          (t1, 0), (dauer, 0))
            r_v, r_t = kt((0, r_funke), (t0, r_funke), (t1, r_funke * 0.45),
                          (dauer, r_funke * 0.45))
            out.append(
                f'<circle r="{r_funke}" fill="{farbe}" opacity="0">'
                f'<animate attributeName="cx" values="{x_v}" keyTimes="{x_t}" '
                f'dur="{D}" repeatCount="indefinite"/>'
                f'<animate attributeName="cy" values="{y_v}" keyTimes="{y_t}" '
                f'dur="{D}" repeatCount="indefinite"/>'
                f'<animate attributeName="r" values="{r_v}" keyTimes="{r_t}" '
                f'dur="{D}" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="{o_v}" keyTimes="{o_t}" '
                f'dur="{D}" repeatCount="indefinite"/></circle>')
        # heller Blitz im Moment der Explosion
        bo_v, bo_t = kt((0, 0), (t0, 0), (t0 + .08, .85), (t0 + .5, 0), (dauer, 0))
        out.append(
            f'<circle cx="{bx}" cy="{by}" r="30" fill="#FFFFFC" opacity="0">'
            f'<animate attributeName="opacity" values="{bo_v}" keyTimes="{bo_t}" '
            f'dur="{D}" repeatCount="indefinite"/></circle>')
        return "".join(out)

    # Hauptrakete in der Mitte
    HX, HY, HT = C, 128, 0.15
    teile.append(rakete(HX, HY, HT, 7.5))
    teile.append(explosion(HX, HY, HT + 1.25, 26, 108, "#F5D76E", 5.2))

    # zweite, kleinere Rakete zeitversetzt seitlich
    NX, NY, NT = int(S * 0.30), 168, 2.35
    teile.append(rakete(NX, NY, NT, 5.5, "#FFC8A8"))
    teile.append(explosion(NX, NY, NT + 1.25, 16, 62, "#FF9A5A", 4.0))

    # Jahreszahl -- steht, sobald die erste Explosion verglueht
    d, br = text_path(jahr, "fonts/Uniform Bold.ttf", 62, 0.05)
    t_ein = HT + 1.55
    jz_v, jz_t = kt((0, 0), (t_ein, 0), (t_ein + .45, 1),
                    (dauer - .8, 1), (dauer - .15, 0), (dauer, 0))
    teile.append(
        f'<g fill="#FFE9A8" opacity="0" transform="translate({C-br/2:.0f},{HY+52})">'
        f'{d}<animate attributeName="opacity" values="{jz_v}" keyTimes="{jz_t}" '
        f'dur="{D}" repeatCount="indefinite"/></g>')

    # Funken um die Zahl
    r = _rd.Random(5)
    for k in range(22):
        px = C - br / 2 + r.uniform(-8, br + 8)
        py = HY + 56 + r.uniform(-58, 14)
        v0 = t_ein + .5 + r.uniform(0, dauer - t_ein - 1.6)
        fo_v, fo_t = kt((0, 0), (v0, 0), (v0 + .25, .95), (v0 + .8, 0), (dauer, 0))
        teile.append(
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(2.2,4.2):.1f}" '
            f'fill="#FFD24A" opacity="0">'
            f'<animate attributeName="opacity" values="{fo_v}" keyTimes="{fo_t}" '
            f'dur="{D}" repeatCount="indefinite"/></circle>')

    return "".join(teile)

A["pb_silvester_anim"] = bewegt(
    "#070E24", GALLIANO, "#F5D76E", IVORY,
    muster([STERN], 18, 21) + feuerwerk(), feld(flaeche("#12204A")))

# 24-Stunden-Event -- das Sternenbild wandert durch, dazu Funkeln
def sternfeld(n=44, versatz=0):
    return "".join(
        f'<circle cx="{(i*97)%S + versatz}" cy="{(i*53)%308}" '
        f'r="{1.6+(i%3)*.7:.1f}" fill="#FFFFFC" opacity=".25">'
        f'<animate attributeName="opacity" values=".14;.95;.14" '
        f'dur="{2.4+(i%6)*.6:.1f}s" begin="{(i%9)*.35:.2f}s" '
        f'repeatCount="indefinite"/></circle>' for i in range(n))

_himmel = (f'<g>{sternfeld(44, 0)}{sternfeld(44, S)}'
           f'<animateTransform attributeName="transform" type="translate" '
           f'from="0 0" to="{-S} 0" dur="48s" repeatCount="indefinite"/></g>')
_schimmer = (f'<g transform="rotate({ANG:.3f} {C} {C})">'
             f'<rect x="-170" y="{KANTE_Y-3}" width="150" height="{BAR+6}" '
             f'fill="#8FC0FF" opacity=".85">'
             f'<animate attributeName="x" from="-170" to="{S+20}" dur="3.4s" '
             f'repeatCount="indefinite"/></rect></g>')
A["pb_nacht_anim"] = bewegt(
    "#04091A", GALLIANO, "#2B6EFF", IVORY, _himmel,
    feld(flaeche("#0A1836")) + _schimmer)

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    open("neu/pb_halloween.svg", "w", encoding="utf-8").write(halloween(False))
    for k, v in A.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"Kuerbis + {len(A)} animierte Fassungen:", ", ".join(A))

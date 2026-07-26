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
def rippen(farbe=ORANGE2, opa=".55"):
    """Kuerbisrippen: Boegen ueber die ganze Scheibe."""
    out = []
    for i in range(1, 7):
        t = i / 7
        x = S * t
        bow = (t - .5) * 2
        rx = abs(bow) * S * 0.46 + 8
        out.append(f'<path d="M{x:.0f},-10 C{x - bow*rx:.0f},{S*.3:.0f} '
                   f'{x - bow*rx:.0f},{S*.7:.0f} {x:.0f},{S+10:.0f}" '
                   f'fill="none" stroke="{farbe}" stroke-width="9" '
                   f'opacity="{opa}" stroke-linecap="round"/>')
    return "".join(out)

def stiel():
    return (f'<g transform="translate({C},20)">'
            f'<path d="M-13,26 C-11,4 -5,-8 0,-14 C6,-6 11,4 13,26 Z" fill="#3E6B34"/>'
            f'<path d="M0,-13 C10,-24 22,-22 26,-11" fill="none" stroke="#3E6B34" '
            f'stroke-width="7" stroke-linecap="round"/></g>')

def netz(ecke, r, speichen, boegen, opa=".5"):
    """Spinnennetz -- links und rechts bewusst unterschiedlich gross."""
    x0, y0 = (0, 0) if ecke == "lo" else (S, 0)
    a0, a1 = (0, 90) if ecke == "lo" else (90, 180)
    d = []
    for k in range(speichen + 1):
        a = math.radians(a0 + (a1 - a0) * k / speichen)
        d.append(f'M{x0},{y0} L{x0+math.cos(a)*r:.1f},{y0+math.sin(a)*r:.1f}')
    for j in range(1, boegen + 1):
        rr = r * j / boegen
        pts = []
        for k in range(speichen + 1):
            a = math.radians(a0 + (a1 - a0) * k / speichen)
            pts.append(f'{x0+math.cos(a)*rr:.1f},{y0+math.sin(a)*rr:.1f}')
        d.append("M" + " L".join(pts))
    return (f'<g stroke="#CFC7B4" stroke-width="1.5" fill="none" opacity="{opa}">'
            f'<path d="{" ".join(d)}"/></g>')

SPINNE_KOERPER = (
    '<ellipse cx="0" cy="0" rx="7" ry="9" fill="#12080F"/>'
    '<circle cx="0" cy="-9" r="4.5" fill="#12080F"/>'
    '<g stroke="#12080F" stroke-width="2" stroke-linecap="round" fill="none">'
    '<path d="M-6,-3 L-15,-9 M-7,0 L-17,-1 M-6,3 L-15,8 M-5,6 L-12,14"/>'
    '<path d="M6,-3 L15,-9 M7,0 L17,-1 M6,3 L15,8 M5,6 L12,14"/></g>'
    '<circle cx="-2.6" cy="-9.5" r="1.3" fill="#E5720A"/>'
    '<circle cx="2.6" cy="-9.5" r="1.3" fill="#E5720A"/>')

def spinne(x, y, faden, animiert=False):
    schwung = ('<animateTransform attributeName="transform" type="rotate" '
               'values="-7 0 0;7 0 0;-7 0 0" dur="4.5s" repeatCount="indefinite" '
               'calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>'
               ) if animiert else ""
    return (f'<g transform="translate({x},{y})">{schwung}'
            f'<line x1="0" y1="0" x2="0" y2="{faden}" stroke="#CFC7B4" '
            f'stroke-width="1.4" opacity=".65"/>'
            f'<g transform="translate(0,{faden+9})">{SPINNE_KOERPER}</g></g>')

def halloween(animiert=False):
    """Das Icon selbst wird zum Kuerbis: Rippen, Stiel, glimmender Kern."""
    heli, bar, _ = heli_on_edge(418, C, KANTE_Y, GLUT, CUT, BAR, NACHT)
    glut = ('<animate attributeName="opacity" values=".16;.44;.16" dur="3.2s" '
            'repeatCount="indefinite"/>') if animiert else ""
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{ORANGE}"/>'
            + rippen()
            + f'<circle cx="{C}" cy="{S*.34:.0f}" r="{R*.72:.0f}" fill="{GLUT}" '
              f'opacity=".16">{glut}</circle>'
            + stiel()
            + oben(netz("lo", 194, 6, 4, ".55") + netz("ru", 126, 4, 3, ".38")
                   + muster([KUERBIS, FLEDER, KNOCHEN], 12, 9)
                   + spinne(int(S * .70), 0, 92, animiert))
            + feld(flaeche(ORANGE2) + rippen("#9E4703", ".45"))
            + heli + bar
            + word_max(KANTE_Y + BAR + 6, NACHT))
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

# Pride -- die Streifen wandern um einen vollen Satz nach oben
_h = (S - KANTE_Y + 34) / len(PRIDE)
A["pb_pride_anim"] = bewegt(
    STRATOS, GALLIANO, "#2B6EFF", STRATOS, "",
    feld('<g>' + streifen(PRIDE + PRIDE)
         + f'<animateTransform attributeName="transform" type="translate" '
           f'values="0 0;0 {-_h*len(PRIDE):.2f}" dur="7s" repeatCount="indefinite"/>'
         + '</g>'))

# Weihnachten -- Schnee faellt
_flocken = "".join(
    f'<circle cx="{(i*67)%S}" cy="{-((i*29)%330)}" r="{1.8+(i%3)*1.1:.1f}" '
    f'fill="#FFFFFC" opacity="{.45+.14*(i%4):.2f}">'
    f'<animate attributeName="cy" from="{-((i*29)%330)-40}" to="{KANTE_Y+30}" '
    f'dur="{7+(i%5)*1.7:.1f}s" repeatCount="indefinite"/></circle>' for i in range(40))
A["pb_weihnachten_anim"] = bewegt(
    "#0E2E2B", GALLIANO, "#F08A80", IVORY, _flocken, feld(flaeche("#C0392B")))

# Jahreswechsel -- Raketen zuenden nacheinander
_rak = "".join(
    f'<g transform="translate({72+i*90},{62+(i%3)*66})" opacity="0">{RAKETE}'
    f'<animate attributeName="opacity" values="0;1;0" dur="2.4s" '
    f'begin="{i*0.55:.2f}s" repeatCount="indefinite"/>'
    f'<animateTransform attributeName="transform" type="scale" additive="sum" '
    f'values="0.35;1.35;1.7" dur="2.4s" begin="{i*0.55:.2f}s" '
    f'repeatCount="indefinite"/></g>' for i in range(5))
A["pb_silvester_anim"] = bewegt(
    "#070E24", GALLIANO, "#F5D76E", IVORY,
    muster([STERN], 22, 21) + _rak, feld(flaeche("#12204A")))

# 24-Stunden-Event -- Sterne funkeln, ein blauer Schimmer laeuft ueber die Kante
_sterne = "".join(
    f'<circle cx="{(i*97)%S}" cy="{(i*53)%310}" r="1.9" fill="#FFFFFC" opacity=".2">'
    f'<animate attributeName="opacity" values=".15;.95;.15" dur="{2.4+(i%6)*.6:.1f}s" '
    f'begin="{(i%9)*.35:.2f}s" repeatCount="indefinite"/></circle>' for i in range(55))
_schimmer = (f'<g transform="rotate({ANG:.3f} {C} {C})">'
             f'<rect x="-170" y="{KANTE_Y-3}" width="150" height="{BAR+6}" '
             f'fill="#8FC0FF" opacity=".85">'
             f'<animate attributeName="x" from="-170" to="{S+20}" dur="3.4s" '
             f'repeatCount="indefinite"/></rect></g>')
A["pb_nacht_anim"] = bewegt(
    "#04091A", GALLIANO, "#2B6EFF", IVORY, _sterne,
    feld(flaeche("#0A1836")) + _schimmer)

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    open("neu/pb_halloween.svg", "w", encoding="utf-8").write(halloween(False))
    for k, v in A.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"Kuerbis + {len(A)} animierte Fassungen:", ", ".join(A))

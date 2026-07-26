# -*- coding: utf-8 -*-
"""Profilbilder: Grundfassung und Sondereditionen.

Die Regel stammt aus den bestehenden Fassungen (1_Logo_Pride.png,
3_Logo_XMAS.png in S:\\06_VAR): der Hubschrauber bleibt immer Gold, veraendert
wird das **untere Feld** unter der Kante -- und bei Bedarf bekommt das obere
Feld ein Muster. Die Wortmarke nimmt die Farbe, die auf dem unteren Feld traegt.

Weil die Kante um -3,27 Grad gekippt ist, laufen auch die Streifen im unteren
Feld parallel dazu. Sonst entsteht ein zweiter, widersprechender Winkel.
"""
import os
from mark import (STRATOS, GALLIANO, IVORY, C, R, S, ANG, svg, disc,
                  heli_on_edge, word_max, uid, EDGE, CUT, BAR)

KANTE_Y = EDGE + CUT

def feld(inhalt):
    """Inhalt ins untere Feld -- gedreht wie die Kante, randabfallend."""
    return (f'<g transform="rotate({ANG:.3f} {C} {C})">'
            f'<g transform="translate(0,{KANTE_Y})">{inhalt}</g></g>')

def streifen(farben):
    h = (S - KANTE_Y + 110) / len(farben)
    return "".join(f'<rect x="{-S}" y="{i*h:.2f}" width="{S*3}" height="{h+0.6:.2f}" '
                   f'fill="{c}"/>' for i, c in enumerate(farben))

def flaeche(farbe):
    return f'<rect x="{-S}" y="0" width="{S*3}" height="{S*2}" fill="{farbe}"/>'

def oben(inhalt):
    """Muster ins obere Feld -- an der Kante abgeschnitten."""
    cid = uid("o")
    return (f'<defs><clipPath id="{cid}">'
            f'<rect x="{-S}" y="{-S}" width="{S*3}" height="{S+KANTE_Y}" '
            f'transform="rotate({ANG:.3f} {C} {C})"/>'
            f'</clipPath></defs><g clip-path="url(#{cid})">{inhalt}</g>')

def edition(unten, bar=IVORY, wort=IVORY, obenmuster="", bg=STRATOS, cid=None):
    cid = cid or uid("e")
    heli, barsvg, _ = heli_on_edge(418, C, KANTE_Y, GALLIANO, CUT, BAR, bar)
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{bg}"/>'
            + (oben(obenmuster) if obenmuster else "")
            + feld(unten) + heli + barsvg
            + word_max(KANTE_Y + BAR + 6, wort))
    return svg(disc(body, cid))

# ---------------------------------------------------------------- Muster
def muster(elemente, n=30, seed=7):
    import random
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(-20, S + 20), r.uniform(-20, KANTE_Y + 20)
        sc = r.uniform(0.7, 1.35)
        rot = r.uniform(-25, 25)
        out.append(f'<g transform="translate({x:.0f},{y:.0f}) scale({sc:.2f}) '
                   f'rotate({rot:.0f})" opacity="{r.uniform(.55,.95):.2f}">'
                   f'{r.choice(elemente)}</g>')
    return "".join(out)

GESCHENK = ('<rect x="-11" y="-9" width="22" height="18" fill="#E8C9A0"/>'
            '<rect x="-2.5" y="-9" width="5" height="18" fill="#C0392B"/>'
            '<rect x="-11" y="-1.5" width="22" height="4" fill="#C0392B"/>')
KERZE    = ('<rect x="-4" y="-8" width="8" height="18" fill="#E8C9A0"/>'
            '<rect x="-4" y="-8" width="8" height="18" fill="#C0392B" opacity=".45"/>'
            '<path d="M0,-14 q4,4 0,6 q-4,-2 0,-6" fill="#F5D76E"/>')
BEEREN   = ('<circle cx="-6" cy="0" r="4" fill="#FFFFFC"/>'
            '<circle cx="3" cy="-4" r="4" fill="#FFFFFC"/>'
            '<circle cx="4" cy="5" r="4" fill="#FFFFFC"/>')
BLATT    = '<path d="M0,-10 q9,10 0,20 q-9,-10 0,-20" fill="#2E6B4F"/>'
KUERBIS  = ('<ellipse cx="0" cy="0" rx="11" ry="9" fill="#E5720A"/>'
            '<rect x="-1.5" y="-13" width="3" height="5" fill="#2E6B4F"/>'
            '<path d="M-5,-2 l3,4 l-3,0 z M5,-2 l-3,4 l3,0 z" fill="#1A0E22"/>')
FLEDER   = ('<path d="M-12,0 q6,-7 6,2 q6,-9 12,0 q-6,4 -12,1 q-6,3 -6,-3 z" '
            'fill="#1A0E22"/>')
STERN    = '<circle r="1.8" fill="#FFFFFC"/>'

PRIDE = ["#E40303", "#FF8C00", "#FFED00", "#008026", "#004DFF", "#750787"]
DE    = ["#000000", "#DD0000", "#FFCE00"]
AT    = ["#ED2939", "#FFFFFF", "#ED2939"]

def _gold():
    """Invers: goldene Flaeche, Zeichen in Stratos."""
    h, b, _ = heli_on_edge(418, C, KANTE_Y, STRATOS, CUT, BAR, STRATOS)
    return svg(disc(f'<circle cx="{C}" cy="{C}" r="{R}" fill="{GALLIANO}"/>'
                    + h + b + word_max(KANTE_Y + BAR + 6, STRATOS), uid("g")))

E = {}
E["pb_standard"] = edition(flaeche(STRATOS), IVORY, IVORY)
E["pb_gold"]     = _gold()

# Pride -- Regenbogen unten, Wortmarke in Stratos, genau wie in eurer Fassung
E["pb_pride"] = edition(streifen(PRIDE), "#2B6EFF", STRATOS)

# Weihnachten -- Muster oben, rotes Feld unten
E["pb_weihnachten"] = edition(
    flaeche("#C0392B"), "#F08A80", IVORY,
    obenmuster=muster([GESCHENK, KERZE, BEEREN, BLATT], 30, 4), bg="#0E2E2B")

# Halloween -- Kuerbisse oben, oranges Feld unten
E["pb_halloween"] = edition(
    flaeche("#E5720A"), "#1A0E22", "#1A0E22",
    obenmuster=muster([KUERBIS, FLEDER], 20, 9), bg="#1A0E22")

# Nationalfeiertage
E["pb_einheit"] = edition(streifen(DE), IVORY, IVORY)
E["pb_at"]      = edition(streifen(AT), IVORY, STRATOS)
KREUZ = (f'<g transform="translate({C},150)">'
         f'<rect x="-15" y="-48" width="30" height="96" fill="#DA291C"/>'
         f'<rect x="-48" y="-15" width="96" height="30" fill="#DA291C"/></g>')
E["pb_ch"] = edition(flaeche("#DA291C"), IVORY, IVORY, obenmuster=KREUZ)

# 24-Stunden-Event
E["pb_nacht"] = edition(
    flaeche("#0A1836"), "#2B6EFF", IVORY,
    obenmuster=muster([STERN], 70, 11), bg="#04091A")

# Leere Vorlage fuer den Generator
_h, _b, _ = heli_on_edge(418, C, KANTE_Y, GALLIANO, CUT, BAR, IVORY)
E["pb_vorlage"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + oben('<g id="muster-oben"></g>')
    + feld('<g id="feld-unten">'
           + f'<rect x="{-S}" y="0" width="{S*3}" height="{S*2}" fill="#141C31"/>'
           + "".join(f'<rect x="{i*44-S}" y="0" width="22" height="{S*2}" fill="#1C2740"/>'
                     for i in range(24)) + '</g>')
    + _h + _b + word_max(KANTE_Y + BAR + 6, IVORY), uid("v")))

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    for k, v in E.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"{len(E)} Profilbilder:", ", ".join(E))

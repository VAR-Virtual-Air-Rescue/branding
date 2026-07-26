# -*- coding: utf-8 -*-
"""Profilbilder: Grundfassung und Sondereditionen.

Regel: das Zeichen bleibt unangetastet. Veraendert wird ausschliesslich der
Hintergrund und optional ein Ring. Damit bleibt die Marke in jeder Edition
dieselbe und der Generator braucht nur eine Datei auszutauschen.
"""
import math, os
from mark import (MARKS, STRATOS, GALLIANO, IVORY, C, R, S, ANG, svg, disc,
                  heli_on_edge, word_max, var_at, uid, EDGE, CUT, BAR)

def kern(bg=None, heli=GALLIANO, bar=IVORY, wort=IVORY, cid=None):
    """Das Zeichen ohne eigenen Hintergrund -- fuer Editionen."""
    h, b, _ = heli_on_edge(418, C, EDGE + CUT, heli, CUT, BAR, bar)
    body = h + b + word_max(EDGE + CUT + BAR + 6, wort)
    return (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{bg}"/>' if bg else "") + body

def edition(hintergrund, ring=None, ringw=26, cid=None, heli=GALLIANO,
            bar=IVORY, wort=IVORY):
    """Sonderedition: eigener Hintergrund, Zeichen unveraendert darueber."""
    cid = cid or uid("e")
    inner_r = R - (ringw if ring else 0)
    parts = [f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>']
    if ring:
        parts.append(ring)
    sub = uid("s")
    parts.append(f'<defs><clipPath id="{sub}"><circle cx="{C}" cy="{C}" '
                 f'r="{inner_r}"/></clipPath></defs><g clip-path="url(#{sub})">'
                 f'{hintergrund}{kern(heli=heli, bar=bar, wort=wort)}</g>')
    return svg(disc("".join(parts), cid))

def streifen(farben, winkel=0, deckkraft=1.0):
    n = len(farben); h = S / n
    inner = "".join(f'<rect x="{-S}" y="{i*h:.1f}" width="{S*3}" height="{h+1:.1f}" '
                    f'fill="{c}"/>' for i, c in enumerate(farben))
    return (f'<g opacity="{deckkraft}" transform="rotate({winkel} {C} {C})">'
            f'{inner}</g>')

def ringstreifen(farben, ringw=26):
    """Farbring aussen -- die zurueckhaltende Variante."""
    rr = R - ringw/2
    U = 2*math.pi*rr
    seg = U/len(farben)
    out = []
    for i, c in enumerate(farben):
        out.append(f'<circle cx="{C}" cy="{C}" r="{rr:.2f}" fill="none" stroke="{c}" '
                   f'stroke-width="{ringw}" stroke-dasharray="{seg:.2f} {U-seg:.2f}" '
                   f'stroke-dashoffset="{-i*seg:.2f}" transform="rotate(-90 {C} {C})"/>')
    return "".join(out)

PRIDE = ["#E40303", "#FF8C00", "#FFED00", "#008026", "#004DFF", "#750787"]
DE    = ["#000000", "#DD0000", "#FFCE00"]
AT    = ["#ED2939", "#FFFFFF", "#ED2939"]
CH_R  = "#DA291C"

E = {}
# Grundfassung
E["pb_standard"] = svg(disc(kern(bg=STRATOS), uid("p")))
E["pb_gold"]     = svg(disc(f'<circle cx="{C}" cy="{C}" r="{R}" fill="{GALLIANO}"/>'
                            + kern(heli=STRATOS, bar=STRATOS, wort=STRATOS), uid("p")))

# Sondereditionen -- Ringvariante
E["pb_pride"]    = edition("", ringstreifen(PRIDE))
E["pb_einheit"]  = edition("", ringstreifen(DE))
E["pb_at"]       = edition("", ringstreifen(AT))
E["pb_ch"]       = edition("", ringstreifen([CH_R]))
# Schweiz zusaetzlich mit Kreuz im Ring
E["pb_ch"] = E["pb_ch"].replace("</svg>",
    f'<g transform="translate({C},{R*0.115:.0f})"><rect x="-5" y="-14" width="10" '
    f'height="28" fill="#FFF"/><rect x="-14" y="-5" width="28" height="10" fill="#FFF"/>'
    f'</g></svg>')

# Halloween: Kuerbisorange als Flaeche, Zeichen bleibt
E["pb_halloween"] = edition(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="#1A0E22"/>'
    f'<circle cx="{C}" cy="{S*0.30:.0f}" r="{R*0.78:.0f}" fill="#E5720A" opacity=".22"/>',
    ringstreifen(["#E5720A", "#1A0E22"], 22), 22, heli="#F08A1E")

# Weihnachten: Schnee ueber der Kante
schnee = "".join(
    f'<circle cx="{40+((i*97)%432)}" cy="{30+((i*53)%250)}" r="{2+(i%3)}" '
    f'fill="#FFFFFC" opacity="{.35+.12*(i%4)}"/>' for i in range(46))
E["pb_weihnachten"] = edition(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="#071633"/>{schnee}',
    ringstreifen(["#1E7A3C", "#C0392B"], 24), 24)

# Nachtdienst / 24-Stunden-Event
E["pb_nacht"] = edition(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="#04091A"/>'
    + "".join(f'<circle cx="{28+((i*131)%456)}" cy="{22+((i*71)%230)}" r="1.6" '
              f'fill="#FFFFFC" opacity="{.3+.1*(i%5)}"/>' for i in range(38)),
    ringstreifen(["#2B6EFF", "#04091A"], 22), 22)

# Leere Vorlage fuer den Generator
E["pb_vorlage"] = svg(
    f'<defs><clipPath id="pbclip"><circle cx="{C}" cy="{C}" r="{R}"/></clipPath></defs>'
    f'<g clip-path="url(#pbclip)">'
    f'<rect width="{S}" height="{S}" fill="#141C31"/>'
    + "".join(f'<rect x="{i*32}" y="0" width="16" height="{S}" fill="#1C2740"/>'
              for i in range(16))
    + f'<g id="hintergrund"><!-- hier kommt der Austausch hinein --></g>'
    + kern() + '</g>')

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    for k, v in E.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"{len(E)} Profilbilder:", ", ".join(E))

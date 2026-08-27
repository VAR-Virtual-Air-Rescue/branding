# -*- coding: utf-8 -*-
"""Herleitungs- und Falschanwendungsgrafiken fuers Brandbook."""
import json, os
from mark import (MARKS, STRATOS, GALLIANO, IVORY, var_at, svg, disc, _heli,
                  heli_on_edge, S, C, R, EDGE, CUT, BAR, _inner, ANG)

E = {}

# ---------------------------------------------------------------- 01 Foto
# Abstraktion der Vorlage: Hubschrauber auf einem Klinikdach, Abendhimmel.
sky = ('<defs><linearGradient id="ev1" x1="0" y1="0" x2="0" y2="1">'
       '<stop offset="0%" stop-color="#33506E"/><stop offset="55%" stop-color="#6E7E8C"/>'
       '<stop offset="100%" stop-color="#9AA3A8"/></linearGradient></defs>'
       f'<rect width="{S}" height="{S}" fill="url(#ev1)"/>')
bldg = (f'<rect x="52" y="316" width="408" height="196" fill="#2B3340"/>'
        f'<rect x="52" y="300" width="408" height="18" fill="#3E4855"/>')
win = "".join(f'<rect x="{78+ (i%6)*62}" y="{352+(i//6)*54}" width="34" height="30" '
              f'fill="#5D6C7C" opacity="{.55 if i%3 else .8}"/>' for i in range(12))
E["_evo_foto"] = svg(sky + bldg + win + _heli(300, 108, 206, "#C43A32"))

# ---------------------------------------------------------------- 02 Entwurf
# Der erste Entwurf: Silhouette steht auf einem Band und wird unten angeschnitten.
band_y, band_h = 300, 62
E["_evo_entwurf"] = svg(
    f'<rect width="{S}" height="{S}" fill="#E9E7E2"/>'
    + _heli(400, 50, band_y - 94, "#1D3A8A")
    + f'<rect x="18" y="{band_y}" width="{S-36}" height="{band_h}" fill="#B9BDC2"/>'
    + f'<g transform="translate(40,{band_y+42})">'
    + _inner(svg("")).join([""])  # Platzhalter, Text folgt als Pfade unten
    + '</g>')

# Text im Band: "VIRTUAL AIR RESCUE"
from text2path import text_path
t, tw_ = text_path("VIRTUAL AIR RESCUE", "fonts/Uniform Bold.ttf", 30, 0.05)
E["_evo_entwurf"] = svg(
    f'<rect width="{S}" height="{S}" fill="#E9E7E2"/>'
    + _heli(400, 50, band_y - 94, "#1D3A8A")
    + f'<rect x="18" y="{band_y}" width="{S-36}" height="{band_h}" fill="#B9BDC2"/>'
    + f'<g fill="#1D3A8A" transform="translate({(S-tw_)/2:.1f},{band_y+42})">{t}</g>')

# ---------------------------------------------------------------- 03 Heute
PERSIAN, DODGER = "#233EE5", "#2B6EFF"
HOR = 261
E["_evo_heute"] = svg(disc(
    f'<rect x="0" y="0" width="{S}" height="{HOR}" fill="{STRATOS}"/>'
    f'<rect x="0" y="{HOR}" width="{S}" height="{S-HOR}" fill="{PERSIAN}"/>'
    f'<rect x="0" y="{HOR-11}" width="{S}" height="16" fill="{DODGER}"/>'
    + _heli(430, 41, 75, GALLIANO) + var_at(330, 256, 385, STRATOS), "ev3"))

# ---------------------------------------------------------------- Falschanwendung
def base(cid, heli_col=GALLIANO, bar_col=IVORY, word_col=IVORY, bg=STRATOS,
         heli_w=382, edge=EDGE, cut=CUT):
    heli, barsvg, _ = heli_on_edge(heli_w, C, edge + cut, heli_col, cut, BAR, bar_col)
    return disc(f'<circle cx="{C}" cy="{C}" r="{R}" fill="{bg}"/>'
                + heli + barsvg + var_at(228, C, 398, word_col), cid)

# Verzerrt
E["_dont_stretch"] = svg(f'<g transform="translate(0,64) scale(1,0.75)">{base("d1")}</g>')

# Fremde Farben
E["_dont_color"] = svg(base("d2", heli_col="#E5484D", bar_col="#3ECF8E",
                            word_col="#B36BFF", bg="#2A1A4A"))

# Heli schwebt -- der Bezug zur Kante ist weg
# Heli loest sich von der Kante -- der Bezug, um den es geht, ist weg
E["_dont_float"] = svg(base("d3", cut=-60))

# Gedreht
E["_dont_rotate"] = svg(f'<g transform="rotate(-14 {C} {C})">{base("d4")}</g>')

# Effekte
E["_dont_shadow"] = svg(
    '<defs><filter id="dsh" x="-30%" y="-30%" width="160%" height="160%">'
    '<feDropShadow dx="14" dy="18" stdDeviation="14" flood-color="#000" flood-opacity=".65"/>'
    '</filter><linearGradient id="dgr" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0%" stop-color="{GALLIANO}"/><stop offset="100%" stop-color="#FF3DAE"/>'
    '</linearGradient></defs>'
    f'<g filter="url(#dsh)">{base("d5", heli_col="url(#dgr)")}</g>')

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    for k, v in E.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"{len(E)} Zusatzgrafiken:", ", ".join(E))

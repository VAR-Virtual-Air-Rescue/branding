# -*- coding: utf-8 -*-
"""Baut alle VAR-Logokonzepte als echte Vektor-SVGs (kein eingebettetes Raster)."""
import json, os, math
from text2path import text_path

T = json.load(open("traced.json"))
HELI   = T["heli"]["levels"]["mittel"]["d"]     # 1000 x 318.5
HELI_H = T["heli"]["h"]
VAR    = T["var"]["levels"]["mittel"]["d"]      # 1000 x 482.16
VAR_H  = T["var"]["h"]

STRATOS, GALLIANO, IVORY = "#00113A", "#D5A507", "#FFFFFC"
PERSIAN, DODGER = "#233EE5", "#2B6EFF"

S = C = 512, 256
S, C, R = 512, 256, 256
HORIZON = 261

def _place(d, srcw, srch, w, cx, cy, fill):
    s = w / srcw; h = srch * s
    return (f'<g fill="{fill}" transform="translate({cx-w/2:.2f},{cy-h/2:.2f}) '
            f'scale({s:.5f})"><path d="{d}" fill-rule="evenodd"/></g>')

def heli(w, cx, cy, fill): return _place(HELI, 1000, HELI_H, w, cx, cy, fill)
def var(w, cx, cy, fill):  return _place(VAR, 1000, VAR_H, w, cx, cy, fill)

def svg(body, w=512, h=512, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">'
            f'{body}</svg>')

def disc(inner, cid):
    return (f'<defs><clipPath id="{cid}"><circle cx="{C}" cy="{C}" r="{R}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})">{inner}</g>')

def ring_rotor(rr, sw, col, gaps=2, blade=0.42, rot=-49):
    U = 2*math.pi*rr
    on  = U*blade
    off = U*(1-gaps*blade)/gaps
    return (f'<circle cx="{C}" cy="{C}" r="{rr:.2f}" fill="none" stroke="{col}" '
            f'stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-dasharray="{on:.1f} {off:.1f}" transform="rotate({rot} {C} {C})"/>')

# =====================  KONZEPTE  =====================
K = {}

# K0 – Ist-Zustand, erstmals als echter Vektor
K["k0_ist"] = svg(disc(
    f'<rect x="0" y="0" width="{S}" height="{HORIZON}" fill="{STRATOS}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="{S-HORIZON}" fill="{PERSIAN}"/>'
    f'<rect x="0" y="{HORIZON-11}" width="{S}" height="16" fill="{DODGER}"/>'
    + heli(430, 256, 148, GALLIANO) + var(330, 256, 385, STRATOS), "c0"))

# K1 – Reduktion: eine Fläche, Gold als einziger Akzent
K["k1_reduktion"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="6" fill="{GALLIANO}"/>'
    + heli(404, 256, 150, GALLIANO) + var(244, 256, 376, IVORY), "c1"))

# K2 – Horizont: zwei Felder, aber Gold statt Blau
K["k2_horizont"] = svg(disc(
    f'<rect x="0" y="0" width="{S}" height="{HORIZON}" fill="{STRATOS}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="{S-HORIZON}" fill="{GALLIANO}"/>'
    + heli(390, 256, 143, IVORY) + var(244, 256, 376, STRATOS), "c2"))

# K3 – Signet: Badge ohne Wortmarke, Wortmarke lebt daneben
K["k3_signet"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    f'<rect x="0" y="350" width="{S}" height="8" fill="{GALLIANO}"/>'
    + heli(452, 256, 228, GALLIANO), "c3"))

# K4 – Rotor: Rotorkreis wird zum Ring
K["k4_rotor"] = svg(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + heli(346, 256, 262, GALLIANO)
    + ring_rotor(R-20, 24, GALLIANO))

# =====================  APP-ICONS / FAVICON  =====================
# Der Heli ist 3,1:1 breit und ueberlebt 16 px nicht. Dafuer braucht es
# eine eigene, quadratisch gedachte Variante.
A = {}
A["icon_monogramm"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + var(372, 256, 262, GALLIANO), "a1"))
A["icon_monogramm_gold"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{GALLIANO}"/>'
    + var(372, 256, 262, STRATOS), "a2"))
A["icon_heli_gross"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + heli(600, 268, 256, GALLIANO), "a3"))
A["icon_horizont"] = svg(disc(
    f'<rect x="0" y="0" width="{S}" height="{HORIZON}" fill="{STRATOS}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="{S-HORIZON}" fill="{GALLIANO}"/>'
    + heli(400, 256, 140, IVORY) + var(300, 256, 372, STRATOS), "a4"))

# =====================  VARIANTEN  =====================
V = {}
# Monochrom (einfarbig, für Stick/Gravur/Fax/1c-Druck)
V["k1_mono_dunkel"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="6" fill="{IVORY}"/>'
    + heli(404, 256, 150, IVORY) + var(244, 256, 376, IVORY), "m1"))
V["k1_mono_hell"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{IVORY}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="6" fill="{STRATOS}"/>'
    + heli(404, 256, 150, STRATOS) + var(244, 256, 376, STRATOS), "m2"))
V["k1_invers"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{IVORY}"/>'
    f'<rect x="0" y="{HORIZON}" width="{S}" height="6" fill="{GALLIANO}"/>'
    + heli(404, 256, 150, GALLIANO) + var(244, 256, 376, STRATOS), "m3"))
V["k4_mono_dunkel"] = svg(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + heli(340, 256, 256, IVORY) + ring_rotor(R-24, 17, IVORY))

# =====================  LOCKUPS  =====================
WORT = "fonts/Uniform Bold.ttf"

def lockup_h(badge_inner, h=340, ink=None, rule=None, sub=None):
    """Badge links, Wortmarke rechts. Text als Pfade -> keine Font-Abhaengigkeit."""
    ink  = ink or STRATOS
    rule = rule or GALLIANO
    sub  = sub or STRATOS
    bs, pad = 260, 36
    gx = pad + bs + 46
    t1, w1 = text_path("VIRTUAL AIR RESCUE", WORT, 68, 0.045)
    t2, w2 = text_path("VIRTUELLE LUFTRETTUNG", WORT, 22, 0.34)
    tw = max(w1, w2)
    body = (f'<g transform="translate({pad},{(h-bs)/2}) scale({bs/512})">{badge_inner}</g>'
            f'<g fill="{ink}" transform="translate({gx},{h/2+8})">{t1}</g>'
            f'<rect x="{gx}" y="{h/2+34}" width="{tw:.0f}" height="3" fill="{rule}"/>'
            f'<g fill="{sub}" opacity=".7" transform="translate({gx},{h/2+78})">{t2}</g>')
    return svg(body, int(gx + tw + pad), h)

def lockup_v(badge_inner, ink=None, rule=None, sub=None):
    ink  = ink or STRATOS
    rule = rule or GALLIANO
    sub  = sub or STRATOS
    bs, pad = 430, 40
    t1, w1 = text_path("VIRTUAL AIR RESCUE", WORT, 60, 0.045)
    t2, w2 = text_path("VIRTUELLE LUFTRETTUNG", WORT, 21, 0.34)
    tw = max(w1, w2)
    w  = int(max(bs, tw) + 2*pad)
    yb = pad
    y1 = yb + bs + 84
    body = (f'<g transform="translate({(w-bs)/2},{yb}) scale({bs/512})">{badge_inner}</g>'
            f'<g fill="{ink}" transform="translate({(w-w1)/2:.1f},{y1})">{t1}</g>'
            f'<rect x="{(w-tw)/2:.1f}" y="{y1+24}" width="{tw:.0f}" height="3" fill="{rule}"/>'
            f'<g fill="{sub}" opacity=".7" transform="translate({(w-w2)/2:.1f},{y1+66})">{t2}</g>')
    return svg(body, w, int(y1 + 92))

# Badge-Innereien ohne <svg>-Hülle für die Lockups
BADGE = {k: v.split(">",1)[1].rsplit("</svg>",1)[0] for k, v in K.items()}
L = {"lockup_h_k1": lockup_h(BADGE["k1_reduktion"]),
     "lockup_h_k2": lockup_h(BADGE["k2_horizont"]),
     "lockup_h_k3": lockup_h(BADGE["k3_signet"]),
     "lockup_v_k1": lockup_v(BADGE["k1_reduktion"]),
     "lockup_v_k3": lockup_v(BADGE["k3_signet"]),
     # Negativfassung fuer dunkle Oberflaechen (Leitstelle, Hub, Discord)
     "lockup_h_k1_neg": lockup_h(BADGE["k1_reduktion"], ink=IVORY, sub=IVORY),
     "lockup_h_k3_neg": lockup_h(BADGE["k3_signet"], ink=IVORY, sub=IVORY)}

os.makedirs("out", exist_ok=True)
allf = {**K, **V, **L, **A}
for k, v in allf.items():
    open(f"out/{k}.svg", "w").write(v)
print(f"{len(allf)} SVGs geschrieben")
for k in K: print(f"  {k:18s} {len(K[k]):>6d} Bytes")

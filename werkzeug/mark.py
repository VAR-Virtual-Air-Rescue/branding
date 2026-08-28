# -*- coding: utf-8 -*-
"""VAR-Markenzeichen.

Der Hubschrauber steht auf der Kante eines Dachlandeplatzes und wird von ihr
angeschnitten -- so wie im ersten Entwurf, der aus dem Foto eines Klinikdachs
entstand.

Die Kante ist nicht waagerecht, sondern um -3,27 Grad gekippt. Das ist kein
Gestaltungseinfall, sondern gemessen: die untere Stuetzhuelle der Zeichnung, also
genau die Linie, auf der dieser Hubschrauber tatsaechlich aufliegen wuerde.
Dadurch passen Rumpfunterkante und Balkenoberkante exakt aufeinander.
"""
import json, math, itertools
from text2path import text_path

_uid = itertools.count(1)
def uid(p='u'): return f"{p}{next(_uid)}"

T = json.load(open("traced.json"))
HELI, HELI_H = T["heli"]["levels"]["mittel"]["d"], T["heli"]["h"]   # 1000 x 318.5
VAR,  VAR_H  = T["var"]["levels"]["mittel"]["d"],  T["var"]["h"]    # 1000 x 482.16

TILT = json.load(open("tilt.json"))
ANG  = TILT["angle"]                 # -3.27 Grad
SP1, SP2 = TILT["p1"], TILT["p2"]    # Stuetzpunkte in der 1000er-Zeichnung

STRATOS  = "#00113A"
GALLIANO = "#D5A507"
IVORY    = "#FFFFFC"
SIGNAL   = "#2B6EFF"
INK      = "#050B1C"

S, C, R = 512, 256, 256

# ---------------------------------------------------------------- Bausteine
def _heli(w, ox, oy, fill, oid=""):
    s = w / 1000
    return (f'<g fill="{fill}"{oid} transform="translate({ox:.2f},{oy:.2f}) '
            f'scale({s:.5f})"><path d="{HELI}" fill-rule="evenodd"/></g>')

def var_at(w, cx, cy, fill):
    s = w / 1000
    return (f'<g fill="{fill}" transform="translate({cx-w/2:.2f},{cy-VAR_H*s/2:.2f}) '
            f'scale({s:.5f})"><path d="{VAR}" fill-rule="evenodd"/></g>')

def svg(body, w=S, h=S, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{defs}{body}</svg>')

def disc(inner, cid, r=R):
    return (f'<defs><clipPath id="{cid}"><circle cx="{C}" cy="{C}" r="{r}"/></clipPath>'
            f'</defs><g clip-path="url(#{cid})">{inner}</g>')

def _support(w, ox, oy):
    """Stuetzlinie des platzierten Helis: Punkt und Steigung in Badge-Koordinaten."""
    s = w / 1000
    px, py = ox + SP1[0] * s, oy + SP1[1] * s
    return px, py, math.tan(math.radians(ANG))

def heli_on_edge(w, cx, edge_y, fill, cut=26, bar=13, bar_col=IVORY, oid=""):
    """Setzt Heli und Kante so, dass die Rumpfunterkante auf der Balkenoberkante liegt.

    `edge_y` ist die Hoehe der Kante in der Mitte des Zeichens.
    `cut` ist die Tiefe, mit der der Rumpf hinter der Kante verschwindet.
    """
    s = w / 1000
    ox = cx - w / 2
    # oy so waehlen, dass die Stuetzlinie in Bildmitte genau auf edge_y liegt
    k = math.tan(math.radians(ANG))
    y_at_cx = SP1[1] * s + k * (cx - (ox + SP1[0] * s))
    oy = edge_y - y_at_cx
    heli = _heli(w, ox, oy, fill, oid)
    # Balken: gedrehtes Rechteck, Oberkante genau auf der Stuetzlinie
    L = S * 2.4
    bar_svg = (f'<g transform="translate({cx},{edge_y}) rotate({ANG:.3f})">'
               f'<rect x="{-L/2:.1f}" y="0" width="{L:.1f}" height="{bar}" '
               f'fill="{bar_col}"/></g>')
    return heli, bar_svg, oy

def rotor(rr, sw, col, blades=2, blade=0.40, rot=None, cap="round"):
    """Rotorkreis als unterbrochener Ring."""
    rot = ANG - 47 if rot is None else rot
    U = 2 * math.pi * rr
    on = U * blade
    off = U * (1 - blades * blade) / blades
    return (f'<circle cx="{C}" cy="{C}" r="{rr:.2f}" fill="none" stroke="{col}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}" '
            f'stroke-dasharray="{on:.1f} {off:.1f}" transform="rotate({rot:.1f} {C} {C})"/>')


# --- Wortmarke: mitgekippt und bis an den Kreisrand ------------------------
import re as _re
_VP = None
def _var_points(steps=14):
    """Punkte der Wortmarke, Beziers aufgeloest -- fuer die Randberechnung."""
    global _VP
    if _VP is not None:
        return _VP
    toks = _re.findall(r'[MLCZ]|-?\d+(?:\.\d+)?', VAR)
    pts = []; i = 0; cur = (0.0, 0.0); start = cur
    while i < len(toks):
        c = toks[i]
        if c == "M":
            cur = (float(toks[i+1]), float(toks[i+2])); start = cur; pts.append(cur); i += 3
        elif c == "L":
            cur = (float(toks[i+1]), float(toks[i+2])); pts.append(cur); i += 3
        elif c == "C":
            p1 = (float(toks[i+1]), float(toks[i+2])); p2 = (float(toks[i+3]), float(toks[i+4]))
            p3 = (float(toks[i+5]), float(toks[i+6]))
            for k in range(1, steps+1):
                t = k/steps; u = 1-t
                pts.append((u*u*u*cur[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0],
                            u*u*u*cur[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]))
            cur = p3; i += 7
        elif c == "Z":
            cur = start; i += 1
        else:
            i += 1
    _VP = pts
    return pts

_WCACHE = {}

def _wort_masse(top, rad, schnitt, gap, kappe=12.0):
    """Groesste Wortmarke, die den konzentrischen Beschnitt um hoechstens `schnitt`
    ueberlaeuft -- und der waagerechte Versatz, bei dem sie am weitesten kommt.

    Warum ein Versatz noetig ist: die Wortmarke wird um den Mittelpunkt gekippt,
    liegt mit ihrem Schwerpunkt aber deutlich darunter. Waere sie vor dem Kippen
    mittig, saesse sie danach zu weit rechts und das Bein des R stiesse zuerst an.

    Warum er gedeckelt ist: ohne Grenze wandert das Optimum auf rund 34 px nach
    links. Die Luft waere dann zwar auf beiden Seiten gleich, die Wortmarke saesse
    aber sichtbar aus der Mitte -- das Auge liest die Buchstaben, nicht den Abstand.
    `kappe` begrenzt den Ausgleich deshalb auf das, was die Kippung verursacht.

    Der Abstand zum Mittelpunkt aendert sich beim Drehen nicht, deshalb genuegt es,
    ueber die ungedrehte Lage zu rechnen. max(Abstand) ist konvex in `dx`, also
    findet eine Drittelsuche den besten Versatz zuverlaessig.
    """
    schl = (round(top, 3), round(rad, 3), round(schnitt, 3), round(gap, 3),
            round(kappe, 3))
    if schl in _WCACHE:
        return _WCACHE[schl]
    pts = _var_points()

    def dmax(w, dx):
        sc = w / 1000.0
        ox = C - w / 2 + dx
        return max(math.hypot(ox + px*sc - C, top + py*sc - C) for px, py in pts)

    def bestes_dx(w):
        lo, hi = -kappe, kappe
        for _ in range(60):
            a, b = lo + (hi-lo)/3, hi - (hi-lo)/3
            if dmax(w, a) < dmax(w, b): hi = b
            else: lo = a
        return (lo + hi) / 2

    grenze = (rad - gap) + schnitt     # Beschnittkreis plus zugelassener Ueberlauf
    lo, hi = 60.0, rad * 3.0
    for _ in range(44):
        mid = (lo + hi) / 2
        if dmax(mid, bestes_dx(mid)) <= grenze: lo = mid
        else: hi = mid
    erg = (lo, bestes_dx(lo))
    _WCACHE[schl] = erg
    return erg


def word_max(top, fill, rad=R, gap=7.0, schnitt=32.0, tilt=True, cid=None):
    """Wortmarke unter der Kante.

    Sie laeuft absichtlich ueber den Rand hinaus und wird von einem Kreis
    geschnitten, der konzentrisch zum Zeichen liegt. Dadurch ist die Schnittkante
    ueberall gleich weit vom Rand entfernt -- eine Optimierung auf den einzelnen
    weitesten Punkt genuegt nicht, weil dann nur die Ecken den Rand beruehren und
    alles dazwischen abfaellt.

    `gap`   Abstand der Schnittkante zum Rand. 0 = buendig.
    `schnitt`  wie weit die Buchstaben ueber den Beschnittkreis hinauslaufen
            duerfen, in Einheiten des 512er Zeichens. Der Anschnitt ist gewollt --
            er ist dieselbe Geste wie der Hubschrauber, den die Kante anschneidet.
            Er muss nur beherrscht bleiben: 32 vergroessert die Wortmarke auf 399
            und nimmt unten bis zu 46 Einheiten von 191 Buchstabenhoehe. V, A und R
            bleiben dabei zweifelsfrei. Ab etwa 48 verlieren der Fuss des V und das
            Bein des R ihre Abschluesse, und es liest sich als Fehler statt als
            Absicht. 0 heisst: die Wortmarke beruehrt den Beschnitt gerade eben.

            Voraussetzung ist die vollstaendige Zeichnung. Die Fassung, die bis
            28.08.2026 in traced.json lag, war schon beschnitten (s. trace_var.py) --
            jeder Anschnitt kam dort zum zweiten Mal und sah nach Panne aus.
    """
    inner = rad - gap
    w, dx = _wort_masse(top, rad, schnitt, gap)
    sc = w/1000
    cid = cid or uid("wc")
    body = (f'<g fill="{fill}" transform="translate({C-w/2+dx:.2f},{top:.2f}) '
            f'scale({sc:.5f})"><path d="{VAR}" fill-rule="evenodd"/></g>')
    body = (f'<defs><clipPath id="{cid}"><circle cx="{C}" cy="{C}" r="{inner:.2f}"/>'
            f'</clipPath></defs><g clip-path="url(#{cid})">{body}</g>')
    if tilt:
        body = f'<g transform="rotate({ANG:.3f} {C} {C})">{body}</g>'
    return body

# ---------------------------------------------------------------- Fassungen
EDGE = 226      # Kante mit Wortmarke darunter: EDGE + CUT = 256 = Kreismitte.
                # Die Kante ist damit ein Durchmesser -- die laengste Sehne, die
                # der Kreis hergibt. Himmel und Feld sind gleich hoch, und die
                # Wortmarke bekommt die Haelfte statt eines Drittels.
EDGE_LEER = 300 # Kante ohne Wortmarke darunter: Signet, R2-R5, App-Icon.
                # Dort brauchte die Mitte niemand -- sie erzeugt nur eine leere
                # Haelfte und verkleinert den Hubschrauber, der hier alles traegt.
CUT  = 30
BAR  = 13

def mark(bg=STRATOS, heli_col=GALLIANO, bar_col=IVORY, word_col=IVORY, lower=None,
         cid="m", heli_w=414, word_top=None, with_word=True, edge=EDGE,
         bar=BAR, cut=CUT):
    heli, barsvg, _ = heli_on_edge(heli_w, C, edge + cut, heli_col, cut, bar, bar_col)
    parts = [f'<circle cx="{C}" cy="{C}" r="{R}" fill="{bg}"/>']
    if lower:
        k = math.tan(math.radians(ANG))
        L = S * 2.4
        parts.append(f'<g transform="translate({C},{edge+cut}) rotate({ANG:.3f})">'
                     f'<rect x="{-L/2:.1f}" y="0" width="{L:.1f}" height="{S}" '
                     f'fill="{lower}"/></g>')
    parts.append(heli)
    parts.append(barsvg)
    if with_word:
        parts.append(word_max(word_top if word_top is not None else edge + cut + bar + 6,
                              word_col))
    return svg(disc("".join(parts), cid))

MARKS = {}

# --- Grundfassungen -------------------------------------------------------
MARKS["n1_kante"]   = mark(cid="n1")
MARKS["n2_ivory"]   = mark(heli_col=IVORY, bar_col=GALLIANO, cid="n2")
MARKS["n3_zweifeld"]= mark(heli_col=IVORY, bar_col=IVORY, lower=GALLIANO,
                           word_col=STRATOS, cid="n3")
MARKS["n4_signet"]  = mark(with_word=False, heli_w=442, edge=318, cid="n4")  # tief, s. EDGE_LEER

# --- Rotorfassungen -------------------------------------------------------
def rotor_mark(cid, ring_r=234, sw=20, ring_col=GALLIANO, heli_col=GALLIANO,
               bar_col=IVORY, bg=STRATOS, heli_w=344, edge=EDGE_LEER, blades=2,
               blade=0.40, with_word=False, word_col=IVORY, word_y=404, word_w=190,
               inner_r=None, cap="round"):
    inner_r = inner_r if inner_r is not None else R
    heli, barsvg, _ = heli_on_edge(heli_w, C, edge + CUT, heli_col, CUT, BAR, bar_col)
    body = f'<circle cx="{C}" cy="{C}" r="{inner_r}" fill="{bg}"/>' + heli + barsvg
    if with_word:
        body += word_max(edge + CUT + BAR + 6, word_col, rad=inner_r,
                         schnitt=32.0 * inner_r / R)
    return svg(disc(body, cid, inner_r) + rotor(ring_r, sw, ring_col, blades, blade, cap=cap))

# R1  Ring aussen, Heli auf der Kante, Wortmarke darunter
# R1 traegt die Wortmarke, also Kante durch die Mitte des inneren Kreises
MARKS["r1_rotor"] = rotor_mark("r1", ring_r=236, sw=19, inner_r=216, heli_w=267,
                               edge=EDGE, with_word=True)
# R2  Zwei Rotorblaetter, kein gefuellter Innenkreis -- offene Fassung
MARKS["r2_offen"] = rotor_mark("r2", ring_r=238, sw=17, inner_r=222, heli_w=326,
                               edge=300, blades=2, blade=0.44)
# R3  Drei Blaetter, engerer Ring, Heli gross
MARKS["r3_dreiblatt"] = rotor_mark("r3", ring_r=240, sw=15, inner_r=226, heli_w=346,
                                   edge=304, blades=3, blade=0.27)
# R4  Rotorbogen statt Ring: nur der Blattschlag ueber dem Heli
def r4(cid="r4"):
    heli, barsvg, _ = heli_on_edge(360, C, 292 + CUT, GALLIANO, CUT, BAR, IVORY)
    import math as _m
    rr, sw = 214, 16
    U = 2 * _m.pi * rr
    arc = (f'<circle cx="{C}" cy="{C}" r="{rr}" fill="none" stroke="{GALLIANO}" '
           f'stroke-width="{sw}" stroke-linecap="round" '
           f'stroke-dasharray="{U*0.40:.1f} {U:.1f}" '
           f'transform="rotate({ANG-196:.1f} {C} {C})"/>')
    inner = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
             + arc + heli + barsvg)
    return svg(disc(inner, cid))
MARKS["r4_bogen"] = r4()

# R5  Rotor als voller Ring in Ivory, Heli und Kante in Gold
MARKS["r5_ivory_ring"] = rotor_mark("r5", ring_r=236, sw=18, ring_col=IVORY,
                                    heli_col=GALLIANO, bar_col=IVORY, inner_r=208,
                                    heli_w=306, edge=292, blades=2, blade=0.43)

# --- Ableitungen ----------------------------------------------------------
MARKS["n1_mono_negativ"] = mark(heli_col=IVORY, bar_col=IVORY, cid="mn")
MARKS["n1_mono_positiv"] = mark(bg=IVORY, heli_col=STRATOS, bar_col=STRATOS,
                                word_col=STRATOS, cid="mp")
MARKS["n1_hell"]         = mark(bg=IVORY, heli_col=GALLIANO, bar_col=STRATOS,
                                word_col=STRATOS, cid="mh")

MARKS["icon_monogramm"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + var_at(376, C, 262, GALLIANO), "i1"))
MARKS["icon_monogramm_gold"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{GALLIANO}"/>'
    + var_at(376, C, 262, STRATOS), "i2"))
def icon_kante():
    # Bewusst tief: unter 32 px zaehlt allein, dass der Hubschrauber als
    # Hubschrauber lesbar bleibt. Er braucht die volle Breite des Kreises.
    heli, barsvg, _ = heli_on_edge(500, C, 336, GALLIANO, 34, 22, IVORY)
    return svg(disc(f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
                    + heli + barsvg, "i3"))
MARKS["icon_kante"] = icon_kante()

# ---------------------------------------------------------------- Lockups
WORT = "fonts/Uniform Bold.ttf"
def _inner(s): return s.split(">", 1)[1].rsplit("</svg>", 1)[0]

def lockup_h(key="n1_kante", h=340, ink=STRATOS, rule=GALLIANO, sub=None,
             claim="VIRTUELLE LUFTRETTUNG"):
    sub = sub or ink
    bs, pad = 258, 36
    gx = pad + bs + 46
    t1, w1 = text_path("VIRTUAL AIR RESCUE", WORT, 68, 0.045)
    t2, w2 = text_path(claim, WORT, 22, 0.34)
    tw = max(w1, w2)
    body = (f'<g transform="translate({pad},{(h-bs)/2}) scale({bs/512})">'
            f'{_inner(MARKS[key])}</g>'
            f'<g fill="{ink}" transform="translate({gx},{h/2+8})">{t1}</g>'
            f'<rect x="{gx}" y="{h/2+34}" width="{tw:.0f}" height="3" fill="{rule}"/>'
            f'<g fill="{sub}" opacity=".7" transform="translate({gx},{h/2+78})">{t2}</g>')
    return svg(body, int(gx + tw + pad), h)

def lockup_v(key="n1_kante", ink=STRATOS, rule=GALLIANO, sub=None):
    sub = sub or ink
    bs, pad = 430, 40
    t1, w1 = text_path("VIRTUAL AIR RESCUE", WORT, 60, 0.045)
    t2, w2 = text_path("VIRTUELLE LUFTRETTUNG", WORT, 21, 0.34)
    tw = max(w1, w2); w = int(max(bs, tw) + 2 * pad); y1 = pad + bs + 84
    body = (f'<g transform="translate({(w-bs)/2},{pad}) scale({bs/512})">'
            f'{_inner(MARKS[key])}</g>'
            f'<g fill="{ink}" transform="translate({(w-w1)/2:.1f},{y1})">{t1}</g>'
            f'<rect x="{(w-tw)/2:.1f}" y="{y1+24}" width="{tw:.0f}" height="3" fill="{rule}"/>'
            f'<g fill="{sub}" opacity=".7" transform="translate({(w-w2)/2:.1f},{y1+66})">{t2}</g>')
    return svg(body, w, int(y1 + 92))

LOCKUPS = {
    "lockup_h":     lockup_h(),
    "lockup_h_neg": lockup_h(ink=IVORY),
    "lockup_v":     lockup_v(),
    "lockup_v_neg": lockup_v(ink=IVORY),
}

if __name__ == "__main__":
    import os
    os.makedirs("neu", exist_ok=True)
    for k, v in {**MARKS, **LOCKUPS}.items():
        open(f"neu/{k}.svg", "w").write(v)
    print(f"{len(MARKS)+len(LOCKUPS)} Dateien  |  Kantenwinkel {ANG:+.2f} Grad")

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

# Die beiden Scheiben, aus dem Hubschrauberpfad herausgeloest. Der Pfad hat fuenf
# Teilpfade: 0 ist der Rumpf, 1 die Fenestron-Oeffnung im Heck, 2 das Kabinen-
# fenster, 3 die Frontscheibe, 4 ein Spalt unter dem Rotormast. Nur 2 und 3 sind
# Scheiben; 1 und 4 sind Durchbrueche und bleiben offen.
import re as _re0
_HELI_TEILE = _re0.findall(r"M[^M]*", HELI)
SCHEIBEN = _HELI_TEILE[2] + _HELI_TEILE[3]

# Als Loch im Pfad wirkten die Scheiben vollstaendig durchsichtig. Sie bekommen
# jetzt einen Hauch der Rumpffarbe -- nicht eine feste Farbe, damit es auf jedem
# Untergrund traegt: auf Stratos, auf Ivory, auf den Flaggen der Editionen.
# Ab etwa 60 % verschmilzt die Frontscheibe mit der Nase.
SCHEIBE_DECKUNG = 0.45

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
            f'scale({s:.5f})"><path d="{HELI}" fill-rule="evenodd"/>'
            f'<path d="{SCHEIBEN}" opacity="{SCHEIBE_DECKUNG}"/></g>')

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

def _var_konturen(steps=24):
    """Die Wortmarke als geschlossene Polygonzuege -- fuer Schnitte auf Hoehe y."""
    global _VK
    if _VK is not None:
        return _VK
    toks = _re.findall(r"[MLCZ]|-?\d+(?:\.\d+)?", VAR)
    ks, k = [], []
    i = 0; cur = (0.0, 0.0); start = cur
    while i < len(toks):
        c = toks[i]
        if c == "M":
            if k: ks.append(k)
            cur = (float(toks[i+1]), float(toks[i+2])); start = cur; k = [cur]; i += 3
        elif c == "L":
            cur = (float(toks[i+1]), float(toks[i+2])); k.append(cur); i += 3
        elif c == "C":
            p1 = (float(toks[i+1]), float(toks[i+2])); p2 = (float(toks[i+3]), float(toks[i+4]))
            p3 = (float(toks[i+5]), float(toks[i+6]))
            for j in range(1, steps+1):
                t = j/steps; u = 1-t
                k.append((u*u*u*cur[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0],
                          u*u*u*cur[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]))
            cur = p3; i += 7
        elif c == "Z":
            k.append(start); cur = start; i += 1
        else:
            i += 1
    if k: ks.append(k)
    _VK = ks
    return ks
_VK = None


def _schnitte(y):
    """Waagerechter Schnitt durch die Wortmarke auf Hoehe y -- Paare von x."""
    xs = []
    for k in _var_konturen():
        for (x1, y1), (x2, y2) in zip(k, k[1:]):
            if ((y1 <= y < y2) or (y2 <= y < y1)) and y2 != y1:
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return [(xs[i], xs[i+1]) for i in range(0, len(xs)-1, 2)]


_FUESSE = None

def _fuesse():
    """Die Fuesse auf der Grundlinie mit der Neigung ihrer beiden Aussenkanten.

    Die Staemme dieser Wortmarke sind geneigt und verjuengen sich nach unten --
    das Bein des A laeuft mit +0,41 je Einheit nach rechts, der Keil des V
    schliesst sich nach 136 Einheiten. Eine Verlaengerung senkrecht nach unten
    setzt deshalb einen sichtbaren Knick an. Stattdessen werden beide Aussenkanten
    in ihrer eigenen Richtung weitergefuehrt; laufen sie zusammen, endet der Fuss
    dort von selbst.
    """
    global _FUESSE
    if _FUESSE is not None:
        return _FUESSE
    REF = 40.0
    unten, oben = _schnitte(VAR_H - 1.0), _schnitte(VAR_H - REF)
    out = []
    for ua, ub in unten:
        kand = [(oa, ob) for oa, ob in oben if not (ob < ua - 5 or oa > ub + 5)]
        if not kand:
            continue
        oa, ob = max(kand, key=lambda t: min(t[1], ub) - max(t[0], ua))
        sl, sr = (ua - oa) / (REF - 1.0), (ub - ob) / (REF - 1.0)
        treff = (ub - ua) / (sl - sr) if sl > sr else float("inf")
        out.append((ua, ub, sl, sr, treff))
    _FUESSE = out
    return out


# Wie weit die Fuesse weitergefuehrt werden, in Pfadeinheiten. 200 reicht in jedem
# Fall bis hinter den Beschnitt -- daran zu drehen aendert am Bild nichts mehr.
VERLAENGERUNG = 200.0


# Die Verlaengerung beginnt ein Stueck oberhalb der Grundlinie und schiebt sich
# unter den Buchstaben. Stiesse sie genau auf die Grundlinie, zeichnete der
# Renderer an der Naht eine Haarlinie -- zwei Flaechen gleicher Farbe, die sich
# nur beruehren, decken die Kante nicht.
UEBERLAPP = 4.0


def _fuss_pfad(tiefe=VERLAENGERUNG):
    d = []
    u = UEBERLAPP
    for xa, xb, sl, sr, treff in _fuesse():
        t = min(tiefe, treff)
        d.append("M%.2f %.2f L%.2f %.2f L%.2f %.2f L%.2f %.2f Z"
                 % (xa - sl*u, VAR_H - u, xb - sr*u, VAR_H - u,
                    xb + sr*t, VAR_H + t, xa + sl*t, VAR_H + t))
    return "".join(d)


_WCACHE = {}

# Die Wortmarke haengt unten am Kreis, nicht oben an der Kante. So sitzt sie im
# Ursprungslogo, und so liest sie sich auch: sie steht auf dem Grund des Zeichens
# und wird von dessen Rundung angeschnitten -- dieselbe Geste wie beim
# Hubschrauber, den die Kante anschneidet.
WORT_BREITE = 0.828   # Anteil des Durchmessers, aus dem Ursprungslogo gemessen


def _wort_lage(rad, gap, breite, oben, kappe=12.0):
    """Breite, Oberkante und waagerechter Versatz der Wortmarke.

    Die Wortmarke liegt oben am Balken an; `oben` ist dessen Unterkante. Die
    Groesse steht fest (Anteil des Durchmessers). Unten enden die Buchstaben nicht
    von selbst am Rand -- ihre Fuesse werden weitergefuehrt, bis der Beschnitt sie
    abschneidet (s. `_fuesse`). Sichtbar wird das nur beim A: V und R liegen so weit
    aussen, dass die Rundung sie schon oberhalb der Grundlinie kappt.

    Bleibt der waagerechte Versatz. Die Wortmarke wird um den Mittelpunkt gekippt,
    liegt mit ihrem Schwerpunkt aber darunter; ohne Ausgleich stiesse das Bein des
    R zuerst an. max(Abstand zum Mittelpunkt) ist konvex im Versatz, eine
    Drittelsuche findet ihn also zuverlaessig. `kappe` begrenzt ihn: ohne Grenze
    wandert das Optimum so weit, dass die Wortmarke sichtbar aus der Mitte sitzt.
    """
    schl = (round(rad, 3), round(gap, 3), round(breite, 4), round(oben, 3),
            round(kappe, 3))
    if schl in _WCACHE:
        return _WCACHE[schl]
    pts = _var_points()
    inner = rad - gap
    w = breite * 2 * rad
    oy = float(oben)

    def dmax(dx):
        sc = w / 1000.0
        ox = C - w / 2 + dx
        return max(math.hypot(ox + px*sc - C, oy + py*sc - C) for px, py in pts)

    lo, hi = -kappe, kappe
    for _ in range(60):
        x, y = lo + (hi-lo)/3, hi - (hi-lo)/3
        if dmax(x) < dmax(y): hi = y
        else: lo = x
    erg = (w, oy, (lo + hi) / 2)
    _WCACHE[schl] = erg
    return erg


def word_max(fill, oben, rad=R, gap=7.0, breite=WORT_BREITE, tilt=True, cid=None):
    """Wortmarke unten im Zeichen, von der Rundung angeschnitten.

    `oben`   Unterkante des Balkens -- dort liegt die Wortmarke an.
    `breite` Anteil des Durchmessers. 0.828 ist am Ursprungslogo gemessen.
    `gap`    Abstand des Beschnittkreises zum sichtbaren Rand.

    Die Wortmarke fuellt das Feld zwischen Balken und Rundung: oben liegt sie am
    Strich an, unten werden die Fuesse weitergefuehrt und vom Beschnitt gekappt.
    Sichtbar ist das beim A, das dadurch bis in den Rahmen laeuft; V und R kappt die
    Rundung ohnehin schon oberhalb der Grundlinie. Voraussetzung ist die vollstaendige
    Zeichnung -- die Fassung, die bis 28.08.2026 in traced.json lag, war schon
    beschnitten (s. trace_var.py), und jeder Anschnitt kam dort zum zweiten Mal.
    """
    inner = rad - gap
    w, oy, dx = _wort_lage(rad, gap, breite, oben)
    sc = w / 1000.0
    cid = cid or uid("wc")
    body = (f'<g fill="{fill}" transform="translate({C-w/2+dx:.2f},{oy:.2f}) '
            f'scale({sc:.5f})"><path d="{VAR}" fill-rule="evenodd"/>'
            f'<path d="{_fuss_pfad()}"/></g>')
    body = (f'<defs><clipPath id="{cid}"><circle cx="{C}" cy="{C}" r="{inner:.2f}"/>'
            f'</clipPath></defs><g clip-path="url(#{cid})">{body}</g>')
    if tilt:
        body = f'<g transform="rotate({ANG:.3f} {C} {C})">{body}</g>'
    return body


# ---------------------------------------------------------------- Fassungen
# Der Hubschrauber ist 444 breit -- so nah an den Rand, wie es traegt: die
# Rotorspitzen behalten 11 Einheiten Luft. Bei der Mindestgroesse von 96 px sind
# das noch zwei sichtbare Pixel Grund; darunter uebernimmt ohnehin das Signet.
EDGE = 226      # Kante mit Wortmarke darunter: EDGE + CUT = 256 = Kreismitte.
                # Die Kante ist damit ein Durchmesser -- die laengste Sehne, die
                # der Kreis hergibt. Himmel und Feld sind gleich hoch, und die
                # Wortmarke bekommt die Haelfte statt eines Drittels.
EDGE_LEER = 300 # Kante ohne Wortmarke darunter: Signet, R2-R5, App-Icon.
                # Dort brauchte die Mitte niemand -- sie erzeugt nur eine leere
                # Haelfte und verkleinert den Hubschrauber, der hier alles traegt.
CUT  = 30
BAR  = 13


# Die Fuge zwischen Kante und Wortmarke ist so stark wie die Kante selbst.
# Fugenlos verschmelzen die flachen Oberkanten von V und R mit dem Balken --
# zusammen ein Drittel der Wortmarkenbreite -- und die Kante wird zum
# Unterstrich, was sie ausdruecklich nicht sein soll. Die Zahl ist nicht
# gegriffen: die Kante misst sich an sich selbst, und wenn BAR sich aendert,
# wandert die Fuge mit. 13 sind bei der Mindestgroesse von 96 px noch 2,4 px
# und im Druck bei 22 mm noch 0,56 mm -- sie schliesst sich also nirgends.
FUGE = BAR
def mark(bg=STRATOS, heli_col=GALLIANO, bar_col=IVORY, word_col=IVORY, lower=None,
         cid="m", heli_w=444, word_top=None, with_word=True, edge=EDGE,
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
        parts.append(word_max(word_col, edge + cut + bar + FUGE))
    return svg(disc("".join(parts), cid))

MARKS = {}

# --- Grundfassungen -------------------------------------------------------
MARKS["n1_kante"]   = mark(cid="n1")
MARKS["n2_ivory"]   = mark(heli_col=IVORY, bar_col=GALLIANO, cid="n2")
MARKS["n3_zweifeld"]= mark(heli_col=IVORY, bar_col=IVORY, lower=GALLIANO,
                           word_col=STRATOS, cid="n3")
MARKS["n4_signet"]  = mark(with_word=False, heli_w=442, edge=318, cid="n4")  # tief, s. EDGE_LEER

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

# -*- coding: utf-8 -*-
"""VAR-Vorlagensystem: Social Media, Video, Veranstaltung.

Durchgaengiges Element in allen Formaten ist die Kante -- derselbe Balken, auf dem
im Zeichen der Hubschrauber steht. Sie traegt in jeder Vorlage die Absenderzeile.
"""
import math, os
from text2path import text_path
from mark import (MARKS, STRATOS, GALLIANO, IVORY, SIGNAL, INK, _inner)

BOLD = "fonts/Uniform Bold.ttf"
REG  = "fonts/Uniform.ttf"
BLK  = "fonts/Uniform Black.ttf"

_uid = [0]
def uid(p="u"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"

# ---------------------------------------------------------------- Textsatz
# Zeichen, die Uniform nicht hat, werden vom Setzer still verschluckt -- die
# Breite bleibt stehen, der Buchstabe fehlt. So verschwand ein Pfeil aus zwei
# Vorlagen, ohne dass irgendwo etwas schieflief. Deshalb wird mitgeschrieben,
# was fehlt; der Bauschritt meldet es am Ende.
FEHLENDE = set()

def _pruefe(s, font, size):
    for ch in set(s):
        if not ch.strip():
            continue
        d, _ = text_path(ch, font, 40, 0)
        if len(d) < 5:
            FEHLENDE.add((ch, os.path.basename(font)))


def txt(s, size, fill, x=0, y=0, font=BOLD, tracking=0.04, anchor="start", opacity=None):
    _pruefe(s, font, size)
    d, w = text_path(s, font, size, tracking)
    if anchor == "middle": x -= w / 2
    elif anchor == "end":  x -= w
    o = f' opacity="{opacity}"' if opacity else ""
    return f'<g fill="{fill}"{o} transform="translate({x:.1f},{y:.1f})">{d}</g>', w

def tw(s, size, font=BOLD, tracking=0.04):
    return text_path(s, font, size, tracking)[1]

# ---------------------------------------------------------------- Szenen
# Statt Platzhalterkaesten: prozedurale Kulissen, damit die Vorlagen zeigen,
# wie sie mit echtem Bildmaterial wirken.
SCENES = {
    "sunset": [("#F5C86B", 0), ("#E39A42", .34), ("#7A5B33", .52),
               ("#22301F", .70), ("#141D14", 1)],
    "alpine": [("#8FC4E8", 0), ("#BBD9EC", .38), ("#5F7F63", .58), ("#3C5A45", .78),
               ("#243A2C", 1)],
    "night":  [("#0B1834", 0), ("#132749", .40), ("#1B3358", .62), ("#0A1426", 1)],
    "forest": [("#93C3E0", 0), ("#A8CDDF", .30), ("#4E7A4A", .48), ("#335C36", .74),
               ("#1E3A22", 1)],
}

def ridge(w, h, base, col, amp=0.045, seed=3, steps=9):
    """Gelaendekante als Silhouette -- damit die Kulisse nicht als Farbfleck liest."""
    import random
    r = random.Random(seed)
    pts = []
    for i in range(steps + 1):
        x = w * i / steps
        y = base * h + (r.random() - .5) * amp * h * 2
        pts.append((x, y))
    d = f"M0,{h} L0,{pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        mx = (x0 + x1) / 2
        d += f" Q{mx:.1f},{y0:.1f} {x1:.1f},{y1:.1f}"
    d += f" L{w},{h} Z"
    return f'<path d="{d}" fill="{col}"/>'

def scene(w, h, kind="sunset", ident=None, sun=True):
    ident = ident or uid("sc")
    stops = "".join(f'<stop offset="{o*100:.0f}%" stop-color="{c}"/>' for c, o in SCENES[kind])
    extra = ""
    if sun and kind in ("sunset", "forest"):
        extra = (f'<radialGradient id="{ident}s"><stop offset="0%" stop-color="#FFF6DC" '
                 f'stop-opacity=".95"/><stop offset="100%" stop-color="#FFF6DC" '
                 f'stop-opacity="0"/></radialGradient>')
    body = (f'<defs><linearGradient id="{ident}" x1="0" y1="0" x2="0" y2="1">{stops}'
            f'</linearGradient>{extra}</defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{ident})"/>')
    if extra:
        body += (f'<ellipse cx="{w*.62:.0f}" cy="{h*.34:.0f}" rx="{w*.42:.0f}" '
                 f'ry="{h*.22:.0f}" fill="url(#{ident}s)"/>')
    RIDGES = {
        "sunset": [(.52, "#3A3524", .03, 5), (.60, "#221F16", .04, 9)],
        "forest": [(.44, "#40684A", .028, 4), (.54, "#2C4A34", .035, 8)],
        "alpine": [(.40, "#7C93A8", .05, 2), (.52, "#4A6455", .04, 6),
                   (.63, "#2E4536", .03, 11)],
        "night":  [(.56, "#101E38", .035, 7), (.66, "#0A1424", .03, 12)],
    }
    for base, col, amp, seed in RIDGES.get(kind, []):
        body += ridge(w, h, base, col, amp, seed)
    return body

def shade(w, h, top=0.0, bottom=0.72, ident=None, col="#00081C"):
    """Verlauf von unten, damit Text auf jedem Foto lesbar bleibt."""
    ident = ident or uid("sh")
    return (f'<defs><linearGradient id="{ident}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{col}" stop-opacity="{top}"/>'
            f'<stop offset="55%" stop-color="{col}" stop-opacity="{bottom*.45:.2f}"/>'
            f'<stop offset="100%" stop-color="{col}" stop-opacity="{bottom}"/>'
            f'</linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{ident})"/>')

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{body}</svg>')

def badge(size, x, y, key="n1_kante"):
    """Marke einsetzen. Die clipPath-IDs werden pro Aufruf umbenannt, sonst gibt es
    doppelte IDs, sobald eine Vorlage die Marke mehrfach zeigt."""
    import re
    s = _inner(MARKS[key])
    suf = uid("b")
    for m in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{m}"', f'id="{m}{suf}"').replace(f'url(#{m})', f'url(#{m}{suf})')
    return f'<g transform="translate({x},{y}) scale({size/512:.5f})">{s}</g>'

# ---------------------------------------------------------------- Die Kante
# Derselbe Winkel wie im Zeichen. Er ist der Grund, warum ein Beitrag ohne Logo
# als VAR-Beitrag zu erkennen ist: die Kante laeuft in jedem Format randabfallend
# durch und traegt darunter den Absender -- genau wie im Zeichen, wo sie den
# Hubschrauber traegt und die Wortmarke darunter steht.
from mark import ANG as KANTE_WINKEL

def _gekippt(w, y, inhalt):
    """Inhalt in das Bezugssystem der gekippten Kante setzen.

    `y` ist die Hoehe der Kantenoberkante **in der Bildmitte**. Zu den Raendern
    laeuft sie auseinander: bei 1080 Breite um rund 31 Einheiten je Seite.
    """
    return (f'<g transform="translate({w/2:.1f},{y:.1f}) '
            f'rotate({KANTE_WINKEL:.4f})">{inhalt}</g>')


def kante_luft(w, zugabe=14):
    """Wie weit Text ueber der Kante bleiben muss.

    Die Kante steigt nach rechts an: ueber die Bildbreite um w*tan(3,27 Grad),
    also die Haelfte davon gegenueber der Bildmitte. Wer nur zur Mittelhoehe
    misst, laesst den Text auf der rechten Seite in die Kante laufen.
    """
    import math
    return w * math.tan(math.radians(abs(KANTE_WINKEL))) / 2 + zugabe


def kante(w, y, h, col=GALLIANO):
    """Randabfallender Balken im Markenwinkel. `y` gilt in der Bildmitte."""
    L = w * 2.6
    return _gekippt(w, y, f'<rect x="{-L/2:.0f}" y="0" width="{L:.0f}" '
                          f'height="{h}" fill="{col}"/>')


def feld(w, h_bild, y, col=STRATOS):
    """Die Flaeche unter der Kante, bis ueber den Bildrand hinaus."""
    L = w * 2.6
    return _gekippt(w, y, f'<rect x="{-L/2:.0f}" y="0" width="{L:.0f}" '
                          f'height="{h_bild*2:.0f}" fill="{col}"/>')


def absenderleiste(w, y, h, badge_size=None, url="VIRTUALAIRRESCUE.COM", right=None,
                   col=STRATOS, kante_col=GALLIANO, ink=IVORY):
    """Der wiederkehrende Fuss: gekippte Kante, darunter Flaeche mit Marke und URL.

    `y` ist die Oberkante der Kante in der Bildmitte, `h` die Hoehe der Flaeche
    darunter -- ebenfalls in der Bildmitte gemessen. Alles steht im Bezugssystem
    der Kante, laeuft also parallel zu ihr. Das ist der Punkt: im Zeichen steht
    die Wortmarke ebenfalls parallel unter der Kante, nicht waagerecht.
    """
    ks = max(3, int(h * 0.075))
    bs = badge_size or int(h * 0.62)
    pad = int(h * 0.20)
    tx = pad + bs + h * 0.24
    size = h * 0.185
    gap = h * 0.36
    L = w * 2.6
    if right:
        for _ in range(20):
            if tx + tw(url, size, BOLD, .16) + gap + tw(right, size, BOLD, .16) <= w - pad:
                break
            size *= 0.94
    # Die Flaeche laeuft weit ueber den Bildrand hinaus. Mit einem Vielfachen von
    # `h` reichte sie bei hohen Formaten nicht bis unten -- dort steht die Kante
    # weit oberhalb der Bildmitte, und darunter kam wieder das Foto zum Vorschein.
    innen = [f'<rect x="{-L/2:.0f}" y="0" width="{L:.0f}" height="{L:.0f}" fill="{col}"/>',
             f'<rect x="{-L/2:.0f}" y="{-ks}" width="{L:.0f}" height="{ks}" fill="{kante_col}"/>']
    # Die Inhalte sitzen relativ zum linken Bildrand -- der liegt bei -w/2.
    lx = -w / 2
    innen.append(badge(bs, lx + pad, (h - bs) / 2))
    t, _ = txt(url, size, ink, lx + tx, h * 0.5 + size * 0.36, BOLD, 0.16)
    innen.append(t)
    if right:
        t2, _ = txt(right, size, kante_col, lx + w - pad, h * 0.5 + size * 0.36,
                    BOLD, 0.16, "end")
        innen.append(t2)
    return _gekippt(w, y, "".join(innen))


def scrim(w, h, y, staerke=.88, anlauf=.55, col="#00081C"):
    """Abdunklung, die auf die Kante zulaeuft statt auf den Bildrand.

    `shade` lief bis zum unteren Bildrand aus. Sitzt die Kante aber deutlich
    darueber -- bei 9:16 fast in der Bildmitte --, ist der Text an seiner
    Standposition erst halb abgedeckt und faellt auf hellen Bildern auseinander.
    Dieser Verlauf erreicht seine volle Staerke genau an der Kante; darunter ist
    die Flaeche ohnehin deckend.

    `anlauf` ist der Anteil der Strecke von oben bis zur Kante, ab dem er einsetzt.
    """
    ident = uid("sr")
    y = max(y, 1)
    a = min(max(anlauf, 0.0), 0.98)
    return (f'<defs><linearGradient id="{ident}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="0" y2="{y:.0f}">'
            f'<stop offset="0%" stop-color="{col}" stop-opacity="0"/>'
            f'<stop offset="{a*100:.0f}%" stop-color="{col}" stop-opacity="{staerke*0.18:.2f}"/>'
            f'<stop offset="100%" stop-color="{col}" stop-opacity="{staerke}"/>'
            f'</linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{ident})"/>')


def foto(w, h, datei, x=0, y=0, bw=None, bh=None, cid=None):
    """Ein echtes Bild einsetzen, formatfuellend beschnitten.

    Die Vorlagen im Repo tragen prozedurale Kulissen als Platzhalter; diese
    Funktion nimmt stattdessen eine Datei, damit sich eine Vorlage mit echtem
    Material gegenpruefen laesst.
    """
    import base64, mimetypes, io
    bw = bw or w; bh = bh or h
    cid = cid or uid("f")
    mt = mimetypes.guess_type(datei)[0] or "image/png"
    d = base64.b64encode(io.open(datei, "rb").read()).decode()
    return (f'<defs><clipPath id="{cid}"><rect x="{x}" y="{y}" width="{bw}" '
            f'height="{bh}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><image x="{x}" y="{y}" width="{bw}" '
            f'height="{bh}" preserveAspectRatio="xMidYMid slice" '
            f'href="data:{mt};base64,{d}"/></g>')

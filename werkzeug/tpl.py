# -*- coding: utf-8 -*-
"""VAR-Vorlagensystem: Social Media, Video, Veranstaltung.

Durchgaengiges Element in allen Formaten ist die Kante -- derselbe Balken, auf dem
im Zeichen der Hubschrauber steht. Sie traegt in jeder Vorlage die Absenderzeile.
"""
import math
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
def txt(s, size, fill, x=0, y=0, font=BOLD, tracking=0.04, anchor="start", opacity=None):
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
def kante(w, y, h, col=GALLIANO):
    return f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="{col}"/>'

def absenderleiste(w, y, h, badge_size=None, url="VIRTUALAIRRESCUE.COM", right=None):
    """Der wiederkehrende Fuss: Kante, Marke, URL -- rechts optional ein Rubrikwort.

    Die Schriftgroesse wird so weit verkleinert, dass URL und Rubrik sich nie beruehren.
    """
    bs = badge_size or int(h * 0.72)
    pad = int(h * 0.16)
    tx = pad + bs + h * 0.22
    size = h * 0.20
    gap = h * 0.36
    if right:
        for _ in range(16):
            if tx + tw(url, size, BOLD, .16) + gap + tw(right, size, BOLD, .16) <= w - pad:
                break
            size *= 0.94
    parts = [f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="{STRATOS}"/>',
             kante(w, y, max(3, int(h * 0.055)))]
    parts.append(badge(bs, pad, y + (h - bs) / 2 + h * 0.03))
    t, _ = txt(url, size, IVORY, tx, y + h * 0.60, BOLD, 0.16)
    parts.append(t)
    if right:
        t2, _ = txt(right, size, GALLIANO, w - pad, y + h * 0.60, BOLD, 0.16, "end")
        parts.append(t2)
    return "".join(parts)

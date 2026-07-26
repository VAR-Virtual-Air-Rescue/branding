# -*- coding: utf-8 -*-
"""Kartendarstellung nach dem Vorbild von RescueTrack.

Keine leuchtenden Kurven. Ein ruhiger, dunkler Grundriss mit Strassennetz,
Fahrzeuge als farbige Beschriftungsfahnen mit Statusziffer, Flugwege als duenne
durchgezogene Linien wie bei ADS-B-Karten.
"""
import math, random

# Kartenfarben -- entnommen der Anmutung von RescueTrack, nicht der Marke
LAND   = "#1E2A22"
LAND2  = "#243026"
WATER  = "#16283A"
ROAD   = "#4A5350"
ROAD2  = "#333B38"
AUTOB  = "#6B7470"
BORDER = "#2FA3A0"
LABEL  = "#8A9490"
TRACK  = "#D08A2C"     # gedecktes Bernstein statt Neonblau

# Statusfarben wie im Leitstellenbetrieb
ST = {1: "#2E7D46", 2: "#2E7D46", 3: "#B3312C", 4: "#B3312C",
      7: "#B3312C", 8: "#8A7A1E", 6: "#4A5058"}


def _roads(w, h, seed=7):
    """Ruhiges Strassennetz: weiche Bogen statt Zickzack, wenige starke Achsen."""
    r = random.Random(seed)

    def curve(x, y, n, step, jitter):
        d = f"M{x:.0f},{y:.0f}"
        ang = r.uniform(0, 6.283)
        for _ in range(n):
            ang += r.uniform(-jitter, jitter)
            nx = x + math.cos(ang) * step
            ny = y + math.sin(ang) * step
            d += f" Q{x + math.cos(ang) * step * .5:.0f},{y + math.sin(ang) * step * .5:.0f} {nx:.0f},{ny:.0f}"
            x, y = nx, ny
        return d

    out = []
    for _ in range(20):
        out.append(f'<path d="{curve(r.uniform(0,w), r.uniform(0,h), 5, min(w,h)*.13, .55)}" '
                   f'fill="none" stroke="{ROAD2}" stroke-width="1" opacity=".55"/>')
    for _ in range(5):
        out.append(f'<path d="{curve(r.uniform(0,w), r.uniform(0,h), 6, min(w,h)*.20, .32)}" '
                   f'fill="none" stroke="{AUTOB}" stroke-width="1.7" opacity=".38"/>')
    return "".join(out)

def _patches(w, h, seed=3):
    r = random.Random(seed)
    out = []
    for _ in range(16):
        cx, cy = r.uniform(0, w), r.uniform(0, h)
        rx, ry = r.uniform(w * .05, w * .16), r.uniform(h * .06, h * .18)
        out.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                   f'fill="{LAND2}" opacity=".8"/>')
    for _ in range(3):
        x, y = r.uniform(0, w), r.uniform(0, h)
        d = f"M{x:.0f},{y:.0f}"
        for _ in range(6):
            x += r.uniform(-w * .18, w * .18); y += r.uniform(0, h * .2)
            d += f" L{x:.0f},{y:.0f}"
        out.append(f'<path d="{d}" fill="none" stroke="{WATER}" stroke-width="2.4"/>')
    return "".join(out)


def flag(x, y, status, name, side="r", scale=1.0):
    """Fahrzeugfahne: Statusziffer im dunklen Kasten, daneben der Funkrufname."""
    col = ST.get(status, ST[6])
    fs = 11 * scale
    padx = 7 * scale
    numw = 17 * scale
    txw = len(name) * fs * 0.62 + padx * 2
    hgt = 17 * scale
    ox = x + 9 * scale if side == "r" else x - (numw + txw) - 9 * scale
    oy = y - hgt / 2
    return (f'<g font-family="monospace" font-size="{fs:.1f}">'
            f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{numw+txw:.1f}" height="{hgt:.1f}" '
            f'fill="{col}"/>'
            f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{numw:.1f}" height="{hgt:.1f}" '
            f'fill="#000" opacity=".26"/>'
            f'<text x="{ox+numw/2:.1f}" y="{oy+hgt*0.72:.1f}" fill="#FFF" '
            f'text-anchor="middle" font-weight="bold">{status}</text>'
            f'<text x="{ox+numw+padx:.1f}" y="{oy+hgt*0.72:.1f}" fill="#FFF">{name}</text>'
            f'</g>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.6*scale:.1f}" fill="#FFF"/>')


def station(x, y, label=None, scale=1.0):
    s = 5 * scale
    out = (f'<path d="M{x-s:.1f},{y:.1f} H{x+s:.1f} M{x:.1f},{y-s:.1f} V{y+s:.1f}" '
           f'stroke="{BORDER}" stroke-width="{1.6*scale:.1f}"/>')
    if label:
        out += (f'<text x="{x:.1f}" y="{y-s-4*scale:.1f}" fill="{BORDER}" '
                f'font-family="monospace" font-size="{9*scale:.1f}" text-anchor="middle" '
                f'letter-spacing="1">{label}</text>')
    return out


def incident(x, y, scale=1.0):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9*scale:.1f}" fill="none" '
            f'stroke="#D93B34" stroke-width="{2*scale:.1f}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.4*scale:.1f}" fill="#D93B34"/>')


def track(pts, dash=False):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.0f},{y:.0f}" for i, (x, y) in enumerate(pts))
    da = ' stroke-dasharray="5 4"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{TRACK}" stroke-width="1.6" '
            f'stroke-linejoin="round"{da}/>')


def heli_icon(x, y, ang, scale=1.0):
    s = scale
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.0f})">'
            f'<path d="M{7*s:.1f},0 L{-5*s:.1f},{3.6*s:.1f} L{-5*s:.1f},{-3.6*s:.1f} Z" '
            f'fill="#FFF"/>'
            f'<line x1="{-9*s:.1f}" y1="0" x2="{9*s:.1f}" y2="0" stroke="#FFF" '
            f'stroke-width="{0.9*s:.1f}" opacity=".7" '
            f'transform="rotate(38)"/></g>')


def basemap(w, h, seed=7):
    return (f'<rect width="{w}" height="{h}" fill="{LAND}"/>'
            + _patches(w, h, seed) + _roads(w, h, seed))


def svg(w, h, body, slice_=True):
    par = ' preserveAspectRatio="xMidYMid slice"' if slice_ else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{par}>'
            f'{body}</svg>')

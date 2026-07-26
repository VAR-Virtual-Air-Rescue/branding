# -*- coding: utf-8 -*-
"""Setzt Text in Uniform und liefert reine SVG-Pfaddaten -> keine Font-Abhaengigkeit
in den ausgelieferten SVGs und keine Font-Einbettung im Web."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

_cache = {}
def _font(path):
    if path not in _cache:
        f = TTFont(path)
        _cache[path] = (f, f.getGlyphSet(), f["head"].unitsPerEm, f.getBestCmap(), f["hmtx"])
    return _cache[path]

def text_path(s, font="fonts/Uniform.ttf", size=100, tracking=0.0):
    """tracking in em. Gibt (d, breite, hoehe_em) zurueck; Baseline liegt auf y=0."""
    f, gs, upm, cmap, hmtx = _font(font)
    sc = size / upm
    x = 0.0
    out = []
    for ch in s:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.35 + tracking * size
            continue
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
        gs[gname].draw(pen)
        d = pen.getCommands()
        if d:
            out.append(f'<path transform="translate({x:.2f},0) scale({sc:.6f},{-sc:.6f})" d="{d}"/>')
        x += hmtx[gname][0] * sc + tracking * size
    return "".join(out), x - tracking * size

if __name__ == "__main__":
    d, w = text_path("VIRTUAL AIR RESCUE", size=100, tracking=0.05)
    print("Breite:", round(w,1), "Zeichen:", len(d))

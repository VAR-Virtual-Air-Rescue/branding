# -*- coding: utf-8 -*-
"""Setzt die Brand-Preview-Seite zusammen: HTML-Template + echte SVG-Quellen."""
import re, sys, io
from text2path import text_path

SVG = {}
import os
for f in os.listdir("out"):
    if f.endswith(".svg"):
        SVG[f[:-4]] = open("out/" + f, encoding="utf-8").read()

_ctr = [0]

def inject(name, cls="", extra=""):
    """SVG einbetten, IDs eindeutig machen, Groesse per CSS steuerbar."""
    _ctr[0] += 1
    s = SVG[name]
    for m in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{m}"', f'id="{m}_{_ctr[0]}"')
        s = s.replace(f'url(#{m})', f'url(#{m}_{_ctr[0]})')
    s = re.sub(r'<svg ', f'<svg class="{cls}" {extra} ', s, count=1)
    s = re.sub(r'\swidth="\d+"\s+height="\d+"', ' ', s, count=1)
    return s

def wordmark(text, size, fill, tracking=0.045, font="fonts/Uniform Bold.ttf", cls=""):
    d, w = text_path(text, font, size, tracking)
    h = size * 1.05
    return (f'<svg class="{cls}" viewBox="0 -{size*0.78:.1f} {w:.1f} {h:.1f}" '
            f'fill="{fill}" role="img" aria-label="{text}">{d}</svg>')

tpl = open("page.html", encoding="utf-8").read()

def repl(m):
    kind, arg = m.group(1), m.group(2)
    if kind == "SVG":
        parts = arg.split("|")
        return inject(parts[0], parts[1] if len(parts) > 1 else "")
    if kind == "WORD":
        p = arg.split("|")
        return wordmark(p[0], float(p[1]), p[2], float(p[3]) if len(p) > 3 else 0.045,
                        p[4] if len(p) > 4 else "fonts/Uniform Bold.ttf",
                        p[5] if len(p) > 5 else "")
    raise KeyError(kind)

out = re.sub(r'\{\{(SVG|WORD):([^}]+)\}\}', repl, tpl)

# Alles ausserhalb von ASCII als numerische Entity ausgeben. Die Seite wird in einen
# fremden <head> eingehaengt; so ist sie unabhaengig davon, welches Charset dort steht.
out = "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in out)

open("../var-brand.html", "w", encoding="ascii").write(out)
print("geschrieben:", len(out), "Zeichen ->", os.path.abspath("../var-brand.html"))

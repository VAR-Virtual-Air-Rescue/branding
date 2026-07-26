# -*- coding: utf-8 -*-
"""Baut eine HTML-Seite aus Vorlage + echten SVG-Quellen.

  {{SVG:name|klasse}}      SVG aus neu/ oder tpl/ einbetten (IDs werden eindeutig)
  {{WORD:Text|Groesse|Farbe|Tracking|Font|Klasse}}   Schriftzug in Uniform als Pfade
"""
import re, os, sys
from text2path import text_path

STORE = {}
for d in ("neu", "tpl"):
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".svg"):
                STORE[f[:-4]] = open(os.path.join(d, f), encoding="utf-8").read()

_n = [0]

def inject(name, cls=""):
    _n[0] += 1
    s = STORE[name]
    for m in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{m}"', f'id="{m}_{_n[0]}"').replace(f'url(#{m})', f'url(#{m}_{_n[0]})')
    s = re.sub(r'<svg ', f'<svg class="{cls}" ', s, count=1)
    s = re.sub(r'\swidth="[\d.]+"\s+height="[\d.]+"', ' ', s, count=1)
    return s

def wordmark(text, size, fill, tracking=0.045, font="fonts/Uniform Bold.ttf", cls=""):
    d, w = text_path(text, font, size, tracking)
    return (f'<svg class="{cls}" viewBox="0 -{size*0.78:.1f} {w:.1f} {size*1.05:.1f}" '
            f'fill="{fill}" role="img" aria-label="{text}">{d}</svg>')

def build(tpl_path, out_path):
    tpl = open(tpl_path, encoding="utf-8").read()

    def repl(m):
        kind, arg = m.group(1), m.group(2)
        p = arg.split("|")
        if kind == "SVG":
            return inject(p[0], p[1] if len(p) > 1 else "")
        return wordmark(p[0], float(p[1]), p[2],
                        float(p[3]) if len(p) > 3 else 0.045,
                        p[4] if len(p) > 4 else "fonts/Uniform Bold.ttf",
                        p[5] if len(p) > 5 else "")

    out = re.sub(r'\{\{(SVG|WORD):([^}]+)\}\}', repl, tpl)
    out = "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in out)
    open(out_path, "w", encoding="ascii").write(out)

    # Pruefungen
    import collections
    ids = re.findall(r'\sid="([^"]+)"', out)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    refs = set(re.findall(r'url\(#([^)]+)\)', out))
    bad = [t for t in ("div", "section", "svg", "table", "ol", "ul", "li", "p",
                       "header", "footer", "main", "style", "figure", "script")
           if len(re.findall(rf'<{t}[\s>]', out)) != len(re.findall(rf'</{t}>', out))]
    print(f"{out_path}: {round(len(out.encode())/1024)} KB | Platzhalter: "
          f"{len(re.findall(r'\{\{', out))} | doppelte IDs: {len(dup)} | "
          f"tote Refs: {sorted(refs - set(ids)) or 0} | unbalanciert: {bad or 0}")

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])

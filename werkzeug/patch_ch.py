# -*- coding: utf-8 -*-
"""Schweizer Fassung: Bergkette mit Matterhorn im oberen Feld, Flagge in der
Silhouette. Das untere Feld bleibt Stratos wie in der Grundfassung."""
p = "editions.py"
s = open(p, encoding="utf-8").read()

a = s.index("# Kreuz im unteren Feld")
b = s.index("# 24-Stunden-Event")

NEU = '''# Schweiz -- Bergkette mit Matterhorn, die Flagge steckt in der Silhouette
BERGE = (
    # hintere Kette, blasser
    "M-20,300 L40,214 L86,246 L134,180 L182,238 L228,196 L268,242 L312,188 "
    "L352,236 L398,192 L446,244 L500,206 L540,300 Z"
)
# Das Matterhorn: steile Pyramide, Gipfel nach rechts gekippt
MATTERHORN = (
    "M96,306 L188,120 L206,96 L214,110 L206,132 L262,214 L318,306 Z"
)

def schweiz():
    """Rote Berge, weisses Kreuz darin -- alles auf die Silhouette beschnitten."""
    cid = uid("chm")
    kreuz = (f'<g transform="translate(202,206)">'
             f'<rect x="-13" y="-40" width="26" height="80" fill="#FFFFFC"/>'
             f'<rect x="-40" y="-13" width="80" height="26" fill="#FFFFFC"/></g>')
    return (
        # hintere Kette in gedecktem Rot, damit die Tiefe stimmt
        f'<path d="{BERGE}" fill="#8E1F17" opacity=".85"/>'
        # Matterhorn mit Flagge darin
        f'<defs><clipPath id="{cid}"><path d="{MATTERHORN}"/></clipPath></defs>'
        f'<path d="{MATTERHORN}" fill="#DA291C"/>'
        f'<g clip-path="url(#{cid})">{kreuz}</g>'
        # Schneefeld auf der Nordflanke, ein Hauch
        f'<path d="M206,96 L214,110 L206,132 L232,170 L206,178 L188,120 Z" '
        f'fill="#FFFFFC" opacity=".30"/>')

E["pb_ch"] = edition(flaeche(STRATOS), IVORY, IVORY, obenmuster=schweiz())

'''
s = s[:a] + NEU + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("Schweiz neu")

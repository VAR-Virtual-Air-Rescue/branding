# -*- coding: utf-8 -*-
"""Wortmarke neu abnehmen -- aus der vollstaendigen Zeichnung.

Die Fassung, die bis 28.08.2026 in `traced.json` stand, war **schon beschnitten**:
sie wurde von einer Grafik abgenommen, in der die Wortmarke bereits im Badge-Kreis
sass. Fuss des V links und Bein des R rechts fehlten deshalb, jeweils entlang eines
Kreisbogens. Zusammen rund 7 Prozent der Flaeche.

Das hat lange niemand gesehen, weil das Zeichen die Wortmarke ohnehin konzentrisch
beschneidet -- der fehlende Teil lag genau dort, wo der Beschnitt sowieso zugreift.
Sichtbar wurde es erst, als die Kante in die Kreismitte wanderte und die Wortmarke
Platz bekam: dann kappte der alte Beschnitt zum zweiten Mal.

Quelle ist jetzt `quellen/var_wortmarke.png`, freigestellt und unbeschnitten.
Aufruf aus `brand/werkzeug` heraus:

    python trace_var.py

Schreibt den neuen `var`-Zweig in `traced.json`; `heli` bleibt unberuehrt.
"""
import json, numpy as np, potrace
from PIL import Image
from trace_lib import to_path

QUELLE = "quellen/var_wortmarke.png"
ZIEL_W = 1000.0

# Freigestellt: alles, was nicht durchsichtig ist, gehoert zur Wortmarke.
im = Image.open(QUELLE).convert("RGBA")
a = np.array(im).astype(int)
m = a[..., 3] > 128

ys, xs = np.where(m)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
sc = ZIEL_W / (x1 - x0 + 1)
hoehe = round((y1 - y0 + 1) * sc, 2)

# Dieselben Stufen wie im urspruenglichen Lauf (trace.py), damit die Zeichnung
# gleich charakterisiert bleibt: `fein` fuer grosse Groessen, `mittel` im Einsatz.
STUFEN = {"fein": (1.0, 0.2, 30), "mittel": (1.2, 1.0, 200)}

var = {"bbox": [int(x0), int(y0), int(x1), int(y1)],
       "w": round((x1 - x0 + 1) * sc, 2), "h": hoehe, "levels": {},
       "quelle": QUELLE}

# potrace bekommt hier die Gegenmaske -- genau wie im urspruenglichen `trace.py`.
# Mit der Maske selbst kommt das Negativ heraus.
for lab, (alphamax, opttol, turdsize) in STUFEN.items():
    p = potrace.Bitmap(~m).trace(turdsize=turdsize, alphamax=alphamax,
                                 opticurve=True, opttolerance=opttol)
    d, n = to_path(p, x0, y0, sc)
    var["levels"][lab] = {"d": d, "contours": n, "chars": len(d)}
    print("  %-7s %2d Konturen, %5d Zeichen" % (lab, n, len(d)))

T = json.load(open("traced.json"))
alt = T["var"]
T["var"] = var
json.dump(T, open("traced.json", "w"))
print("\nvorher  w %.2f  h %.2f  (Verhaeltnis %.4f)"
      % (alt["w"], alt["h"], alt["w"] / alt["h"]))
print("jetzt   w %.2f  h %.2f  (Verhaeltnis %.4f)"
      % (var["w"], var["h"], var["w"] / var["h"]))

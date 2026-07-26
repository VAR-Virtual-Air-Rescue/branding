# -*- coding: utf-8 -*-
"""Einsatz-Tagebuch: sechs Overlays fuer ein Reel.

Je Schritt ein Fenster fuer Foto oder Video. Statusziffer und Farbe stammen aus
FMS_STATUS_COLORS des Monorepos, damit das Reel dieselbe Sprache spricht wie die
Leitstelle.
"""
import os
from tpl import svg, scene, shade, badge, txt, tw, uid, STRATOS, GALLIANO, IVORY, BOLD, REG, BLK

FMS = {"1":"rgb(10,134,25)","2":"rgb(10,134,25)","3":"rgb(140,10,10)",
       "4":"rgb(140,10,10)","7":"rgb(140,10,10)","8":"rgb(186,105,0)"}

SCHRITTE = [
    ("3", "ALARMIERUNG",  "VU KLEMMT · B27",        "18:42", "night"),
    ("3", "AUSRÜCKEN",     "ABFLUG STATION STUTTGART",  "18:44", "sunset"),
    ("4", "ANKOMMEN",     "LANDUNG AM EINSATZORT",     "18:53", "forest"),
    ("7", "ABFLUG KLINIK","PATIENT AN BORD",           "19:11", "alpine"),
    ("8", "ANKUNFT KLINIK","DACHLANDEPLATZ MARIENHOSPITAL","19:26","night"),
    ("1", "EINSATZKLAR",  "FREI ÜBER FUNK",       "19:38", "sunset"),
]

W, H = 1080, 1920
FUSS = 470          # Hoehe des Textbereichs unten
T = {}

def overlay(i, st, titel, unten, zeit, kind, leer=False):
    col = FMS[st]
    b = []
    if leer:
        b.append(f'<rect width="{W}" height="{H}" fill="#141C31"/>')
        b += [f'<rect x="{x}" y="0" width="26" height="{H}" fill="#1B2540"/>'
              for x in range(0, W, 52)]
        t,_ = txt("FOTO ODER VIDEO", 34, IVORY, W/2, H*0.34, BOLD, .18, "middle", ".5")
        b.append(t)
        t,_ = txt("HOCHFORMAT 9:16", 24, IVORY, W/2, H*0.34+52, BOLD, .18, "middle", ".3")
        b.append(t)
    else:
        b.append(scene(W, H, kind))
    # Abdunklung nur im Fussbereich, damit das Bild oben frei bleibt
    b.append(f'<defs><linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="#00081C" stop-opacity="0"/>'
             f'<stop offset="100%" stop-color="#00081C" stop-opacity=".93"/>'
             f'</linearGradient></defs>'
             f'<rect x="0" y="{H-FUSS-260}" width="{W}" height="{FUSS+260}" fill="url(#g{i})"/>')

    # Kopfzeile: Marke + Einsatznummer
    b.append(badge(104, 56, 210))
    t,_ = txt("VIRTUAL AIR RESCUE", 26, IVORY, 176, 272, BOLD, .16); b.append(t)
    t,_ = txt("EINSATZ-TAGEBUCH · CHRISTOPH 51", 22, GALLIANO, 176, 308, BOLD, .14)
    b.append(t)

    # Fortschrittsleiste: sechs Punkte, der aktuelle gefuellt
    y0 = H - FUSS - 46
    seg = (W - 112) / (len(SCHRITTE) - 1)
    b.append(f'<rect x="56" y="{y0-1}" width="{W-112}" height="2" fill="{IVORY}" opacity=".22"/>')
    for k in range(len(SCHRITTE)):
        x = 56 + seg * k
        aktiv = k == i
        fertig = k < i
        r = 9 if aktiv else 5
        f = col if aktiv else (GALLIANO if fertig else "rgba(255,255,252,.28)")
        b.append(f'<circle cx="{x:.0f}" cy="{y0}" r="{r}" fill="{f}"/>')
        if aktiv:
            b.append(f'<circle cx="{x:.0f}" cy="{y0}" r="{r+7}" fill="none" '
                     f'stroke="{col}" stroke-width="2" opacity=".55"/>')

    # Statuskachel
    ky = H - FUSS + 34
    b.append(f'<rect x="56" y="{ky}" width="112" height="112" fill="{col}"/>')
    t,_ = txt(st, 68, IVORY, 112, ky+82, BLK, .01, "middle"); b.append(t)
    t,_ = txt("STATUS", 18, IVORY, 112, ky+134, BOLD, .2, "middle", ".6"); b.append(t)

    # Schritt und Titel
    t,_ = txt(f"SCHRITT {i+1} VON {len(SCHRITTE)}", 24, GALLIANO, 200, ky+34, BOLD, .18)
    b.append(t)
    t,_ = txt(titel, 76, IVORY, 200, ky+112, BLK, .01); b.append(t)
    b.append(f'<rect x="200" y="{ky+142}" width="150" height="5" fill="{GALLIANO}"/>')
    t,_ = txt(unten, 28, IVORY, 200, ky+196, BOLD, .06, opacity=".85"); b.append(t)

    # Uhrzeit rechts
    t,_ = txt(zeit, 44, IVORY, W-56, ky+82, BOLD, .04, "end"); b.append(t)
    t,_ = txt("UTC", 18, IVORY, W-56, ky+112, BOLD, .2, "end", ".5"); b.append(t)

    # Absenderkante ganz unten
    b.append(f'<rect x="0" y="{H-8}" width="{W}" height="8" fill="{GALLIANO}"/>')
    return svg(W, H, "".join(b))

for i, (st, titel, unten, zeit, kind) in enumerate(SCHRITTE):
    T[f"tb_{i+1}_{titel.lower().replace(' ','_').replace('ü','ue').replace('Ü','ue')}"] = \
        overlay(i, st, titel, unten, zeit, kind)
T["tb_leer"] = overlay(2, "4", "ANKOMMEN", "LANDUNG AM EINSATZORT", "18:53", "forest", leer=True)

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    for k, v in T.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"{len(T)} Overlays:", ", ".join(T))

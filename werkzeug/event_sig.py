# -*- coding: utf-8 -*-
"""Ein Banner je Anlass -- jedes mit eigenem Gesicht.

    python werkzeug/event_sig.py [--fotos <ordner>]

Der Unterschied zu `events.py`: dort waehlt man eine **Machart** (Depesche,
Bild, Plakat) und bekommt sie in Markenfarben. Hier gehoert zu jedem Anlass eine
**Signatur** -- Grundfarbe, Akzent, Untergrund, Titelsatz --, und die macht ihn
auf den ersten Blick unterscheidbar.

Was dabei nie wechselt, steht in `signatur.py`: die gekippte Kante, die
Absenderleiste mit Zeichen und Adresse, Uniform in Versalien. Drei Termine
untereinander im Kanal sehen dadurch verschieden aus und gehoeren trotzdem
sichtbar zusammen.

Die Gebietskarte aus `event_banner.py` laesst sich dazuschalten -- sie nimmt die
Akzentfarbe der Signatur an, statt immer Gold zu sein.
"""
import io, os, sys, glob, json

from tpl import (svg, scrim, badge, kante_luft, absenderleiste, foto, scene,
                 txt, tw, uid, KANTE_STAERKE, BOLD, REG, BLK, IVORY, STRATOS)
from events import fuss, zeile, passt
from signatur import (SIGNATUREN, Signatur, textur, titel, kontrast,
                      pruefe_signaturen)
from event_banner import gebietskarte

T = {}

_FOTOS = []
if "--fotos" in sys.argv:
    _FOTOS = sorted(glob.glob(os.path.join(sys.argv[sys.argv.index("--fotos") + 1], "*.jpg")))

FORMATE = [("discord_titel", 800, 320),
           ("discord_ankuendigung", 1200, 630),
           ("instagram", 1080, 1350)]


def banner(W, H, sig, kopf, kicker, angaben, rubrik,
           gebiet=None, bildanteil=0.0, seed=7):
    """Ein Event-Banner in der Signatur `sig`.

    `kopf`      eine oder zwei Zeilen Schlagzeile
    `kicker`    die kleine Zeile darueber
    `angaben`   Liste von Zeilen unter der Schlagzeile (Datum, Zeit, Ort)
    `gebiet`    Kuerzel aus gebiete.json, dann kommt die Karte dazu
    `bildanteil` 0 bis 1 -- wie viel der Flaeche ein Foto bekommt
    """
    foot = fuss(H)
    y = H - foot
    luft = kante_luft(W)
    px = W * .06
    hoch = H > W * 1.05

    b = [f'<rect width="{W}" height="{H}" fill="{sig.grund}"/>']

    # Untergrund zuerst -- er faerbt, er traegt nicht.
    b.append(textur(sig.untergrund, W, y, sig.akzent, seed))

    # Bild oder Karte in die rechte Haelfte (quer) beziehungsweise nach oben.
    inhalt_rechts = 0.0
    if gebiet:
        if hoch:
            kw, kh = W * .90, (y - luft) * .42
            kx, ky = W * .05, H * .05
        else:
            kw, kh = W * .42, (y - luft) * .78
            kx, ky = W * .55, (y - luft - kh) / 2
        karte, g = gebietskarte(gebiet, kw, kh, fuellung=sig.ink,
                                markerfarbe=sig.akzent, markerschrift=sig.grund)
        b.append(f'<g transform="translate({kx:.0f},{ky:.0f})">{karte}</g>')
        inhalt_rechts = 0.0 if hoch else .46
    elif bildanteil > 0:
        if hoch:
            bw, bh = W, (y - luft) * bildanteil
            bx, by = 0, 0
        else:
            bw, bh = W * bildanteil, y + luft
            bx, by = W - bw, 0
        datei = _FOTOS[0] if _FOTOS else None
        bild = (foto(bw, bh, datei, 0, 0, bw, bh) if datei
                else scene(int(bw), int(bh), "night"))
        cid = uid("bf")
        b.append(f'<defs><clipPath id="{cid}"><rect x="{bx:.0f}" y="{by:.0f}" '
                 f'width="{bw:.0f}" height="{bh:.0f}"/></clipPath></defs>'
                 f'<g clip-path="url(#{cid})"><g transform="translate({bx:.0f},{by:.0f})">'
                 f'{bild}</g></g>')
        if not hoch:
            # Verlauf vom Grund ins Bild, damit die Schrift links nicht auf einer
            # Kante endet.
            gid = uid("vl")
            b.append(f'<defs><linearGradient id="{gid}" x1="0" x2="1">'
                     f'<stop offset="0" stop-color="{sig.grund}"/>'
                     f'<stop offset="1" stop-color="{sig.grund}" stop-opacity="0"/>'
                     f'</linearGradient></defs>'
                     f'<rect x="{bx:.0f}" y="0" width="{bw*.55:.0f}" height="{H}" '
                     f'fill="url(#{gid})"/>')
            inhalt_rechts = bildanteil
        else:
            b.append(scrim(W, H, y))

    # --- Text -------------------------------------------------------------
    tb = (W - 2 * px) * (1 - inhalt_rechts) - (0 if hoch else W * .02)
    ks = passt(max(kopf, key=len), (W * .085 if hoch else H * .125), BLK, .01, tb)
    ag = max(15, (W * .026 if hoch else H * .034))
    kg = max(13, (W * .022 if hoch else H * .024))

    hoehe = ks * (1.06 * (len(kopf) - 1) + .78) + kg * 1.6 + len(angaben) * ag * 1.45
    oben = max(H * .13, (y - luft - hoehe) / 2 + kg)
    if gebiet and hoch:
        oben = H * .05 + (y - luft) * .42 + H * .075

    zeile(b, kicker, kg, sig.akzent, px, oben, BOLD, .18)
    kopf_svg, unterkante = titel(sig.satz, kopf, ks, sig, px, oben + kg * 1.6 + ks * .78, tb)
    b.append(kopf_svg)

    ay = unterkante + ag * 1.7
    for i, zl in enumerate(angaben):
        zeile(b, zl, ag if i == 0 else ag * .88,
              sig.ink if i == 0 else sig.akzent, px, ay + i * ag * 1.45,
              BOLD if i == 0 else REG, .04 if i == 0 else .02,
              # Die dritte Zeile ist der Zusatz, nicht das Kleingedruckte:
              # bei .75 auf einem ohnehin gedeckten Grund war sie kaum zu
              # lesen.
              op=None if i < 2 else ".88")

    # Die Leiste ist der feste Teil -- sie nimmt die Signatur nicht an.
    b.append(absenderleiste(W, y, foot, right=rubrik,
                            col=Signatur.LEISTE, kante_col=Signatur.LEISTE_AKZENT,
                            ink=Signatur.LEISTE_INK))
    return svg(W, H, "".join(b))


# =========================================================================
#  Die Anlaesse
# =========================================================================
ANLAESSE = [
    dict(schluessel="gebietsabend", sig="gebiet", gebiet="BW",
         kicker="BADEN-WÜRTTEMBERG", kopf=["ALLE STATIONEN", "IM LÄNDLE"],
         angaben=["19. APRIL 2026", "15:00 – 21:00 UTC", "10 Stationen besetzt"],
         rubrik="GEBIET"),
    dict(schluessel="overload", sig="overload",
         kicker="LEITSTELLENABEND", kopf=["VAR", "OVERLOAD"],
         angaben=["7. MÄRZ 2026", "19:00 UTC", "Mehrere Lagen gleichzeitig"],
         rubrik="REIHE"),
    dict(schluessel="nachtflug", sig="nachtflug", bild=.44,
         kicker="SECHS STUNDEN", kopf=["NACHTFLUG"],
         angaben=["21. NOVEMBER 2026", "20:00 – 02:00 UTC", "NVG empfohlen"],
         rubrik="REIHE"),
    dict(schluessel="leitstellenabend", sig="leitstelle",
         kicker="ALLE POSITIONEN BESETZT", kopf=["LEITSTELLE", "OFFEN"],
         angaben=["14. DEZEMBER 2026", "1100 ZULU · 1200 LOKAL", "Zuschauer erwünscht"],
         rubrik="OPS"),
    dict(schluessel="bergrettung", sig="berg", bild=.42,
         kicker="WINTERSAISON", kopf=["BERGRETTUNG"],
         angaben=["17. JANUAR 2027", "13:00 UTC", "Winde und Außenlandung"],
         rubrik="SPECIAL"),
    dict(schluessel="sternflug", sig="sternflug",
         kicker="EIN ZIEL, VIELE HERKÜNFTE", kopf=["STERNFLUG", "NACH EDDS"],
         angaben=["9. MAI 2026", "16:00 UTC", "Ankunft im Zeitfenster"],
         rubrik="SPECIAL"),
    dict(schluessel="24stunden", sig="24h",
         kicker="RUND UM DIE UHR", kopf=["24 STUNDEN", "LUFTRETTUNG"],
         angaben=["6. JUNI 2026, 06:00 UTC", "bis 7. JUNI, 06:00 UTC",
                  "Schichtübergabe alle vier Stunden"],
         rubrik="SPECIAL"),
    dict(schluessel="herbstnacht", sig="herbst",
         kicker="ZUR DUNKLEN JAHRESZEIT", kopf=["HERBST-", "NACHTSCHICHT"],
         angaben=["31. OKTOBER 2026", "19:00 UTC", "Kostüme im Cockpit erlaubt"],
         rubrik="SPECIAL"),
]

for f, W, H in FORMATE:
    for a in ANLAESSE:
        T[f"event_{a['schluessel']}_{f}"] = banner(
            W, H, SIGNATUREN[a["sig"]], a["kopf"], a["kicker"], a["angaben"],
            a["rubrik"], gebiet=a.get("gebiet"), bildanteil=a.get("bild", 0.0),
            seed=hash(a["schluessel"]) % 100)


if __name__ == "__main__":
    fehler = pruefe_signaturen()
    if fehler:
        raise SystemExit("Signaturen tragen nicht:\n  " + "\n  ".join(fehler))
    os.makedirs("tpl", exist_ok=True)
    for k, v in T.items():
        open(f"tpl/{k}.svg", "w", encoding="utf-8").write(v)
    from tpl import FEHLENDE
    if FEHLENDE:
        print("FEHLENDE ZEICHEN:", sorted(FEHLENDE))
    print(f"{len(T)} Banner fuer {len(ANLAESSE)} Anlaesse")

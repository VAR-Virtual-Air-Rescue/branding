# -*- coding: utf-8 -*-
"""Erzeugt alle VAR-Vorlagen.

Durchgehendes Element ist die **gekippte Kante** -- derselbe Balken im selben
Winkel wie im Zeichen. Sie laeuft in jedem Format randabfallend durch und traegt
darunter den Absender. Damit ist ein Beitrag auch dann als VAR-Beitrag zu
erkennen, wenn das Logo klein ist oder gar nicht im Bild steht: der Winkel ist
die Marke.

Der Aufbau wiederholt das Zeichen im Grossen -- oben das Bild wie der Himmel,
darunter die Kante, darunter die Flaeche mit dem Absender wie die Wortmarke.

Inhalte mit echten Begriffen aus der Leitstelle: Stichwort, Funkrufname, Station,
Status. Die Kulissen sind Platzhalter; mit `--fotos <ordner>` werden stattdessen
echte Bilder eingesetzt, um jede Vorlage mit Material gegenzupruefen.
"""
import os, sys, glob
from tpl import (svg, scene, shade, scrim, badge, kante, kante_luft, feld, absenderleiste,
                 KANTE_STAERKE,
                 foto, txt, tw, uid, STRATOS, GALLIANO, IVORY, SIGNAL, INK,
                 BOLD, REG, BLK, MARKS, _inner, KANTE_WINKEL)

T = {}

# --- Bildquelle -----------------------------------------------------------
_FOTOS = []
if "--fotos" in sys.argv:
    _ordner = sys.argv[sys.argv.index("--fotos") + 1]
    _FOTOS = sorted(glob.glob(os.path.join(_ordner, "*.jpg")))

_KULISSEN = ["sunset", "alpine", "forest", "night"]
_n = [0]


def bild(w, h, art=None, x=0, y=0, bw=None, bh=None):
    """Platzhalterkulisse -- oder ein echtes Foto, wenn eines vorliegt."""
    i = _n[0]; _n[0] += 1
    if _FOTOS:
        return foto(w, h, _FOTOS[i % len(_FOTOS)], x, y, bw or w, bh or h)
    art = art or _KULISSEN[i % len(_KULISSEN)]
    ident = uid("k")
    return (f'<defs><clipPath id="{ident}"><rect x="{x}" y="{y}" width="{bw or w}" '
            f'height="{bh or h}"/></clipPath></defs><g clip-path="url(#{ident})">'
            f'<g transform="translate({x},{y})">{scene(bw or w, bh or h, art)}</g></g>')


def zeile(b, s, size, fill, x, y, font=BOLD, tr=.04, anchor="start", op=None):
    t, w = txt(s, size, fill, x, y, font, tr, anchor, op)
    b.append(t)
    return w


def strich(b, x, y, w=150, h=4, col=GALLIANO):
    """Kurzer Akzentstrich -- im Markenwinkel, nicht waagerecht."""
    b.append(f'<g transform="translate({x},{y}) rotate({KANTE_WINKEL:.4f})">'
             f'<rect width="{w}" height="{h}" fill="{col}"/></g>')


def beitrag(W, H, foot, kopf, kicker=None, unter=None, rubrik=None,
            kopfgroesse=92, unten_frei=0, kopf2=None):
    """Das Grundmuster: Bild, Kante, Absender. Text steht auf der Kante.

    `unten_frei` haelt bei Hochformaten die Bedienflaeche der Plattform frei --
    Story 384, Reel und TikTok 672. Wer das gleichsetzt, verdeckt sich selbst.
    """
    y = H - unten_frei - foot
    luft = kante_luft(W)
    b = [bild(W, H), scrim(W, H, y)]
    oben = y - luft - 58
    if unter:
        oben -= 62
    if kopf2:
        oben -= kopfgroesse * 1.06
    if kicker:
        zeile(b, kicker, max(24, foot * .17), GALLIANO,
              W * .06, oben - kopfgroesse * 1.06 - 34, BOLD, .16)
    zeile(b, kopf, kopfgroesse, IVORY, W * .06, oben, BLK, .01)
    if kopf2:
        zeile(b, kopf2, kopfgroesse, GALLIANO, W * .06,
              oben + kopfgroesse * 1.06, BLK, .01)
    if unter:
        zeile(b, unter, max(26, foot * .18), IVORY, W * .06,
              y - luft, REG, .02, op=".85")
    b.append(absenderleiste(W, y, foot, right=rubrik))
    return svg(W, H, "".join(b))


# ==========================================================================
#  A  Beitrag mit Bild
# ==========================================================================
T["ig_4x5_foto"] = beitrag(1080, 1350, 190, "CHRISTOPH 22",
                           "VERLEGUNGSFLUG NACH KASSEL",
                           "Sonnenaufgang über dem Reinhardswald.",
                           "LUFTRETTUNG", 92)
T["ig_1x1_foto"] = beitrag(1080, 1080, 168, "WINDENRETTUNG",
                           "STATION ZÜRICH · HB-ZQM", None, None, 78)
T["x_1600x900"] = beitrag(1600, 900, 150, "24 STUNDEN, 7 EINSÄTZE",
                          "SCHICHTBERICHT · STATION HAMBURG", None,
                          "EINSATZRÜCKBLICK", 84)
T["fb_link_1200x630"] = beitrag(1200, 630, 124, "NEUE STATION IN BETRIEB",
                                "CHRISTOPH 51 · STUTTGART", None, None, 62)
T["yt_thumb_1280x720"] = beitrag(1280, 720, 118, "NACHTFLUG",
                                 None, None, "COCKPITVIDEO", 130,
                                 kopf2="IN DIE ALPEN")
T["discord_event_800x320"] = beitrag(800, 320, 78, "NACHTFLUG IN DIE ALPEN",
                                     "SAMSTAG 20:00 UTC · LSZS » LSZH", None,
                                     None, 46)

# ==========================================================================
#  B  Hochformat 9:16
# ==========================================================================
T["story_9x16"] = beitrag(1080, 1920, 200, "CHRISTOPH 12", "JETZT IM EINSATZ",
                          "Primäreinsatz · Status 3", "STORY", 104, 384)
T["reel_titel_9x16"] = beitrag(1080, 1920, 200, "VON DER", "EINSATZTAGEBUCH",
                               "Ein Einsatz in sechs Karten", "REEL", 100, 672,
                               kopf2="ALARMIERUNG")
T["tiktok_9x16"] = beitrag(1080, 1920, 200, "DIE CREW", "HINTER DEN KULISSEN",
                           "Wer nachts fliegt, wenn andere schlafen",
                           "TIKTOK", 104, 672)

# ==========================================================================
#  C  Karussell 4:5 -- Titel, Inhalt, Abschluss
# ==========================================================================
# Zehn Karten je Beitrag sind das Maximum, das alle Plattformen mitmachen.
W, H = 1080, 1350
foot = 170
y = H - foot

T["karussell_titel_4x5"] = beitrag(W, H, foot, "WAS EIN RTH", "DID YOU KNOW?",
                                   "Wischen »", "1 / 7", 92,
                                   kopf2="NACHTS BRAUCHT")

# Inhaltskarte: Text oben auf ruhiger Flaeche, Bild unten bis an die Kante
bildhoehe = 430
bildoben = y - bildhoehe
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
zeile(b, "03", 130, GALLIANO, 64, 210, BLK, .0, op=".32")
zeile(b, "NACHTSICHTBRILLEN", 54, IVORY, 64, 330, BLK, .01)
strich(b, 64, 370)
for i, s in enumerate([
        "Ohne NVG bleibt ein Einsatzort in der Nacht",
        "schwarz. Mit ihr sieht die Crew Gelände,",
        "Leitungen und Hindernisse — und kann dort",
        "landen, wo sonst niemand landen würde."]):
    zeile(b, s, 38, IVORY, 64, 450 + i * 58, REG, .02, op=".88")
b.append(bild(W, bildhoehe + 40, x=0, y=bildoben - 20, bw=W, bh=bildhoehe + 40))
b.append(feld(W, H, y, STRATOS))
b.append(kante(W, bildoben, KANTE_STAERKE))
b.append(absenderleiste(W, y, foot, right="3 / 7"))
T["karussell_inhalt_4x5"] = svg(W, H, "".join(b))

# Abschlusskarte: Aufforderung, kein Bild
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
b.append(badge(280, (W - 280) / 2, 250))
zeile(b, "MEHR DAVON?", 72, IVORY, W / 2, 660, BLK, .01, "middle")
zeile(b, "Folgen · Speichern · Teilen", 34, IVORY, W / 2, 722, REG, .02,
      "middle", op=".80")
strich(b, W / 2 - 80, 782, 160)
zeile(b, "VIRTUALAIRRESCUE.COM", 30, GALLIANO, W / 2, 860, BOLD, .18, "middle")
b.append(absenderleiste(W, y, foot, right="7 / 7"))
T["karussell_abschluss_4x5"] = svg(W, H, "".join(b))

# ==========================================================================
#  D  Inhaltsformate
# ==========================================================================

# --- Einsatzmeldung 1:1 ----------------------------------------------------
# Aufbau wie eine Alarmdepesche: Stichwort gross, darunter die Fakten.
W = H = 1080
foot = 150; y = H - foot
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
b.append(kante(W, 214, KANTE_STAERKE))
zeile(b, "EINSATZ", 28, GALLIANO, 64, 150, BOLD, .18)
zeile(b, "PRIMÄREINSATZ", 88, IVORY, 64, 340, BLK, .01)
for i, (k, v) in enumerate([("FUNKRUFNAME", "CHRISTOPH 22"),
                            ("STATION", "KASSEL"),
                            ("STICHWORT", "VERKEHRSUNFALL, EINGEKLEMMT"),
                            ("STATUS", "3 · AUF ANFAHRT")]):
    yy = 440 + i * 94
    zeile(b, k, 24, GALLIANO, 64, yy, BOLD, .18)
    zeile(b, v, 40, IVORY, 64, yy + 46, BOLD, .04)
b.append(absenderleiste(W, y, foot, right="LEITSTELLE"))
T["einsatzmeldung_1x1"] = svg(W, H, "".join(b))

# --- Statement 4:5 ---------------------------------------------------------
W, H = 1080, 1350
foot = 170; y = H - foot
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
b.append(kante(W, 254, KANTE_STAERKE))
zeile(b, "„", 240, GALLIANO, 52, 470, BLK, .0, op=".30")
for i, s in enumerate(["Wir fliegen nicht,", "weil es geht.",
                       "Wir fliegen, weil", "jemand wartet."]):
    zeile(b, s, 74, IVORY, 64, 440 + i * 94, BLK, .01)
strich(b, 64, 870)
zeile(b, "TOBIAS K. · PILOT · STATION MÜNCHEN", 28, GALLIANO, 64, 930, BOLD, .14)
b.append(absenderleiste(W, y, foot, right="STIMMEN"))
T["statement_4x5"] = svg(W, H, "".join(b))

# --- Veranstaltung 4:5 -----------------------------------------------------
W, H = 1080, 1350
foot = 170; y = H - foot
tren = 640
b = [bild(W, tren + 40, x=0, y=0, bw=W, bh=tren + 40), scrim(W, tren + 40, tren, .70)]
b.append(feld(W, H, tren))
b.append(kante(W, tren, KANTE_STAERKE))
zeile(b, "GEMEINSAMER FLUGABEND", 28, GALLIANO, 64, 760, BOLD, .18)
zeile(b, "NACHTFLUG", 96, IVORY, 64, 876, BLK, .01)
zeile(b, "IN DIE ALPEN", 96, IVORY, 64, 972, BLK, .01)
for i, (k, v) in enumerate([("WANN", "SAMSTAG, 20:00 UTC"),
                            ("WO", "VATSIM · LSZS » LSZH")]):
    zeile(b, k, 24, GALLIANO, 64 + i * 470, 1058, BOLD, .18)
    zeile(b, v, 34, IVORY, 64 + i * 470, 1102, BOLD, .04)
b.append(absenderleiste(W, y, foot, right="TERMIN"))
T["veranstaltung_4x5"] = svg(W, H, "".join(b))

# --- Vergleich 1:1 ---------------------------------------------------------
# Zwei Zustaende, getrennt von der Kante -- nicht von einer senkrechten Linie:
# die Kante ist das Markenelement, sie soll die Trennung sein.
W = H = 1080
foot = 150; y = H - foot
mitte = 468
b = [bild(W, mitte + 40, x=0, y=0, bw=W, bh=mitte + 40)]
b.append(feld(W, H, mitte, STRATOS))
b.append(bild(W, y - mitte + 40, x=0, y=mitte - 20, bw=W, bh=y - mitte + 60))
b.append(feld(W, H, y, STRATOS))
b.append(kante(W, mitte, KANTE_STAERKE))
# Die Beschriftungen liegen auf Fotos -- ohne eigene Flaeche waeren sie je nach
# Motiv unlesbar. Ein kleines Feld im Markenwinkel traegt sie.
def marke(b, s, x, y, col=IVORY):
    w = tw(s, 30, BOLD, .18) + 44
    b.append(f'<g transform="translate({x},{y}) rotate({KANTE_WINKEL:.4f})">'
             f'<rect width="{w:.0f}" height="52" fill="{STRATOS}" opacity=".88"/></g>')
    zeile(b, s, 30, col, x + 22, y + 35, BOLD, .18)

marke(b, "VORHER", 56, 52)
marke(b, "NACHHER", 56, mitte + 60, GALLIANO)
b.append(absenderleiste(W, y, foot, right="AUSBAU"))
T["vergleich_1x1"] = svg(W, H, "".join(b))

# --- Vierbild 1:1 ----------------------------------------------------------
W = H = 1080
foot = 150; g = 8
cell = (W - g) / 2
top = (H - foot - g) / 2
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
for i in range(4):
    cx = (i % 2) * (cell + g)
    cy = (i // 2) * (top + g)
    b.append(bild(cell, top, x=cx, y=cy, bw=cell, bh=top))
    zeile(b, "0%d" % (i + 1), 26, IVORY, cx + 22, cy + 46, BOLD, .1, op=".8")
b.append(absenderleiste(W, H - foot, foot, right="EINSATZRÜCKBLICK"))
T["fb_1x1_vierbild"] = svg(W, H, "".join(b))

# --- Zahl 1:1 --------------------------------------------------------------
# Eine Zahl, ein Satz. Fuer Bilanzen, Jubilaeen, Meilensteine.
W = H = 1080
foot = 150; y = H - foot
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
b.append(kante(W, 640, KANTE_STAERKE))
zeile(b, "IM JAHR 2026", 28, GALLIANO, 64, 190, BOLD, .18)
zeile(b, "1.284", 230, IVORY, 64, 460, BLK, .0)
zeile(b, "EINSÄTZE GEFLOGEN", 44, GALLIANO, 64, 550, BLK, .02)
for i, s in enumerate(["Davon 312 in der Nacht, 87 mit der Winde",
                       "und 41 grenzüberschreitend."]):
    zeile(b, s, 34, IVORY, 64, 740 + i * 52, REG, .02, op=".85")
b.append(absenderleiste(W, y, foot, right="BILANZ"))
T["zahl_1x1"] = svg(W, H, "".join(b))

# --- Crew 4:5 --------------------------------------------------------------
W, H = 1080, 1350
foot = 170; y = H - foot
tren = 750
b = [bild(W, tren + 40, x=0, y=0, bw=W, bh=tren + 40), scrim(W, tren + 40, tren, .55)]
b.append(feld(W, H, tren))
b.append(kante(W, tren, KANTE_STAERKE))
zeile(b, "NEU IM TEAM", 28, GALLIANO, 64, 872, BOLD, .18)
zeile(b, "MARIE L.", 92, IVORY, 64, 980, BLK, .01)
zeile(b, "NOTFALLSANITÄTERIN · STATION LEIPZIG", 28, IVORY, 64, 1032,
      BOLD, .12, op=".85")
strich(b, 64, 1074)
zeile(b, "„Ich wollte immer dahin, wo es schnell gehen muss.“", 32, IVORY,
      64, 1136, REG, .02, op=".85")
b.append(absenderleiste(W, y, foot, right="CREW"))
T["crew_4x5"] = svg(W, H, "".join(b))

# ==========================================================================
#  E  Video und Kanal
# ==========================================================================

# --- Live-Overlay ----------------------------------------------------------
# Der Rahmen bleibt schmal: das Bild ist der Inhalt, nicht die Grafik.
W, H = 1920, 1080
b = [absenderleiste(W, H - 96, 96, right=None)]
b.append(f'<circle cx="{W-150}" cy="{H-52}" r="10" fill="#E5484D"/>')
zeile(b, "LIVE", 30, "#E5484D", W - 60, H - 42, BLK, .16, "end")
T["overlay_live_1920x1080"] = svg(W, H, "".join(b))

# --- Bauchbinde ------------------------------------------------------------
W, H = 1920, 1080
bx, by, bw_, bh_ = 90, 780, 800, 152
b = [f'<g transform="translate({bx+bw_/2},{by}) rotate({KANTE_WINKEL:.4f})">'
     f'<rect x="{-bw_/2:.0f}" y="0" width="{bw_}" height="{bh_}" fill="{STRATOS}" '
     f'opacity=".94"/>'
     f'<rect x="{-bw_/2:.0f}" y="-7" width="{bw_}" height="7" fill="{GALLIANO}"/></g>']
b.append(badge(76, bx + 26, by + 40))
zeile(b, "TOBIAS K.", 46, IVORY, bx + 128, by + 80, BLK, .01)
zeile(b, "PILOT · STATION MÜNCHEN", 24, GALLIANO, bx + 128, by + 120, BOLD, .16)
T["overlay_lowerthird_1920x1080"] = svg(W, H, "".join(b))

# --- YouTube-Kanalbild -----------------------------------------------------
# Sichtbar ist auf dem Handy nur der mittlere Streifen 1546 x 423.
W, H = 2560, 1440
sx, sy = (W - 1546) / 2, (H - 423) / 2
b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>', bild(W, H),
     f'<rect width="{W}" height="{H}" fill="{STRATOS}" opacity=".74"/>']
b.append(kante(W, H / 2 + 160, KANTE_STAERKE))
b.append(badge(158, sx, sy + 54))
zeile(b, "VIRTUAL AIR RESCUE", 84, IVORY, sx + 200, sy + 172, BLK, .02)
zeile(b, "VIRTUELLE LUFTRETTUNG · VATSIM · MSFS", 30, GALLIANO,
      sx + 200, sy + 224, BOLD, .18)
T["yt_kanalbild_2560x1440"] = svg(W, H, "".join(b))


# ==========================================================================
if __name__ == "__main__":
    ziel = "tpl_fotos" if _FOTOS else "tpl"
    os.makedirs(ziel, exist_ok=True)
    for k, v in T.items():
        open(os.path.join(ziel, k + ".svg"), "w", encoding="utf-8").write(v)
    print("%d Vorlagen -> %s/" % (len(T), ziel))
    from tpl import FEHLENDE
    if FEHLENDE:
        print("ACHTUNG -- Zeichen ohne Glyphe, sie fehlen im Ergebnis:")
        for ch, f in sorted(FEHLENDE):
            print("   U+%04X in %s" % (ord(ch), f))

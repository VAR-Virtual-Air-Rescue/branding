# -*- coding: utf-8 -*-
"""Erzeugt alle VAR-Vorlagen. Inhalte mit echten Begriffen aus der Leitstelle:
Stichwort, Funkrufname, Station, Status, Disponent."""
import os
from tpl import (svg, scene, shade, badge, kante, absenderleiste, txt, tw, uid,
                 STRATOS, GALLIANO, IVORY, SIGNAL, INK, BOLD, REG, BLK, MARKS, _inner)

T = {}

# ============================================================ 1  Instagram 4:5
W, H = 1080, 1350
foot = 190
body = [scene(W, H, "sunset"), shade(W, H, 0, .78)]
t, _ = txt("CHRISTOPH 22", 92, IVORY, 64, H - foot - 210, BLK, .01)
body.append(t)
t, _ = txt("VERLEGUNGSFLUG NACH KASSEL", 34, GALLIANO, 64, H - foot - 150, BOLD, .14)
body.append(t)
body.append(f'<rect x="64" y="{H-foot-124}" width="150" height="4" fill="{GALLIANO}"/>')
t, _ = txt("Sonnenaufgang über dem Reinhardswald.", 31, IVORY, 64, H - foot - 66,
           REG, .02, opacity=".85")
body.append(t)
body.append(absenderleiste(W, H - foot, foot, right="LUFTRETTUNG"))
T["ig_4x5_foto"] = svg(W, H, "".join(body))

# ============================================================ 2  Instagram 1:1
W = H = 1080
foot = 168
body = [scene(W, H, "alpine"), shade(W, H, 0, .70)]
t, _ = txt("WINDENRETTUNG", 78, IVORY, 56, H - foot - 152, BLK, .01)
body.append(t)
t, _ = txt("STATION ZÜRICH  ·  HB-ZQM", 30, GALLIANO, 56, H - foot - 100, BOLD, .14)
body.append(t)
body.append(absenderleiste(W, H - foot, foot))
T["ig_1x1_foto"] = svg(W, H, "".join(body))

# ============================================================ 3  1:1 Vierbild
W = H = 1080
foot = 150
g = 8
cell = (W - g) / 2
top = (H - foot - g) / 2
body = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
for i, k in enumerate(["sunset", "forest", "alpine", "night"]):
    cx = (i % 2) * (cell + g)
    cy = (i // 2) * (top + g)
    ident = uid("q")
    body.append(f'<defs><clipPath id="{ident}"><rect x="{cx}" y="{cy}" '
                f'width="{cell}" height="{top}"/></clipPath></defs>'
                f'<g clip-path="url(#{ident})">'
                f'<g transform="translate({cx},{cy})">{scene(cell, top, k)}</g></g>')
    n, _ = txt(f"0{i+1}", 26, IVORY, cx + 22, cy + 46, BOLD, .1, opacity=".8")
    body.append(n)
body.append(absenderleiste(W, H - foot, foot, right="EINSATZRÜCKBLICK"))
T["fb_1x1_vierbild"] = svg(W, H, "".join(body))

# ============================================================ 4  Story / Reel 9:16
W, H = 1080, 1920
body = [scene(W, H, "forest"), shade(W, H, .22, .80)]
# Sichere Zonen: oben 250 (Profilzeile), unten 340 (Aktionen)
body.append(badge(132, 64, 190))
t, _ = txt("VIRTUAL AIR RESCUE", 30, IVORY, 214, 268, BOLD, .16)
body.append(t)
t, _ = txt("SEKUNDÄR", 34, STRATOS, 0, 0, BOLD, .16)
tw_ = tw("SEKUNDÄR", 34, BOLD, .16)
body.append(f'<rect x="64" y="{H-720}" width="{tw_+56:.0f}" height="62" fill="{GALLIANO}"/>')
t, _ = txt("SEKUNDÄR", 34, STRATOS, 92, H - 720 + 43, BOLD, .16)
body.append(t)
t, _ = txt("INTENSIV-", 104, IVORY, 64, H - 570, BLK, .01); body.append(t)
t, _ = txt("VERLEGUNG", 104, IVORY, 64, H - 460, BLK, .01); body.append(t)
body.append(f'<rect x="64" y="{H-420}" width="190" height="5" fill="{GALLIANO}"/>')
t, _ = txt("Christoph Europa 5  ·  Station Niebüll", 33, IVORY, 64, H - 356,
           REG, .02, opacity=".88"); body.append(t)
T["story_9x16"] = svg(W, H, "".join(body))

# ============================================================ 5  Reel-Titelkarte
W, H = 1080, 1920
body = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>',
        scene(W, int(H * .58), "night")]
body.append(f'<g opacity=".5">{shade(W, int(H*.58), 0, .9)}</g>')
body.append(kante(W, int(H * .58), 14))
t, _ = txt("FOLGE 04", 34, GALLIANO, 64, int(H * .58) + 120, BOLD, .18); body.append(t)
t, _ = txt("NACHTFLUG", 118, IVORY, 64, int(H * .58) + 262, BLK, .01); body.append(t)
t, _ = txt("MIT NVG", 118, GALLIANO, 64, int(H * .58) + 384, BLK, .01); body.append(t)
t, _ = txt("Wie unsere Crews bei Dunkelheit", 34, IVORY, 64, int(H*.58)+470, REG, .02,
           opacity=".8"); body.append(t)
t, _ = txt("an unbekannten Landestellen arbeiten.", 34, IVORY, 64, int(H*.58)+516, REG,
           .02, opacity=".8"); body.append(t)
body.append(badge(120, 64, H - 260))
t, _ = txt("VIRTUALAIRRESCUE.COM", 28, IVORY, 202, H - 190, BOLD, .18, opacity=".7")
body.append(t)
T["reel_titel_9x16"] = svg(W, H, "".join(body))

# ============================================================ 6  Statement 4:5
W, H = 1080, 1350
body = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
body.append(f'<circle cx="{W-90}" cy="150" r="360" fill="{GALLIANO}" opacity=".07"/>')
t, _ = txt("STIMMEN AUS DER LEITSTELLE", 30, GALLIANO, 80, 190, BOLD, .18); body.append(t)
for i, line in enumerate(["„Die ersten", "drei Minuten", "entscheiden."]):
    col = GALLIANO if i == 2 else IVORY
    t, _ = txt(line, 96, col, 80, 420 + i * 118, BLK, .01); body.append(t)
body.append(f'<rect x="80" y="{420+3*118-40}" width="160" height="5" fill="{GALLIANO}"/>')
t, _ = txt("Marco, Disponent LST 02", 32, IVORY, 80, 420 + 3 * 118 + 30, REG, .03,
           opacity=".75"); body.append(t)
body.append(absenderleiste(W, H - 170, 170))
T["statement_4x5"] = svg(W, H, "".join(body))

# ============================================================ 7  Einsatzmeldung 1:1
W = H = 1080
body = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
        f'<rect width="{W}" height="{H}" fill="{STRATOS}" opacity=".85"/>']
# Raster als Anmutung eines Lagebilds
for i in range(0, W, 60):
    body.append(f'<rect x="{i}" y="0" width="1" height="{H}" fill="{IVORY}" opacity=".035"/>')
    body.append(f'<rect x="0" y="{i}" width="{W}" height="1" fill="{IVORY}" opacity=".035"/>')
body.append(f'<circle cx="{W*.72:.0f}" cy="{H*.36:.0f}" r="210" fill="none" '
            f'stroke="{GALLIANO}" stroke-width="2" opacity=".28"/>')
body.append(f'<circle cx="{W*.72:.0f}" cy="{H*.36:.0f}" r="130" fill="none" '
            f'stroke="{GALLIANO}" stroke-width="2" opacity=".45"/>')
body.append(f'<circle cx="{W*.72:.0f}" cy="{H*.36:.0f}" r="9" fill="{GALLIANO}"/>')
tw_ = tw("EINSATZ LÄUFT", 30, BOLD, .18)
body.append(f'<rect x="64" y="86" width="{tw_+52:.0f}" height="56" fill="{GALLIANO}"/>')
t, _ = txt("EINSATZ LÄUFT", 30, STRATOS, 90, 124, BOLD, .18); body.append(t)
t, _ = txt("VU KLEMMT", 96, IVORY, 64, 330, BLK, .01); body.append(t)
t, _ = txt("PRIMÄREINSATZ", 32, GALLIANO, 64, 388, BOLD, .16); body.append(t)
rows = [("FUNKRUFNAME", "CHRISTOPH 51"), ("STATION", "STUTTGART"),
        ("STATUS", "3 — AUF ANFAHRT"), ("DISPONENT", "LST 01")]
for i, (k, v) in enumerate(rows):
    y = 520 + i * 92
    body.append(f'<rect x="64" y="{y-34}" width="3" height="56" fill="{GALLIANO}"/>')
    t, _ = txt(k, 24, IVORY, 92, y - 8, BOLD, .16, opacity=".55"); body.append(t)
    t, _ = txt(v, 40, IVORY, 92, y + 34, BOLD, .03); body.append(t)
body.append(absenderleiste(W, H - 150, 150))
T["einsatzmeldung_1x1"] = svg(W, H, "".join(body))

# ============================================================ 8  Veranstaltung 4:5
W, H = 1080, 1350
body = [scene(W, H, "night"), f'<rect width="{W}" height="{H}" fill="{STRATOS}" opacity=".5"/>']
body.append(f'<rect x="0" y="0" width="{W}" height="10" fill="{GALLIANO}"/>')
body.append(badge(150, 80, 96))
t, _ = txt("GEMEINSCHAFTSFLUG", 30, GALLIANO, 80, 348, BOLD, .18); body.append(t)
t, _ = txt("ALPEN-", 130, IVORY, 80, 500, BLK, .01); body.append(t)
t, _ = txt("ROTATION", 130, IVORY, 80, 632, BLK, .01); body.append(t)
body.append(f'<rect x="80" y="686" width="{W-160}" height="3" fill="{IVORY}" opacity=".25"/>')
info = [("WANN", "SA 12.09.  ·  19:00Z"), ("WO", "LSZH — LSZB — LSGS"),
        ("WER", "PILOTEN + DISPONENTEN"), ("ANMELDUNG", "HUB › VERANSTALTUNGEN")]
for i, (k, v) in enumerate(info):
    y = 776 + i * 88
    t, _ = txt(k, 23, GALLIANO, 80, y, BOLD, .16); body.append(t)
    t, _ = txt(v, 36, IVORY, 300, y + 4, BOLD, .04); body.append(t)
body.append(absenderleiste(W, H - 160, 160, right="VERANSTALTUNG"))
T["veranstaltung_4x5"] = svg(W, H, "".join(body))

# ============================================================ 9  Discord-Event 800x320
W, H = 800, 320
body = [scene(W, H, "sunset")]
body.append(f'<rect width="{W}" height="{H}" fill="{STRATOS}" opacity=".62"/>')
body.append(f'<rect x="0" y="0" width="{W}" height="6" fill="{GALLIANO}"/>')
body.append(badge(84, 40, 52))
t, _ = txt("DISPO-SCHULUNG", 22, GALLIANO, 148, 96, BOLD, .18); body.append(t)
t, _ = txt("STICHWORT-", 52, IVORY, 148, 158, BLK, .01); body.append(t)
t, _ = txt("KATALOG", 52, IVORY, 148, 214, BLK, .01); body.append(t)
t, _ = txt("MI 20:00Z  ·  SPRACHKANAL LST", 20, IVORY, 148, 258, BOLD, .14,
           opacity=".78"); body.append(t)
body.append(f'<rect x="0" y="{H-5}" width="{W}" height="5" fill="{GALLIANO}"/>')
T["discord_event_800x320"] = svg(W, H, "".join(body))

# ============================================================ 10 YouTube-Thumbnail
W, H = 1280, 720
body = [scene(W, H, "alpine")]
body.append(f'<defs><linearGradient id="ytg" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{STRATOS}" stop-opacity=".95"/>'
            f'<stop offset="58%" stop-color="{STRATOS}" stop-opacity="0"/>'
            f'</linearGradient></defs><rect width="{W}" height="{H}" fill="url(#ytg)"/>')
t, _ = txt("SO FLIEGT", 86, IVORY, 60, 250, BLK, .01); body.append(t)
t, _ = txt("EINE WINDE", 86, GALLIANO, 60, 348, BLK, .01); body.append(t)
body.append(f'<rect x="60" y="392" width="150" height="6" fill="{GALLIANO}"/>')
t, _ = txt("REGA · H145 · REALER ABLAUF", 26, IVORY, 60, 452, BOLD, .16,
           opacity=".85"); body.append(t)
body.append(badge(96, 60, H - 156))
t, _ = txt("VIRTUAL AIR RESCUE", 24, IVORY, 172, H - 100, BOLD, .18, opacity=".8")
body.append(t)
T["yt_thumb_1280x720"] = svg(W, H, "".join(body))

# ============================================================ 11 YouTube-Kanalbild
W, H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
sx, sy = (W - SAFE_W) / 2, (H - SAFE_H) / 2
body = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
body.append(f'<g transform="translate(0,{H*.30:.0f})">{scene(W, int(H*.40), "night")}</g>')
body.append(f'<rect y="{H*.30:.0f}" width="{W}" height="{H*.40:.0f}" fill="{STRATOS}" '
            f'opacity=".55"/>')
body.append(kante(W, int(H * .30 + H * .40), 12))
bs = 210
body.append(badge(bs, sx, sy + (SAFE_H - bs) / 2))
t, w1 = txt("VIRTUAL AIR RESCUE", 104, IVORY, sx + bs + 60, sy + SAFE_H / 2 + 10, BLK, .02)
body.append(t)
body.append(f'<rect x="{sx+bs+60:.0f}" y="{sy+SAFE_H/2+42:.0f}" width="{w1:.0f}" '
            f'height="4" fill="{GALLIANO}"/>')
t, _ = txt("VIRTUELLE LUFTRETTUNG · EIGENE LEITSTELLE · EIGENER CLIENT",
           30, IVORY, sx + bs + 60, sy + SAFE_H / 2 + 108, BOLD, .18, opacity=".72")
body.append(t)
T["yt_kanalbild_2560x1440"] = svg(W, H, "".join(body))

# ============================================================ 12 Lower Third
W, H = 1920, 1080
body = [scene(W, H, "forest"), f'<rect width="{W}" height="{H}" fill="#000" opacity=".08"/>']
lx, ly, lw, lh = 90, H - 300, 900, 132
body.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{STRATOS}" '
            f'opacity=".94"/>')
body.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="6" fill="{GALLIANO}"/>')
body.append(f'<rect x="{lx}" y="{ly}" width="8" height="{lh}" fill="{GALLIANO}"/>')
t, _ = txt("SANDRA HOFFMANN", 44, IVORY, lx + 42, ly + 66, BLK, .02); body.append(t)
t, _ = txt("HEMS TC  ·  STATION MÜNCHEN", 24, GALLIANO, lx + 42, ly + 106,
           BOLD, .16); body.append(t)
# Eckmarke oben rechts
body.append(f'<g opacity=".92">{badge(96, W-96-56, 56)}</g>')
T["overlay_lowerthird_1920x1080"] = svg(W, H, "".join(body))

# ============================================================ 13 Live-Kachel
W, H = 1920, 1080
body = [scene(W, H, "night"), f'<rect width="{W}" height="{H}" fill="#000" opacity=".12"/>']
bx, by, bw, bh = 56, 56, 520, 130
body.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{STRATOS}" '
            f'opacity=".9"/>')
body.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="5" fill="{GALLIANO}"/>')
body.append(badge(84, bx + 22, by + 23))
t, _ = txt("LEITSTELLE LIVE", 30, IVORY, bx + 128, by + 58, BLK, .03); body.append(t)
body.append(f'<circle cx="{bx+136}" cy="{by+96}" r="7" fill="#E5484D"/>')
t, _ = txt("3 EINSÄTZE  ·  7 LUFTFAHRZEUGE", 21, GALLIANO, bx + 154, by + 103,
           BOLD, .14); body.append(t)
# Statusstreifen unten
sy2 = H - 92
body.append(f'<rect x="0" y="{sy2}" width="{W}" height="92" fill="{STRATOS}" opacity=".88"/>')
body.append(f'<rect x="0" y="{sy2}" width="{W}" height="4" fill="{GALLIANO}"/>')
cols = [("STICHWORT", "VU KLEMMT"), ("FUNKRUFNAME", "CHRISTOPH 51"),
        ("STATUS", "3"), ("FLUGZEIT", "00:12:40")]
x = 64
for k, v in cols:
    t, w1 = txt(k, 18, IVORY, x, sy2 + 38, BOLD, .16, opacity=".55"); body.append(t)
    t, w2 = txt(v, 28, IVORY, x, sy2 + 72, BOLD, .04); body.append(t)
    x += max(w1, w2) + 90
T["overlay_live_1920x1080"] = svg(W, H, "".join(body))

# ============================================================ 14 TikTok / Shorts
W, H = 1080, 1920
body = [scene(W, H, "sunset")]
body.append(f'<g opacity=".55">{shade(W, H, .3, .55)}</g>')
# Rechts 320 px und unten 520 px bleiben frei -- dort liegt die App-Bedienung
body.append(badge(104, 56, 240))
t, _ = txt("VIRTUAL AIR RESCUE", 26, IVORY, 176, 302, BOLD, .16); body.append(t)
tw_ = tw("TEIL 2 VON 3", 26, BOLD, .16)
body.append(f'<rect x="56" y="400" width="{tw_+44:.0f}" height="50" fill="{GALLIANO}"/>')
t, _ = txt("TEIL 2 VON 3", 26, STRATOS, 78, 432, BOLD, .16); body.append(t)
t, _ = txt("AUSSEN-", 96, IVORY, 56, 600, BLK, .01); body.append(t)
t, _ = txt("LANDUNG", 96, GALLIANO, 56, 700, BLK, .01); body.append(t)
t, _ = txt("Was die Crew vorher abfragt", 32, IVORY, 56, 764, REG, .02, opacity=".9")
body.append(t)
body.append(f'<rect x="56" y="{H-560}" width="{W-376}" height="4" fill="{GALLIANO}" '
            f'opacity=".6"/>')
t, _ = txt("MEHR IM HUB › WISSENSDATENBANK", 24, IVORY, 56, H - 510, BOLD, .16,
           opacity=".7"); body.append(t)
T["tiktok_9x16"] = svg(W, H, "".join(body))

# ============================================================ 15 Zwei-Bild-Vergleich
W = H = 1080
foot = 150
body = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']
half = (W - 6) / 2
for i, k in enumerate(["night", "sunset"]):
    ident = uid("cmp")
    body.append(f'<defs><clipPath id="{ident}"><rect x="{i*(half+6)}" y="0" '
                f'width="{half}" height="{H-foot-6}"/></clipPath></defs>'
                f'<g clip-path="url(#{ident})"><g transform="translate({i*(half+6)},0)">'
                f'{scene(half, H-foot-6, k)}</g></g>')
    lab = ["VORHER", "NACHHER"][i]
    tw_ = tw(lab, 24, BOLD, .16)
    body.append(f'<rect x="{i*(half+6)+24}" y="24" width="{tw_+40:.0f}" height="48" '
                f'fill="{GALLIANO}"/>')
    t, _ = txt(lab, 24, STRATOS, i * (half + 6) + 44, 55, BOLD, .16); body.append(t)
body.append(absenderleiste(W, H - foot, foot, right="LEITSTELLE V2"))
T["vergleich_1x1"] = svg(W, H, "".join(body))

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs("tpl", exist_ok=True)
    for k, v in T.items():
        open(f"tpl/{k}.svg", "w", encoding="utf-8").write(v)
        print(f"  {k:34s} {len(v):>7d} B")
    print(f"{len(T)} Vorlagen")

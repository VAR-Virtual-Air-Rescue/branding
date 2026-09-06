# -*- coding: utf-8 -*-
"""Vorlagen fuer Veranstaltungen.

Drei Formate, zwei Anlassarten, drei Macharten -- daraus entstehen die Dateien
in `vorlagen/event_*`.

    Formate    Discord-Titelbild 800x320 · Discord-Ankuendigung 1200x630
               Instagram-Beitrag 1080x1350
    Anlassart  wiederkehrend (Dienstagsflug, Schichtdienst) und besonders
               (Jahresevent, Rekordnacht, Fly-in)
    Machart    A Depesche · B Bild · C Plakat

**Warum drei Macharten und nicht drei Farbvarianten:** eine Auswahl ist nur dann
eine, wenn die Fassungen etwas anderes koennen. Die Depesche traegt viele
Angaben und kein Bild, das Bild traegt Stimmung und wenig Text, das Plakat
traegt ein Datum und sonst fast nichts. Wer eine Ankuendigung schreibt, waehlt
danach, was er zu sagen hat -- nicht danach, welche Farbe ihm gefaellt.

**Wiederkehrend gegen besonders** ist kein Etikett, sondern eine andere
Gewichtung. Wiederkehrend heisst: der Rhythmus ist die Nachricht -- der Wochentag
steht gross, das Datum klein, es gibt eine Reihenbezeichnung. Besonders heisst:
der Anlass ist die Nachricht -- die Schlagzeile steht gross, das Datum als
Marke daneben, und der Goldanteil steigt.
"""
import os, sys, glob

from tpl import (svg, scene, scrim, badge, kante, kante_luft, feld,
                 absenderleiste, foto, txt, tw, uid, KANTE_STAERKE,
                 STRATOS, GALLIANO, IVORY, SIGNAL, INK, BOLD, REG, BLK)

T = {}

# --- Bildquelle (wie in tpl_build) ---------------------------------------
_FOTOS = []
if "--fotos" in sys.argv:
    _FOTOS = sorted(glob.glob(os.path.join(sys.argv[sys.argv.index("--fotos") + 1], "*.jpg")))
_KULISSEN = ["night", "alpine", "sunset", "forest"]
_n = [0]


def bild(w, h, art=None, x=0, y=0):
    i = _n[0]; _n[0] += 1
    if _FOTOS:
        return foto(w, h, _FOTOS[i % len(_FOTOS)], x, y, w, h)
    ident = uid("k")
    return (f'<defs><clipPath id="{ident}"><rect x="{x}" y="{y}" width="{w}" '
            f'height="{h}"/></clipPath></defs><g clip-path="url(#{ident})">'
            f'<g transform="translate({x},{y})">'
            f'{scene(w, h, art or _KULISSEN[i % len(_KULISSEN)])}</g></g>')


def fuss(H):
    """Hoehe der Absenderleiste.

    Nicht rein prozentual: bei 320 Zeilen Hoehe waeren 14,5 % noch 46
    Einheiten, und darin muessen Zeichen, Adresse und Rubrik nebeneinander
    stehen. Unter 88 wird die Leiste zum Strich.
    """
    return int(max(88, H * .145))


def zeile(b, s, size, fill, x, y, font=BOLD, tr=.04, anchor="start", op=None):
    t, _ = txt(s, size, fill, x, y, font, tr, anchor, op)
    b.append(t)


def passt(s, size, font, tr, max_b):
    """Groesse so lange verkleinern, bis die Zeile in die Breite passt.

    Ohne das laeuft "WINTERNACHTFLUG NACH SPITZBERGEN" bei 800 Einheiten Breite
    aus dem Bild, und niemand sieht es, weil im Entwurf "FLY-IN" stand.
    """
    for _ in range(28):
        if tw(s, size, font, tr) <= max_b:
            break
        size *= 0.95
    return size


def marke(b, w, y, groesse=34):
    """Zeichen und Adresse, ohne die gekippte Flaeche -- fuer Plakate, die
    unten schon eine Farbflaeche haben."""
    b.append(badge(groesse, w * .055, y - groesse * .5))
    zeile(b, "VIRTUALAIRRESCUE.COM", groesse * .42, IVORY,
          w * .055 + groesse * 1.45, y + groesse * .16, BOLD, .16, op=".85")


# =========================================================================
#  A  Depesche -- viele Angaben, kein Bild
# =========================================================================
def depesche(W, H, kopf, zeilen, rubrik, wiederkehrend, unter=None):
    """Aufbau wie eine Einsatzmeldung: Rubrik, Schlagzeile, Datenzeilen.

    Die Datenzeilen stehen in einem Raster mit Beschriftung darueber -- so
    liest sich WANN/WO/WER wie im Lagebild und nicht wie ein Werbetext.
    """
    foot = fuss(H)
    y = H - foot
    luft = kante_luft(W)
    b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']

    # Ein schmales Band im Markenwinkel als Hintergrundstruktur -- dieselbe
    # Neigung wie die Kante, sonst entsteht ein zweiter Winkel.
    b.append(f'<g opacity=".5"><rect x="{-W}" y="{H*.30:.0f}" width="{W*3}" '
             f'height="{H*.42:.0f}" fill="#0A1730" '
             f'transform="rotate(-3.2747 {W/2} {H/2})"/></g>')

    px = W * .06
    hoch = H > W * 1.05
    lab_g = max(13, H * .022 if not hoch else W * .026)
    wert_g = max(19, H * .040 if not hoch else W * .046)

    if hoch:
        # Untereinander: drei Spalten auf 1080 Breite sind schmal, drei Zeilen
        # lesen sich wie ein Lagebild.
        schritt = wert_g * 1.9
        oben_daten = y - luft - H * .02 - schritt * (len(zeilen) - 1)
        for i, (lab, wert) in enumerate(zeilen):
            zy = oben_daten + i * schritt
            zeile(b, lab, lab_g, GALLIANO, px, zy - wert_g * .92, BOLD, .18)
            zeile(b, wert, wert_g, IVORY, px, zy, BOLD, .03)
        block_oben = oben_daten - wert_g * .92 - lab_g * 1.6
    else:
        sp = (W - 2 * px) / len(zeilen)
        wert_y = y - luft - H * .012
        lab_y = wert_y - wert_g * .95
        for i, (lab, wert) in enumerate(zeilen):
            x = px + i * sp
            zeile(b, lab, lab_g, GALLIANO, x, lab_y, BOLD, .18)
            # Jeder Wert muss in seine eigene Spalte passen, sonst laufen sie
            # ineinander -- die Breite wird geprueft, nicht gehofft.
            zeile(b, wert, passt(wert, wert_g, BOLD, .03, sp * .92),
                  IVORY, x, wert_y, BOLD, .03)
        block_oben = lab_y - lab_g * 2.6

    ks = passt(kopf, (H * .115 if not hoch else W * .105), BLK, .01, W - 2 * px)
    unter_g = max(16, H * .030 if not hoch else W * .032)
    kick_g = max(15, H * .026 if not hoch else W * .026)

    if hoch:
        # Im Hochformat von oben setzen -- unten gestapelt bliebe die halbe
        # Flaeche leer.
        kick_y = H * .20
        kopf_y = kick_y + ks * .95
    else:
        kopf_y = block_oben - (unter_g * 1.6 if unter else 0)
        kick_y = kopf_y - ks * .78 - kick_g * .9

    zeile(b, "SERIENTERMIN" if wiederkehrend else "SONDERVERANSTALTUNG",
          kick_g, GALLIANO, px, kick_y, BOLD, .18)
    zeile(b, kopf, ks, IVORY, px, kopf_y, BLK, .01)
    if unter:
        zeile(b, unter, unter_g, IVORY, px, kopf_y + unter_g * 1.6, REG, .02, op=".82")

    b.append(absenderleiste(W, y, foot, right=rubrik))
    return svg(W, H, "".join(b))


# =========================================================================
#  B  Bild -- Stimmung, wenig Text
# =========================================================================
def bildvorlage(W, H, kopf, kopf2, unter, rubrik, wiederkehrend, kulisse=None):
    foot = fuss(H)
    y = H - foot
    luft = kante_luft(W)
    b = [bild(W, H, kulisse), scrim(W, H, y)]

    px = W * .06
    # Beide Schlagzeilen mit derselben Groesse -- also muss die *laengere*
    # ueber die Breite entscheiden. Vorher wurde nur die erste gemessen, und
    # "DER LUFTRETTUNG" endete als "DER LUFTRETTU".
    ks = passt(kopf, H * .105, BLK, .01, W - 2 * px)
    if kopf2:
        ks = min(ks, passt(kopf2, ks, BLK, .01, W - 2 * px))
    unter_g = max(16, H * .030)
    kick_g = max(15, H * .026)

    # Unterste Zeile zuerst, dann nach oben. Der Kicker stand vorher auf der
    # Schlagzeile, weil sein Abstand von einer Groesse ausging, die `passt()`
    # danach noch verkleinert hat.
    unter_y = y - luft - H * .012
    kopf2_y = unter_y - (unter_g * 1.6 if unter else 0)
    kopf_y = kopf2_y - (ks * 1.06 if kopf2 else 0)
    # Versalhoehe der Schlagzeile plus eigene Hoehe des Kickers.
    kick_y = kopf_y - ks * .78 - kick_g * .9

    zeile(b, "JEDE WOCHE" if wiederkehrend else "EINMALIG",
          kick_g, GALLIANO, px, kick_y, BOLD, .18)
    zeile(b, kopf, ks, IVORY, px, kopf_y, BLK, .01)
    if kopf2:
        zeile(b, kopf2, ks, GALLIANO, px, kopf2_y, BLK, .01)
    if unter:
        zeile(b, unter, unter_g, IVORY, px, unter_y, REG, .02, op=".88")

    b.append(absenderleiste(W, y, foot, right=rubrik))
    return svg(W, H, "".join(b))


# =========================================================================
#  C  Plakat -- Datum gross, sonst fast nichts
# =========================================================================
def plakat(W, H, tag, monat, kopf, unter, rubrik, wiederkehrend):
    """Das Datum traegt die Flaeche.

    Bei wiederkehrenden Terminen steht statt des Datums der Wochentag -- wer
    jeden Dienstag fliegt, braucht kein Datum, sondern den Tag.
    """
    b = [f'<rect width="{W}" height="{H}" fill="{GALLIANO}"/>']
    # Unteres Feld in Stratos, an der Kante getrennt -- der Aufbau des Zeichens
    # im Grossen.
    schnitt = H * (.52 if H > W else .58)
    b.append(feld(W, H, schnitt, STRATOS))
    b.append(kante(W, schnitt, KANTE_STAERKE))

    px = W * .06
    # Der Platz fuer die Tageszahl ist, was der Monat danebenlaesst -- nicht
    # eine feste Quote. Sonst schrumpft ein Wochentag auf die Breite, die eine
    # zweistellige Zahl braucht, und darueber bleibt das halbe Feld leer.
    monat_b = tw(monat, max(18, H * .045), BOLD, .16)
    platz = W - 2 * px - monat_b - W * .022
    gross = passt(tag, H * (.34 if H > W else .44), BLK, -.02, platz)
    tag_b = tw(tag, gross, BLK, -.02)
    zeile(b, tag, gross, STRATOS, px, schnitt - H * .07, BLK, -.02)
    # Der Monat bekommt, was nach der Tageszahl uebrig bleibt -- sonst laeuft er
    # rechts aus dem Bild.
    mx = px + tag_b + W * .022
    zeile(b, monat, passt(monat, max(18, H * .045), BOLD, .16, W - px - mx),
          STRATOS, mx, schnitt - H * .07, BOLD, .16)

    kick = "SERIENTERMIN" if wiederkehrend else "SONDERVERANSTALTUNG"
    zeile(b, kick, max(14, H * .024), STRATOS, px, H * .10, BOLD, .18, op=".70")

    ks = passt(kopf, H * .075, BLK, .01, W - 2 * px)
    zeile(b, kopf, ks, IVORY, px, schnitt + kante_luft(W) + H * .085, BLK, .01)
    if unter:
        zeile(b, unter, max(15, H * .030), IVORY, px,
              schnitt + kante_luft(W) + H * .085 + ks * .80, REG, .02, op=".85")

    marke(b, W, H - H * .075, max(28, H * .055))
    if rubrik:
        zeile(b, rubrik, max(13, H * .024), GALLIANO, W - px, H - H * .065,
              BOLD, .18, "end")
    return svg(W, H, "".join(b))


# =========================================================================
#  Die Vorlagen
# =========================================================================
FORMATE = [
    ("discord_titel", 800, 320),
    ("discord_ankuendigung", 1200, 630),
    ("instagram", 1080, 1350),
]

# Inhalte mit echten Begriffen aus der Leitstelle. Wiederkehrend ist der
# Dienstagsflug, besonders die Rekordnacht.
WIEDER = dict(
    kopf="DIENSTAGSFLUG", kopf2="AB 19:00 UTC",
    unter="Jede Woche, eine Station, alle Rufgruppen.",
    rubrik="SERIE", tag="DIENSTAG", monat="19:00 UTC",
    daten=[("WANN", "DI 19:00z"), ("WO", "EDDF · EDDM"), ("WER", "Alle Rollen")],
)
SPECIAL = dict(
    kopf="LANGE NACHT", kopf2="DER LUFTRETTUNG",
    unter="24 Stunden, alle Stationen besetzt.",
    rubrik="SPECIAL", tag="14.", monat="NOVEMBER",
    daten=[("WANN", "14.11. 18:00z"), ("WO", "Alle Stationen"), ("DAUER", "24 Stunden")],
)

for fname, W, H in FORMATE:
    for art, d in (("wiederkehrend", WIEDER), ("special", SPECIAL)):
        wk = art == "wiederkehrend"
        T[f"event_{fname}_{art}_a_depesche"] = depesche(
            W, H, d["kopf"], d["daten"], d["rubrik"], wk, d["unter"])
        T[f"event_{fname}_{art}_b_bild"] = bildvorlage(
            W, H, d["kopf"], d["kopf2"], d["unter"], d["rubrik"], wk)
        T[f"event_{fname}_{art}_c_plakat"] = plakat(
            W, H, d["tag"], d["monat"], d["kopf"], d["unter"], d["rubrik"], wk)


if __name__ == "__main__":
    os.makedirs("tpl", exist_ok=True)
    for k, v in T.items():
        open(f"tpl/{k}.svg", "w", encoding="utf-8").write(v)
    from tpl import FEHLENDE
    if FEHLENDE:
        print("FEHLENDE ZEICHEN:", sorted(FEHLENDE))
    print(f"{len(T)} Event-Vorlagen")

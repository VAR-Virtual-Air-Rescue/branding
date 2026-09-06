# -*- coding: utf-8 -*-
"""Jedes Event bekommt sein eigenes Aussehen -- und bleibt VAR.

Der erste Anlauf mit den Event-Vorlagen hatte einen Fehler, den man erst sieht,
wenn zwoelf Banner nebeneinander liegen: sie sahen alle gleich aus. Stratos,
Gold, dieselbe Kante, dieselbe Aufteilung. Wer drei Termine im Kanal
uebereinander sieht, kann sie nicht auseinanderhalten -- und genau das konnten
die alten Aushaenge: THE LÄND war gelb, OVERLOAD schwarz-rot, das
Oesterreich-Banner blau. Jeder Anlass hatte ein Gesicht.

Die Loesung ist kein Freibrief, sondern ein Vertrag: **fester Rahmen,
variabler Innenraum.**

    Fest        Die gekippte Kante im Markenwinkel. Die Absenderleiste mit
                Zeichen und Adresse. Uniform in Versalien. Der Hubschrauber im
                Zeichen bleibt Gold -- immer.

    Variabel    Grundfarbe und Akzent. Der Untergrund. Der Titelsatz.

Dass die Grundfarbe wechseln darf, ist keine Ausnahme, die hier erfunden wird --
die Profilbilder machen es seit jeher so: Halloween ist orange, Weihnachten rot,
Pride ein Regenbogen, und der Hubschrauber bleibt in allen Gold. Dieselbe Regel,
eine Ebene hoeher.

Was **nicht** variabel ist: die drei Markenfarben behalten ihre Rolle. Galliano
bleibt Akzent und wird nie zur Textflaeche unter Ivory (2,3:1). Deshalb traegt
jede Signatur ihre Schriftfarbe mit, und `pruefe_signaturen()` rechnet nach,
statt sich darauf zu verlassen.
"""
import math

from tpl import (txt, tw, uid, STRATOS, GALLIANO, IVORY, SIGNAL,
                 BOLD, REG, BLK, KANTE_WINKEL)


# =========================================================================
#  Die Signatur
# =========================================================================
class Signatur:
    """Das Aussehen eines Anlasses.

    `grund`     Flaeche des Banners
    `akzent`    Linien, Kicker, Hervorhebung
    `ink`       Schriftfarbe auf dem Grund
    `untergrund` Name einer Textur aus TEXTUREN
    `satz`      Name einer Titelbehandlung aus SAETZE
    Die **Absenderleiste faerbt nicht mit**: Stratos, Gold, Ivory, immer. Sie
    ist der Teil, an dem man VAR erkennt, egal wie bunt es darueber zugeht --
    ein Rahmen, der mitwechselt, ist keiner. Als sie noch mitfaerbte, war bei
    zwei Signaturen die Rubrik unsichtbar, weil Akzent und Leiste dieselbe Farbe
    hatten.
    """

    LEISTE = STRATOS
    LEISTE_AKZENT = GALLIANO
    LEISTE_INK = IVORY

    def __init__(self, name, grund, akzent, ink, untergrund="keine",
                 satz="massiv"):
        self.name = name
        self.grund = grund
        self.akzent = akzent
        self.ink = ink
        self.untergrund = untergrund
        self.satz = satz


# --- Farben, die keine Markenfarben sind ---------------------------------
# Sie stehen hier und nicht im Brandbook unter "Farbe": das sind Anlassfarben,
# keine Markenfarben. Wer sie in einer Oberflaeche verwendet, hat etwas
# missverstanden.
MITTERNACHT = "#04091A"
TIEFROT     = "#8E1F17"
EISBLAU     = "#1B3A4B"
MOOS        = "#1E3B2F"
# Derselbe Ton wie im Profilbild `pb_halloween`. Das dunklere #B14E04 sah
# besser aus und traegt die Schrift nicht: 3,5:1 statt 6,0:1.
KUERBIS     = "#E5720A"
ASCHE       = "#1A1D24"

SIGNATUREN = {
    # Der Standard. Wer nichts waehlt, bekommt das hier.
    "standard": Signatur("Standard", STRATOS, GALLIANO, IVORY,
                         "keine", "massiv"),

    # Gebietsabend -- ruhig, damit die Karte die Nachricht bleibt.
    "gebiet": Signatur("Gebiet", STRATOS, GALLIANO, IVORY,
                       "raster", "massiv"),

    # Overload -- die Lage laeuft aus dem Ruder. Rot, und der Titel versetzt.
    "overload": Signatur("Overload", TIEFROT, IVORY, IVORY,
                         "puls", "versetzt"),

    # Nachtflug -- fast schwarz, Signalblau als einziger Farbpunkt.
    "nachtflug": Signatur("Nachtflug", MITTERNACHT, SIGNAL, IVORY,
                          "sterne", "umriss"),

    # Leitstelle -- Gold als Flaeche, Schrift in Stratos. Der helle Termin.
    "leitstelle": Signatur("Leitstelle", GALLIANO, STRATOS, STRATOS,
                           "raster", "massiv"),

    # Berg -- Hoehenlinien, kuehl.
    "berg": Signatur("Berg", EISBLAU, IVORY, IVORY,
                     "hoehenlinien", "gestapelt"),

    # Sternflug -- viele kommen zu einem Punkt.
    "sternflug": Signatur("Sternflug", MOOS, GALLIANO, IVORY,
                          "strahlen", "gestapelt"),

    # 24 Stunden -- der Balken laeuft einmal herum.
    "24h": Signatur("24 Stunden", STRATOS, GALLIANO, IVORY,
                    "stundenband", "gestapelt"),

    # Herbst/Halloween -- die einzige Signatur, die von einer Edition erbt.
    "herbst": Signatur("Herbst", KUERBIS, "#1A0E22", "#1A0E22",
                       "streuung", "massiv"),
}


# =========================================================================
#  Untergruende
# =========================================================================
def _rand(seed):
    import random
    return random.Random(seed)


def textur(name, w, h, farbe, seed=7):
    """Der Untergrund. Immer flaechig und leise -- er traegt nichts, er faerbt.

    Deckkraft bleibt niedrig: alles darueber muss lesbar bleiben, und ein
    Untergrund, den man als Muster liest statt als Flaeche, konkurriert mit der
    Schlagzeile.
    """
    r = _rand(seed)
    if name == "keine":
        return ""

    if name == "raster":
        # Feines Netz im Markenwinkel -- Lagebild, Leitstelle, Ordnung.
        schritt = max(28, h / 14)
        lin = []
        n = int(w * 2.4 / schritt)
        for i in range(n):
            x = -w * .7 + i * schritt
            lin.append(f"M{x:.0f},{-h} L{x:.0f},{h*2:.0f}")
        m = int(h * 2.4 / schritt)
        for i in range(m):
            yy = -h * .7 + i * schritt
            lin.append(f"M{-w:.0f},{yy:.0f} L{w*2:.0f},{yy:.0f}")
        return (f'<g transform="rotate({KANTE_WINKEL:.4f} {w/2:.0f} {h/2:.0f})" '
                f'opacity=".10"><path d="{" ".join(lin)}" stroke="{farbe}" '
                f'stroke-width="1.2" fill="none"/></g>')

    if name == "sterne":
        p = []
        for i in range(90):
            x, y = r.uniform(0, w), r.uniform(0, h)
            rr = r.uniform(1.0, 2.8)
            p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" '
                     f'opacity="{r.uniform(.20,.75):.2f}"/>')
        return f'<g fill="{farbe}">{"".join(p)}</g>'

    if name == "puls":
        # Konzentrische Boegen von links unten -- eine Meldung, die sich
        # ausbreitet.
        cx, cy = w * .12, h * .92
        ringe = []
        for i in range(9):
            rr = (i + 1) * max(w, h) * .11
            ringe.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" '
                         f'opacity="{max(.05, .30 - i*.03):.2f}"/>')
        return (f'<g fill="none" stroke="{farbe}" stroke-width="{max(2, h/160):.1f}">'
                f'{"".join(ringe)}</g>')

    if name == "hoehenlinien":
        # Wellenlinien, die nach unten flacher werden -- eine Gelaendekarte,
        # nicht ein Dekor.
        bahnen = []
        for i in range(11):
            yy = h * (.10 + i * .085)
            amp = h * .045 * (1 - i / 14)
            pts = []
            for k in range(13):
                x = w * k / 12
                pts.append(f"{x:.0f},{yy + math.sin(k * .9 + i) * amp:.0f}")
            bahnen.append("M" + " L".join(pts))
        return (f'<g fill="none" stroke="{farbe}" stroke-width="1.6" opacity=".16">'
                f'<path d="{" ".join(bahnen)}"/></g>')

    if name == "strahlen":
        # Linien, die auf einen Punkt zulaufen -- der Sternflug im Bild.
        zx, zy = w * .78, h * .40
        lin = []
        for i in range(22):
            a = 2 * math.pi * i / 22
            lin.append(f"M{zx + math.cos(a)*w:.0f},{zy + math.sin(a)*w:.0f} "
                       f"L{zx + math.cos(a)*w*.07:.0f},{zy + math.sin(a)*w*.07:.0f}")
        return (f'<g fill="none" stroke="{farbe}" stroke-width="1.4" opacity=".14">'
                f'<path d="{" ".join(lin)}"/></g>')

    if name == "stundenband":
        # Vierundzwanzig Striche, einer je Stunde, im Markenwinkel. Sie stehen
        # ueber die ganze Hoehe -- am oberen Rand allein sahen sie aus wie ein
        # verrutschtes Element und nicht wie ein Untergrund.
        st = []
        for i in range(24):
            x = w * (i + .5) / 24
            lang = (i % 6 == 0)
            st.append(f'<rect x="{x:.0f}" y="0" width="{max(2, w/420):.1f}" '
                      f'height="{h:.0f}" opacity="{.55 if lang else .28:.2f}"/>')
        return (f'<g transform="rotate({KANTE_WINKEL:.4f} {w/2:.0f} {h/2:.0f})" '
                f'fill="{farbe}" opacity=".28">{"".join(st)}</g>')

    if name == "streuung":
        p = []
        for i in range(46):
            x, y = r.uniform(0, w), r.uniform(0, h)
            s = r.uniform(3, 9)
            rot = r.uniform(0, 360)
            p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{s:.1f}" '
                     f'height="{s*.5:.1f}" transform="rotate({rot:.0f} {x:.0f} {y:.0f})" '
                     f'opacity="{r.uniform(.10,.30):.2f}"/>')
        return f'<g fill="{farbe}">{"".join(p)}</g>'

    raise ValueError("unbekannte Textur: " + name)


# =========================================================================
#  Titelsatz
# =========================================================================
def titel(satz, worte, groesse, sig, x, y, breite):
    """Die Schlagzeile setzen. `worte` ist eine Liste von ein bis zwei Zeilen.

    Gibt (svg, unterkante) zurueck -- die Unterkante braucht der Aufrufer, um
    darunter weiterzustapeln.
    """
    g = groesse
    if satz == "massiv":
        out, yy = [], y
        for i, w in enumerate(worte):
            t, _ = txt(w, g, sig.ink if i == 0 else sig.akzent, x, yy, BLK, .01)
            out.append(t)
            yy += g * 1.06
        return "".join(out), yy - g * 1.06

    if satz == "versetzt":
        # Zweites Wort haengt unter dem ersten und beginnt, wo es endet -- der
        # Versatz kommt aus dem Winkel, nicht aus einem Schatten.
        w1 = worte[0]
        w2 = worte[1] if len(worte) > 1 else ""
        t1, _ = txt(w1, g, sig.ink, x, y, BLK, -.01)
        out = [t1]
        if w2:
            b1 = tw(w1, g, BLK, -.01)
            t2, _ = txt(w2, g, sig.akzent, x + b1 + g * .06, y + g * .86, BLK, -.01)
            out.append(t2)
            return "".join(out), y + g * .86
        return "".join(out), y

    if satz == "umriss":
        # Erste Zeile als Umriss, zweite gefuellt. Der Umriss braucht Groesse:
        # unter etwa 40 Einheiten laeuft die Linie in sich selbst.
        out, yy = [], y
        for i, w in enumerate(worte):
            t, _ = txt(w, g, "none", x, yy, BLK, .01)
            if i == 0 and g >= 40:
                # Die Strichstaerke steht am aeusseren `<g>`, der Buchstabenpfad
                # darin traegt aber `scale(g/1000)` -- und der skaliert die Linie
                # mit. Aus 4,6 werden so 0,28, und der Umriss ist eine
                # Haarlinie. Also vorher durch denselben Faktor teilen.
                #
                # (`vector-effect="non-scaling-stroke"` waere der kuerzere Weg,
                # aber ob resvg ihn beachtet, ist nicht gesagt -- gerechnet
                # stimmt es sicher.)
                dick = max(2.8, g * .058) * 1000.0 / g
                t = t.replace('fill="none"',
                              f'fill="none" stroke="{sig.ink}" '
                              f'stroke-width="{dick:.1f}" '
                              f'stroke-linejoin="round"')
            else:
                t = t.replace('fill="none"', f'fill="{sig.ink}"')
            out.append(t)
            yy += g * 1.06
        return "".join(out), yy - g * 1.06

    if satz == "gestapelt":
        # Zeilen abwechselnd in Schrift- und Akzentfarbe, eng gesetzt.
        out, yy = [], y
        for i, w in enumerate(worte):
            t, _ = txt(w, g, sig.ink if i % 2 == 0 else sig.akzent, x, yy, BLK, .01)
            out.append(t)
            yy += g * .94
        return "".join(out), yy - g * .94

    raise ValueError("unbekannter Satz: " + satz)


# =========================================================================
#  Nachrechnen statt vertrauen
# =========================================================================
def _L(hexfarbe):
    h = hexfarbe.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def kontrast(a, b):
    la, lb = _L(a), _L(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def pruefe_signaturen(mindest_ink=4.5, mindest_akzent=3.0):
    """Jede Signatur nachrechnen.

    Die Schrift auf dem Grund muss Flie&szlig;text tragen (4,5:1), der Akzent
    mindestens als grosse Schrift und Linie erkennbar sein (3:1). Ohne diese
    Pruefung waere das Signatursystem eine Einladung, sich eine huebsche Farbe
    auszusuchen und die Lesbarkeit zu verlieren -- genau der Fehler, der die
    Niederlande-Edition unlesbar gemacht hat.
    """
    fehler = []
    for k, s in SIGNATUREN.items():
        ki = kontrast(s.ink, s.grund)
        ka = kontrast(s.akzent, s.grund)
        kl = kontrast(Signatur.LEISTE_INK, Signatur.LEISTE)
        if ki < mindest_ink:
            fehler.append(f"{k}: Schrift auf Grund nur {ki:.2f}:1")
        if ka < mindest_akzent:
            fehler.append(f"{k}: Akzent auf Grund nur {ka:.2f}:1")
        if kl < mindest_ink:
            fehler.append(f"{k}: Absenderleiste nur {kl:.2f}:1")
    return fehler


if __name__ == "__main__":
    print("%-12s %-9s %-9s %8s %8s   %s %s"
          % ("Signatur", "Grund", "Akzent", "Schrift", "Akzent", "Untergrund", "Satz"))
    print("-" * 78)
    for k, s in SIGNATUREN.items():
        print("%-12s %-9s %-9s %7.2f:1 %6.2f:1   %-13s %s"
              % (k, s.grund, s.akzent, kontrast(s.ink, s.grund),
                 kontrast(s.akzent, s.grund), s.untergrund, s.satz))
    f = pruefe_signaturen()
    print()
    print("\n".join(f) if f else "alle Signaturen tragen")

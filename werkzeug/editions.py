# -*- coding: utf-8 -*-
"""Profilbilder: Grundfassung und Sondereditionen.

Die Regel stammt aus den bestehenden Fassungen (1_Logo_Pride.png,
3_Logo_XMAS.png in S:\\06_VAR): der Hubschrauber bleibt immer Gold, veraendert
wird das **untere Feld** unter der Kante -- und bei Bedarf bekommt das obere
Feld ein Muster. Die Wortmarke nimmt die Farbe, die auf dem unteren Feld traegt.

Weil die Kante um -3,27 Grad gekippt ist, laufen auch die Streifen im unteren
Feld parallel dazu. Sonst entsteht ein zweiter, widersprechender Winkel.
"""
import os
from mark import (STRATOS, GALLIANO, IVORY, C, R, S, ANG, svg, disc,
                  heli_on_edge, word_max, uid, EDGE, CUT, BAR, FUGE)

KANTE_Y = EDGE + CUT

def feld(inhalt):
    """Inhalt ins untere Feld -- gedreht wie die Kante, an ihr abgeschnitten.

    Der Schnitt ist noetig: ohne ihn ragt zum Beispiel der senkrechte Balken des
    Schweizer Kreuzes nach oben in den Himmel hinein.
    """
    cid = uid("f")
    return (f'<defs><clipPath id="{cid}">'
            f'<rect x="{-S}" y="{KANTE_Y}" width="{S*3}" height="{S*2}" '
            f'transform="rotate({ANG:.3f} {C} {C})"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><g transform="rotate({ANG:.3f} {C} {C})">'
            f'<g transform="translate(0,{KANTE_Y})">{inhalt}</g></g></g>')

def streifen(farben, gewichte=None):
    """Streifen fuellen genau das sichtbare untere Feld.

    Vorher liefen sie ueber die Kreisunterkante hinaus -- bei drei Farben landete
    der dritte Streifen komplett ausserhalb des Zeichens.

    `gewichte` macht die Hoehen ungleich, und das ist seit dem Umbau des Zeichens
    noetig: die Wortmarke laeuft jetzt bis in den Rahmen und liegt damit auf
    *allen* Streifen. Bei der niederlaendischen Flagge gibt es keine
    Schriftfarbe, die auf Rot, Weiss und Blau zugleich traegt --

        Stratos  auf Rot 2,8   auf Weiss 18,4   auf Blau 1,6
        Ivory    auf Rot 5,4   auf Weiss  1,0   auf Blau 8,9

    -- also muss die Farbe, die keine traegt, so schmal werden, dass sie nur
    noch die Fuge zwischen den beiden anderen ist. Gemessen wurde das, nicht
    geschaetzt: gleich hohe Streifen lassen 46 % der Buchstabenflaeche unter
    3:1 verschwinden, die gewaehlten Hoehen 7 %.
    """
    gewichte = gewichte or [1] * len(farben)
    hoehe = S - KANTE_Y + 34
    summe = float(sum(gewichte))
    y, out = 0.0, []
    for c, g in zip(farben, gewichte):
        h = hoehe * g / summe
        out.append(f'<rect x="{-S}" y="{y:.2f}" width="{S*3}" height="{h+0.6:.2f}" '
                   f'fill="{c}"/>')
        y += h
    return "".join(out)

def flaeche(farbe):
    return f'<rect x="{-S}" y="0" width="{S*3}" height="{S*2}" fill="{farbe}"/>'

def oben(inhalt):
    """Muster ins obere Feld -- an der Kante abgeschnitten."""
    cid = uid("o")
    return (f'<defs><clipPath id="{cid}">'
            f'<rect x="{-S}" y="{-S}" width="{S*3}" height="{S+KANTE_Y}" '
            f'transform="rotate({ANG:.3f} {C} {C})"/>'
            f'</clipPath></defs><g clip-path="url(#{cid})">{inhalt}</g>')

def edition(unten, bar=IVORY, wort=IVORY, obenmuster="", bg=STRATOS, cid=None):
    cid = cid or uid("e")
    heli, barsvg, _ = heli_on_edge(444, C, KANTE_Y, GALLIANO, CUT, BAR, bar)
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{bg}"/>'
            + (oben(obenmuster) if obenmuster else "")
            + feld(unten) + heli + barsvg
            + word_max(wort, KANTE_Y + BAR + FUGE))
    return svg(disc(body, cid))

# ---------------------------------------------------------------- Muster
def muster(elemente, n=30, seed=7):
    import random
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(-20, S + 20), r.uniform(-20, KANTE_Y + 20)
        sc = r.uniform(0.7, 1.35)
        rot = r.uniform(-25, 25)
        out.append(f'<g transform="translate({x:.0f},{y:.0f}) scale({sc:.2f}) '
                   f'rotate({rot:.0f})" opacity="{r.uniform(.55,.95):.2f}">'
                   f'{r.choice(elemente)}</g>')
    return "".join(out)

GESCHENK = ('<rect x="-11" y="-9" width="22" height="18" fill="#E8C9A0"/>'
            '<rect x="-2.5" y="-9" width="5" height="18" fill="#C0392B"/>'
            '<rect x="-11" y="-1.5" width="22" height="4" fill="#C0392B"/>')
KERZE    = ('<rect x="-4" y="-8" width="8" height="18" fill="#E8C9A0"/>'
            '<rect x="-4" y="-8" width="8" height="18" fill="#C0392B" opacity=".45"/>'
            '<path d="M0,-14 q4,4 0,6 q-4,-2 0,-6" fill="#F5D76E"/>')
BEEREN   = ('<circle cx="-6" cy="0" r="4" fill="#FFFFFC"/>'
            '<circle cx="3" cy="-4" r="4" fill="#FFFFFC"/>'
            '<circle cx="4" cy="5" r="4" fill="#FFFFFC"/>')
BLATT    = '<path d="M0,-10 q9,10 0,20 q-9,-10 0,-20" fill="#2E6B4F"/>'
KUERBIS  = ('<ellipse cx="0" cy="0" rx="11" ry="9" fill="#E5720A"/>'
            '<rect x="-1.5" y="-13" width="3" height="5" fill="#2E6B4F"/>'
            '<path d="M-5,-2 l3,4 l-3,0 z M5,-2 l-3,4 l3,0 z" fill="#1A0E22"/>')
FLEDER   = ('<path d="M-12,0 q6,-7 6,2 q6,-9 12,0 q-6,4 -12,1 q-6,3 -6,-3 z" '
            'fill="#1A0E22"/>')
STERN    = '<circle r="1.8" fill="#FFFFFC"/>'
SPINNE   = ('<g stroke="#1A0E22" stroke-width="1.6" fill="none">'
            '<path d="M-9,-9 L9,9 M9,-9 L-9,9 M0,-12 L0,12 M-12,0 L12,0"/>'
            '<circle r="4"/><circle r="8"/><circle r="12"/></g>')
KNOCHEN  = ('<g fill="#E8E2D0"><rect x="-9" y="-2" width="18" height="4" rx="2"/>'
            '<circle cx="-10" cy="-3" r="3"/><circle cx="-10" cy="3" r="3"/>'
            '<circle cx="10" cy="-3" r="3"/><circle cx="10" cy="3" r="3"/></g>')

def netz(ecke="lo", r=170, n=5):
    """Spinnennetz in einer Ecke -- Speichen plus Boegen."""
    import math as _m
    x0, y0 = (0, 0) if ecke == "lo" else (S, 0)
    a0, a1 = (0, 90) if ecke == "lo" else (90, 180)
    out = []
    for k in range(n + 1):
        a = _m.radians(a0 + (a1 - a0) * k / n)
        out.append(f'M{x0},{y0} L{x0+_m.cos(a)*r:.1f},{y0+_m.sin(a)*r:.1f}')
    for j in range(1, 5):
        rr = r * j / 4
        pts = []
        for k in range(n + 1):
            a = _m.radians(a0 + (a1 - a0) * k / n)
            pts.append(f'{x0+_m.cos(a)*rr:.1f},{y0+_m.sin(a)*rr:.1f}')
        out.append("M" + " L".join(pts))
    return (f'<g stroke="#CFC7B4" stroke-width="1.6" fill="none" opacity=".5">'
            f'<path d="{" ".join(out)}"/></g>')

PRIDE = ["#E40303", "#FF8C00", "#FFED00", "#008026", "#004DFF", "#750787"]
DE    = ["#000000", "#DD0000", "#FFCE00"]
AT    = ["#ED2939", "#FFFFFF", "#ED2939"]

def _gold():
    """Invers: goldene Flaeche, Zeichen in Stratos."""
    h, b, _ = heli_on_edge(444, C, KANTE_Y, STRATOS, CUT, BAR, STRATOS)
    return svg(disc(f'<circle cx="{C}" cy="{C}" r="{R}" fill="{GALLIANO}"/>'
                    + h + b + word_max(STRATOS, KANTE_Y + BAR + FUGE), uid("g")))

E = {}
E["pb_standard"] = edition(flaeche(STRATOS), IVORY, IVORY)
E["pb_gold"]     = _gold()

# Pride -- Regenbogen unten, Wortmarke in Stratos, genau wie in eurer Fassung
E["pb_pride"] = edition(streifen(PRIDE), "#2B6EFF", STRATOS)

# Weihnachten -- Muster oben, rotes Feld unten
E["pb_weihnachten"] = edition(
    flaeche("#C0392B"), "#F08A80", IVORY,
    obenmuster=muster([GESCHENK, KERZE, BEEREN, BLATT], 30, 4), bg="#0E2E2B")

# Halloween -- Kuerbisse oben, oranges Feld unten
E["pb_halloween"] = edition(
    flaeche("#E5720A"), "#1A0E22", "#1A0E22",
    obenmuster=(netz("lo") + netz("ru")
                + muster([KUERBIS, KUERBIS, FLEDER, SPINNE, KNOCHEN], 26, 9)),
    bg="#1A0E22")

# Nationalfeiertage
# Gold traegt kein Ivory (2,3:1). Der Streifen wird deshalb schmaler, damit die
# Fuesse der Buchstaben ueberwiegend auf Rot stehen: 9 % unsichtbare Flaeche
# werden so zu 3 %.
E["pb_einheit"] = edition(streifen(DE, [40, 36, 24]), IVORY, IVORY)
E["pb_at"]      = edition(streifen(AT), IVORY, STRATOS)
# Schweiz -- Bergkette mit Matterhorn, die Flagge steckt in der Silhouette
BERGE = (
    # hintere Kette, blasser. Die Enden liegen weit ausserhalb des Kreises,
    # damit sie auch nach dem Verkleinern noch randabfallend sind.
    "M-300,300 L40,214 L86,246 L134,180 L182,238 L228,196 L268,242 L312,188 "
    "L352,236 L398,192 L446,244 L500,206 L820,300 Z"
)
# Das Matterhorn: steile Pyramide, Gipfel nach rechts gekippt
MATTERHORN = (
    "M96,306 L188,120 L206,96 L214,110 L206,132 L262,214 L318,306 Z"
)

def schweiz():
    """Rote Berge, weisses Kreuz darin -- alles auf die Silhouette beschnitten.

    Gezeichnet wurde die Kette fuer das alte, hoehere Himmelsfeld: Fusslinie
    bei y=303, 27 px ueber der damaligen Kante. Seit die Kante in der Mitte
    liegt, wird die ganze Silhouette um denselben Faktor verkleinert und so
    verschoben, dass der Abstand zur Kante gleich bleibt. Die Winkel des
    Matterhorns bleiben dabei unangetastet -- eine reine Stauchung haette es
    flacher gemacht, und die Steilheit ist der ganze Witz an dem Berg.

    Zusaetzlich steht die Kette 60 Einheiten links der Mitte. Seit der
    Hubschrauber bis an den Rand reicht, laege das Kreuz sonst hinter der Kabine
    und waere nur noch zur Haelfte zu sehen; links steht es ueber dem duennen
    Heckausleger frei.
    """
    cid = uid("chm")
    FUSS, ALT_KANTE = 303.0, 330.0
    f = KANTE_Y / ALT_KANTE                       # Himmel neu zu Himmel alt
    dy = (KANTE_Y - (ALT_KANTE - FUSS)) - FUSS    # Fusslinie auf gleichen Abstand
    kreuz = (f'<g transform="translate(202,206)">'
             f'<rect x="-13" y="-40" width="26" height="80" fill="#FFFFFC"/>'
             f'<rect x="-40" y="-13" width="80" height="26" fill="#FFFFFC"/></g>')
    return (
        f'<g transform="translate(-60,{dy:.2f}) translate({C},{FUSS}) scale({f:.4f}) translate({-C},{-FUSS})">'
        # hintere Kette in gedecktem Rot, damit die Tiefe stimmt
        f'<path d="{BERGE}" fill="#8E1F17" opacity=".85"/>'
        # Matterhorn mit Flagge darin
        f'<defs><clipPath id="{cid}"><path d="{MATTERHORN}"/></clipPath></defs>'
        f'<path d="{MATTERHORN}" fill="#DA291C"/>'
        f'<g clip-path="url(#{cid})">{kreuz}</g>'
        # Schneefeld auf der Nordflanke, ein Hauch
        f'<path d="M206,96 L214,110 L206,132 L232,170 L206,178 L188,120 Z" '
        f'fill="#FFFFFC" opacity=".30"/>'
        f'</g>')

E["pb_ch"] = edition(flaeche(STRATOS), IVORY, IVORY, obenmuster=schweiz())

# 24-Stunden-Event
E["pb_nacht"] = edition(
    flaeche("#0A1836"), "#2B6EFF", IVORY,
    obenmuster=muster([STERN], 70, 11), bg="#04091A")

# --- weitere Anlaesse -----------------------------------------------------
def burst(r=80, n=16, sw=6, farbe="#F5D76E", innen="#FFFFFC"):
    """Eine Feuerwerkskugel: Strahlen nach aussen, Funkenpunkte an den Spitzen.

    Grosszuegig dimensioniert, und das ist der ganze Punkt. Die alte Fassung
    streute sechsundzwanzig Raketen von je 28 Einheiten Breite in den Himmel --
    bei einem Profilbild von 40 px sind das zwei Pixel, also nichts. Silvester
    war dadurch von der Grundfassung nicht zu unterscheiden, und ein Anlass, den
    man nicht erkennt, ist keiner.

    Drei grosse Kugeln statt sechsundzwanzig kleiner: bei 40 px bleiben davon
    Formen uebrig, die man als Feuerwerk liest.
    """
    import math as _m
    strahlen, funken = [], []
    for i in range(n):
        a = 2 * _m.pi * i / n
        dx, dy = _m.cos(a), _m.sin(a)
        # Jeder zweite Strahl kuerzer -- eine Kugel mit lauter gleich langen
        # Strahlen sieht aus wie ein Zahnrad.
        rr = r if i % 2 == 0 else r * 0.62
        strahlen.append(f'M{dx*r*0.16:.1f},{dy*r*0.16:.1f} L{dx*rr:.1f},{dy*rr:.1f}')
        funken.append(f'<circle cx="{dx*rr:.1f}" cy="{dy*rr:.1f}" r="{sw*0.62:.1f}"/>')
    return (f'<g stroke="{farbe}" stroke-width="{sw}" stroke-linecap="round" '
            f'fill="none"><path d="{" ".join(strahlen)}"/></g>'
            f'<g fill="{farbe}">{"".join(funken)}</g>'
            f'<circle r="{sw*0.9:.1f}" fill="{innen}"/>')


def feuerwerk_himmel():
    """Drei Kugeln, dazu ein paar Funken. Sie stehen ueber dem Rotor, nicht
    dahinter -- der Hubschrauber reicht bis dicht an den Rand, und alles unter
    y=150 verschwaende hinter der Kabine."""
    return (f'<g transform="translate(118,104)">{burst(78, 16, 6.5)}</g>'
            f'<g transform="translate(360,72)" opacity=".95">'
            f'{burst(58, 12, 5.5, "#FFFFFC", "#F5D76E")}</g>'
            f'<g transform="translate(268,168)" opacity=".75">'
            f'{burst(44, 12, 4.5)}</g>'
            + muster([STERN], 26, 21))


E["pb_silvester"] = edition(
    flaeche("#12204A"), "#F5D76E", IVORY,
    obenmuster=feuerwerk_himmel(), bg="#070E24")


# Niederlande -- Lifeliner-Stationen
# Stratos verschwand im Blau -- 46 % der Buchstabenflaeche lagen unter 3:1.
# Ivory traegt auf Rot und Blau; das Weiss dazwischen bleibt als schmale Fuge
# stehen, damit die Flagge erkennbar bleibt, ohne die Schrift zu schlucken.
E["pb_nl"] = edition(streifen(["#AE1C28", "#FFFFFC", "#21468B"], [48, 4, 48]),
                     IVORY, IVORY)

# Jubilaeum -- der Hubschrauber ist die Kerze.
#
# Der Docht sitzt auf dem Rotorkopf, die Flamme brennt zwischen den Blaettern.
# Nichts steht vor dem Hubschrauber: der erste Anlauf stellte eine Ziffernkerze
# links auf die Kante und verdeckte damit den Heckausleger -- das Zeichen wird
# von der Kante angeschnitten und von sonst nichts. Die Ziffer steht links oben
# im Himmel, hinter allem, als Block-2 aus dem Anniversary-Satz (die Linien-2
# des Banners zerfaellt bei 128 px zur Schraffur, s. jubilaeum.py).
#
# Welches Jahr, steht in JUBILAEUM_JAHR; die bewegte Fassung nimmt dasselbe.
from jubilaeum import docht_und_flamme, ziffer
JUBILAEUM_JAHR = "2"

def _jubilaeum(bewegt=False):
    heli, barsvg, _ = heli_on_edge(444, C, KANTE_Y, GALLIANO, CUT, BAR, STRATOS)
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
            + oben(muster([STERN], 40, 33) + ziffer(JUBILAEUM_JAHR, bewegt))
            + feld(flaeche(GALLIANO)) + heli + barsvg
            + docht_und_flamme(bewegt)
            + word_max(STRATOS, KANTE_Y + BAR + FUGE))
    return svg(disc(body, uid("j")))

E["pb_jubilaeum"] = _jubilaeum()

# Leere Vorlage fuer den Generator
_h, _b, _ = heli_on_edge(444, C, KANTE_Y, GALLIANO, CUT, BAR, IVORY)
E["pb_vorlage"] = svg(disc(
    f'<circle cx="{C}" cy="{C}" r="{R}" fill="{STRATOS}"/>'
    + oben('<g id="muster-oben"></g>')
    + feld('<g id="feld-unten">'
           + f'<rect x="{-S}" y="0" width="{S*3}" height="{S*2}" fill="#141C31"/>'
           + "".join(f'<rect x="{i*44-S}" y="0" width="22" height="{S*2}" fill="#1C2740"/>'
                     for i in range(24)) + '</g>')
    + _h + _b + word_max(IVORY, KANTE_Y + BAR + FUGE), uid("v")))

if __name__ == "__main__":
    os.makedirs("neu", exist_ok=True)
    for k, v in E.items():
        open(f"neu/{k}.svg", "w", encoding="utf-8").write(v)
    print(f"{len(E)} Profilbilder:", ", ".join(E))

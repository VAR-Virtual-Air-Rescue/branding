# -*- coding: utf-8 -*-
"""Event-Banner nach dem Vorbild der bisherigen Aushaenge.

Grundlage sind vier Banner, die es schon gab -- THE LÄND, VAR OVERLOAD,
"Leitstellen für den Norden & NRW" und das Österreich-Event. Uebernommen ist
nicht ihr Aussehen, sondern das, was in ihnen funktioniert hat:

    Gebietssilhouette   Bundesland oder Land als Form, darin die Stationen als
                        nummerierte Marker. Das ist die staerkste Idee der
                        Vorlage: sie sagt in einem Bild, *wo* gespielt wird,
                        und wer seine Station darin findet, ist gemeint.
    Zulu und lokal      Zwei Zeiten nebeneinander. Bei VATSIM ist Zulu
                        verbindlich, aber niemand plant seinen Abend danach.
    Partnerlogo         Ein fester Platz dafuer. Auf dem alten Banner sass das
                        VATSIM-Logo frei im Bild; als Feld ist es keine
                        Verhandlung mehr.
    Reihentitel         Ein eigener Schriftzug fuer eine benannte Reihe, ohne
                        Foto. Traegt einen Wiedererkennungswert, den ein
                        Datumsbanner nicht aufbaut.

**Was bewusst nicht uebernommen wurde:** der Schlagschatten und das Leuchten
aus dem OVERLOAD-Banner. Schatten stehen im Brandbook unter den
Falschanwendungen, und ein Zeichen, das leuchtet, ist keins mehr. Der Versatz
kommt hier aus dem Markenwinkel -- dieselbe Wirkung, aus dem eigenen Bauteil.

Ebenso wenig uebernommen: die gelbe Flaeche des LÄND-Banners. Das Gelb dort ist
das Landesgelb von Baden-Wuerttemberg, nicht Galliano; nebeneinander sieht das
aus wie ein Druckfehler. Die Gebietsedition traegt deshalb Stratos und Gold.
"""
import io, json, os, sys, glob, re, math

from tpl import (svg, scene, scrim, badge, kante, kante_luft, feld,
                 absenderleiste, foto, txt, tw, uid, KANTE_STAERKE,
                 STRATOS, GALLIANO, IVORY, SIGNAL, INK, BOLD, REG, BLK)
from events import fuss, zeile, passt, bild, FORMATE

T = {}
HIER = os.path.dirname(os.path.abspath(__file__))
GEBIETE = json.load(io.open(os.path.join(HIER, "gebiete.json"), encoding="utf-8"))


# =========================================================================
#  Gebietssilhouette
# =========================================================================
def _grenzen(d):
    """Umschliessendes Rechteck eines Pfades aus lauter M-x,y-Ketten."""
    xs, ys = [], []
    for stueck in d.split("M")[1:]:
        for q in stueck.rstrip("Z").split():
            if "," in q:
                x, y = q.split(",")
                xs.append(float(x)); ys.append(float(y))
    return min(xs), min(ys), max(xs), max(ys)


def _kuerzel(name):
    """Was im Marker steht.

    Die Nummer, wenn es eine gibt -- "Christoph 53" wird zu "53". Sonst die
    ersten drei Buchstaben des letzten Wortes: "Christoph Ortenau" wird "ORT".
    Ausgeschrieben passt kein Name in einen Kreis von zwanzig Einheiten.
    """
    m = re.search(r"(\d+)\s*$", name)
    if m:
        return m.group(1)
    letzt = name.split()[-1] if name.split() else name
    return letzt[:3].upper()


def gebietskarte(schluessel, w, h, fuellung=IVORY, marker=True,
                 markerfarbe=GALLIANO, markerschrift=STRATOS, foto_datei=None):
    """Die Silhouette eines Gebiets, eingepasst in w x h, mit Stationsmarkern.

    `fuellung` ist die Flaechenfarbe; mit `foto_datei` wird stattdessen ein Bild
    in die Form geschnitten -- die Machart des Oesterreich-Banners.

    Der Massstab kommt aus dem Umriss, nicht aus den Markern: sonst zoege eine
    einzelne Station am Rand die ganze Karte klein.
    """
    g = GEBIETE["gebiete"][schluessel]
    x0, y0, x1, y1 = _grenzen(g["d"])
    sc = min(w / (x1 - x0), h / (y1 - y0))
    dx = (w - (x1 - x0) * sc) / 2 - x0 * sc
    dy = (h - (y1 - y0) * sc) / 2 - y0 * sc
    cid = uid("geb")

    if foto_datei is not None:
        # Ohne echtes Foto eine Kulisse in die Form schneiden. Waere hier die
        # Flaeche eingesetzt, saehen die beiden Macharten in der Vorlage gleich
        # aus -- und zwei identische Dateien sind keine Auswahl.
        inneres = (foto(w, h, foto_datei, 0, 0, w, h) if foto_datei
                   else scene(int(w), int(h), "alpine"))
        inhalt = (f'<defs><clipPath id="{cid}"><path d="{g["d"]}" '
                  f'transform="translate({dx:.1f},{dy:.1f}) scale({sc:.4f})"/>'
                  f'</clipPath></defs><g clip-path="url(#{cid})">{inneres}</g>'
                  # Ein feiner Rand, damit die Form auf dunklem Grund nicht
                  # ausfranst.
                  f'<path d="{g["d"]}" fill="none" stroke="{IVORY}" '
                  f'stroke-width="{2.2/sc:.2f}" opacity=".85" '
                  f'transform="translate({dx:.1f},{dy:.1f}) scale({sc:.4f})"/>')
    else:
        inhalt = (f'<path d="{g["d"]}" fill="{fuellung}" '
                  f'transform="translate({dx:.1f},{dy:.1f}) scale({sc:.4f})"/>')

    if not marker:
        return inhalt, g

    # Markergroesse am Massstab: auf einem 320 hohen Banner ist die Karte klein,
    # und ein Kreis mit fester Groesse verdeckte dort das halbe Gebiet.
    r = max(9.0, min(20.0, (x1 - x0) * sc * 0.045))

    punkte = []
    for sid in g.get("stationen", []):
        st = GEBIETE["stationen"].get(str(sid))
        if st:
            punkte.append((st["x"] * sc + dx, st["y"] * sc + dy, _kuerzel(st["name"])))

    # Wie eng stehen sie? Oesterreich hat 42 Stationen auf einer schmalen Form;
    # beschriftete Kreise ueberdecken sich dort gegenseitig und die Karte wird
    # zu einer Traube. Ab einem gewissen Gedraenge zaehlt nur noch, *dass* dort
    # eine Station ist -- die Nummer liest ohnehin niemand mehr.
    eng = False
    if len(punkte) > 1:
        naechste = []
        for i, (ax, ay, _) in enumerate(punkte):
            d = min(math.hypot(ax - bx, ay - by)
                    for j, (bx, by, _) in enumerate(punkte) if j != i)
            naechste.append(d)
        naechste.sort()
        eng = naechste[len(naechste) // 2] < r * 2.3

    teile = [inhalt]
    if eng:
        rp = max(3.0, r * 0.42)
        for mx, my, _ in punkte:
            teile.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{rp:.1f}" '
                         f'fill="{markerfarbe}" stroke="{markerschrift}" '
                         f'stroke-width="{rp*0.35:.1f}"/>')
    else:
        for mx, my, lab in punkte:
            # Die Beschriftung wird auf den Kreis eingepasst statt abgeschnitten
            # -- "ORT" ist breiter als "53".
            gr = passt(lab, r * 1.05, BLK, .0, r * 1.5)
            teile.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r:.1f}" '
                         f'fill="{markerfarbe}"/>')
            t, _ = txt(lab, gr, markerschrift, mx, my + gr * .36, BLK, .0, "middle")
            teile.append(t)
    return "".join(teile), g


def gebietsbanner(W, H, schluessel, kopf, datum, zeit, machart="flaeche",
                  rubrik="GEBIET", kulisse=None):
    """Bild und Text nebeneinander im Querformat, uebereinander im Hochformat.

    Die Karte bekommt die groessere Haelfte -- sie ist die Nachricht.
    """
    g = GEBIETE["gebiete"][schluessel]
    foot = fuss(H)
    y = H - foot
    luft = kante_luft(W)
    px = W * .06
    hoch = H > W * 1.05
    b = [f'<rect width="{W}" height="{H}" fill="{STRATOS}"/>']

    # `""` heisst: Form ausschneiden, aber es liegt kein Foto vor -- dann
    # kommt eine Kulisse hinein. `None` heisst: gefuellte Flaeche.
    datei = None
    if machart == "foto":
        datei = _FOTOS[0] if _FOTOS else ""

    if hoch:
        # Im Hochformat traegt die Karte den oberen Teil. Mit knapp der Haelfte
        # der Hoehe blieb unter dem Text ein leeres Drittel stehen.
        kw, kh = W * .92, (y - luft) * .58
        kx, ky = W * .04, H * .05
    else:
        kw, kh = W * .44, (y - luft) * .82
        kx, ky = W * .53, (y - luft - kh) / 2

    karte, _ = gebietskarte(schluessel, kw, kh,
                            fuellung=IVORY if machart == "flaeche" else IVORY,
                            markerfarbe=GALLIANO, markerschrift=STRATOS,
                            foto_datei=datei)
    b.append(f'<g transform="translate({kx:.0f},{ky:.0f})">{karte}</g>')

    # Text
    tb = (W - 2 * px) if hoch else (W * .44)
    ks = passt(kopf, (W * .085 if hoch else H * .115), BLK, .01, tb)
    zg = max(16, (W * .030 if hoch else H * .040))
    kick_g = max(14, (W * .024 if hoch else H * .026))

    if hoch:
        basis = ky + kh + H * .085
    else:
        basis = (y - luft) * .52

    zeile(b, g["name"].upper(), kick_g, GALLIANO, px, basis - ks * .82 - kick_g * .8,
          BOLD, .18)
    zeile(b, kopf, ks, IVORY, px, basis, BLK, .01)
    zeile(b, datum, zg, IVORY, px, basis + zg * 1.7, BOLD, .04)
    zeile(b, zeit, zg * .82, GALLIANO, px, basis + zg * 3.0, BOLD, .08)
    zeile(b, f'{len(g.get("stationen", []))} STATIONEN', kick_g, IVORY,
          px, basis + zg * 4.3, BOLD, .18, op=".70")

    b.append(absenderleiste(W, y, foot, right=rubrik))
    return svg(W, H, "".join(b))


# =========================================================================
#  Treffpunkt -- Zulu und lokal, Platz fuers Partnerlogo
# =========================================================================
def partnerfeld(w, h, x, y, beschriftung="PARTNERLOGO"):
    """Ein Feld, kein freistehendes Logo.

    Auf dem alten Banner sass das VATSIM-Logo frei auf der Flaeche, in seinem
    eigenen Blau. Als umrandetes Feld hat es eine Groesse und einen Ort, und
    fremde Farben stehen darin statt daneben.
    """
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<rect width="{w:.0f}" height="{h:.0f}" fill="{IVORY}" opacity=".08"/>'
            f'<rect width="{w:.0f}" height="{h:.0f}" fill="none" stroke="{IVORY}" '
            f'stroke-width="1.5" stroke-dasharray="6 5" opacity=".45"/>'
            f'{txt(beschriftung, min(h * .30, w * .13), IVORY, w / 2, h / 2 + h * .10, BOLD, .16, "middle", ".55")[0]}'
            f'</g>')


def datumsmarke(tag, monat, x, y, gr=34):
    """Tageszahl ueber Monat, in einem Kasten -- die Marke vom NRW-Banner."""
    bw = max(tw(tag, gr, BLK, .0), tw(monat, gr * .38, BOLD, .12)) + gr * .9
    bh = gr * 2.05
    t1, _ = txt(tag, gr, IVORY, bw / 2, gr * .95, BLK, .0, "middle")
    t2, _ = txt(monat, gr * .38, GALLIANO, bw / 2, gr * 1.60, BOLD, .12, "middle")
    return (f'<g transform="translate({x - bw:.0f},{y:.0f})">'
            f'<rect width="{bw:.0f}" height="{bh:.0f}" fill="{STRATOS}"/>'
            f'{t1}{t2}</g>'), bw, bh


def treffpunkt(W, H, kopf, zulu, lokal, ort, tag, monat, rubrik="OPS",
               kulisse=None, partner=True):
    """Bild, Zeiten, Partnerfeld -- und die Schlagzeile in einem eigenen Band.

    Der Aufbau folgt dem alten NRW-Banner: Bild links, Angaben rechts,
    Schlagzeile unten quer. Nur ist das Band unten hier die gekippte Flaeche der
    Marke und kein aufgesetzter Kasten.
    """
    foot = fuss(H)
    y = H - foot                       # Oberkante der Kante in der Bildmitte
    luft = kante_luft(W)
    px = W * .05
    hoch = H > W * 1.05
    b = [f'<rect width="{W}" height="{H}" fill="{GALLIANO}"/>']

    # Die Schlagzeile bekommt ein eigenes Band ueber der Kante. Alles andere
    # muss darueber bleiben -- deshalb wird ihre Hoehe zuerst bestimmt.
    kb = W - 2 * px
    ks = passt(kopf, H * (.075 if not hoch else .062), BLK, .01, kb)
    kopf_y = y - luft - H * .020
    frei = kopf_y - ks * .80           # ab hier abwaerts gehoert es der Zeile

    # --- Bildfeld ---------------------------------------------------------
    # Wie flach ist das Format? Bei 800 x 320 hat die rechte Spalte gerade Platz
    # fuer Datum und Zeiten -- ein Partnerfeld daneben landet darauf. Dann steht
    # es unter dem Bild, und das Bild wird dafuer kuerzer.
    flach = (not hoch) and H < W * .55
    # Auf dem flachen Format hat das Partnerfeld keinen Platz, ohne dass das
    # Foto zum Streifen wird. Dann lieber kein Feld als ein unkenntliches Bild.
    if flach:
        partner = False
    pw = min(W * .26, W - 2 * px)
    ph = pw * .34

    if hoch:
        bw, bh = W - 2 * px, (frei - H * .10) * .52
        bx, by = px, H * .07
    else:
        bw = W * .48
        bh = frei - H * .10 - ((ph + H * .05) if (flach and partner) else 0)
        bx, by = px, H * .06
    b.append(f'<g transform="translate({bx:.0f},{by:.0f})">{bild(bw, bh, kulisse)}</g>')

    # --- rechte Spalte ----------------------------------------------------
    tx = px if hoch else bx + bw + W * .045
    tb = (W - 2 * px) if hoch else (W - tx - px)

    dg = max(24, H * .050)
    dm, dbw, dbh = datumsmarke(tag, monat, W - px, H * .055, dg)
    b.append(dm)

    toben = (by + bh + H * .075) if hoch else (H * .055 + dbh + H * .075)
    zg = max(18, H * .046)
    zeile(b, "TREFFPUNKT", max(14, H * .026), STRATOS, tx, toben, BOLD, .18, op=".70")
    zeile(b, f"{zulu} ZULU", zg, STRATOS, tx, toben + zg * 1.35, BLK, .02)
    zeile(b, f"{lokal} LOKAL", zg * .78, STRATOS, tx, toben + zg * 2.45, BOLD, .04, op=".78")
    if ort:
        zeile(b, ort, max(15, H * .030), STRATOS, tx, toben + zg * 3.6, REG, .02, op=".82")

    # Das Partnerfeld sitzt unten in der rechten Spalte -- oberhalb des Bandes,
    # das der Schlagzeile gehoert.
    if partner:
        if flach:
            b.append(partnerfeld(pw, ph, bx, by + bh + H * .04))
        else:
            b.append(partnerfeld(pw, ph, tx, frei - ph - H * .035))

    b.append(absenderleiste(W, y, foot, right=rubrik))
    zeile(b, kopf, ks, STRATOS, px, kopf_y, BLK, .01)
    return svg(W, H, "".join(b))


# =========================================================================
#  Reihentitel -- der Schriftzug ist das Banner
# =========================================================================
def reihe(W, H, wort1, wort2, unter, rubrik="REIHE", invers=False):
    """VAR plus ein Wort, im Markenwinkel versetzt.

    Das Vorbild setzte die beiden Woerter mit Schlagschatten und Leuchten
    uebereinander. Beides steht im Brandbook unter den Falschanwendungen. Der
    Versatz kommt hier aus dem Winkel selbst: das zweite Wort sitzt auf der
    gekippten Linie und laeuft mit ihr nach rechts oben.
    """
    bg, w1c, w2c = (STRATOS, IVORY, GALLIANO) if not invers else (GALLIANO, STRATOS, IVORY)
    foot = fuss(H)
    y = H - foot
    px = W * .06
    b = [f'<rect width="{W}" height="{H}" fill="{bg}"/>']

    ug = max(16, H * .034)
    # Der Stapel ist: Wort, Linie, zweites Wort, Unterzeile. Er muss zwischen
    # den oberen Rand und die Kante passen -- sonst schiebt sich die Unterzeile
    # in das zweite Wort.
    platz = (y - kante_luft(W)) - H * .12 - (ug * 1.9 if unter else 0)
    gr = min(W * .17, H * .30, platz / 1.9)
    gr = passt(wort1 + wort2, gr, BLK, -.01, (W - 2 * px) * 1.02)
    hoehe = gr * 1.86 + (ug * 1.9 if unter else 0)
    mitte = max(H * .10 + gr * .72, (y - kante_luft(W) - hoehe) / 2 + gr * .72)
    b1 = tw(wort1, gr, BLK, -.01)

    # Die Linie zwischen beiden Woertern -- dasselbe Bauteil wie im Zeichen.
    b.append(kante(W, mitte + gr * .12, KANTE_STAERKE, w2c))

    t1, _ = txt(wort1, gr, w1c, px, mitte, BLK, -.01)
    b.append(t1)
    # Das zweite Wort haengt unter der Linie und beginnt, wo das erste endet.
    t2, _ = txt(wort2, gr, w2c, px + b1 + gr * .06, mitte + gr * .86, BLK, -.01)
    b.append(t2)

    if unter:
        b.append(txt(unter, ug, w1c, px, mitte + gr * .86 + ug * 1.9,
                     REG, .02, opacity=".80")[0])

    b.append(absenderleiste(W, y, foot, right=rubrik,
                            col=bg if invers else STRATOS,
                            kante_col=w2c, ink=w1c if invers else IVORY))
    return svg(W, H, "".join(b))


# =========================================================================
#  Die Vorlagen
# =========================================================================
_FOTOS = []
if "--fotos" in sys.argv:
    _FOTOS = sorted(glob.glob(os.path.join(sys.argv[sys.argv.index("--fotos") + 1], "*.jpg")))

# Ein Bundesland, ein Land -- damit beide Faelle in den Vorlagen stehen.
GEBIETSFAELLE = [
    ("bw", "BW", "ALLE STATIONEN IM LÄNDLE", "19. APRIL 2026", "15:00 – 21:00 UTC"),
    ("at", "AT", "ÖSTERREICH-EVENT", "20. JUNI 2026", "19:00 UTC"),
]

for fname, W, H in FORMATE:
    for kurz, schluessel, kopf, datum, zeit in GEBIETSFAELLE:
        T[f"event_gebiet_{kurz}_{fname}_flaeche"] = gebietsbanner(
            W, H, schluessel, kopf, datum, zeit, "flaeche")
    T[f"event_gebiet_bw_{fname}_foto"] = gebietsbanner(
        W, H, "BW", "ALLE STATIONEN IM LÄNDLE", "19. APRIL 2026",
        "15:00 – 21:00 UTC", "foto")

    T[f"event_treffpunkt_{fname}"] = treffpunkt(
        W, H, "LEITSTELLEN FÜR DEN NORDEN", "1100", "1200",
        "EDDH · EDDV · EDDW", "14.", "DEZEMBER")

    T[f"event_reihe_{fname}"] = reihe(
        W, H, "VAR", "OVERLOAD", "Wenn alle Melder gleichzeitig gehen.")
    T[f"event_reihe_{fname}_invers"] = reihe(
        W, H, "VAR", "NACHTFLUG", "Sechs Stunden, kein Tageslicht.", invers=True)


if __name__ == "__main__":
    os.makedirs("tpl", exist_ok=True)
    for k, v in T.items():
        open(f"tpl/{k}.svg", "w", encoding="utf-8").write(v)
    from tpl import FEHLENDE
    if FEHLENDE:
        print("FEHLENDE ZEICHEN:", sorted(FEHLENDE))
    print(f"{len(T)} Event-Banner")

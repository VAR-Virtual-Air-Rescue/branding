# -*- coding: utf-8 -*-
"""Umrisse der Einsatzgebiete -- Laender und deutsche Bundeslaender.

    python werkzeug/gebiete.py

Erzeugt `werkzeug/gebiete.json`: je Gebiet ein Umriss als SVG-Pfad, dazu die
Stationen, die darin liegen.

**Warum eine eigene Datei und nicht `karte.json` erweitern:** die Livekarte auf
der Website braucht Laendergrenzen und laedt sie in jede Seite. Bundeslaender
braucht sie nicht; sie hier hineinzuschreiben machte die Seite groesser, ohne
dass jemand etwas davon haette.

**Dieselbe Projektion wie `livekarte.py`.** Das ist keine Kosmetik: die
Stationskoordinaten in `karte.json` liegen bereits im projizierten Raum
(1000 x 1087). Ein anderer Kartenausschnitt hier, und Umriss und Marker lieferten
zwei verschiedene Karten uebereinander.

Quelle: Natural Earth (gemeinfrei), 10-m-Datensatz fuer die Bundeslaender --
der 110-m-Satz kennt nur Staaten.
"""
import io, json, math, os, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HIER, "gebiete.json")
KARTE = os.path.join(HIER, "karte.json")

NE_LAND = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
           "master/geojson/ne_10m_admin_1_states_provinces.geojson")

# Wie in livekarte.py, Wort fuer Wort -- die beiden muessen zusammenpassen.
LON0, LON1 = 2.0, 18.0
LAT0, LAT1 = 44.5, 55.6
BREITE = 1000.0


def merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


Y_OBEN, Y_UNTEN = merc(LAT1), merc(LAT0)
SPANNE_X = LON1 - LON0
SPANNE_Y = Y_OBEN - Y_UNTEN
HOEHE = BREITE * SPANNE_Y / math.radians(SPANNE_X)


def proj(lon, lat):
    return ((lon - LON0) / SPANNE_X * BREITE,
            (Y_OBEN - merc(lat)) / SPANNE_Y * HOEHE)


def vereinfache(p, eps):
    """Douglas-Peucker. Feiner als in der Livekarte (0,8 statt 2,2): ein
    Bundesland wird auf einem Banner gross gezeigt, ein Land nur klein."""
    if len(p) < 3:
        return p
    ax, ay = p[0]; bx, by = p[-1]
    dx, dy = bx - ax, by - ay
    lg = math.hypot(dx, dy)
    weit, idx = 0.0, 0
    for i in range(1, len(p) - 1):
        px, py = p[i]
        d = (math.hypot(px - ax, py - ay) if lg == 0
             else abs(dy * px - dx * py + bx * ay - by * ax) / lg)
        if d > weit:
            weit, idx = d, i
    if weit <= eps:
        return [p[0], p[-1]]
    return vereinfache(p[:idx + 1], eps)[:-1] + vereinfache(p[idx:], eps)


def im_ring(x, y, ring):
    """Strahlensatz: liegt der Punkt im Polygon?

    Wird gebraucht, um jeder Station ihr Gebiet zuzuordnen. Ueber ein
    umschliessendes Rechteck ginge es nicht -- Bayern und Baden-Wuerttemberg
    ueberlappen sich in ihren Rechtecken betraechtlich.
    """
    drin = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xs = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xs:
                drin = not drin
    return drin


def hole(url):
    req = urllib.request.Request(url, headers={"User-Agent": "VAR-Brand-Build"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


# Was gezeigt werden soll. Die Schluessel sind das, was in der Vorlage steht.
BUNDESLAENDER = {
    "BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin",
    "BB": "Brandenburg", "HB": "Bremen", "HH": "Hamburg", "HE": "Hessen",
    "MV": "Mecklenburg-Vorpommern", "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz", "SL": "Saarland",
    "SN": "Sachsen", "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein",
    "TH": "Thüringen",
}
# Ganze Staaten kommen aus der Livekarte -- dort liegen sie schon projiziert.
STAATEN = {"DE": "Deutschland", "AT": "Österreich", "CH": "Schweiz",
           "NL": "Niederlande", "LU": "Luxemburg", "IT": "Italien"}


def main():
    sys.setrecursionlimit(20000)
    karte = json.load(io.open(KARTE, encoding="utf-8"))
    stationen = karte["stationen"]

    gebiete = {}

    # --- Staaten: Pfade aus karte.json uebernehmen ------------------------
    for L in karte["laender"]:
        if L["i"] in STAATEN:
            gebiete[L["i"]] = {"name": STAATEN[L["i"]], "art": "staat", "d": L["d"]}

    # --- Bundeslaender: aus Natural Earth ---------------------------------
    print("Bundeslaender laden (rund 38 MB) ...")
    geo = hole(NE_LAND)
    nach_name = {v: k for k, v in BUNDESLAENDER.items()}
    gefunden = 0
    for f in geo["features"]:
        p = f["properties"]
        if (p.get("iso_a2") or p.get("adm0_a3")) not in ("DE", "DEU"):
            continue
        name = p.get("name") or ""
        kuerzel = nach_name.get(name)
        if not kuerzel:
            continue
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        teile, ringe = [], []
        for poly in polys:
            ring = poly[0]
            if len(ring) < 6:
                continue
            pts = [proj(lo, la) for lo, la in ring]
            r = vereinfache(pts, 0.8)
            if len(r) >= 3:
                teile.append("M" + " ".join("%.1f,%.1f" % q for q in r) + "Z")
                ringe.append(r)
        if not teile:
            continue
        drin = [s for s in stationen if any(im_ring(s[2], s[3], r) for r in ringe)]
        gebiete[kuerzel] = {"name": name, "art": "bundesland", "d": "".join(teile),
                            "stationen": [s[0] for s in drin]}
        gefunden += 1
        print("  %-3s %-24s %2d Stationen" % (kuerzel, name, len(drin)))

    # --- Stationen der Staaten ueber die Landespfade ----------------------
    # Fuer Staaten liegen nur die vereinfachten Pfade vor; die Zuordnung geht
    # deshalb ueber dieselbe Punktprobe, nur auf den groberen Ringen.
    for iso, g in gebiete.items():
        if g["art"] != "staat":
            continue
        ringe = []
        for stueck in g["d"].split("M")[1:]:
            pts = [tuple(map(float, q.split(","))) for q in
                   stueck.rstrip("Z").split() if "," in q]
            if len(pts) >= 3:
                ringe.append(pts)
        drin = [s for s in stationen if any(im_ring(s[2], s[3], r) for r in ringe)]
        g["stationen"] = [s[0] for s in drin]
        print("  %-3s %-24s %2d Stationen" % (iso, g["name"], len(drin)))

    daten = {
        "quelle": "Natural Earth, gemeinfrei",
        "proj": karte["proj"],
        "stationen": {str(s[0]): {"name": s[1], "x": s[2], "y": s[3]} for s in stationen},
        "gebiete": gebiete,
    }
    io.open(ZIEL, "w", encoding="utf-8").write(
        json.dumps(daten, ensure_ascii=False, separators=(",", ":")))
    print("\n%d Gebiete, %d KB" % (len(gebiete), os.path.getsize(ZIEL) // 1024))


if __name__ == "__main__":
    main()

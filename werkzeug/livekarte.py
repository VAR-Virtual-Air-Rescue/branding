# -*- coding: utf-8 -*-
"""Grundlage der Livekarte auf der Website: Umrisse und Stationen.

Was hier **eingebacken** wird, ist der unveraenderliche Teil -- Laendergrenzen
und Stationsstandorte. Die Luftfahrzeuge kommen zur Laufzeit dazu.

Bewusst groeber als die Karte in der Wissensdatenbank: die Seite traegt alles
inline und soll klein bleiben. Deshalb der 110-m-Datensatz von Natural Earth
und eine kraeftigere Vereinfachung.

Quellen
  Stationen  ops.virtualairrescue.com/api/stations  (oeffentlich lesbar)
  Umrisse    Natural Earth, gemeinfrei

Aufruf:  python livekarte.py [--stand JJJJ-MM-TT]
"""
import io, json, math, os, re, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HIER, "..", "..", "web", "karte.json")

API = "https://ops.virtualairrescue.com/api/stations"
NE = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
      "master/geojson/ne_110m_admin_0_countries.geojson")

EINSATZ = {"DE", "AT", "CH", "NL", "LU", "LI", "IT"}
NACHBARN = {"FR", "CZ", "PL", "DK", "SI", "BE", "SK", "HU", "HR"}

LON0, LON1 = 2.0, 18.0
LAT0, LAT1 = 44.5, 55.6
BREITE = 1000.0

# Eintraege, die nicht in eine Veroeffentlichung gehoeren -- dieselbe Regel wie
# in der Wissensdatenbank.
RAUS = re.compile("NICHT NUTZEN|DEV[ ]*[0-9]|(^|[ ])Test([ ]|$)", re.I)


def merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


Y_OBEN, Y_UNTEN = merc(LAT1), merc(LAT0)
SPANNE_X = LON1 - LON0
SPANNE_Y = Y_OBEN - Y_UNTEN
HOEHE = BREITE * SPANNE_Y / math.radians(SPANNE_X)


def proj(lon, lat):
    return ((lon - LON0) / SPANNE_X * BREITE,
            (Y_OBEN - merc(lat)) / SPANNE_Y * HOEHE)


def hole(url):
    req = urllib.request.Request(url, headers={"User-Agent": "VAR-Website-Build"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def vereinfache(p, eps):
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


print("Stationen ...")
roh = hole(API)
stationen = []
for s in roh:
    if s.get("latitude") is None or s.get("longitude") is None:
        continue
    if RAUS.search((s.get("bosCallsign") or "") + " " + (s.get("bosCallsignShort") or "")):
        continue
    if not (LAT0 <= s["latitude"] <= LAT1 and LON0 <= s["longitude"] <= LON1):
        continue
    x, y = proj(s["longitude"], s["latitude"])
    stationen.append([s.get("id"), s.get("bosCallsign") or "", round(x, 1), round(y, 1)])

print("  %d Stationen" % len(stationen))

print("Umrisse ...")
geo = hole(NE)
sys.setrecursionlimit(10000)
laender = []
for f in geo["features"]:
    p = f["properties"]
    iso = p.get("ISO_A2_EH") or p.get("ISO_A2") or ""
    if iso not in EINSATZ | NACHBARN:
        continue
    g = f["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    teile = []
    for poly in polys:
        ring = poly[0]
        lons = [c[0] for c in ring]; lats = [c[1] for c in ring]
        if max(lons) < LON0 - 2 or min(lons) > LON1 + 2:
            continue
        if max(lats) < LAT0 - 2 or min(lats) > LAT1 + 2:
            continue
        if len(ring) < 6:
            continue
        pts = [proj(min(max(lo, LON0 - 2), LON1 + 2),
                    min(max(la, LAT0 - 2), LAT1 + 2)) for lo, la in ring]
        r = vereinfache(pts, 2.2)
        if len(r) >= 3:
            teile.append("M" + " ".join("%.0f,%.0f" % q for q in r) + "Z")
    if teile:
        laender.append({"i": iso, "e": iso in EINSATZ, "d": "".join(teile)})

daten = {
    "stand": (sys.argv[sys.argv.index("--stand") + 1] if "--stand" in sys.argv else None),
    # Damit das Skript in der Seite Live-Positionen selbst projizieren kann.
    "proj": {"lon0": LON0, "lon1": LON1, "yOben": round(Y_OBEN, 8),
             "spanneY": round(SPANNE_Y, 8), "breite": round(BREITE, 1),
             "hoehe": round(HOEHE, 1)},
    "laender": laender,
    "stationen": stationen,
}

os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, separators=(",", ":")))
print()
print("geschrieben: %s  (%.0f KB)" % (os.path.normpath(ZIEL), os.path.getsize(ZIEL) / 1024))
print("  %d Laender, %d Stationen, Bild %.0f x %.0f"
      % (len(laender), len(stationen), BREITE, HOEHE))

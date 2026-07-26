# -*- coding: utf-8 -*-
"""Halloween neu: sichtbare Spinne, kraeftigere Kontraste, echte Bewegung.

Vorher war die Spinne rund 34 px in einem 512er Zeichen -- als Discord-Icon
also gut acht Pixel. Und animiert bewegten sich nur der Glimmkern und ein
kaum wahrnehmbarer Schwung. Beides ist jetzt deutlich groesser und schneller.
"""
p = "anim.py"
s = open(p, encoding="utf-8").read()

a = s.index("# ---------------------------------------------------------------- Kuerbis")
b = s.index("# ---------------------------------------------------------------- Animiert")

NEU = '''# ---------------------------------------------------------------- Kuerbis
KUERBIS_HELL = "#F07C10"
KUERBIS_TIEF = "#B14E04"
SCHNITT      = "#14090E"
GLIMM        = "#FFC24A"
FADEN        = "#E8E2D4"

def rippen(farbe=KUERBIS_TIEF, opa=".5", breite=11):
    """Kuerbisrippen: Boegen ueber die ganze Scheibe."""
    out = []
    for i in range(1, 7):
        t = i / 7
        x = S * t
        bow = (t - .5) * 2
        rx = abs(bow) * S * 0.46 + 8
        out.append(f'<path d="M{x:.0f},-10 C{x - bow*rx:.0f},{S*.3:.0f} '
                   f'{x - bow*rx:.0f},{S*.7:.0f} {x:.0f},{S+10:.0f}" '
                   f'fill="none" stroke="{farbe}" stroke-width="{breite}" '
                   f'opacity="{opa}" stroke-linecap="round"/>')
    return "".join(out)

def stiel():
    return (f'<g transform="translate({C},22)">'
            f'<path d="M-15,30 C-13,4 -6,-10 0,-17 C7,-8 13,4 15,30 Z" fill="#3E6B34"/>'
            f'<path d="M0,-16 C12,-28 26,-26 31,-13" fill="none" stroke="#3E6B34" '
            f'stroke-width="8" stroke-linecap="round"/></g>')

def netz(ecke, r, speichen, boegen, opa=".72"):
    """Spinnennetz -- links und rechts bewusst unterschiedlich gross."""
    x0, y0 = (0, 0) if ecke == "lo" else (S, 0)
    a0, a1 = (0, 90) if ecke == "lo" else (90, 180)
    d = []
    for k in range(speichen + 1):
        w = math.radians(a0 + (a1 - a0) * k / speichen)
        d.append(f'M{x0},{y0} L{x0+math.cos(w)*r:.1f},{y0+math.sin(w)*r:.1f}')
    for j in range(1, boegen + 1):
        rr = r * j / boegen
        pts = []
        for k in range(speichen + 1):
            w = math.radians(a0 + (a1 - a0) * k / speichen)
            pts.append(f'{x0+math.cos(w)*rr:.1f},{y0+math.sin(w)*rr:.1f}')
        d.append("M" + " L".join(pts))
    return (f'<g stroke="{FADEN}" stroke-width="2.2" fill="none" opacity="{opa}">'
            f'<path d="{" ".join(d)}"/></g>')

def faeden():
    """Spinnfaeden vom Kreisrand zum Hubschrauber -- er haengt selbst im Netz."""
    ziele  = [(150, 216), (272, 196), (378, 210)]
    aussen = [(22, 40),   (198, -8),  (486, 58)]
    out = []
    for (ax, ay), (zx, zy) in zip(aussen, ziele):
        mx, my = (ax + zx) / 2, (ay + zy) / 2 + 22
        out.append(f'<path d="M{ax},{ay} Q{mx:.0f},{my:.0f} {zx},{zy}" fill="none" '
                   f'stroke="{FADEN}" stroke-width="2" opacity=".62"/>')
        for t in (.34, .64):
            px = ax + (zx - ax) * t
            py = ay + (zy - ay) * t + 15
            out.append(f'<path d="M{px-14:.0f},{py-6:.0f} Q{px:.0f},{py+7:.0f} '
                       f'{px+14:.0f},{py-6:.0f}" fill="none" stroke="{FADEN}" '
                       f'stroke-width="1.6" opacity=".45"/>')
    return "".join(out)

SPINNE_KOERPER = (
    '<ellipse cx="0" cy="4" rx="17" ry="21" fill="#0E0710"/>'
    '<circle cx="0" cy="-19" r="11.5" fill="#0E0710"/>'
    '<g stroke="#0E0710" stroke-width="4.6" stroke-linecap="round" fill="none">'
    '<path d="M-13,-6 C-27,-14 -34,-24 -33,-33"/>'
    '<path d="M-15,2 C-31,-1 -40,-6 -42,-14"/>'
    '<path d="M-15,11 C-31,14 -38,21 -39,30"/>'
    '<path d="M-11,19 C-22,28 -26,38 -24,47"/>'
    '<path d="M13,-6 C27,-14 34,-24 33,-33"/>'
    '<path d="M15,2 C31,-1 40,-6 42,-14"/>'
    '<path d="M15,11 C31,14 38,21 39,30"/>'
    '<path d="M11,19 C22,28 26,38 24,47"/></g>'
    '<circle cx="-4.6" cy="-21" r="3.4" fill="#FF9A1E"/>'
    '<circle cx="4.6" cy="-21" r="3.4" fill="#FF9A1E"/>'
    '<circle cx="-4.6" cy="-21" r="1.4" fill="#14090E"/>'
    '<circle cx="4.6" cy="-21" r="1.4" fill="#14090E"/>')

def spinne(x, faden, animiert=False):
    """Haengende Spinne. Der Schwung dreht um den Aufhaengepunkt, nicht um sie selbst."""
    schwung = ('<animateTransform attributeName="transform" type="rotate" '
               'values="-15 0 0;15 0 0;-15 0 0" dur="3.4s" repeatCount="indefinite" '
               'calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>'
               ) if animiert else ""
    ab = ('<animateTransform attributeName="transform" type="translate" '
          'values="0 0;0 18;0 0" dur="5.1s" repeatCount="indefinite" '
          'calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" '
          'additive="sum"/>') if animiert else ""
    # Aeussere Gruppe traegt die Position, die innere die Bewegung. Ein
    # animateTransform ohne additive ersetzt sonst das transform der Gruppe --
    # die Spinne landet dann am linken Bildrand.
    return (f'<g transform="translate({x},0)"><g>{schwung}{ab}'
            f'<line x1="0" y1="0" x2="0" y2="{faden}" stroke="{FADEN}" '
            f'stroke-width="2.2" opacity=".8"/>'
            f'<g transform="translate(0,{faden+22})">{SPINNE_KOERPER}</g></g></g>')

def fledermaus(x0, y0, x1, y1, dauer, verzug, gross=1.0):
    """Fledermaus fliegt durchs Bild, Fluegel schlagen."""
    fl = ('<path d="M-26,0 C-17,-13 -9,-9 0,0 C9,-9 17,-13 26,0 '
          'C17,5 9,3 0,9 C-9,3 -17,5 -26,0 Z" fill="#160A14">'
          '<animate attributeName="d" dur="0.42s" repeatCount="indefinite" '
          'values="M-26,0 C-17,-13 -9,-9 0,0 C9,-9 17,-13 26,0 C17,5 9,3 0,9 '
          'C-9,3 -17,5 -26,0 Z;'
          'M-22,-9 C-15,-20 -8,-13 0,-3 C8,-13 15,-20 22,-9 C15,-1 8,-1 0,6 '
          'C-8,-1 -15,-1 -22,-9 Z;'
          'M-26,0 C-17,-13 -9,-9 0,0 C9,-9 17,-13 26,0 C17,5 9,3 0,9 '
          'C-9,3 -17,5 -26,0 Z"/></path>')
    return (f'<g opacity="0"><g transform="scale({gross})">{fl}</g>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="{x0} {y0};{x1} {y1}" dur="{dauer}s" begin="{verzug}s" '
            f'repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;0.12;0.85;1" dur="{dauer}s" begin="{verzug}s" '
            f'repeatCount="indefinite"/></g>')

def halloween(animiert=False):
    """Das Icon selbst ist der Kuerbis: Rippen, Stiel, Glimmkern, ausgeschnittene Marke."""
    heli, bar, _ = heli_on_edge(418, C, KANTE_Y, SCHNITT, CUT, BAR, "#6B3402")
    puls = ('<animate attributeName="opacity" values=".22;.62;.22" dur="2.4s" '
            'repeatCount="indefinite"/>') if animiert else ""
    tiere = (fledermaus(-60, 96, S + 60, 62, 7.5, 0.0, 1.0)
             + fledermaus(S + 60, 168, -60, 132, 9.5, 3.2, 0.72)) if animiert else \\
            muster([FLEDER], 5, 3)
    body = (f'<circle cx="{C}" cy="{C}" r="{R}" fill="{KUERBIS_HELL}"/>'
            + rippen()
            # Glimmkern direkt hinter der Marke, damit der Schnitt beleuchtet wirkt
            + f'<ellipse cx="{C}" cy="{S*.40:.0f}" rx="{R*.86:.0f}" ry="{R*.52:.0f}" '
              f'fill="{GLIMM}" opacity=".22">{puls}</ellipse>'
            + stiel()
            + oben(netz("lo", 206, 6, 4) + netz("ru", 132, 4, 3, ".52")
                   + faeden()
                   + muster([KUERBIS, KNOCHEN], 7, 9)
                   + tiere
                   + spinne(int(S * .74), 118, animiert))
            + feld(flaeche(KUERBIS_TIEF) + rippen("#7E3603", ".42"))
            + heli + bar
            + word_max(KANTE_Y + BAR + 6, SCHNITT))
    return svg(disc(body, uid("h")))

'''
s = s[:a] + NEU + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("Halloween neu geschrieben")

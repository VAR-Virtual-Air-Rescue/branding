# -*- coding: utf-8 -*-
"""Ueberarbeitet die Animationen nach der Rueckmeldung."""
p = "anim.py"
s = open(p, encoding="utf-8").read()

# --- Halloween: dunkler Hubschrauber, Faeden vom Rand zum Heli --------------
s = s.replace('    heli, bar, _ = heli_on_edge(418, C, KANTE_Y, GLUT, CUT, BAR, NACHT)',
              '    heli, bar, _ = heli_on_edge(418, C, KANTE_Y, NACHT, CUT, BAR, "#7A3B02")')

s = s.replace('''            + oben(netz("lo", 194, 6, 4, ".55") + netz("ru", 126, 4, 3, ".38")
                   + muster([KUERBIS, FLEDER, KNOCHEN], 12, 9)
                   + spinne(int(S * .70), 0, 92, animiert))''',
'''            + oben(netz("lo", 194, 6, 4, ".5") + netz("ru", 126, 4, 3, ".34")
                   + faeden()
                   + muster([KUERBIS, FLEDER, KNOCHEN], 10, 9)
                   + spinne(int(S * .68), 0, 104, animiert))''')

FAEDEN = '''def faeden():
    """Spinnfaeden vom Kreisrand zum Hubschrauber -- er haengt selbst im Netz."""
    ziele  = [(150, 216), (268, 198), (372, 210), (206, 234)]
    aussen = [(26, 44),   (198, -6),  (474, 66),  (14, 172)]
    out = []
    for (ax, ay), (zx, zy) in zip(aussen, ziele):
        mx, my = (ax + zx) / 2, (ay + zy) / 2 + 20
        out.append(f'<path d="M{ax},{ay} Q{mx:.0f},{my:.0f} {zx},{zy}" fill="none" '
                   f'stroke="#CFC7B4" stroke-width="1.3" opacity=".45"/>')
        for t in (.34, .62):
            px = ax + (zx - ax) * t
            py = ay + (zy - ay) * t + 13
            out.append(f'<path d="M{px-11:.0f},{py-5:.0f} Q{px:.0f},{py+6:.0f} '
                       f'{px+11:.0f},{py-5:.0f}" fill="none" stroke="#CFC7B4" '
                       f'stroke-width="1.1" opacity=".33"/>')
    return "".join(out)

def halloween(animiert=False):'''
s = s.replace("def halloween(animiert=False):", FAEDEN)

# --- Pride: Welle laeuft von links nach rechts ------------------------------
a = s.index("# Pride -- die Streifen wandern")
b = s.index("# Weihnachten -- Schnee faellt")
PRIDE_NEU = '''# Pride -- die Fahne schwingt, die Welle laeuft von links nach rechts
def pride_welle(spalten=22):
    """Senkrechte Streifen der Flaeche, jede Spalte mit eigener Phase."""
    br = S / spalten
    st = streifen(PRIDE)
    teile = []
    for i in range(spalten):
        cid = uid("pw")
        teile.append(
            f'<defs><clipPath id="{cid}"><rect x="{i*br-0.4:.2f}" y="-60" '
            f'width="{br+0.8:.2f}" height="{S*2}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><g>{st}'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 -8;0 8;0 -8" dur="2.6s" begin="{-(i/spalten)*2.6:.2f}s" '
            f'repeatCount="indefinite" calcMode="spline" '
            f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/></g></g>')
    return "".join(teile)

A["pb_pride_anim"] = bewegt(
    STRATOS, GALLIANO, "#2B6EFF", STRATOS, "", feld(pride_welle()))

'''
s = s[:a] + PRIDE_NEU + s[b:]

# --- Weihnachten: groessere Flocken ----------------------------------------
s = s.replace('r="{1.8+(i%3)*1.1:.1f}" ', 'r="{3.6+(i%4)*1.6:.1f}" ')
s = s.replace('repeatCount="indefinite"/></circle>\' for i in range(40))',
              'repeatCount="indefinite"/></circle>\' for i in range(26))')

# --- Jahreswechsel: Rakete, Explosion, Jahreszahl aus Funken ---------------
a = s.index("# Jahreswechsel -- Raketen zuenden")
b = s.index("# 24-Stunden-Event")
SILV = '''# Jahreswechsel -- die Rakete steigt, explodiert, die Jahreszahl bleibt stehen
from text2path import text_path
import random as _rd

def feuerwerk(jahr="2027", dauer=6.0):
    bx, by = C, 122
    t_auf = 1.3
    teile = []
    # Aufstieg von der Kante nach oben
    teile.append(
        f'<circle r="3.4" fill="#FFE9A8" cx="{bx}" cy="{KANTE_Y}" opacity="0">'
        f'<animate attributeName="cy" values="{KANTE_Y};{by}" dur="{t_auf}s" '
        f'begin="0s;{dauer}s" calcMode="spline" keySplines="0.2 0.7 0.4 1" '
        f'fill="remove"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.9;1" '
        f'dur="{t_auf}s" begin="0s;{dauer}s" fill="remove"/></circle>')
    # Explosion
    for k in range(24):
        aw = k / 24 * 6.2832
        rr = 76 + (k % 4) * 18
        teile.append(
            f'<circle cx="{bx}" cy="{by}" r="2.6" fill="#F5D76E" opacity="0">'
            f'<animate attributeName="cx" values="{bx};{bx+math.cos(aw)*rr:.0f}" '
            f'dur="1.2s" begin="{t_auf}s;{dauer+t_auf}s" fill="remove"/>'
            f'<animate attributeName="cy" '
            f'values="{by};{by+math.sin(aw)*rr*.72+30:.0f}" '
            f'dur="1.2s" begin="{t_auf}s;{dauer+t_auf}s" fill="remove"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;.05;.45;1" dur="1.2s" begin="{t_auf}s;{dauer+t_auf}s" '
            f'fill="remove"/></circle>')
    # Jahreszahl
    d, br = text_path(jahr, "fonts/Uniform Bold.ttf", 74, 0.06)
    teile.append(
        f'<g fill="#FFE9A8" opacity="0" transform="translate({C-br/2:.0f},{by+40})">'
        f'{d}<animate attributeName="opacity" values="0;1;1;0" '
        f'keyTimes="0;.12;.8;1" dur="{dauer-t_auf-0.4:.1f}s" '
        f'begin="{t_auf+0.4:.1f}s;{dauer+t_auf+0.4:.1f}s" fill="remove"/></g>')
    # Funken um die Zahl
    r = _rd.Random(5)
    for k in range(28):
        px = C - br / 2 + r.uniform(0, br)
        py = by + 40 + r.uniform(-48, 12)
        teile.append(
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(1.2,2.8):.1f}" '
            f'fill="#FFD24A" opacity="0">'
            f'<animate attributeName="opacity" values="0;.95;0" dur="1.5s" '
            f'begin="{t_auf+0.5+r.uniform(0,2.6):.2f}s" '
            f'repeatCount="indefinite"/></circle>')
    return "".join(teile)

A["pb_silvester_anim"] = bewegt(
    "#070E24", GALLIANO, "#F5D76E", IVORY,
    muster([STERN], 18, 21) + feuerwerk(), feld(flaeche("#12204A")))

'''
s = s[:a] + SILV + s[b:]

# --- 24 Stunden: Sternenbild wandert ---------------------------------------
a = s.index("# 24-Stunden-Event")
b = s.index("if __name__ ==")
NACHT_NEU = '''# 24-Stunden-Event -- das Sternenbild wandert durch, dazu Funkeln
def sternfeld(n=44, versatz=0):
    return "".join(
        f'<circle cx="{(i*97)%S + versatz}" cy="{(i*53)%308}" '
        f'r="{1.6+(i%3)*.7:.1f}" fill="#FFFFFC" opacity=".25">'
        f'<animate attributeName="opacity" values=".14;.95;.14" '
        f'dur="{2.4+(i%6)*.6:.1f}s" begin="{(i%9)*.35:.2f}s" '
        f'repeatCount="indefinite"/></circle>' for i in range(n))

_himmel = (f'<g>{sternfeld(44, 0)}{sternfeld(44, S)}'
           f'<animateTransform attributeName="transform" type="translate" '
           f'from="0 0" to="{-S} 0" dur="48s" repeatCount="indefinite"/></g>')
_schimmer = (f'<g transform="rotate({ANG:.3f} {C} {C})">'
             f'<rect x="-170" y="{KANTE_Y-3}" width="150" height="{BAR+6}" '
             f'fill="#8FC0FF" opacity=".85">'
             f'<animate attributeName="x" from="-170" to="{S+20}" dur="3.4s" '
             f'repeatCount="indefinite"/></rect></g>')
A["pb_nacht_anim"] = bewegt(
    "#04091A", GALLIANO, "#2B6EFF", IVORY, _himmel,
    feld(flaeche("#0A1836")) + _schimmer)

'''
s = s[:a] + NACHT_NEU + s[b:]

open(p, "w", encoding="utf-8").write(s)
print("anim.py ueberarbeitet")

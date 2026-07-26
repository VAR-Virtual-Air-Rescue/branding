# -*- coding: utf-8 -*-
"""Feuerwerk neu: durchlaufende Schleife statt zweimaligem Abspielen.

Vorher stand an jeder Animation `begin="0s;6s"` mit `fill="remove"` -- damit lief
sie genau zweimal und sprang danach in den Ausgangszustand zurueck, also
unsichtbar. Jetzt hat jedes Element `dur="6s" repeatCount="indefinite"` und die
Phasen liegen ueber `keyTimes` innerhalb dieser einen Schleife.

Alles ist deutlich groesser dimensioniert, damit es als Discord-Icon bei
128 px noch als Feuerwerk lesbar bleibt.
"""
import re

p = "anim.py"
s = open(p, encoding="utf-8").read()

a = s.index("def feuerwerk(")
b = s.index('A["pb_silvester_anim"]')

NEU = '''def feuerwerk(jahr="2027", dauer=6.0):
    """Rakete steigt, explodiert, die Funken lassen die Jahreszahl stehen.

    Eine einzige Schleife von `dauer` Sekunden; jede Phase sitzt ueber keyTimes
    an ihrer Stelle. Grosszuegig dimensioniert -- als Discord-Icon ist das Ganze
    nur rund 128 px gross.
    """
    D = f"{dauer}s"
    teile = []

    def kt(*paare):
        """(zeitpunkt_in_sekunden, wert) -> values/keyTimes fuer eine Schleife."""
        zs = ";".join(f"{v}" for _, v in paare)
        ts = ";".join(f"{min(1, max(0, t / dauer)):.4f}" for t, _ in paare)
        return zs, ts

    def rakete(bx, by, t0, r_auf=7.0, farbe="#FFE9A8"):
        """Aufsteigender Leuchtkoerper mit Schweif."""
        t1 = t0 + 1.25
        cy_v, cy_t = kt((0, KANTE_Y + 40), (t0, KANTE_Y + 40), (t1, by),
                        (t1 + .01, by), (dauer, by))
        op_v, op_t = kt((0, 0), (t0, 0), (t0 + .12, 1), (t1 - .08, 1),
                        (t1, 0), (dauer, 0))
        return (
            # Schweif
            f'<rect x="{bx-2.6:.1f}" y="0" width="5.2" height="34" rx="2.6" '
            f'fill="{farbe}" opacity="0">'
            f'<animate attributeName="y" values="{cy_v}" keyTimes="{cy_t}" '
            f'dur="{D}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op_v}" keyTimes="{op_t}" '
            f'dur="{D}" repeatCount="indefinite"/></rect>'
            # Kopf
            f'<circle cx="{bx}" r="{r_auf}" fill="{farbe}" opacity="0">'
            f'<animate attributeName="cy" values="{cy_v}" keyTimes="{cy_t}" '
            f'dur="{D}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op_v}" keyTimes="{op_t}" '
            f'dur="{D}" repeatCount="indefinite"/></circle>')

    def explosion(bx, by, t0, n=26, weite=104, farbe="#F5D76E", r_funke=5.0):
        out = []
        for k in range(n):
            w = k / n * 6.2832
            zx = bx + math.cos(w) * weite * (0.82 + 0.3 * (k % 3) / 2)
            zy = by + math.sin(w) * weite * 0.66 + 34
            t1 = t0 + 1.15
            x_v, x_t = kt((0, bx), (t0, bx), (t1, f"{zx:.0f}"), (dauer, f"{zx:.0f}"))
            y_v, y_t = kt((0, by), (t0, by), (t1, f"{zy:.0f}"), (dauer, f"{zy:.0f}"))
            o_v, o_t = kt((0, 0), (t0, 0), (t0 + .06, 1), (t0 + .7, 1),
                          (t1, 0), (dauer, 0))
            r_v, r_t = kt((0, r_funke), (t0, r_funke), (t1, r_funke * 0.45),
                          (dauer, r_funke * 0.45))
            out.append(
                f'<circle r="{r_funke}" fill="{farbe}" opacity="0">'
                f'<animate attributeName="cx" values="{x_v}" keyTimes="{x_t}" '
                f'dur="{D}" repeatCount="indefinite"/>'
                f'<animate attributeName="cy" values="{y_v}" keyTimes="{y_t}" '
                f'dur="{D}" repeatCount="indefinite"/>'
                f'<animate attributeName="r" values="{r_v}" keyTimes="{r_t}" '
                f'dur="{D}" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="{o_v}" keyTimes="{o_t}" '
                f'dur="{D}" repeatCount="indefinite"/></circle>')
        # heller Blitz im Moment der Explosion
        bo_v, bo_t = kt((0, 0), (t0, 0), (t0 + .08, .85), (t0 + .5, 0), (dauer, 0))
        out.append(
            f'<circle cx="{bx}" cy="{by}" r="30" fill="#FFFFFC" opacity="0">'
            f'<animate attributeName="opacity" values="{bo_v}" keyTimes="{bo_t}" '
            f'dur="{D}" repeatCount="indefinite"/></circle>')
        return "".join(out)

    # Hauptrakete in der Mitte
    HX, HY, HT = C, 128, 0.15
    teile.append(rakete(HX, HY, HT, 7.5))
    teile.append(explosion(HX, HY, HT + 1.25, 26, 108, "#F5D76E", 5.2))

    # zweite, kleinere Rakete zeitversetzt seitlich
    NX, NY, NT = int(S * 0.30), 168, 2.35
    teile.append(rakete(NX, NY, NT, 5.5, "#FFC8A8"))
    teile.append(explosion(NX, NY, NT + 1.25, 16, 62, "#FF9A5A", 4.0))

    # Jahreszahl -- steht, sobald die erste Explosion verglueht
    d, br = text_path(jahr, "fonts/Uniform Bold.ttf", 62, 0.05)
    t_ein = HT + 1.55
    jz_v, jz_t = kt((0, 0), (t_ein, 0), (t_ein + .45, 1),
                    (dauer - .8, 1), (dauer - .15, 0), (dauer, 0))
    teile.append(
        f'<g fill="#FFE9A8" opacity="0" transform="translate({C-br/2:.0f},{HY+52})">'
        f'{d}<animate attributeName="opacity" values="{jz_v}" keyTimes="{jz_t}" '
        f'dur="{D}" repeatCount="indefinite"/></g>')

    # Funken um die Zahl
    r = _rd.Random(5)
    for k in range(22):
        px = C - br / 2 + r.uniform(-8, br + 8)
        py = HY + 56 + r.uniform(-58, 14)
        v0 = t_ein + .5 + r.uniform(0, dauer - t_ein - 1.6)
        fo_v, fo_t = kt((0, 0), (v0, 0), (v0 + .25, .95), (v0 + .8, 0), (dauer, 0))
        teile.append(
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(2.2,4.2):.1f}" '
            f'fill="#FFD24A" opacity="0">'
            f'<animate attributeName="opacity" values="{fo_v}" keyTimes="{fo_t}" '
            f'dur="{D}" repeatCount="indefinite"/></circle>')

    return "".join(teile)

'''
s = s[:a] + NEU + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("Feuerwerk neu geschrieben")

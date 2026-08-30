# -*- coding: utf-8 -*-
"""Baut eine HTML-Seite aus Vorlage + echten SVG-Quellen.

  {{SVG:name|klasse}}      SVG aus neu/ oder tpl/ einbetten (IDs werden eindeutig)
  {{WORD:Text|Groesse|Farbe|Tracking|Font|Klasse}}   Schriftzug in Uniform als Pfade
  {{FONT:pfad.woff2}}      Schriftschnitt als data-URI -- Pfad relativ zur Vorlage
  {{IMG:datei|alt|klasse|sizes}}   Bild; nimmt WebP und die halbe Breite, wenn da
  {{JSON:datei.json}}      Datei woertlich einsetzen -- Pfad relativ zur Vorlage
"""
import re, os, sys
from text2path import text_path

# Neben den erzeugten Verzeichnissen auch die beiden Ablagen lesen, die im Git
# liegen: `quellen/` fuer handgezeichnete Platzhalter, `../karte/` fuer das
# Lagebild. Ohne sie liess sich web/index.html nicht mehr bauen.
STORE = {}
for d in ("quellen", "../karte", "neu", "tpl"):
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".svg"):
                STORE[f[:-4]] = open(os.path.join(d, f), encoding="utf-8").read()

_n = [0]

def inject(name, cls=""):
    _n[0] += 1
    s = STORE[name]
    for m in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace(f'id="{m}"', f'id="{m}_{_n[0]}"').replace(f'url(#{m})', f'url(#{m}_{_n[0]})')
    s = re.sub(r'<svg ', f'<svg class="{cls}" ', s, count=1)
    s = re.sub(r'\swidth="[\d.]+"\s+height="[\d.]+"', ' ', s, count=1)
    return s

def wordmark(text, size, fill, tracking=0.045, font="fonts/Uniform Bold.ttf", cls=""):
    d, w = text_path(text, font, size, tracking)
    return (f'<svg class="{cls}" viewBox="0 -{size*0.78:.1f} {w:.1f} {size*1.05:.1f}" '
            f'fill="{fill}" role="img" aria-label="{text}">{d}</svg>')

def _js_escape(c):
    """Ein Zeichen als JavaScript-Escape. Ausserhalb der BMP als Ersatzpaar."""
    n = ord(c)
    if n <= 0xFFFF:
        return f"\\u{n:04X}"
    n -= 0x10000
    return f"\\u{0xD800 + (n >> 10):04X}\\u{0xDC00 + (n & 0x3FF):04X}"


def _nach_ascii(out):
    """Alles ASCII machen -- aber im Skript anders als im Text.

    Frueher lief eine einzige Ersetzung ueber die ganze Datei und schrieb
    ueberall `&#NNN;`. **Im `<script>` werden HTML-Entitaeten nicht aufgeloest**:
    dort stand danach woertlich `Au&#223;enlandung`, und genau das erschien auch
    im Einsatzablauf auf der Seite. Der Autor hat das an einer Stelle von Hand
    umgangen (`\\u00fc` in den Pruefungsfragen), an der anderen nicht.

    Deshalb wird jetzt nach Bereich unterschieden: im Skript `\\uXXXX`, sonst
    `&#NNN;`.
    """
    teile = re.split(r'(<script\b[^>]*>.*?</script>)', out, flags=re.S | re.I)
    fertig = []
    for t in teile:
        js = t[:7].lower() == "<script"
        fertig.append("".join(
            c if ord(c) < 128 else (_js_escape(c) if js else f"&#{ord(c)};")
            for c in t))
    return "".join(fertig)


def _webp_masse(pfad):
    """Breite und Hoehe aus dem WebP-Dateikopf. Kein Pillow noetig.

    Zwei Bauformen kommen vor: der einfache verlustbehaftete Rahmen (`VP8 `)
    und der erweiterte (`VP8X`), den Pillow bei Alpha oder Metadaten schreibt.
    """
    with open(pfad, "rb") as f:
        k = f.read(32)
    if k[:4] != b"RIFF" or k[8:12] != b"WEBP":
        return 0, 0
    art = k[12:16]
    if art == b"VP8X":
        b = int.from_bytes(k[24:27], "little") + 1
        h = int.from_bytes(k[27:30], "little") + 1
        return b, h
    if art == b"VP8 ":
        if k[23:26] != b"\x9d\x01\x2a":
            return 0, 0
        b = int.from_bytes(k[26:28], "little") & 0x3FFF
        h = int.from_bytes(k[28:30], "little") & 0x3FFF
        return b, h
    return 0, 0


def build(tpl_path, out_path, inline_images=False):
    """inline_images: Fotos als data-URI einbetten (fuer eine Seite ohne Dateiablage)."""
    import base64, os
    tpl = open(tpl_path, encoding="utf-8").read()

    bild_ordner = os.path.join(os.path.dirname(os.path.abspath(tpl_path)), "img")

    def img(m):
        name, alt, cls, sizes = (m.group(1).split("|") + ["", "", ""])[:4]
        if inline_images:
            path = os.path.join("img_small", name)
            if os.path.exists(path):
                b64 = base64.b64encode(open(path, "rb").read()).decode()
                return (f'<img class="{cls}" src="data:image/jpeg;base64,{b64}" '
                        f'alt="{alt}">')

        # WebP bevorzugen, wenn daneben eines liegt. Die halbe Breite kommt als
        # zweiter Eintrag in srcset dazu -- Telefone laden dann rund ein Viertel
        # der Datenmenge. Die Breiten werden aus dem Dateikopf gelesen, damit
        # nichts von Hand nachgepflegt werden muss.
        stamm = os.path.splitext(name)[0]
        gross = os.path.join(bild_ordner, stamm + ".webp")
        klein = os.path.join(bild_ordner, stamm + "@0.5x.webp")
        if os.path.exists(gross):
            bw, bh = _webp_masse(gross)
            quelle = f'img/{stamm}.webp'
            teile = [f'<img class="{cls}" src="{quelle}"']
            if os.path.exists(klein):
                kw = _webp_masse(klein)[0]
                teile.append(f'srcset="img/{stamm}@0.5x.webp {kw}w, {quelle} {bw}w"')
                if sizes:
                    teile.append(f'sizes="{sizes}"')
            if bw and bh:
                teile.append(f'width="{bw}" height="{bh}"')
            teile.append(f'alt="{alt}" loading="lazy" decoding="async">')
            return " ".join(teile)

        return (f'<img class="{cls}" src="img/{name}" alt="{alt}" '
                f'loading="lazy" decoding="async">')

    tpl = re.sub(r'\{\{IMG:([^}]+)\}\}', img, tpl)

    # Schriftschnitte einbetten. Der Pfad gilt **relativ zur Vorlage**, nicht zum
    # Arbeitsverzeichnis -- gebaut wird aus werkzeug/, die Schriften liegen aber
    # bei der Seite. Eingebettet statt verlinkt, damit die Seite wie die SVGs
    # auch per Doppelklick vollstaendig ist: Browser laden Schriften von file://
    # nicht zuverlaessig nach.
    def font(m):
        rel = m.group(1).strip()
        pfad = os.path.join(os.path.dirname(os.path.abspath(tpl_path)), rel)
        b64 = base64.b64encode(open(pfad, "rb").read()).decode()
        return "data:font/woff2;base64," + b64

    tpl = re.sub(r'\{\{FONT:([^}]+)\}\}', font, tpl)

    # Daten woertlich einsetzen. Fuer die Livekarte: Laenderumrisse und
    # Stationen liegen als JSON daneben und gehoeren in die Seite, damit sie
    # ohne Nachladen dasteht. Nur der bewegliche Teil -- die Luftfahrzeuge --
    # kommt zur Laufzeit dazu.
    def daten(m):
        rel = m.group(1).strip()
        pfad = os.path.join(os.path.dirname(os.path.abspath(tpl_path)), rel)
        roh = open(pfad, encoding="utf-8").read().strip()
        # `</script>` in Daten wuerde den Skriptblock beenden, in dem sie steht.
        return roh.replace("</", "<" + chr(92) + "/")

    tpl = re.sub(r'\{\{JSON:([^}]+)\}\}', daten, tpl)

    def repl(m):
        kind, arg = m.group(1), m.group(2)
        p = arg.split("|")
        if kind == "SVG":
            return inject(p[0], p[1] if len(p) > 1 else "")
        return wordmark(p[0], float(p[1]), p[2],
                        float(p[3]) if len(p) > 3 else 0.045,
                        p[4] if len(p) > 4 else "fonts/Uniform Bold.ttf",
                        p[5] if len(p) > 5 else "")

    out = re.sub(r'\{\{(SVG|WORD):([^}]+)\}\}', repl, tpl)
    out = _nach_ascii(out)
    open(out_path, "w", encoding="ascii").write(out)

    # Pruefungen
    import collections
    ids = re.findall(r'\sid="([^"]+)"', out)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    refs = set(re.findall(r'url\(#([^)]+)\)', out))
    bad = [t for t in ("div", "section", "svg", "table", "ol", "ul", "li", "p",
                       "header", "footer", "main", "style", "figure", "script")
           if len(re.findall(rf'<{t}[\s>]', out)) != len(re.findall(rf'</{t}>', out))]
    print(f"{out_path}: {round(len(out.encode())/1024)} KB | Platzhalter: "
          f"{len(re.findall(r'\{\{', out))} | doppelte IDs: {len(dup)} | "
          f"tote Refs: {sorted(refs - set(ids)) or 0} | unbalanciert: {bad or 0}")

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], "--inline" in sys.argv)

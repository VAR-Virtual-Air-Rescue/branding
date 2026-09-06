# -*- coding: utf-8 -*-
"""Baut das oeffentliche Brandbook: eine einzelne HTML-Datei, die alles
mitbringt und nichts nachlaedt.

    python werkzeug/brandbook.py brandbook/index.html

Jede Grafik ist die Originaldatei aus diesem Paket, inline eingesetzt -- kein
Abbild, kein Screenshot. Wer eine Kachel im Brandbook sieht, sieht die Datei,
die er herunterlaedt. Deshalb faellt hier auch auf, wenn eine kaputt ist.
"""
import re, os, io, sys, base64

HIER = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HIER)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BRAND, "brandbook", "index.html")

_n = [0]


def svg(rel, cls="", style="", label=""):
    """SVG einlesen, IDs eindeutig machen, Groessenattribute entfernen.

    Die IDs muessen umbenannt werden: in einem Dokument mit knapp neunzig SVGs
    ueberschreiben sich sonst gleichnamige Verlaeufe und Clip-Pfade -- sichtbar
    als Kachel, die die Farbe ihres Nachbarn traegt.
    """
    p = os.path.join(BRAND, rel.replace("/", os.sep))
    s = io.open(p, encoding="utf-8").read()
    _n[0] += 1
    pre = "a%d-" % _n[0]
    for i in sorted(set(re.findall(r'\sid="([^"]+)"', s)), key=len, reverse=True):
        s = s.replace('id="%s"' % i, 'id="%s%s"' % (pre, i))
        s = s.replace("url(#%s)" % i, "url(#%s%s)" % (pre, i))
    s = re.sub(r'<svg([^>]*?)\swidth="[^"]*"', r"<svg\1", s, count=1)
    s = re.sub(r'<svg([^>]*?)\sheight="[^"]*"', r"<svg\1", s, count=1)
    attrs = (' class="%s"' % cls if cls else "") + (' style="%s"' % style if style else "")
    attrs += ' role="img" aria-label="%s"' % (label or os.path.basename(rel))
    return re.sub(r"<svg", "<svg" + attrs, s, count=1)


def tile(rel, name, note, stage="navy", label=""):
    return ('<figure class="tile"><div class="stage %s">%s</div>'
            "<figcaption><b>%s</b><span>%s</span></figcaption></figure>"
            % (stage, svg(rel, label=label or name), name, note))


def grid(items, cls, stage_default="plain"):
    out = []
    for it in items:
        rel, nm, note, st = it if len(it) == 4 else it + (stage_default,)
        out.append(tile(rel, nm, note, st))
    return '<div class="grid %s">%s</div>' % (cls, "".join(out))


def datauri(rel, mime):
    with open(os.path.join(BRAND, rel.replace("/", os.sep)), "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


# --- Bestand zaehlen, nicht behaupten -------------------------------------
# Eine gepflegte Zahl steht nach der ersten neuen Datei falsch da, und niemand
# merkt es. Also zaehlen.
def count(folder, ext=".svg"):
    d = os.path.join(BRAND, folder)
    return len([f for f in os.listdir(d) if f.lower().endswith(ext)])


ORDNER = ["logo", "lockup", "icon", "profilbilder", "reel", "vorlagen",
          "karte", "herleitung"]
n_svg = sum(count(d) for d in ORDNER)
n_png = count("png", ".png")
n_wz = len([f for f in os.listdir(HIER) if f.endswith(".py")])

# --- Schriftproben: Umrisse, kein Schriftschnitt --------------------------
_pr = io.open(os.path.join(HIER, "schriftproben.html"), encoding="utf-8").read()
specimens = [x.replace('fill="#FFFFFC"', 'fill="currentColor"')
             for x in re.findall(r'<svg class="ts-\d+".*?</svg>', _pr, re.S)]
SPEC_ROWS = [("Black", "Schlagzeile", "46"), ("Bold", "Auszeichnung", "26"),
             ("Medium", "Zwischenzeile", "24"), ("Regular", "Flie&szlig;text", "22"),
             ("Bold", "Kleinlabel", "15")]
typerows = "".join(
    '<div class="tr"><span class="lbl">%s &middot; %s</span>'
    '<div class="spec" style="--h:%spx">%s</div></div>' % (w, r, h, x)
    for (w, r, h), x in zip(SPEC_ROWS, specimens))

# --- Bausteine ------------------------------------------------------------
FASSUNGEN = [
    ("logo/VAR_logo.svg", "Hauptfassung", "Stratos-Kreis, Hubschrauber Gold", "plain"),
    ("logo/VAR_signet.svg", "Signet", "ohne Wortmarke, ab 40&#8239;px", "plain"),
    ("logo/VAR_logo_zweitfassung.svg", "Zweitfassung", "engere Wortmarke", "plain"),
    ("logo/VAR_logo_zweifeld.svg", "Zweifeld", "Basis der Sondereditionen", "plain"),
    ("logo/VAR_logo_hell.svg", "Hell", "f&uuml;r helle Untergr&uuml;nde", "ivory"),
    ("logo/VAR_logo_mono_positiv.svg", "Einfarbig positiv", "Stempel, Fax, Gravur", "ivory"),
    ("logo/VAR_logo_mono_negativ.svg", "Einfarbig negativ", "eine Farbe auf dunkel", "navy"),
]
UNTERGRUND = [
    ("logo/VAR_logo.svg", "Auf Stratos", "die Regel", "navy"),
    ("logo/VAR_logo_hell.svg", "Auf Ivory", "helle Fassung", "ivory"),
    ("logo/VAR_logo_mono_positiv.svg", "Auf Gold", "einfarbig positiv", "gold"),
    ("logo/VAR_logo.svg", "Auf einem Foto", "ohne Kasten, ohne Schatten", "foto"),
]
ROTOR = [("logo/VAR_r1_rotor.svg", "R1", "Rotor angedeutet"),
         ("logo/VAR_r2_offen.svg", "R2", "offener Kreis"),
         ("logo/VAR_r3_dreiblatt.svg", "R3", "Dreiblatt"),
         ("logo/VAR_r4_bogen.svg", "R4", "Bogen"),
         ("logo/VAR_r5_ivory_ring.svg", "R5", "Ring in Ivory")]
ICONS = [("icon/icon_kante.svg", "App-Icon", "unter 32&#8239;px"),
         ("icon/icon_monogramm.svg", "Monogramm", "VAR als Buchstaben"),
         ("icon/icon_monogramm_gold.svg", "Monogramm Gold", "auf Stratos")]
LOCKUPS = [("lockup/lockup_h.svg", "Waagerecht", "Standardsperrung", "ivory"),
           ("lockup/lockup_h_neg.svg", "Waagerecht negativ", "auf Stratos", "navy"),
           ("lockup/lockup_v.svg", "Senkrecht", "zentriert", "ivory"),
           ("lockup/lockup_v_neg.svg", "Senkrecht negativ", "auf Stratos", "navy")]
PB = [("profilbilder/pb_standard.svg", "Standard", "Grundfassung"),
      ("profilbilder/pb_gold.svg", "Gold", "volle Fl&auml;che"),
      ("profilbilder/pb_einheit.svg", "Einheit", "Deutschland"),
      ("profilbilder/pb_at.svg", "&Ouml;sterreich", "Landesedition"),
      ("profilbilder/pb_ch.svg", "Schweiz", "Landesedition"),
      ("profilbilder/pb_nl.svg", "Niederlande", "Landesedition"),
      ("profilbilder/pb_pride.svg", "Pride", "stehend"),
      ("profilbilder/pb_pride_anim.svg", "Pride", "animiert"),
      ("profilbilder/pb_weihnachten.svg", "Weihnachten", "stehend"),
      ("profilbilder/pb_weihnachten_anim.svg", "Weihnachten", "animiert"),
      ("profilbilder/pb_silvester.svg", "Silvester", "stehend"),
      ("profilbilder/pb_silvester_anim.svg", "Silvester", "animiert"),
      ("profilbilder/pb_halloween.svg", "Halloween", "stehend"),
      ("profilbilder/pb_halloween_anim.svg", "Halloween", "animiert"),
      ("profilbilder/pb_nacht.svg", "Nachtflug", "stehend"),
      ("profilbilder/pb_nacht_anim.svg", "Nachtflug", "animiert"),
      ("profilbilder/pb_jubilaeum.svg", "Jubil&auml;um", "Jahreszahl einsetzbar"),
      ("profilbilder/pb_trauer.svg", "Trauer", "Flor, gedeckt"),
      ("profilbilder/pb_vorlage.svg", "Vorlage", "leeres unteres Feld")]
VORLAGEN = [
    ("vorlagen/ig_4x5_foto.svg", "Instagram Beitrag", "1080&times;1350"),
    ("vorlagen/ig_1x1_foto.svg", "Instagram quadratisch", "1080&times;1080"),
    ("vorlagen/x_1600x900.svg", "X / LinkedIn quer", "1600&times;900"),
    ("vorlagen/fb_link_1200x630.svg", "Linkvorschau", "1200&times;630"),
    ("vorlagen/story_9x16.svg", "Story", "unten 384 frei"),
    ("vorlagen/reel_titel_9x16.svg", "Reel-Titel", "unten 672 frei"),
    ("vorlagen/tiktok_9x16.svg", "TikTok", "unten 672 frei"),
    ("vorlagen/karussell_titel_4x5.svg", "Karussell 1", "Titelkarte"),
    ("vorlagen/karussell_inhalt_4x5.svg", "Karussell 2", "Inhaltskarte"),
    ("vorlagen/karussell_abschluss_4x5.svg", "Karussell 3", "Abschlusskarte"),
    ("vorlagen/einsatzmeldung_1x1.svg", "Einsatzmeldung", "wie eine Depesche"),
    ("vorlagen/statement_4x5.svg", "Statement", "Stimmen aus der Crew"),
    ("vorlagen/zahl_1x1.svg", "Zahl", "Bilanz, Jubil&auml;um"),
    ("vorlagen/crew_4x5.svg", "Crew", "Vorstellung"),
    ("vorlagen/veranstaltung_4x5.svg", "Veranstaltung", "Termin"),
    ("vorlagen/vergleich_1x1.svg", "Vergleich", "vorher / nachher"),
    ("vorlagen/fb_1x1_vierbild.svg", "Vierbild", "R&uuml;ckblick"),
    ("vorlagen/yt_thumb_1280x720.svg", "YouTube-Thumbnail", "1280&times;720"),
    ("vorlagen/yt_kanalbild_2560x1440.svg", "YouTube-Kanalbild", "Mitte 1546&times;423"),
    ("vorlagen/discord_event_800x320.svg", "Discord-Event", "800&times;320"),
    ("vorlagen/overlay_live_1920x1080.svg", "Live-Overlay", "Stream"),
    ("vorlagen/overlay_lowerthird_1920x1080.svg", "Bauchbinde", "Stream"),
]
REEL = [("reel/tb_1_alarmierung.svg", "1 &middot; Alarmierung", "Einsatz geht ein"),
        ("reel/tb_2_ausruecken.svg", "2 &middot; Ausr&uuml;cken", "Start"),
        ("reel/tb_3_ankommen.svg", "3 &middot; Ankommen", "Einsatzstelle"),
        ("reel/tb_4_abflug_klinik.svg", "4 &middot; Abflug", "Richtung Klinik"),
        ("reel/tb_5_ankunft_klinik.svg", "5 &middot; Ankunft", "&Uuml;bergabe"),
        ("reel/tb_6_einsatzklar.svg", "6 &middot; Einsatzklar", "Status 2"),
        ("reel/tb_leer.svg", "Leer", "eigene Beschriftung")]
KARTE = [("karte/_lage.svg", "Lagebild", "Einsatz mit Umfeld"),
         ("karte/_livemap.svg", "Livekarte", "RescueTrack-Anmutung"),
         ("karte/_track.svg", "Spur", "#46b7a3")]
DONTS = [("herleitung/_dont_color.svg", "Farbe tauschen"),
         ("herleitung/_dont_stretch.svg", "Verzerren"),
         ("herleitung/_dont_rotate.svg", "Drehen"),
         ("herleitung/_dont_shadow.svg", "Schatten"),
         ("herleitung/_dont_float.svg", "Kante wegnehmen")]
EVO = [("herleitung/_evo_entwurf.svg", "Ursprungsentwurf",
        "der Anschnitt war von Anfang an da"),
       ("herleitung/_evo_heute.svg", "Vorg&auml;ngerfassung",
        "die Kante fehlt, das Zeichen schwebt")]

MARKE = [
    ("Stratos", "#00113A", "80&#8201;%",
     "Die Grundfl&auml;che. Tr&auml;gt fast jede Anwendung.", "#FFFFFC"),
    ("Galliano", "#D5A507", "15&#8201;%",
     "Kante, Hubschrauber, Hervorhebung. Nie als Textfl&auml;che.", "#00113A"),
    ("Ivory", "#FFFFFC", "5&#8201;%",
     "Schrift auf dunkel, Negativfassung, Papier.", "#00113A"),
    ("Signalblau", "#2B6EFF", "UI",
     "Nur Oberfl&auml;che: Links, Fokus, aktive Zust&auml;nde. Nie im Logo.", "#FFFFFC"),
]
STATUS = [("Kritisch", "#E5484D", "St&ouml;rung, abgebrochener Einsatz"),
          ("Achtung", "#E5920A", "wartet, &uuml;berf&auml;llig"),
          ("Einsatzbereit", "#2FA96B", "Status 1 und 2"),
          ("Im Einsatz", "#2B6EFF", "Status 3, 4 und 7")]
KONTRAST = [("Ivory auf Stratos", "18,37", "Flie&szlig;text, &Uuml;berschriften, alles", "ok"),
            ("Galliano auf Stratos", "8,07", "Flie&szlig;text, Kante, Hervorhebung", "ok"),
            ("Stratos auf Galliano", "8,07", "Flie&szlig;text auf goldener Fl&auml;che", "ok"),
            ("Signalblau auf Stratos", "4,19", "Links, gro&szlig;e Schrift, Bedienelemente", "warn"),
            ("Galliano auf Ivory", "2,27", "nur Fl&auml;chen und Linien, <b>keine Schrift</b>", "no")]
BESTAND = [
    ("logo/", count("logo"),
     "Hauptfassung, Signet, Zweitfassung, Zweifeld, hell, einfarbig, R1&ndash;R5"),
    ("lockup/", count("lockup"), "waagerecht und senkrecht, je positiv und negativ"),
    ("icon/", count("icon"), "App-Icon und zwei Monogramme f&uuml;r alles unter 32&#8239;px"),
    ("profilbilder/", count("profilbilder"),
     "Grundfassung, zw&ouml;lf Sondereditionen, f&uuml;nf davon animiert, Vorlage"),
    ("reel/", count("reel"), "sechs Overlays f&uuml;r das Einsatz-Tagebuch plus leere Vorlage"),
    ("vorlagen/", count("vorlagen"), "Social Media, Video, Stream, Veranstaltungen"),
    ("karte/", count("karte"), "Lagebild, Livekarte, Spur"),
    ("herleitung/", count("herleitung"),
     "Entwurf, Vorg&auml;ngerfassung, f&uuml;nf Falschanwendungen"),
    ("png/", n_png, "512 &middot; 256 &middot; 128 &middot; 64 &middot; 32 &middot; 16 plus f&uuml;nf Vorlagen"),
    ("werkzeug/", n_wz, "Skripte, mit denen sich alles neu erzeugen l&auml;sst"),
    ("website/", "&mdash;", "der Onepager als Anschauungsst&uuml;ck"),
]

TOKENS = """:root {
  /* Marke */
  --var-stratos:      #00113A;
  --var-galliano:     #D5A507;
  --var-ivory:        #FFFFFC;
  --var-signal:       #2B6EFF;

  /* Flaechen, abgeleitet von Stratos */
  --var-bg:           #050B1C;
  --var-surface:      #0B1631;
  --var-surface-2:    #12203F;
  --var-line:         #1E2E52;

  /* Schrift */
  --var-text:         #E7EAF3;
  --var-text-dim:     #8E97AE;

  /* Status */
  --var-status-krit:  #E5484D;
  --var-status-warn:  #E5920A;
  --var-status-bereit:#2FA96B;
  --var-status-aktiv: #2B6EFF;

  /* Die Kante */
  --var-kante:        var(--var-galliano);
  --var-kante-stark:  6px;
  --var-kante-fein:   3px;

  --var-radius:       3px;
  --var-font:         "Uniform", Inter, system-ui, sans-serif;
}"""

NAV = [("marke", "Die Marke"), ("zeichen", "Zeichen"), ("fassungen", "Fassungen"),
       ("groessen", "Gr&ouml;&szlig;en"), ("untergrund", "Untergr&uuml;nde"),
       ("farbe", "Farbe"), ("typografie", "Typografie"), ("kante", "Die Kante"),
       ("profilbilder", "Profilbilder"), ("vorlagen", "Vorlagen"), ("reel", "Reel"),
       ("karte", "Karte"), ("regeln", "Regeln"), ("tokens", "Tokens"),
       ("material", "Material"), ("nutzung", "Nutzung")]

html = io.open(os.path.join(HIER, "brandbook.tpl.html"), encoding="utf-8").read()

rep = {
    "{{LOCKUP}}": svg("lockup/lockup_h_neg.svg", "hero-lockup", label="Virtual Air Rescue"),
    "{{SIGNET}}": svg("logo/VAR_signet.svg", "rail-mark", label="VAR"),
    "{{HERO_LOGO}}": svg("logo/VAR_logo.svg", "", label="VAR Hauptfassung"),
    "{{FOTO}}": datauri("herleitung/_foto_original.jpg", "image/jpeg"),
    "{{NAV}}": "".join('<a href="#%s">%s</a>' % (a, b) for a, b in NAV),
    "{{FASSUNGEN}}": grid(FASSUNGEN, "g4"),
    "{{UNTERGRUND}}": grid(UNTERGRUND, "g4"),
    "{{ROTOR}}": grid(ROTOR, "g5", "navy"),
    "{{ICONS}}": grid(ICONS, "g5", "plain"),
    "{{LOCKUPS}}": grid(LOCKUPS, "g2"),
    "{{PB}}": grid(PB, "g6", "plain"),
    "{{VORLAGEN}}": grid(VORLAGEN, "g4", "plain"),
    "{{REEL}}": grid(REEL, "g4", "plain"),
    "{{KARTE}}": grid(KARTE, "g3", "plain"),
    "{{EVO}}": grid(EVO, "g2", "plain"),
    "{{DONTS}}": "".join(
        '<figure class="tile dont"><div class="stage plain">%s</div>'
        "<figcaption><b>%s</b><span>nicht erlaubt</span></figcaption></figure>"
        % (svg(r, label=n), n) for r, n in DONTS),
    "{{MARKE}}": "".join(
        '<div class="sw"><div class="chip" style="background:%s;color:%s"><span>%s</span>'
        '</div><div class="meta"><div class="nm">%s</div><div class="hx">%s</div>'
        "<p>%s</p></div></div>" % (hx, ink, share, nm, hx, note)
        for nm, hx, share, note, ink in MARKE),
    "{{STATUS}}": "".join(
        '<div class="sw st"><div class="chip" style="background:%s"></div>'
        '<div class="meta"><div class="nm">%s</div><div class="hx">%s</div><p>%s</p>'
        "</div></div>" % (hx, nm, hx, note) for nm, hx, note in STATUS),
    "{{KONTRAST}}": "".join(
        '<tr><td>%s</td><td class="num">%s&#8202;:&#8202;1</td>'
        '<td><span class="dot %s"></span>%s</td></tr>' % (k, v, cls, u)
        for k, v, u, cls in KONTRAST),
    "{{TYPEROWS}}": typerows,
    "{{TOKENS}}": TOKENS.replace("&", "&amp;").replace("<", "&lt;"),
    "{{BESTAND}}": "".join(
        "<tr><td><code>%s</code></td><td class=\"num\">%s</td><td>%s</td></tr>"
        % (f, n, w) for f, n, w in BESTAND),
    "{{NSVG}}": str(n_svg),
    "{{NPNG}}": str(n_png),
}
for k, v in rep.items():
    html = html.replace(k, v)

# Ein uebrig gebliebener Platzhalter stuende im Buch als `{{...}}` -- lieber
# hier abbrechen als das ausliefern.
uebrig = re.findall(r"\{\{[A-Z_]+\}\}", html)
assert not uebrig, "nicht ersetzt: %s" % sorted(set(uebrig))

d = os.path.dirname(os.path.abspath(OUT))
if d and not os.path.isdir(d):
    os.makedirs(d)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
print("Brandbook: %s  (%d KB, %d Grafiken)"
      % (OUT, os.path.getsize(OUT) // 1024, html.count("<svg")))

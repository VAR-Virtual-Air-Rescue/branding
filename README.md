# brand

Alles echte Vektoren. Im Gegensatz zum `branding`-Repository, dessen SVG-Dateien
den Hubschrauber als eingebettetes PNG enthalten (3708 × 1201 px als Base64,
406 KB je Datei).

    logo/          Hauptfassung, Signet, Zweitfassung, Zweifeld, hell, einfarbig,
                   dazu fünf Rotorfassungen R1–R5
    lockup/        waagerecht und senkrecht, je positiv und negativ
    icon/          App-Icons für alles unter 32 px
    profilbilder/  Grundfassung, 12 Sondereditionen, 5 davon animiert, Vorlage
    reel/          6 Overlays für das Einsatz-Tagebuch plus leere Vorlage
    vorlagen/      15 Formate für Social Media, Video und Veranstaltungen
    herleitung/    Foto, Entwurf, heutiges Logo, sechs Falschanwendungen
    karte/         Lagebild und Livekarte in RescueTrack-Anmutung
    png/           512 · 256 · 128 · 64 · 32 · 16
    werkzeug/      Skripte, mit denen sich alles neu erzeugen lässt

## Wo die Kante liegt

Steht eine Wortmarke unter der Kante, läuft sie **durch den Mittelpunkt** — sie
ist dann ein Durchmesser, die längste Sehne, die der Kreis hergibt. Himmel und
Feld sind gleich hoch, VAR bekommt die Hälfte des Zeichens statt eines Drittels.

Die Wortmarke **hängt unten am Kreis**, nicht oben an der Kante — so sitzt sie im
Ursprungslogo. `WORT_BREITE = 0.828` (Anteil des Durchmessers, dort gemessen) und
`WORT_BODEN = 14` (Abstand der Grundlinie über dem tiefsten Punkt des Beschnitts)
stehen in `werkzeug/mark.py`. Was links und rechts über die Rundung hinausragt, wird
abgeschnitten: der Fuß des V und das Bein des R. In der Mitte läuft das A bis unten
durch.

Der waagerechte Sitz wird ausgemittelt, aber auf zwölf Einheiten gedeckelt: die
Wortmarke wird um den Mittelpunkt gekippt und liegt darunter, säße ohne Ausgleich zu
weit rechts — mit vollem Ausgleich aber sichtbar aus der Mitte.

**Die Wortmarke war beschnitten.** Bis zum 28.08.2026 stand in `traced.json` eine
Fassung, die von einer schon im Badge-Kreis sitzenden Grafik abgenommen war: Fuß des
V und Bein des R fehlten, rund sieben Prozent der Fläche. Neu abgenommen wird sie mit
`werkzeug/trace_var.py` aus `werkzeug/quellen/var_wortmarke.png`.

Ohne Wortmarke bleibt sie **tief**: Signet, Rotorfassungen R2–R5 und App-Icon
würden sonst eine leere Hälfte zeigen und den Hubschrauber verkleinern, der dort
allein trägt. Beide Höhen stehen als `EDGE` und `EDGE_LEER` in `werkzeug/mark.py`;
Profilbilder und Animationen leiten ihre Kante daraus ab.

## Größen

Hauptfassung ab 96 px bzw. 22 mm im Druck. Signet ab 40 px. Darunter gilt
ausschließlich das App-Icon — der Hubschrauber ist 3,1 : 1 breit und im runden
Beschnitt unter 100 px kaum noch zu erkennen. Schutzraum rundherum: ein Viertel
des Durchmessers.

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

Die Wortmarke **füllt das Feld zwischen Kante und Rundung**: oben liegt sie am Strich
an, unten werden die Füße weitergeführt, bis der Beschnitt sie kappt. Sichtbar ist das
beim A; V und R kappt die Rundung schon oberhalb der Grundlinie. `WORT_BREITE = 0.828`
(Anteil des Durchmessers, am Ursprungslogo gemessen) und `VERLAENGERUNG = 200` stehen in
`werkzeug/mark.py`.

Die Verlängerung folgt den Kanten der Buchstaben, nicht der Senkrechten: die Stämme sind
geneigt und verjüngen sich nach unten (Bein des A +0,41 je Einheit, Keil des V schließt
sich nach 136). `_fuesse()` liest beide Kantenneigungen aus zwei waagerechten Schnitten
durch die Zeichnung — senkrecht verlängert bekäme jeder Fuß einen Knick.

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

Seine **Scheiben** sind keine Löcher mehr: Kabinenfenster und Frontscheibe bekommen
`SCHEIBE_DECKUNG = 0.45` der Rumpffarbe. Nicht eine feste Farbe — so trägt es auf
Stratos, auf Ivory und auf den Flaggen der Editionen gleichermaßen. Ab etwa 60 %
verschmilzt die Frontscheibe mit der Nase. Die Fenestron-Öffnung im Heck und der Spalt
unter dem Rotormast bleiben offen; das sind Durchbrüche, keine Scheiben.

Der Hubschrauber ist **444** breit — so nah an den Rand, wie es trägt: die Rotorspitzen
behalten 11 Einheiten Luft. Bei der Mindestgröße von 96 px sind das noch zwei sichtbare
Pixel Grund; darunter übernimmt ohnehin das Signet.


Hauptfassung ab 96 px bzw. 22 mm im Druck. Signet ab 40 px. Darunter gilt
ausschließlich das App-Icon — der Hubschrauber ist 3,1 : 1 breit und im runden
Beschnitt unter 100 px kaum noch zu erkennen. Schutzraum rundherum: ein Viertel
des Durchmessers.

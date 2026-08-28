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
    vorlagen/      22 Formate für Social Media, Video und Veranstaltungen
    herleitung/    Foto, Entwurf, heutiges Logo, sechs Falschanwendungen
    karte/         Lagebild und Livekarte in RescueTrack-Anmutung
    png/           512 · 256 · 128 · 64 · 32 · 16
    werkzeug/      Skripte, mit denen sich alles neu erzeugen lässt

## Die Kante in den Vorlagen

Sie ist auch dort **gekippt** — im selben Winkel wie im Zeichen. Bis August 2026 war
der Balken in allen Vorlagen waagerecht; damit fehlte genau das Element, an dem man
die Marke wiedererkennt. Jetzt läuft er in jedem Format randabfallend durch und trägt
darunter den Absender. Ein Beitrag ist dadurch auch dann als VAR-Beitrag zu erkennen,
wenn das Logo klein ist oder gar nicht im Bild steht.

Der Aufbau wiederholt das Zeichen im Großen: oben das Bild wie der Himmel, darunter
die Kante, darunter die Fläche mit dem Absender wie die Wortmarke.

Wie **kräftig** sie auftritt, regelt `KANTE_STAERKE` in `tpl.py`, voreingestellt auf
**5**. Der Winkel selbst wird nicht abgeschwächt — er ist der Marke entnommen, und ein
halbierter Winkel wäre einer, den niemand benennen kann und der zum Zeichen nicht mehr
passt. Geregelt wird die Stärke: als kräftiger Balken (14) beherrscht die Kante die
Kachel, und im Profilraster kippt der ganze Kanal, weil neun Kacheln in dieselbe
Richtung ziehen. Als feine Linie bleibt der Winkel erkennbar, ohne die Aufmerksamkeit
an sich zu ziehen — er liest sich als Detail, nicht als Architektur. `0` lässt die Linie
ganz weg; dann trägt nur der Anschnitt zwischen Bild und Absenderfeld den Winkel.

**Die Kante kippt — was auf ihr steht nicht.** Marke, URL und Rubrik stehen gerade.
Alles mitzukippen war der naheliegende Gedanke, denn im Zeichen steht die Wortmarke
ebenfalls parallel zur Kante. Dort ist die Kante aber das Bauteil und die Wortmarke
gehört dazu; im Beitrag ist sie eine Linie, und ein schräger Absender darunter liest
sich als Fehler statt als Absicht. Aus demselben Grund wirkt der Winkel nur
**randabfallend**: die Bauchbinde ist ein kurzer Kasten und bleibt gerade — geneigt
wäre sie eine schiefe Schachtel.

Weil die Kante nach links abfällt, beginnt die nutzbare Fläche dort am tiefsten. Breite
Formate brauchen deshalb einen höheren Fuß: bei 1600 Breite gehen 46 Einheiten je Seite
vom Band ab, bei 1920 sind es 55.

Zwei Dinge, die dabei zu beachten sind und in `tpl.py` als Funktionen stehen:

- **`kante_luft(w)`** — die Kante steigt nach rechts an, über 1080 Breite um 62
  Einheiten. Text, der nur zur Mittelhöhe misst, läuft rechts in die Kante.
- **`scrim(w, h, y)`** — die Abdunklung läuft auf die Kante zu, nicht auf den
  Bildrand. Sitzt die Kante weit darüber (bei 9:16 fast in der Bildmitte), ist der
  Text sonst nur halb abgedeckt und fällt auf hellen Fotos auseinander.

Mit `python tpl_build.py --fotos <ordner>` wird statt der Platzhalterkulissen echtes
Bildmaterial eingesetzt — so lässt sich jede Vorlage vor dem Einsatz gegenprüfen.

**Uniform hat kein `→`.** Der Setzer verschluckt fehlende Zeichen still, die Breite
bleibt stehen. `tpl.py` schreibt deshalb mit, was fehlt, und der Bauschritt meldet es
am Ende. Vorhanden und benutzbar sind `»`, `·`, `–`, `—`, `•`, `+`, `×`.

## Wo die Kante liegt

Steht eine Wortmarke unter der Kante, läuft sie **durch den Mittelpunkt** — sie
ist dann ein Durchmesser, die längste Sehne, die der Kreis hergibt. Himmel und
Feld sind gleich hoch, VAR bekommt die Hälfte des Zeichens statt eines Drittels.

Die Wortmarke **füllt das Feld zwischen Kante und Rundung**: oben steht sie unter dem
Strich, unten werden die Füße weitergeführt, bis der Beschnitt sie kappt.

Zwischen beiden steht eine **Fuge, so stark wie die Kante selbst** (`FUGE = BAR`). Ohne
sie verschmelzen die flachen Oberkanten von V und R mit dem Balken — zusammen ein Drittel
der Wortmarkenbreite — und die Kante wird zum Unterstrich. Der Schriftzug läuft im selben
Winkel: seine Oberkante liegt auf derselben Geraden wie die Balkenunterkante, nur um die
Fuge versetzt. Sichtbar ist das
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

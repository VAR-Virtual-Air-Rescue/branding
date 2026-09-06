# Virtual Air Rescue — Markenpaket

Das vollständige Material der Marke, dazu das **Brandbook**, das erklärt, wie es
gemeint ist: <https://branding.virtualairrescue.com>

Alles sind echte Vektoren — der Hubschrauber ist gezeichnet, nicht als PNG
eingebettet. Die SVG ist immer der Master, PNGs entstehen aus ihr, nie umgekehrt.

    logo/          Hauptfassung, Signet, Zweitfassung, Zweifeld, hell, einfarbig
    lockup/        waagerecht und senkrecht, je positiv und negativ
    icon/          App-Icons für alles unter 32 px
    profilbilder/  Grundfassung, 11 Sondereditionen, 5 davon animiert, Vorlage
    reel/          6 Overlays für das Einsatz-Tagebuch plus leere Vorlage
    vorlagen/      22 Formate für Social Media, Video und Stream, dazu 18
                   Event-Vorlagen (`event_*`)
    herleitung/    Foto, Entwurf, heutiges Logo, sechs Falschanwendungen
    karte/         Lagebild und Livekarte in RescueTrack-Anmutung
    png/           512 · 256 · 128 · 64 · 32 · 16
    werkzeug/      Skripte, mit denen sich alles neu erzeugen lässt
    brandbook/     das gebaute Brandbook — eine Datei, lädt nichts nach
    website/       der Onepager virtualairrescue.com als Anschauungsstück
    auth/          Anmeldung über den VAR-Hub (eigener Dienst, eigenes Bild)
    konto/         die einzige geschützte Seite

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
am Ende. Vorhanden und benutzbar sind `»`, `«`, `·`, `–`, `—`, `•`, `›`, `‹`, `°`,
`+`, `×`, `…`, `§`, `±`.

Ebenfalls **nicht vorhanden**: `✓`, `★`, `≥` — und `U+2011`, der geschützte
Bindestrich. Der fällt besonders leicht durch, weil er im Editor wie ein normaler
Bindestrich aussieht; in `P‑1` geschrieben ist er im SVG-Satz weg und in HTML in einer
fremden Schrift. Alle vier Schnitte haben dieselben 416 Glyphen — was in einem fehlt,
fehlt in allen.

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

Ohne Wortmarke bleibt sie **tief**: Signet und App-Icon
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

## Das Brandbook bauen

    python werkzeug/brandbook.py brandbook/index.html

Heraus kommt **eine** HTML-Datei mit allen 89 Grafiken darin. Sie lädt nichts
nach — keine Schrift, kein Skript, kein Bild von einem fremden Server — und
funktioniert deshalb auch offline und per Doppelklick.

Die Zahlen im Buch (wie viele Dateien in welchem Ordner) werden beim Bauen
**gezählt**, nicht gepflegt. Eine gepflegte Zahl steht nach der ersten neuen
Datei falsch da, und niemand merkt es.

## Betrieb

Das Brandbook läuft unter `branding.virtualairrescue.com` in zwei Containern
hinter dem bestehenden Traefik:

    cp .env.example .env      # Zugangsdaten eintragen
    docker compose up -d --build

`nginx` liefert aus und hängt im Traefik. `branding-auth` spricht mit dem Hub
und hält das `client_secret`; er hat **keinen** Host-Port und **kein**
Traefik-Netz — nur nginx erreicht ihn.

Der Container baut das Buch selbst — so passen die gezählten Zahlen zum Stand
des Images und nicht zum Stand des Rechners, auf dem zuletzt jemand das Skript
laufen liess. Neben dem Buch liefert er die Markenordner direkt aus, mit
Verzeichnisübersicht:

    branding.virtualairrescue.com/logo/VAR_logo.svg
    branding.virtualairrescue.com/vorlagen/
    branding.virtualairrescue.com/website/

Das Traefik-Netz wird nicht angelegt, sondern erwartet (`external: true`).
Fehlt es, bricht `up` mit einer klaren Meldung ab — besser, als ein Netz
gleichen Namens anzulegen und sich zu wundern, dass der Proxy nichts findet.

## Uniform liegt nicht hier

Die Hausschrift ist lizenzpflichtig; die Schriftdateien gehören deshalb nicht in
ein öffentliches Repository. Das fällt kaum auf:

* In **Logos, Vorlagen und Profilbildern** steckt die Frage gar nicht — dort ist
  jeder Buchstabe bereits ein Pfad.
* Die **Schriftproben** im Brandbook liegen als Umrisse in
  `werkzeug/schriftproben.html`. Eine Schriftprobe, kein Schriftschnitt.
* **Brandbook und Website** fallen auf `system-ui` zurück. Weil Uniform eine
  neutrale Grotesk ist, trägt die Systemschrift dieselbe Anmutung; für den Ton
  sorgen ohnehin Versalien und Laufweite.

Wer die Lizenz hat, legt die Dateien unter `werkzeug/fonts/` beziehungsweise
`website/schrift/` ab und baut neu.



## Vorlagen für Veranstaltungen

`werkzeug/events.py` erzeugt `vorlagen/event_*` — drei Formate, zwei Anlassarten,
drei Macharten:

    Formate    Discord-Titelbild 800×320 · Discord-Ankündigung 1200×630
               Instagram-Beitrag 1080×1350
    Anlassart  Serie (wiederkehrend) · Special (einmalig)
    Machart    A Depesche · B Bild · C Plakat

Die drei Macharten sind eine echte Auswahl, weil sie etwas anderes können: die
**Depesche** trägt viele Angaben und kein Bild, das **Bild** trägt Stimmung und
wenig Text, das **Plakat** trägt ein Datum und sonst fast nichts. Gewählt wird
danach, was zu sagen ist — nicht danach, welche Farbe gefällt.

**Serie gegen Special** ist keine Beschriftung, sondern eine andere Gewichtung.
Bei einer Serie ist der Rhythmus die Nachricht: der Wochentag steht groß, das
Datum klein. Bei einem Special ist der Anlass die Nachricht: die Schlagzeile
steht groß, das Datum als Marke daneben.

Neu bauen, mit eigenen Bildern:

    python werkzeug/events.py --fotos <ordner>

Jede Zeile wird auf ihre verfügbare Breite geprüft und notfalls verkleinert.
Ohne das lief bei 1080 Breite die zweite Schlagzeile aus dem Bild
(`DER LUFTRETTU`) und die drei Datenspalten liefen ineinander — beides fällt im
Entwurf mit kurzen Platzhaltern nicht auf und erst mit echten Texten.

## Anmeldung

`branding.virtualairrescue.com` liegt **vollständig** hinter der Anmeldung —
Brandbook, Markenordner, Vorlagen, alles. Sie läuft über den VAR-Hub und
verlangt die Berechtigung `LOGIN_BRANDING`; geprüft wird zusätzlich, dass das
Konto nicht gesperrt und nicht gelöscht ist und die E-Mail-Adresse bestätigt
wurde.

> **Das Repository ist davon unberührt.** Es ist öffentlich, und dieselben
> Dateien sind dort ohne Anmeldung abrufbar. Wer das Material wirklich
> zurückhalten will, muss das Repository auf privat stellen — die Anmeldung vor
> der Seite allein tut das nicht.

Wie es funktioniert, was daran nicht Standard ist und wie man weitere Bereiche
schützt, steht in [`auth/README.md`](auth/README.md).

    node --test auth/    # 14 Prüfungen gegen einen nachgebauten Hub

**Die Zugangsdaten gehören in `.env`, nicht ins Repository.** Es ist
öffentlich: ein einmal gepushtes Geheimnis ist verbrannt, auch wenn der nächste
Commit es wieder entfernt — es steht dann immer noch in der Historie.

## Nutzung

Der Inhalt dieses Repositorys steht unter GPL-3.0 — das betrifft die Dateien und
die Skripte. Das Zeichen selbst ist die Kennzeichnung von Virtual Air Rescue;
eine Softwarelizenz ist keine Erlaubnis, fremde Kennzeichen als eigene zu
führen. Was im Einzelnen erlaubt ist, steht im Brandbook unter *Nutzung*.

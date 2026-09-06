# Event-Ideen

Zwölf Formate, die zur Sache passen — mit der Vorlage, die sie trägt, und dem,
was vorher entschieden sein muss. Die Reihenfolge ist eine Empfehlung: oben
steht, was am wenigsten Vorbereitung braucht und am meisten hergibt.

Alle genannten Vorlagen liegen in `vorlagen/` und werden mit
`werkzeug/events.py` beziehungsweise `werkzeug/event_banner.py` erzeugt.

---

## 1 · Gebietsabend

**Ein Bundesland oder Land pro Termin, alle seine Stationen besetzt.**

Die stärkste Idee aus den bisherigen Bannern — und die einzige, die sich selbst
erklärt: Wer seine Station auf der Karte findet, ist gemeint. Als Reihe
angelegt rotiert das Gebiet, und nach sechzehn Terminen war jedes Bundesland
einmal dran.

* Vorlage `event_gebiet_*` — die Silhouette kommt aus `werkzeug/gebiete.json`,
  die Stationsmarker setzen sich selbst. **22 Gebiete sind vorbereitet:** alle
  sechzehn Bundesländer sowie DE, AT, CH, NL, LU und IT.
* Zu entscheiden: Reihenfolge der Gebiete, und ob Stationen außerhalb
  mitspielen dürfen (Zubringer, Verlegungen ins Gebiet hinein).

## 2 · Dienstagsflug

**Der wöchentliche Termin. Immer gleich, deshalb ohne Ankündigungsaufwand.**

Eine Serie lebt davon, dass niemand mehr nachsehen muss. Das Banner nennt den
Wochentag groß und das Datum klein — genau dafür ist die Serienfassung gebaut.

* Vorlage `event_*_wiederkehrend_*`, alle drei Macharten.
* Zu entscheiden: fester Wochentag und feste Uhrzeit. Ohne beides ist es keine
  Serie.

## 3 · VAR Overload

**Alles gleichzeitig: Massenanfall, mehrere Einsatzstellen, zu wenig Fluggerät.**

Kein Flugevent, sondern ein Leitstellenevent — der Reiz liegt darin, dass die
Disposition zu wenig hat und priorisieren muss. Braucht vorbereitete Lagen und
mindestens zwei Disponenten.

* Vorlage `event_reihe_*` — der Schriftzug trägt das Banner, kein Foto nötig.
* Zu entscheiden: Wer schreibt die Lagen? Das ist die eigentliche Arbeit.

## 4 · Nachtflug

**Sechs Stunden, kein Tageslicht.** NVG, Außenlandung im Dunkeln, beleuchtete
Landeplätze.

* Vorlage `event_reihe_*` in der inversen Fassung, oder `event_*_b_bild` mit
  einem Nachtbild.
* Passt zum Profilbild `pb_nacht` — Kanal und Ankündigung ziehen dann am selben
  Strang.

## 5 · Leitstellenabend

**Die Leitstelle ist besetzt, alle Positionen gehen online, Zuschauer erwünscht.**

Der Termin, an dem man sieht, was VAR von einem Zufallsflug unterscheidet. Gute
Gelegenheit für ein Partnerlogo — VATSIM, ein Nachbar-Netzwerk, eine befreundete
VA.

* Vorlage `event_treffpunkt_*` — Zulu **und** lokal, Partnerfeld eingebaut.
  Auf dem flachen Discord-Titelbild entfällt das Partnerfeld; drei Marken auf
  320 px sind Gedränge.
* Zu entscheiden: welche Positionen, und wer sie besetzt.

## 6 · Tag der offenen Leitstelle

**Für Neue.** Mitlesen, mithören, Fragen stellen — ohne selbst zu fliegen.

Der niedrigschwellige Einstieg, den eine VA mit eigener Disposition anbieten
kann und eine ohne nicht.

* Vorlage `event_treffpunkt_*` oder `event_*_a_depesche` (viele Angaben, kein
  Bild).
* Zu entscheiden: Wer betreut die Fragen? Nicht nebenbei disponieren lassen.

## 7 · Sternflug

**Alle fliegen zum selben Platz.** Ein Ziel, viele Herkünfte, Ankunft im
Zeitfenster.

* Vorlage `event_*_c_plakat` — ein Datum, ein Ort, sonst nichts.
* Zu entscheiden: Platz mit genug Abstellfläche, und ob Anflug gestaffelt wird.

## 8 · Bergrettung / Winterdienst

**Saisonal:** Winde, Außenlandung am Hang, Wetterminimum.

* Vorlage `event_*_b_bild` mit Alpenmotiv, oder `event_gebiet_*` mit AT oder CH.
* Zu entscheiden: Mindestwetter und ob mit oder ohne Winde geflogen wird.

## 9 · Grenzgänger

**Zwei Länder, zwei Verfahren, ein Einsatz.** Verlegung über die Grenze,
Funkwechsel, unterschiedliche Statusgruppen.

* Vorlage `event_*_a_depesche` — hier zählen die Angaben, nicht das Bild.
* **Offen:** Die Gebietskarte zeigt derzeit *ein* Gebiet. Zwei nebeneinander
  wäre eine Erweiterung von `gebietskarte()` — machbar, aber nicht gebaut.

## 10 · Neue Station

**Eine Station geht in Betrieb.** Erstflug, Rufname, Einzugsgebiet.

* Vorlage `event_*_c_plakat` oder `vorlagen/veranstaltung_4x5.svg`.
* Zu entscheiden: Wer fliegt den Erstflug — das ist der Anlass, nicht die
  Station.

## 11 · 24 Stunden

**Rund um die Uhr, mit Schichtübergaben.** Das Format, das am ehesten zeigt,
dass eine Leitstelle mehr ist als ein Abend.

* Vorlage `event_*_a_depesche` (WANN/WO/DAUER) oder `event_reihe_*`.
* Zu entscheiden: Schichtplan. Ohne ihn schläft es um drei Uhr ein.

## 12 · Jahresbilanz

**Zahlen statt Termin:** Einsätze, Flugstunden, besetzte Stationen, längster
Flug.

Kein Event, sondern der Beitrag danach — gehört trotzdem hierher, weil er die
Reihe abschließt.

* Vorlage `vorlagen/zahl_1x1.svg` für eine einzelne Zahl,
  `vorlagen/karussell_*` für mehrere.

---

## Was für alle gilt

**Zulu ist verbindlich, lokal ist freundlich.** Beide Zeiten nennen. Die
Treffpunkt-Vorlage hat dafür zwei Zeilen, weil eine nicht reicht.

**Ein Termin, ein Banner, drei Formate.** Discord-Titelbild, Ankündigung und
Instagram-Beitrag entstehen aus demselben Aufruf — sie unterscheiden sich im
Zuschnitt, nicht im Inhalt.

**Serie oder Special entscheidet die Gewichtung**, nicht die Farbe. Bei einer
Serie ist der Rhythmus die Nachricht, bei einem Special der Anlass.

**Texte prüfen sich selbst.** Jede Zeile wird auf ihre Breite gemessen und
notfalls verkleinert. Trotzdem gilt: kurze Schlagzeilen tragen besser. Was auf
1080 px in zwei Zeilen passt, passt auf 800 × 320 in keine.

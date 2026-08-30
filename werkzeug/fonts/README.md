# fonts

**Hier fehlen vier Dateien** — und zwar mit Absicht.

    Uniform.ttf          Uniform Medium.ttf
    Uniform Bold.ttf     Uniform Black.ttf

Uniform ist eine kommerzielle Schrift von Richard Miller (MillerType), bezogen über
MyFonts, „All rights reserved". Sie darf nicht mitveröffentlicht werden. In diesem
Repository liegt sie deshalb nicht; im internen `var-v3` schon.

## Ohne sie fehlt was

`text2path.py` wandelt Text in Pfade und liest die Dateien von hier. Betroffen sind
die Lockups (`lockup/`), die Schriftproben im Brandbook und alle Vorlagen mit Text.
Die **Zeichen selbst** — Logo, Signet, Icons, Profilbilder — brauchen sie nicht: dort
ist die Wortmarke bereits ein Pfad und stammt aus `traced.json`.

Die fertigen SVGs im Bestand sind davon **nicht** betroffen. In ihnen ist der Text
längst in Kurven gewandelt; sie zeigen die Schrift, ohne sie zu enthalten. Nur das
**Neuerzeugen** braucht die Dateien.

## Nachlegen

Die vier Dateien aus dem internen Repository hierher kopieren, dann laufen alle
Generatoren wieder durch. Der Renderer lädt sie relativ zum Arbeitsverzeichnis —
also immer aus `werkzeug/` heraus aufrufen.

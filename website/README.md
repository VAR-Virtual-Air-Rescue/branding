# website

Der Onepager für **virtualairrescue.com** — hier als Anschauungsmaterial: er zeigt,
wie die Marke in einer echten Anwendung zusammengeht. Die Seite läuft ohne Server,
ohne Build und ohne externe Anfragen; `index.html` per Doppelklick öffnen genügt.

    index.tpl.html   Quelle
    index.html       gebaut — SVGs und Bilder sind eingebettet
    img/             sechs Motive, je als WebP in voller und halber Breite
    karte.json       Länderumrisse und Stationen für die Livekarte

Neu bauen:

    python ../werkzeug/mkpage.py index.tpl.html index.html

## Die Schrift fehlt hier — mit Absicht

`index.tpl.html` bindet Uniform über `{{FONT:schrift/uniform-*.woff2}}` ein. Diese
vier Schriftdateien sind **lizenzpflichtig und liegen deshalb nicht in diesem
Repository**. Die hier abgelegte `index.html` ist dieselbe gebaute Seite, aus der
die vier `@font-face`-Regeln entfernt wurden.

Sichtbar ist das kaum: der Schriftstapel fällt auf `system-ui` zurück, und weil
Uniform eine neutrale Grotesk ist, trägt die Systemschrift dieselbe Anmutung. Wer
die Lizenz hat, legt die Dateien unter `schrift/` ab und baut neu — dann sind sie
wieder drin.

Warum sie überhaupt eingebettet werden statt nachgeladen: die Seite soll ohne eine
einzige externe Anfrage auskommen. Das gilt für Schrift, Logos und Bilder
gleichermaßen.

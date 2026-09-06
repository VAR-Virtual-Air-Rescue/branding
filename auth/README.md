# Anmeldung über den VAR-Hub

Der Dienst, der aus einer Hub-Anmeldung eine eigene Sitzung macht. Er liefert
keine Inhalte aus — das bleibt nginx — und ist von außen nicht erreichbar.

    hub.mjs      alles, was mit dem Hub spricht
    sitzung.mjs  signierte Cookies, ohne Datenbank
    konfig.mjs   Umgebungsvariablen, mit Abbruch statt Rateverhalten
    server.mjs   die vier Routen
    pruefstand.mjs   nginx-Ersatz für die Arbeit ohne Docker

## Kein OIDC

Es sieht aus wie OAuth2 und heißt auch so, aber es ist es nicht: keine
Discovery, kein `/.well-known`, kein JWKS, kein `/token` nach Spezifikation.
Eine Standardbibliothek scheitert an genau diesen Stellen. Deshalb steht der
ganze Umgang mit dem Hub in **einer** Datei — mit den Eigenheiten als
Kommentar daneben, statt verstreut über Routen.

Die drei, die am ehesten Zeit kosten:

* **`state` ist Pflicht.** Fehlt er, hängt der Hub literal `null` an den
  Callback — die Prüfung vergleicht dann Müll mit Müll.
* **`application/x-www-form-urlencoded` ist Pflicht.** Mit JSON antwortet der
  Hub mit 415.
* **Der Code lebt 60 Sekunden.** Zwischen Callback und Einlösen steht deshalb
  nichts, was warten könnte. Ein 410 ist endgültig, der Hub löscht den Code
  dabei.

Und eine, die man nicht behandeln kann: fehlt dem Nutzer `LOGIN_BRANDING` oder
passt die `redirect_uri` nicht, zeigt der Hub **seine eigene Fehlerseite und
leitet nicht zurück**. Es gibt also keinen Fehler-Callback zum Auswerten — der
Nutzer kommt einfach nie an. Das `state`-Cookie läuft deshalb nach zehn Minuten
von selbst ab.

## Was der Browser bekommt

Nicht das Hub-Token. Es ist 30 Tage gültig, mit einem hub-internen Geheimnis
signiert und öffnet den ganzen Hub. Wir tauschen es einmal gegen den
Nutzerdatensatz und werfen es weg; was bleibt, ist eine eigene Sitzung:
HMAC-signiert, `httpOnly`, `SameSite=Lax`, standardmäßig sieben Tage.

`SameSite=Lax` und nicht `Strict`: der Nutzer kommt vom Hub per Weiterleitung
zurück, und bei `Strict` schickt der Browser bei diesem Wechsel kein Cookie mit
— die `state`-Prüfung schlüge dann **immer** fehl.

In der Sitzung steht wenig: `id`, `publicId`, Name, Bild, VATSIM-CID. Der
Hub-Datensatz enthält daneben E-Mail-Adresse, Badges, Moodle-Verknüpfung und
sämtliche Client-Einstellungen — das gehört nicht in ein Cookie im Browser des
Nutzers.

Das Signaturverfahren ist bewusst **kein** JWT, obwohl das Format ähnlich
aussieht: ein JWT trägt seinen Algorithmus in den Daten, und das ist die
bekannteste Fußangel der Bauart (`alg: none`). Hier gibt es ein Verfahren, es
steht nicht in den Daten, und es ist deshalb nicht verhandelbar.

## Routen

| Route | Was sie tut |
|---|---|
| `GET /api/auth/login?ziel=/pfad` | schickt zum Hub, legt den signierten `state` ab |
| `GET /api/auth/callback` | prüft `state`, löst den Code ein, stellt die Sitzung aus |
| `GET /api/auth/me` | die eigene Sitzung als JSON, sonst 401 |
| `GET /api/auth/pruefen` | 200/401 für `auth_request` in nginx |
| `POST /api/auth/logout` | löscht die eigene Sitzung |

`ziel` wird geprüft: nur Pfade auf dieser Seite. `//fremde.example` und
`/\fremde.example` sehen wie Pfade aus, werden vom Browser aber als Adresse
gelesen — ungeprüft wäre das eine offene Weiterleitung.

**Abmelden nur per POST.** Eine Abmeldung, die ein fremdes Bild in einem Forum
auslösen kann, ist keine. Der Hub selbst hat keinen Abmeldeendpunkt: wer sich
hier abmeldet und gleich wieder anmeldet, kommt ohne Passwort durch, weil die
Hub-Anmeldung bestehen bleibt.

## Was geschützt ist

Standardmäßig nur `/konto/`. **Das Brandbook bleibt offen** — es ist als
öffentliches Dokument gebaut.

Weitere Bereiche schützt man in der `nginx.conf`, nicht hier:

    location /intern/ {
      auth_request /_pruefe;
      error_page 401 = @anmelden;
      try_files $uri $uri/ =404;
    }

Der Vorteil gegenüber einer Prüfung im Seitenskript: die Datei geht gar nicht
erst hinaus.

## Prüfen

    node --test auth/          # 14 Prüfungen gegen einen nachgebauten Hub

Der echte Hub verlangt einen Menschen, der auf „Zugriff zulassen“ klickt — für
einen automatischen Lauf ist er damit nicht zu haben. Geprüft wird deshalb
alles, was *danach* passiert: `state`-Prüfung, die vier Zutrittsbedingungen,
dass das Hub-Token nirgends beim Browser landet, offene Weiterleitungen,
gefälschte Sitzungen, abgelaufene Codes.

Im Browser durchgehen, ohne Docker:

    node auth/server.mjs &     # mit gesetzten Umgebungsvariablen
    node auth/pruefstand.mjs   # http://localhost:8433

Der Prüfstand bildet ab, was im Betrieb nginx tut — statische Dateien,
`/api/auth/` weiterreichen, `/konto/` nur an Angemeldete. Nicht für den
Betrieb.

## Einstellungen

Siehe `../.env.example`. Der Dienst **startet nicht**, wenn `HUB_CLIENT_ID`,
`HUB_CLIENT_SECRET` oder ein mindestens 32 Zeichen langes `SESSION_SECRET`
fehlen. Das ist Absicht: ein Anmeldedienst, der sich stillschweigend ein
zufälliges Signaturgeheimnis nimmt, wirft bei jedem Neustart alle Sitzungen weg
— und niemand versteht, warum die Anmeldung „manchmal“ nicht hält.

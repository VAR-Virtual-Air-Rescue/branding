// Der Anmeldedienst der Branding-Seite.
//
// Er liefert keine Inhalte aus -- das macht weiterhin nginx. Er kann genau
// eines: aus einer Hub-Anmeldung eine eigene Sitzung machen und diese Sitzung
// auf Nachfrage bestaetigen. Deshalb steht er auch nicht im Traefik; nginx ist
// das einzige, was ihn erreicht.

import { createServer } from "node:http";
import { cfg } from "./konfig.mjs";
import { autorisierungsAdresse, tokenHolen, nutzerHolen, zutrittPruefen, sitzungsdaten } from "./hub.mjs";
import {
  packen, auspacken, sitzungAusstellen, zufallswert, cookiesLesen, NAMEN,
  sitzungsCookie, sitzungsCookieLoeschen, stateCookie, stateCookieLoeschen,
} from "./sitzung.mjs";

const STATE_TTL = 600;

// --- Antworten -------------------------------------------------------------

function json(res, status, daten, cookies = []) {
  const koerper = JSON.stringify(daten);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    // Antworten dieses Dienstes haengen an einem Cookie. Zwischengespeichert
    // waere die Antwort des einen die Antwort des naechsten.
    "Cache-Control": "no-store",
    ...(cookies.length ? { "Set-Cookie": cookies } : {}),
  });
  res.end(koerper);
}

function weiter(res, ort, cookies = []) {
  res.writeHead(302, {
    Location: ort,
    "Cache-Control": "no-store",
    ...(cookies.length ? { "Set-Cookie": cookies } : {}),
  });
  res.end();
}

/**
 * Fehlerseite statt Fehler-JSON.
 *
 * Hier landet ein Mensch, kein Programm: er hat auf "Anmelden" geklickt und
 * steht jetzt vor einem Problem, das er meist nicht selbst geschaffen hat --
 * fehlende Berechtigung, abgelaufener Code, Hub nicht erreichbar. Ein
 * JSON-Objekt hilft ihm nicht weiter.
 */
function fehlerseite(res, status, titel, text, cookies = []) {
  const html = `<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${titel} &middot; VAR Branding</title>
<style>
  :root{color-scheme:dark}
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#050B1C;
    color:#E7EAF3;font:15px/1.6 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;padding:24px}
  main{max-width:44ch}
  .kante{height:5px;background:#D5A507;margin-bottom:22px;transform:rotate(-3.2747deg);
    transform-origin:left center}
  h1{font-size:23px;font-weight:800;letter-spacing:-.02em;margin:0 0 10px}
  p{color:#8E97AE;margin:0 0 18px}
  a{color:#2B6EFF}
</style></head><body><main>
<div class="kante"></div>
<h1>${titel}</h1>
<p>${text}</p>
<p><a href="/">Zurück zum Brandbook</a></p>
</main></body></html>`;
  res.writeHead(status, {
    "Content-Type": "text/html; charset=utf-8",
    "Cache-Control": "no-store",
    ...(cookies.length ? { "Set-Cookie": cookies } : {}),
  });
  res.end(html);
}

/**
 * Ein Rücksprungziel, dem man trauen kann.
 *
 * Nur Pfade auf dieser Seite. `//fremde.example` und `/\fremde.example` sehen
 * wie Pfade aus, werden vom Browser aber als Adresse gelesen -- damit waere
 * dies eine offene Weiterleitung, die jemand anhaengt, um seinen Link
 * vertrauenswuerdig aussehen zu lassen.
 */
function zielPruefen(roh) {
  if (typeof roh !== "string" || !roh.startsWith("/")) return "/";
  if (roh.startsWith("//") || roh.startsWith("/\\")) return "/";
  return roh;
}

// --- Routen ----------------------------------------------------------------

/** Schritt 1: zum Hub schicken. */
function anmelden(req, res, url) {
  const ziel = zielPruefen(url.searchParams.get("ziel"));
  const wert = zufallswert();

  // Der Zufallswert geht an den Hub, Zufallswert *und* Ziel liegen signiert im
  // Cookie. Der Hub bekommt das Ziel nie zu sehen und kann es nicht faelschen.
  const cookie = packen({ s: wert, ziel }, STATE_TTL);
  weiter(res, autorisierungsAdresse(wert), [stateCookie(cookie)]);
}

/** Schritt 2 bis 4: Code einloesen, Nutzer holen, Sitzung ausstellen. */
async function rueckruf(req, res, url) {
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const cookies = cookiesLesen(req.headers.cookie);
  const erwartet = auspacken(cookies[NAMEN.state]);

  // Das state-Cookie ist ab hier verbraucht, egal wie es ausgeht.
  const weg = [stateCookieLoeschen()];

  if (!erwartet) {
    return fehlerseite(res, 400, "Anmeldung abgelaufen",
      "Der Anmeldevorgang ist zu lange her oder wurde in einem anderen Browser begonnen. " +
      "Bitte noch einmal von vorn.", weg);
  }
  if (!state || state !== erwartet.s) {
    return fehlerseite(res, 400, "Anmeldung abgebrochen",
      "Die Rückmeldung des Hubs passt nicht zu dieser Anmeldung. Aus Sicherheitsgründen " +
      "wurde sie verworfen.", weg);
  }
  if (!code) {
    return fehlerseite(res, 400, "Anmeldung unvollständig",
      "Der Hub hat keinen Anmeldecode mitgeschickt.", weg);
  }

  try {
    // Ab hier laeuft eine Uhr: der Code ist 60 Sekunden gueltig. Zwischen
    // diesen beiden Aufrufen steht deshalb nichts weiter.
    const token = await tokenHolen(code);
    const nutzer = await nutzerHolen(token);

    const grund = zutrittPruefen(nutzer);
    if (grund) {
      return fehlerseite(res, 403, "Kein Zugang", grund, weg);
    }

    // Das Token wird hier nicht weiterverwendet und nicht gespeichert. Es
    // verlaesst diese Funktion nicht.
    const sitzung = sitzungAusstellen(sitzungsdaten(nutzer));
    return weiter(res, erwartet.ziel || "/", [...weg, sitzungsCookie(sitzung)]);
  } catch (e) {
    console.error("[anmeldung] fehlgeschlagen:", e.status ?? "", e.message,
      e.hubText ? `| Hub: ${e.hubText}` : "");
    const abgelaufen = e.status === 410;
    return fehlerseite(res, abgelaufen ? 400 : 502,
      abgelaufen ? "Anmeldecode abgelaufen" : "Der Hub antwortet nicht",
      abgelaufen
        ? "Der Code des Hubs ist nur 60 Sekunden gültig und war schon zu alt. Bitte noch einmal anmelden."
        : "Die Anmeldung beim Hub hat nicht geklappt. Bitte später noch einmal versuchen.",
      weg);
  }
}

function abmelden(req, res) {
  // Der Hub hat keinen Abmeldeendpunkt. Wir loeschen unsere Sitzung; die
  // Anmeldung am Hub selbst bleibt bestehen. Wer sich hier abmeldet und gleich
  // wieder anmeldet, kommt deshalb ohne Passwort durch -- das ist so, und es
  // gehoert in die Oberflaeche geschrieben, nicht hier weggeschummelt.
  weiter(res, "/", [sitzungsCookieLoeschen()]);
}

function werBinIch(req, res) {
  const s = auspacken(cookiesLesen(req.headers.cookie)[NAMEN.sitzung]);
  if (!s) return json(res, 401, { angemeldet: false });
  const { exp, ...daten } = s;
  return json(res, 200, { angemeldet: true, ...daten, gueltigBis: exp });
}

/**
 * Fuer `auth_request` in nginx: nur der Status zaehlt, der Koerper wird
 * verworfen. Nicht angemeldet ist hier kein Fehler, sondern eine Auskunft.
 */
function pruefen(req, res) {
  const s = auspacken(cookiesLesen(req.headers.cookie)[NAMEN.sitzung]);
  if (!s) {
    res.writeHead(401, { "Cache-Control": "no-store" });
    return res.end();
  }
  res.writeHead(200, {
    "Cache-Control": "no-store",
    // nginx reicht diese Koepfe an die geschuetzte Seite weiter, wenn es sie
    // per `auth_request_set` abholt.
    "X-VAR-Nutzer": String(s.id ?? ""),
    "X-VAR-Name": encodeURIComponent(s.name ?? ""),
  });
  res.end();
}

// --- Verteiler -------------------------------------------------------------

const server = createServer((req, res) => {
  const url = new URL(req.url, cfg.basisUrl);
  const pfad = url.pathname.replace(/\/+$/, "") || "/";

  if (req.method === "GET" && pfad === "/api/auth/login") return anmelden(req, res, url);
  if (req.method === "GET" && pfad === "/api/auth/callback") return rueckruf(req, res, url);
  if (req.method === "GET" && pfad === "/api/auth/me") return werBinIch(req, res);
  if (req.method === "GET" && pfad === "/api/auth/pruefen") return pruefen(req, res);

  // Abmelden nur per POST: eine Abmeldung, die ein fremdes Bild im Forum
  // ausloesen kann, ist keine.
  if (req.method === "POST" && pfad === "/api/auth/logout") return abmelden(req, res);
  if (req.method === "GET" && pfad === "/api/auth/logout") {
    return fehlerseite(res, 405, "Abmelden nur per Formular",
      "Diese Adresse nimmt nur POST entgegen.");
  }

  if (pfad === "/api/auth/gesundheit") return json(res, 200, { ok: true });

  return json(res, 404, { fehler: "unbekannte Route" });
});

server.listen(cfg.port, "0.0.0.0", () => {
  console.log(
    `Anmeldedienst laeuft auf :${cfg.port}\n` +
      `  Hub          ${cfg.hubUrl}\n` +
      `  client_id    ${cfg.clientId}\n` +
      `  redirect_uri ${cfg.redirectUri}\n` +
      `  Berechtigung ${cfg.permission}\n` +
      `  Sitzung      ${cfg.sessionTage} Tage`
  );
});

for (const signal of ["SIGTERM", "SIGINT"]) {
  process.on(signal, () => server.close(() => process.exit(0)));
}

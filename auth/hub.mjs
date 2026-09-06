// Der Weg zum Hub. Alles, was mit hub.virtualairrescue.com spricht, steht hier
// -- und nur hier, damit die Eigenheiten dieses Verfahrens an einer Stelle
// dokumentiert sind statt verstreut in Routen.
//
// Es ist kein OIDC. Es gibt keine Discovery, kein /.well-known, keine JWKS und
// kein /token nach Spezifikation. Wer hier eine Standardbibliothek einsetzt,
// scheitert an genau diesen Stellen.

import { cfg } from "./konfig.mjs";

/** Der Nutzer wird hierhin geschickt. Kein POST, keine Zwischenseite. */
export function autorisierungsAdresse(state) {
  const u = new URL("/oauth", cfg.hubUrl);
  u.searchParams.set("client_id", cfg.clientId);
  u.searchParams.set("redirect_uri", cfg.redirectUri);
  // `state` ist hier nicht optional. Der Hub haengt den Wert unveraendert an
  // den Callback -- fehlt er, steht dort die Zeichenkette "null", und die
  // Pruefung im Callback vergleicht dann Muell mit Muell.
  u.searchParams.set("state", state);
  return u.toString();
}

// Der Hub antwortet im Fehlerfall mit Klartext, nicht mit JSON. Die Codes sind
// eindeutig genug, um daraus eine brauchbare Meldung zu machen -- der
// Klartext-Body taugt dafuer nicht, er ist nicht fuer Endnutzer geschrieben.
const TAUSCH_FEHLER = {
  400: "Der Hub hat die Anfrage abgelehnt: code oder client_id fehlte.",
  401: "Der Hub kennt diese Zugangsdaten nicht (client_id oder client_secret falsch).",
  404: "Der Hub kennt diesen Anmeldecode nicht.",
  410: "Der Anmeldecode war aelter als 60 Sekunden. Bitte noch einmal anmelden.",
  415: "Der Hub hat den Inhaltstyp abgelehnt.",
  500: "Im Hub ist etwas schiefgegangen.",
};

/**
 * Code gegen Zugangstoken tauschen. Ausschliesslich serverseitig -- hier liegt
 * das `client_secret` im Spiel.
 *
 * Der Code lebt 60 Sekunden. Deshalb steht zwischen Callback und diesem Aufruf
 * nichts, was warten koennte: kein Datenbankzugriff, kein Logging in ein
 * fremdes System, keine Wiederholung mit Verzoegerung. Ein 410 ist endgueltig,
 * der Hub loescht den Code dabei.
 */
export async function tokenHolen(code) {
  const body = new URLSearchParams({
    code,
    client_id: cfg.clientId,
    client_secret: cfg.clientSecret,
  });

  const r = await fetch(new URL("/api/auth/accessToken", cfg.hubUrl), {
    method: "POST",
    // Pflicht. Mit application/json antwortet der Hub mit 415.
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
    signal: AbortSignal.timeout(cfg.hubTimeoutMs),
  });

  if (!r.ok) {
    const klartext = await r.text().catch(() => "");
    const err = new Error(TAUSCH_FEHLER[r.status] ?? `Hub antwortete mit ${r.status}.`);
    err.status = r.status;
    err.hubText = klartext.slice(0, 200);
    throw err;
  }

  const daten = await r.json();
  if (!daten?.access_token) {
    throw new Error("Der Hub antwortete mit 200, aber ohne access_token.");
  }
  return daten.access_token;
}

/**
 * Den Nutzerdatensatz holen.
 *
 * Das JWT ist mit einem hub-internen Geheimnis signiert, das diese Anwendung
 * nicht hat. Es hier selbst zu pruefen ginge nur ohne Signaturpruefung -- also
 * gar nicht. Stattdessen fragen wir den Hub: antwortet er mit 200, war das
 * Token gueltig. Das ist zugleich die einzige Stelle, an der wir das Token
 * ueberhaupt brauchen; danach wird es verworfen.
 */
export async function nutzerHolen(accessToken) {
  const r = await fetch(new URL("/api/user", cfg.hubUrl), {
    headers: { Authorization: `Bearer ${accessToken}` },
    signal: AbortSignal.timeout(cfg.hubTimeoutMs),
  });

  if (r.status === 401) throw new Error("Der Hub hat das Zugangstoken abgelehnt.");
  if (r.status === 404) throw new Error("Der Hub kennt diesen Nutzer nicht.");
  if (!r.ok) throw new Error(`Der Hub antwortete beim Nutzerabruf mit ${r.status}.`);

  return r.json();
}

/**
 * Darf dieser Nutzer herein?
 *
 * Vier Bedingungen, und alle vier werden hier geprueft und nicht anderswo. Der
 * Hub laesst die Zustimmungsseite nur sehen, wer `LOGIN_BRANDING` hat -- aber
 * darauf allein sollte sich diese Anwendung nicht verlassen: sie ist der Ort,
 * an dem die Sitzung entsteht, also gehoert die Entscheidung hierher.
 *
 * Rueckgabe: `null`, wenn alles passt, sonst der Grund als Text.
 */
export function zutrittPruefen(nutzer) {
  if (!nutzer || typeof nutzer !== "object") return "Der Hub lieferte keinen Nutzerdatensatz.";
  if (nutzer.isBanned) return "Dieses Konto ist gesperrt.";
  if (nutzer.isDeleted) return "Dieses Konto ist geloescht.";

  // `emailVerified` kommt je nach Datensatz als `true` oder als Zeitstempel des
  // Bestaetigungsmoments. Beides bedeutet bestaetigt; `false`, `null` und ein
  // fehlendes Feld bedeuten es nicht.
  if (!nutzer.emailVerified) return "Die E-Mail-Adresse dieses Kontos ist nicht bestaetigt.";

  const rechte = Array.isArray(nutzer.permissions) ? nutzer.permissions : [];
  if (!rechte.includes(cfg.permission)) {
    return `Diesem Konto fehlt die Berechtigung ${cfg.permission}.`;
  }
  return null;
}

/**
 * Aus dem vollstaendigen Hub-Datensatz wird das, was in der Sitzung landet.
 *
 * Bewusst wenig: der Datensatz enthaelt Badges, Moodle-Verknuepfung, saemtliche
 * Client-Einstellungen und die E-Mail-Adresse. Davon steht das meiste in einem
 * Cookie schlecht -- es waechst, es veraltet, und es liegt beim Nutzer im
 * Browser. Was die Branding-Seite anzeigt, ist ein Name und ein Bild.
 */
export function sitzungsdaten(nutzer) {
  return {
    id: nutzer.id,
    publicId: nutzer.publicId ?? null,
    name: nutzer.fullName || [nutzer.firstname, nutzer.lastname].filter(Boolean).join(" "),
    vorname: nutzer.firstname ?? null,
    bild: nutzer.image ?? null,
    vatsimCid: nutzer.vatsimCid ?? null,
  };
}

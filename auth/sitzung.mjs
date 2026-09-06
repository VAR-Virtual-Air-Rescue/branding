// Die eigene Sitzung: ein signiertes Cookie, keine Datenbank.
//
// Das Hub-JWT geht bewusst *nicht* an den Browser. Es ist 30 Tage gueltig, mit
// einem fremden Geheimnis signiert und oeffnet den ganzen Hub -- was davon im
// Browser eines Nutzers liegt, liegt zu viel. Wir tauschen es einmal gegen den
// Nutzerdatensatz ein und werfen es weg. Was bleibt, ist diese Sitzung: von
// uns ausgestellt, von uns signiert, nur fuer diese Seite.
//
// Kein JWT, obwohl das Format aehnlich aussieht. Ein JWT braucht einen
// Algorithmus-Kopf, und der ist die bekannteste Fussangel der Bauart
// (`alg: none`). Hier gibt es genau ein Verfahren, es steht nicht in den Daten,
// und es ist deshalb nicht verhandelbar.

import { createHmac, timingSafeEqual, randomBytes } from "node:crypto";
import { cfg } from "./konfig.mjs";

const SITZUNGS_COOKIE = "var_branding_sitzung";
const STATE_COOKIE = "var_branding_state";

function b64url(buf) {
  return Buffer.from(buf).toString("base64url");
}

function signieren(nutzlast) {
  return createHmac("sha256", cfg.sessionSecret).update(nutzlast).digest();
}

/**
 * Nutzlast + Signatur, beides base64url, durch einen Punkt getrennt.
 *
 * Dasselbe Verfahren traegt die Sitzung und den `state` des Anmeldevorgangs.
 * Der `state` muss neben dem Zufallswert das Ziel mitfuehren, auf das nach der
 * Anmeldung zurueckgesprungen wird -- und dieses Ziel darf der Nutzer zwischen
 * Hinweg und Rueckweg nicht austauschen koennen. Signiert ist es davor sicher,
 * ohne dass es dafuer einen Serverspeicher braucht.
 */
export function packen(daten, ttlSekunden) {
  const inhalt = { ...daten, exp: Math.floor(Date.now() / 1000) + ttlSekunden };
  const teil = b64url(JSON.stringify(inhalt));
  return `${teil}.${b64url(signieren(teil))}`;
}

export const sitzungAusstellen = (daten) => packen(daten, cfg.sessionTage * 86400);

/**
 * Signiertes Cookie einlesen. Gibt die Daten zurueck oder `null` -- nie einen
 * halb geprueften Zustand, und nie eine Teilinformation darueber, woran es
 * lag.
 */
export function auspacken(roh) {
  if (!roh || typeof roh !== "string") return null;
  const punkt = roh.lastIndexOf(".");
  if (punkt < 1) return null;

  const teil = roh.slice(0, punkt);
  const sig = Buffer.from(roh.slice(punkt + 1), "base64url");
  const erwartet = signieren(teil);

  // Laengen zuerst: `timingSafeEqual` wirft bei ungleicher Laenge, statt false
  // zu liefern.
  if (sig.length !== erwartet.length) return null;
  if (!timingSafeEqual(sig, erwartet)) return null;

  let inhalt;
  try {
    inhalt = JSON.parse(Buffer.from(teil, "base64url").toString("utf8"));
  } catch {
    return null;
  }

  // Die Ablaufzeit steht *innerhalb* der Signatur. Das Max-Age des Cookies
  // allein wuerde nichts sichern -- der Browser entscheidet, was er sendet,
  // nicht wir.
  if (typeof inhalt?.exp !== "number" || inhalt.exp * 1000 < Date.now()) return null;
  return inhalt;
}

export function zufallswert(bytes = 32) {
  return randomBytes(bytes).toString("base64url");
}

// --- Cookies ---------------------------------------------------------------

function bauen(name, wert, { maxAge, loeschen = false }) {
  const teile = [
    `${name}=${loeschen ? "" : wert}`,
    "Path=/",
    "HttpOnly",
    // Lax und nicht Strict: der Nutzer kommt vom Hub per Weiterleitung zurueck,
    // und bei Strict schickt der Browser bei diesem Wechsel kein Cookie mit --
    // die state-Pruefung im Callback schluege dann immer fehl.
    "SameSite=Lax",
    loeschen ? "Max-Age=0" : `Max-Age=${maxAge}`,
  ];
  if (!cfg.unsicherErlaubt) teile.push("Secure");
  return teile.join("; ");
}

export const sitzungsCookie = (wert) =>
  bauen(SITZUNGS_COOKIE, wert, { maxAge: cfg.sessionTage * 86400 });
export const sitzungsCookieLoeschen = () =>
  bauen(SITZUNGS_COOKIE, "", { loeschen: true });

// Der state lebt nur zwischen Hinweg und Rueckweg. Zehn Minuten sind reichlich
// fuer eine Anmeldung und kurz genug, dass ein abgebrochener Versuch nicht
// tagelang im Browser liegt -- und abgebrochen wird hier oefter als anderswo:
// wem `LOGIN_BRANDING` fehlt, den schickt der Hub gar nicht erst zurueck.
export const stateCookie = (wert) => bauen(STATE_COOKIE, wert, { maxAge: 600 });
export const stateCookieLoeschen = () => bauen(STATE_COOKIE, "", { loeschen: true });

export function cookiesLesen(header) {
  const raus = {};
  if (!header) return raus;
  for (const stueck of header.split(";")) {
    const i = stueck.indexOf("=");
    if (i < 1) continue;
    raus[stueck.slice(0, i).trim()] = decodeURIComponent(stueck.slice(i + 1).trim());
  }
  return raus;
}

export const sitzungLesen = auspacken;

export const NAMEN = { sitzung: SITZUNGS_COOKIE, state: STATE_COOKIE };

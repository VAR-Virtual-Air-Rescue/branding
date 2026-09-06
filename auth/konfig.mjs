// Alles Einstellbare an einer Stelle, und nichts davon im Code fest.
//
// Der Dienst startet nicht, wenn ein Geheimnis fehlt. Das ist Absicht: ein
// Anmeldedienst, der ohne `SESSION_SECRET` hochkommt und sich stillschweigend
// einen Zufallswert nimmt, wirft bei jedem Neustart alle Sitzungen weg -- und
// niemand versteht, warum die Anmeldung "manchmal" nicht haelt.

function pflicht(name) {
  const v = process.env[name];
  if (!v || !v.trim()) {
    console.error(
      `\nStart abgebrochen: ${name} ist nicht gesetzt.\n` +
        `Siehe .env.example -- die Datei nennt jede Variable und wofuer sie da ist.\n`
    );
    process.exit(1);
  }
  return v.trim();
}

function zahl(name, standard) {
  const v = process.env[name];
  if (v === undefined || v === "") return standard;
  const n = Number(v);
  if (!Number.isFinite(n) || n <= 0) {
    console.error(`Start abgebrochen: ${name} ist keine positive Zahl (${v}).`);
    process.exit(1);
  }
  return n;
}

const basisUrl = (process.env.BRANDING_BASE_URL || "https://branding.virtualairrescue.com")
  .replace(/\/+$/, "");

// Ein zu kurzes Signaturgeheimnis ist schlimmer als ein offensichtlich
// fehlendes -- es sieht nach Sicherheit aus. 32 Zeichen sind das Minimum, das
// wir durchgehen lassen.
const geheimnis = pflicht("SESSION_SECRET");
if (geheimnis.length < 32) {
  console.error(
    `\nStart abgebrochen: SESSION_SECRET ist nur ${geheimnis.length} Zeichen lang.\n` +
      `Mindestens 32. Erzeugen mit:  openssl rand -hex 32\n`
  );
  process.exit(1);
}

export const cfg = {
  hubUrl: (process.env.HUB_URL || "https://hub.virtualairrescue.com").replace(/\/+$/, ""),
  clientId: pflicht("HUB_CLIENT_ID"),
  clientSecret: pflicht("HUB_CLIENT_SECRET"),

  basisUrl,
  // Der Hub prueft die redirect_uri als Praefix gegen die hinterlegte Adresse.
  // Unterpfade sind damit erlaubt -- deshalb dieser hier und nicht die nackte
  // Domain.
  redirectUri: `${basisUrl}/api/auth/callback`,

  permission: process.env.ERFORDERLICHE_PERMISSION || "LOGIN_BRANDING",

  sessionSecret: geheimnis,
  // Kuerzer als die 30 Tage des Hub-JWT: die Sitzung ist unsere, nicht seine,
  // und wir koennen sie jederzeit neu ausstellen.
  sessionTage: zahl("SESSION_TAGE", 7),

  hubTimeoutMs: zahl("HUB_TIMEOUT_MS", 8000),
  port: zahl("PORT", 8080),

  // Nur fuer die Entwicklung: ohne HTTPS setzt der Browser ein `Secure`-Cookie
  // nicht. Im Betrieb hinter Traefik bleibt das aus.
  unsicherErlaubt: process.env.COOKIE_UNSICHER === "1",
};

if (cfg.unsicherErlaubt) {
  console.warn(
    "COOKIE_UNSICHER=1 -- Sitzungscookies werden ohne `Secure` gesetzt. " +
      "Das gehoert in die Entwicklung, nicht in den Betrieb."
  );
}

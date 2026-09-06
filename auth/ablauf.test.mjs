// Der ganze Anmeldeweg gegen einen nachgebauten Hub.
//
//     node --test auth/
//
// Warum ein nachgebauter Hub und nicht der echte: der echte verlangt einen
// Menschen, der auf "Zugriff zulassen" klickt. Damit ist er fuer einen
// automatischen Lauf nicht zu haben -- und genau deshalb ist alles, was
// *danach* passiert, umso wichtiger zu pruefen. Der Nachbau haelt sich an die
// Eigenheiten, die dokumentiert sind: Klartext-Fehler, Pflicht-Inhaltstyp,
// 60-Sekunden-Code.

import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";

const NUTZER_OK = {
  id: 42, publicId: "abc123", firstname: "Max", lastname: "Mustermann",
  email: "max@example.com", image: "https://example.com/max.png", vatsimCid: 1234567,
  fullName: "Max Mustermann - 1234", permissions: ["LOGIN_BRANDING", "IRGENDWAS"],
  emailVerified: true, isBanned: false, isDeleted: false,
};

let hub, hubPort, dienst, dienstPort;
const hubZustand = { codes: new Map(), nutzer: NUTZER_OK, tauschStatus: 200 };

function freierPort(server) {
  return server.address().port;
}

before(async () => {
  // --- Hub-Nachbau ---------------------------------------------------------
  hub = createServer((req, res) => {
    const url = new URL(req.url, "http://x");

    if (url.pathname === "/oauth") {
      // Der echte Hub zeigt hier eine Zustimmungsseite. Der Nachbau springt
      // sofort zurueck -- geprueft wird, was wir mit der Rueckmeldung machen.
      const code = "c" + Math.random().toString(16).slice(2, 10);
      hubZustand.codes.set(code, Date.now());
      const ziel = new URL(url.searchParams.get("redirect_uri"));
      ziel.searchParams.set("code", code);
      ziel.searchParams.set("state", url.searchParams.get("state") ?? "null");
      res.writeHead(302, { Location: ziel.toString() });
      return res.end();
    }

    if (url.pathname === "/api/auth/accessToken") {
      if (req.headers["content-type"] !== "application/x-www-form-urlencoded") {
        res.writeHead(415, { "Content-Type": "text/plain" });
        return res.end("unsupported media type");
      }
      let roh = "";
      req.on("data", (c) => (roh += c));
      return req.on("end", () => {
        if (hubZustand.tauschStatus !== 200) {
          res.writeHead(hubZustand.tauschStatus, { "Content-Type": "text/plain" });
          return res.end("fehler");
        }
        const p = new URLSearchParams(roh);
        if (!p.get("code")) { res.writeHead(400); return res.end("no code"); }
        if (p.get("client_secret") !== "geheim-geheim") {
          res.writeHead(401, { "Content-Type": "text/plain" });
          return res.end("bad client");
        }
        if (!hubZustand.codes.has(p.get("code"))) {
          res.writeHead(404, { "Content-Type": "text/plain" });
          return res.end("unknown code");
        }
        hubZustand.codes.delete(p.get("code"));
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ access_token: "jwt.aus.dem.hub", token_type: "Bearer" }));
      });
    }

    if (url.pathname === "/api/user") {
      if (req.headers.authorization !== "Bearer jwt.aus.dem.hub") {
        res.writeHead(401); return res.end();
      }
      res.writeHead(200, { "Content-Type": "application/json" });
      return res.end(JSON.stringify(hubZustand.nutzer));
    }

    res.writeHead(404); res.end();
  });
  hub.listen(0, "127.0.0.1");
  await once(hub, "listening");
  hubPort = freierPort(hub);

  // --- Anmeldedienst -------------------------------------------------------
  // Einen freien Port besorgen, indem wir einen aufmachen und gleich wieder
  // schliessen. Fest verdrahtete Portnummern in Tests kollidieren irgendwann.
  const probe = createServer();
  probe.listen(0, "127.0.0.1");
  await once(probe, "listening");
  dienstPort = freierPort(probe);
  await new Promise((r) => probe.close(r));

  // `new URL(...).pathname` gaebe unter Windows `/C:/...` -- spawn macht daraus
  // einen Pfad, den es nicht gibt.
  const serverPfad = fileURLToPath(new URL("./server.mjs", import.meta.url));
  dienst = spawn(process.execPath, [serverPfad], {
    env: {
      ...process.env,
      HUB_URL: `http://127.0.0.1:${hubPort}`,
      HUB_CLIENT_ID: "5",
      HUB_CLIENT_SECRET: "geheim-geheim",
      BRANDING_BASE_URL: `http://127.0.0.1:${dienstPort}`,
      SESSION_SECRET: "x".repeat(48),
      COOKIE_UNSICHER: "1",
      PORT: String(dienstPort),
    },
    stdio: ["ignore", "pipe", "inherit"],
  });
  // Auf die Startmeldung warten, statt blind zu schlafen.
  for await (const stueck of dienst.stdout) {
    if (String(stueck).includes("Anmeldedienst laeuft")) break;
  }
});

after(() => {
  dienst?.kill();
  hub?.close();
});

const basis = () => `http://127.0.0.1:${dienstPort}`;

/** Cookies aus `set-cookie` in einen Kopfwert zusammenfassen. */
function cookieKopf(vorher, antwort) {
  const topf = new Map(vorher.map((c) => [c.split("=")[0], c]));
  for (const s of antwort.headers.getSetCookie?.() ?? []) {
    const stueck = s.split(";")[0];
    const [name, wert] = [stueck.slice(0, stueck.indexOf("=")), stueck];
    if (wert.endsWith("=")) topf.delete(name);
    else topf.set(name, wert);
  }
  return [...topf.values()];
}

/** Den ganzen Weg gehen: /login -> Hub -> /callback. Gibt die Cookies zurueck. */
async function anmelden(ziel = "/") {
  const a = await fetch(`${basis()}/api/auth/login?ziel=${encodeURIComponent(ziel)}`,
    { redirect: "manual" });
  assert.equal(a.status, 302, "login leitet weiter");
  let kekse = cookieKopf([], a);

  const hubZiel = a.headers.get("location");
  const b = await fetch(hubZiel, { redirect: "manual" });
  const zurueck = b.headers.get("location");

  const c = await fetch(zurueck, {
    redirect: "manual",
    headers: { cookie: kekse.join("; ") },
  });
  kekse = cookieKopf(kekse, c);
  return { antwort: c, kekse };
}

test("Anmeldeadresse traegt client_id, redirect_uri und state", async () => {
  const r = await fetch(`${basis()}/api/auth/login`, { redirect: "manual" });
  const u = new URL(r.headers.get("location"));
  assert.equal(u.pathname, "/oauth");
  assert.equal(u.searchParams.get("client_id"), "5");
  assert.equal(u.searchParams.get("redirect_uri"), `${basis()}/api/auth/callback`);
  // Ohne state haengt der Hub literal "null" an den Callback.
  assert.ok((u.searchParams.get("state") ?? "").length > 20, "state ist gesetzt und lang");
});

test("der ganze Weg endet mit einer Sitzung", async () => {
  const { antwort, kekse } = await anmelden("/konto/");
  assert.equal(antwort.status, 302);
  assert.equal(antwort.headers.get("location"), "/konto/", "springt auf das Ziel zurueck");

  const sitzung = kekse.find((c) => c.startsWith("var_branding_sitzung="));
  assert.ok(sitzung, "Sitzungscookie gesetzt");

  const roh = antwort.headers.getSetCookie().join(" ");
  assert.match(roh, /HttpOnly/, "Sitzung ist httpOnly");
  assert.match(roh, /SameSite=Lax/, "Lax, sonst kommt das Cookie beim Rueckweg nicht mit");

  const me = await fetch(`${basis()}/api/auth/me`, { headers: { cookie: kekse.join("; ") } });
  const d = await me.json();
  assert.equal(me.status, 200);
  assert.equal(d.angemeldet, true);
  assert.equal(d.name, "Max Mustermann - 1234");
});

test("das Hub-Token landet nirgends beim Browser", async () => {
  const { antwort, kekse } = await anmelden();
  const alles = antwort.headers.getSetCookie().join(" ") + " " + kekse.join(" ");
  assert.ok(!alles.includes("jwt.aus.dem.hub"), "kein Hub-JWT in einem Cookie");

  const me = await fetch(`${basis()}/api/auth/me`, { headers: { cookie: kekse.join("; ") } });
  const text = await me.text();
  assert.ok(!text.includes("jwt.aus.dem.hub"), "kein Hub-JWT in der Auskunft");
  // Auch die E-Mail-Adresse gehoert nicht in die Sitzung.
  assert.ok(!text.includes("max@example.com"), "keine E-Mail-Adresse in der Sitzung");
});

test("falscher state wird abgewiesen", async () => {
  const a = await fetch(`${basis()}/api/auth/login`, { redirect: "manual" });
  const kekse = cookieKopf([], a);
  const r = await fetch(`${basis()}/api/auth/callback?code=egal&state=erfunden`, {
    redirect: "manual",
    headers: { cookie: kekse.join("; ") },
  });
  assert.equal(r.status, 400);
  assert.match(await r.text(), /abgebrochen/i);
});

test("ohne state-Cookie kein Zugang", async () => {
  const r = await fetch(`${basis()}/api/auth/callback?code=egal&state=egal`,
    { redirect: "manual" });
  assert.equal(r.status, 400);
});

test("fehlende Berechtigung sperrt aus", async () => {
  hubZustand.nutzer = { ...NUTZER_OK, permissions: ["SONST_WAS"] };
  const { antwort } = await anmelden();
  assert.equal(antwort.status, 403);
  assert.match(await antwort.text(), /LOGIN_BRANDING/);
  hubZustand.nutzer = NUTZER_OK;
});

test("gesperrt, geloescht, unbestaetigt -- jedes einzeln sperrt aus", async () => {
  for (const [feld, wert, muster] of [
    ["isBanned", true, /gesperrt/i],
    ["isDeleted", true, /gel(oe|ö)scht/i],
    ["emailVerified", false, /best(ae|ä)tigt/i],
  ]) {
    hubZustand.nutzer = { ...NUTZER_OK, [feld]: wert };
    const { antwort } = await anmelden();
    assert.equal(antwort.status, 403, `${feld} muss sperren`);
    assert.match(await antwort.text(), muster);
  }
  hubZustand.nutzer = NUTZER_OK;
});

test("emailVerified als Zeitstempel gilt als bestaetigt", async () => {
  hubZustand.nutzer = { ...NUTZER_OK, emailVerified: "2024-03-01T10:00:00.000Z" };
  const { antwort } = await anmelden();
  assert.equal(antwort.status, 302, "ein Zeitstempel bedeutet bestaetigt");
  hubZustand.nutzer = NUTZER_OK;
});

test("abgelaufener Code: eigene Meldung, kein 502", async () => {
  hubZustand.tauschStatus = 410;
  const { antwort } = await anmelden();
  assert.equal(antwort.status, 400);
  assert.match(await antwort.text(), /60 Sekunden/);
  hubZustand.tauschStatus = 200;
});

test("Hub nicht erreichbar: 502 statt Absturz", async () => {
  hubZustand.tauschStatus = 500;
  const { antwort } = await anmelden();
  assert.equal(antwort.status, 502);
  hubZustand.tauschStatus = 200;
});

test("offene Weiterleitung ist nicht moeglich", async () => {
  for (const boese of ["//example.com", "/\\example.com", "https://example.com"]) {
    const { antwort } = await anmelden(boese);
    assert.equal(antwort.headers.get("location"), "/",
      `${boese} darf nicht als Ziel durchgehen`);
  }
});

test("pruefen antwortet 401 ohne und 200 mit Sitzung", async () => {
  const ohne = await fetch(`${basis()}/api/auth/pruefen`);
  assert.equal(ohne.status, 401);

  const { kekse } = await anmelden();
  const mit = await fetch(`${basis()}/api/auth/pruefen`, {
    headers: { cookie: kekse.join("; ") },
  });
  assert.equal(mit.status, 200);
  assert.equal(mit.headers.get("x-var-nutzer"), "42");
});

test("gefaelschte Sitzung wird nicht angenommen", async () => {
  const { kekse } = await anmelden();
  const echt = kekse.find((c) => c.startsWith("var_branding_sitzung="));
  // Ein Zeichen in der Nutzlast kippen -- die Signatur passt dann nicht mehr.
  const kaputt = echt.slice(0, 30) + (echt[30] === "A" ? "B" : "A") + echt.slice(31);
  const r = await fetch(`${basis()}/api/auth/me`, { headers: { cookie: kaputt } });
  assert.equal(r.status, 401);
});

test("Abmelden loescht die Sitzung, GET geht nicht", async () => {
  const { kekse } = await anmelden();
  const nein = await fetch(`${basis()}/api/auth/logout`, {
    redirect: "manual", headers: { cookie: kekse.join("; ") },
  });
  assert.equal(nein.status, 405, "kein Abmelden per GET");

  const ja = await fetch(`${basis()}/api/auth/logout`, {
    method: "POST", redirect: "manual", headers: { cookie: kekse.join("; ") },
  });
  assert.equal(ja.status, 302);
  assert.match(ja.headers.getSetCookie().join(" "), /var_branding_sitzung=;.*Max-Age=0/);
});

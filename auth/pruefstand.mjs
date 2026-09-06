// Der Stack ohne Docker: ein Prozess, der tut, was im Betrieb nginx und der
// Anmeldedienst gemeinsam tun.
//
//     node auth/pruefstand.mjs
//
// Damit laesst sich der Anmeldeweg im Browser durchgehen, ohne einen Container
// zu bauen. Er bildet dieselben drei Dinge ab wie die nginx.conf: statische
// Dateien ausliefern, /api/auth/ an den Dienst geben und /konto/ nur an
// Angemeldete. Mehr nicht -- gzip, MIME-Tabelle und Verzeichnisuebersicht
// bleiben Sache von nginx.
//
// **Nicht fuer den Betrieb.** Hier steht keine Absicherung, die ueber das
// hinausgeht, was zum Ausprobieren noetig ist.

import { createServer } from "node:http";
import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { join, extname, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const WURZEL = fileURLToPath(new URL("..", import.meta.url));
const DIENST = process.env.AUTH_URL || "http://127.0.0.1:8080";
const PORT = Number(process.env.PRUEFSTAND_PORT || 8433);

const TYPEN = {
  ".html": "text/html; charset=utf-8", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp",
  ".json": "application/json; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".md": "text/markdown; charset=utf-8",
};

/** Anfrage an den Anmeldedienst durchreichen, Cookies in beide Richtungen. */
async function durchreichen(req, res, pfad) {
  const koerper = ["GET", "HEAD"].includes(req.method) ? undefined : await roh(req);
  const r = await fetch(DIENST + pfad, {
    method: req.method,
    headers: { cookie: req.headers.cookie ?? "", "content-type": req.headers["content-type"] ?? "" },
    body: koerper,
    redirect: "manual",
  });
  const kopf = {};
  for (const [k, v] of r.headers) if (k !== "set-cookie") kopf[k] = v;
  const kekse = r.headers.getSetCookie();
  if (kekse.length) kopf["set-cookie"] = kekse;
  res.writeHead(r.status, kopf);
  res.end(Buffer.from(await r.arrayBuffer()));
}

function roh(req) {
  return new Promise((f) => {
    const t = [];
    req.on("data", (c) => t.push(c));
    req.on("end", () => f(Buffer.concat(t)));
  });
}

/** Das Gegenstueck zu `auth_request`. */
async function angemeldet(req) {
  const r = await fetch(DIENST + "/api/auth/pruefen", {
    headers: { cookie: req.headers.cookie ?? "" },
  });
  return r.status === 200;
}

async function datei(res, pfad) {
  try {
    let p = join(WURZEL, normalize(pfad).replace(/^([/\\])+/, ""));
    if ((await stat(p)).isDirectory()) p = join(p, "index.html");
    const s = await stat(p);
    res.writeHead(200, {
      "Content-Type": TYPEN[extname(p)] ?? "application/octet-stream",
      "Content-Length": s.size,
    });
    createReadStream(p).pipe(res);
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("nicht gefunden");
  }
}

createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const pfad = url.pathname;

  if (pfad.startsWith("/api/auth/")) return durchreichen(req, res, pfad + url.search);

  if (pfad.startsWith("/konto")) {
    if (!(await angemeldet(req))) {
      res.writeHead(302, { Location: "/api/auth/login?ziel=" + encodeURIComponent(pfad) });
      return res.end();
    }
    return datei(res, pfad === "/konto" ? "/konto/index.html" : pfad);
  }

  if (pfad === "/") return datei(res, "/brandbook/index.html");
  return datei(res, pfad);
}).listen(PORT, () => {
  console.log(`Pruefstand auf http://localhost:${PORT}  (Dienst: ${DIENST})`);
  console.log("Nicht fuer den Betrieb -- im Betrieb macht das nginx.");
});

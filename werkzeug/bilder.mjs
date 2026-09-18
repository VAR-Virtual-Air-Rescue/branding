// Bewegte SVG-Fassungen als Bildfolge -- fuer GIF und APNG.
//
//     node bilder.mjs <in.svg> <ausgabeordner> [breite] [fps] [sekunden]
//
// resvg kennt kein SMIL; hier rendert Chromium. Die Zeit wird nicht abgewartet,
// sondern gesetzt: `setCurrentTime(t)` auf dem SVG-Wurzelelement springt die
// Animation exakt an die Stelle, und jedes Bild ist damit ein bestimmter
// Zeitpunkt statt "irgendwann in der Naehe". Sonst haengen die Bilder an der
// Rechenlast beim Aufnehmen, und die Schleife hat am Ende eine andere Laenge
// als am Anfang.
//
// Playwright kommt aus social-studio -- dort ist es installiert, hier nicht.
import { createRequire } from "node:module";
import { readFileSync, mkdirSync } from "node:fs";
import { join, resolve } from "node:path";

const req = createRequire("C:/Users/TimmR/Documents/LH-Virtual/social-studio/package.json");
const { chromium } = req("playwright");

const [eingabe, ordner, breite = "512", fps = "20", sek = "9"] = process.argv.slice(2);
if (!eingabe || !ordner) { console.error("Aufruf: node bilder.mjs in.svg ordner [px] [fps] [s]"); process.exit(1); }

const W = Number(breite), FPS = Number(fps), DAUER = Number(sek);
const N = Math.round(FPS * DAUER);
mkdirSync(ordner, { recursive: true });
const svg = readFileSync(resolve(eingabe), "utf8");

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: W }, deviceScaleFactor: 1 });
// Transparent, damit der Kreis freisteht -- Discord legt es auf seinen eigenen Grund.
await page.setContent(
  `<!doctype html><html><body style="margin:0;background:transparent">` +
  `<div id="w" style="width:${W}px;height:${W}px">${svg}</div></body></html>`);
await page.evaluate(() => {
  const s = document.querySelector("#w svg");
  s.setAttribute("width", "100%"); s.setAttribute("height", "100%");
  s.pauseAnimations();
});
for (let i = 0; i < N; i++) {
  const t = i / FPS;
  await page.evaluate((t) => document.querySelector("#w svg").setCurrentTime(t), t);
  await page.screenshot({ path: join(ordner, `b${String(i).padStart(4, "0")}.png`),
                          omitBackground: true });
}
await browser.close();
console.log(`${N} Bilder nach ${ordner} (${W} px, ${FPS} fps, ${DAUER} s)`);

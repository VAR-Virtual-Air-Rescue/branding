// node render.mjs <in.svg> <out.png> <width>
import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { Resvg } from "@resvg/resvg-js";
const [,, input, output, w] = process.argv;
const fontFiles = readdirSync("fonts").map(f => "fonts/" + f);
const r = new Resvg(readFileSync(input, "utf8"), {
  fitTo: { mode: "width", value: Number(w) },
  background: "rgba(255,255,255,0)",
  font: { fontFiles, loadSystemFonts: true, defaultFontFamily: "Uniform" },
});
writeFileSync(output, r.render().asPng());
console.log("ok", output, w + "px");

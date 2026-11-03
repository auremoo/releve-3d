#!/usr/bin/env node
/* Produit, à partir de logo.svg et favicon.svg, les images servies par GitHub Pages :
   - apple-touch-icon.png (180×180, fond opaque : iOS n'accepte pas de SVG ici et noircit la transparence) ;
   - og-image.png (1200×630, aperçu des liens partagés : les réseaux sociaux n'acceptent pas le SVG).
   Usage : node scripts/build_images.js   (nécessite Playwright et Chromium ; les polices viennent de Google Fonts). */
const path = require("path"), fs = require("fs");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const uri = f => "data:image/svg+xml;base64," + fs.readFileSync(path.join(root, f)).toString("base64");
const logo = uri("favicon.svg"), full = uri("logo.svg"); // full : cadre complet, marges comprises (icône d'app)
const fonts = '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">';

const touch = `<!doctype html><meta charset="utf-8"><style>
html,body{margin:0;width:180px;height:180px;background:#FFFFFF}
img{display:block;width:180px;height:180px}</style><img src="${full}">`;

const ticks = Array.from({length:121}, (_, i) => {
  const x = 10 * i, h = i % 10 === 0 ? 30 : i % 5 === 0 ? 20 : 11;
  const label = i % 10 === 0 && i > 0 && i < 120 ? `<text x="${x + 5}" y="44">${i / 10}</text>` : "";
  return `<line x1="${x}" y1="0" x2="${x}" y2="${h}"/>` + label;
}).join("");

const og = `<!doctype html><meta charset="utf-8">${fonts}<style>
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#EEF2F8;color:#0F1E36;font-family:Archivo,sans-serif;position:relative}
.main{position:absolute;left:96px;right:96px;top:0;bottom:72px;display:flex;align-items:center;gap:56px}
img{width:240px;height:240px;flex:none}
h1{margin:0;font-weight:800;font-stretch:122%;font-size:112px;line-height:1;letter-spacing:-.03em}
p{margin:22px 0 0;font-size:36px;line-height:1.25;color:#56647D;max-width:700px;text-wrap:balance}
.tape{position:absolute;left:0;right:0;bottom:0;height:72px;background:#F26B1D}
.tape svg{display:block}
.tape line{stroke:#1F0E02;stroke-width:2}
.tape text{font:500 18px "IBM Plex Mono",monospace;fill:#1F0E02}
</style>
<div class="main"><img src="${logo}"><div><h1>Relevé 3D</h1><p>Des photos d’un logement ou d’un objet à&nbsp;la maquette 3D cotée, exportable en&nbsp;GLB.</p></div></div>
<div class="tape"><svg width="1200" height="72">${ticks}</svg></div>`;

(async () => {
  const browser = await chromium.launch();
  for (const [file, html, w, h] of [["apple-touch-icon.png", touch, 180, 180], ["og-image.png", og, 1200, 630]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.setContent(html, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(root, file) });
    await page.close();
    console.log(file);
  }
  await browser.close();
})();

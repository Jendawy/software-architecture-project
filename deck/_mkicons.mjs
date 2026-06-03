// Recolor Untitled UI line-icon SVGs and rasterize to crisp transparent PNGs.
// Uses Playwright/Chromium from the capstone Task Manager node_modules.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire('C:/Development/Task Manager/');
const { chromium } = require('playwright');

const HERE = 'C:/Development/Software Architecture - Base/deck';
const SRC = join(HERE, '_icons_src');
const OUT = join(HERE, '_ico');
mkdirSync(OUT, { recursive: true });

const C = {
  indigo: '#4A45C7', clay: '#BC5A2B', teal: '#0E7C72', violet: '#7C3AED',
  green: '#1E7A45', amber: '#B5760C', red: '#BB2D23', ink: '#1B1A17',
  mute: '#8A867E', white: '#FFFFFF',
  indigo_d: '#8E8BF5', violet_d: '#B6A6F7', teal_d: '#4FC2B2',
  green_d: '#5BD08F', amber_d: '#E7B765',
};

// icon -> list of color keys to render
const USES = {
  'clipboard-check': ['indigo'], 'zap': ['indigo'], 'target-04': ['indigo','indigo_d','white'],
  'target-01': ['indigo'], 'cube-01': ['indigo'], 'check-square': ['indigo'],
  'shield-tick': ['indigo'], 'alert-triangle': ['amber'], 'git-branch-01': ['red'],
  'magic-wand-01': ['green'], 'package': ['clay'], 'package-plus': ['clay'],
  'switch-horizontal-01': ['teal'], 'switch-vertical-01': ['indigo'],
  'refresh-cw-01': ['violet','violet_d'], 'book-open-01': ['clay','teal','indigo'],
  'puzzle-piece-01': ['clay','teal','violet','indigo','violet_d','white'],
  'plus-circle': ['clay','teal'], 'file-02': ['clay'], 'compass': ['teal'],
  'grid-01': ['indigo','teal','teal_d','white'], 'dataflow-03': ['indigo'],
  'layers-three-01': ['indigo'], 'settings-01': ['indigo'], 'lock-unlocked-01': ['indigo'],
  'columns-02': ['indigo'], 'anchor': ['indigo'], 'terminal': ['indigo','green','green_d','white'],
  'browser': ['indigo'], 'trend-up-01': ['green'], 'check-circle': ['green'],
  'alert-circle': ['amber'], 'intersect-circle': ['indigo'], 'clock-fast-forward': ['indigo'],
  'check-verified-01': ['green'], 'trophy-01': ['amber','amber_d','white'], 'arrow-narrow-right': ['mute'],
  'list': ['indigo'], 'server-02': ['indigo'], 'code-02': ['indigo'], 'cpu-chip-01': ['indigo'],
  'bar-chart-08': ['green'], 'presentation-chart-01': ['indigo'], 'clock-refresh': ['violet'],
  'lock-01': ['red'], 'arrows-triangle': ['indigo'],
};

const SIZE = 256;          // supersample for crisp downscale in pptx
const STROKE = 1.85;       // slightly lighter than source 2.0 for an elegant line

function recolor(svg, hex) {
  let s = svg.replace(/currentColor/g, hex);
  s = s.replace(/stroke-width="2"/g, `stroke-width="${STROKE}"`);
  // force explicit width/height on root svg
  s = s.replace(/<svg /, `<svg width="${SIZE}" height="${SIZE}" `)
       .replace(/width="24"/, '').replace(/height="24"/, '');
  return s;
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: SIZE, height: SIZE }, deviceScaleFactor: 2 });
let n = 0;
for (const [name, keys] of Object.entries(USES)) {
  const p = join(SRC, name + '.svg');
  if (!existsSync(p)) { console.log('MISS', name); continue; }
  const raw = readFileSync(p, 'utf8');
  for (const k of keys) {
    const svg = recolor(raw, C[k]);
    const html = `<!doctype html><html><body style="margin:0;padding:0;background:transparent">${svg}</body></html>`;
    await page.setContent(html, { waitUntil: 'networkidle' });
    const el = await page.$('svg');
    await el.screenshot({ path: join(OUT, `${name}__${k}.png`), omitBackground: true });
    n++;
  }
}
await browser.close();
console.log('RASTERIZED', n, 'icon pngs ->', OUT);

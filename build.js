#!/usr/bin/env node
// Edit data.json, then run:  node build.js   (add --watch to rebuild on every save)
// Reads data.json, checks it, and writes data.js, which index.html loads.
const fs = require('fs'), path = require('path');
process.chdir(__dirname);
function check(d) {
  const e = [];
  for (const k of ['book', 'extra', 'gal']) if (!d[k]) e.push('missing top-level key: ' + k);
  if (e.length) return e;
  for (const c of d.book) {
    for (const k of ['n', 'title', 'pages', 'sections']) if (c[k] === undefined) e.push(`chapter ${c.n}: missing "${k}"`);
    for (const s of c.sections || []) {
      if (!s.title || s.page === undefined) e.push(`chapter ${c.n}: a section needs "title" and "page"`);
      for (const p of s.paras || []) if (p.t === undefined && p.c === undefined) e.push(`chapter ${c.n} / ${s.title}: a paragraph needs "t" (text) or "c" (caption)`);
    }
  }
  for (const g of d.extra.glossary || []) if (!g.w || !g.d) e.push('glossary entry needs "w" and "d": ' + JSON.stringify(g));
  for (const p of d.extra.people || []) if (!Array.isArray(p) || p.length !== 3) e.push('person must be [name, place, contribution]: ' + JSON.stringify(p));
  for (const g of d.gal) if (!g.i.startsWith('data:') && !fs.existsSync(g.i)) e.push('image file not found: ' + g.i);
  return e;
}
function build() {
  let d;
  try { d = JSON.parse(fs.readFileSync('data.json', 'utf8')); }
  catch (err) { console.log('data.json is not valid JSON: ' + err.message); return; }
  const errs = check(d);
  if (errs.length) { console.log('Not built. Fix these first:'); errs.forEach(x => console.log('  - ' + x)); return; }
  const body = JSON.stringify(d).replace(/<\//g, '<\\/');
  fs.writeFileSync('data.js', '/* AUTO-GENERATED from data.json by build.js. Do not edit; edit data.json. */\nwindow.DURA_DATA=' + body + ';\n');
  const n = d.book.reduce((a, c) => a + c.sections.length, 0);
  console.log(`Built data.js: ${d.book.length} chapters, ${n} topics, ${d.extra.glossary.length} glossary words, ${d.extra.people.length} people, ${d.gal.length} photos`);
}
build();
if (process.argv.includes('--watch')) { console.log('Watching data.json (Ctrl+C to stop)...'); fs.watchFile('data.json', { interval: 800 }, build); }

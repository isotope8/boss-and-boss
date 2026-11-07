// Rebuilds art/README.md: the list of every character id.
// Run from the game folder:  node tools/art-list.js
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const P = eval('(' + html.slice(html.indexOf('const P={') + 8, html.indexOf('\n};', html.indexOf('const P={')) + 2) + ')');
global.registerPack = p => {
  for (const [id, c] of Object.entries(p.people || {})) P[id] = { ...c, pack: p.name };
};
for (const f of fs.readdirSync('packs')) if (!f.startsWith('_')) require('../packs/' + f);
const rows = Object.entries(P).map(([id, c]) =>
  `| \`${id}\` | ${c.n} | ${c.r} | ${c.pack || 'Base game'} | ${['svg', 'png'].some(x => fs.existsSync(`art/${id}.${x}`)) ? 'yes' : ''} |`);
fs.writeFileSync('art/README.md', `# Character art

Put a picture for a character in this folder, named after their **id**:

- \`art/<id>.svg\` (checked first), or
- \`art/<id>.png\`

That's all. Replace a file to change the art; delete it to go back to the emoji.
Portrait shape: **200 × 232** (width × height), the face in the upper half. Square images work too.

| id | Character | Role | Game / pack | Has art |
|---|---|---|---|---|
${rows.join('\n')}
`);
console.log(rows.length + ' characters written to art/README.md');

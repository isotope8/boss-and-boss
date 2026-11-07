# Boss & Boss: Developer Guide

Everything a developer needs to understand, change, test and ship the game. The whole game is ~1,500 lines of plain HTML/JS/CSS: no framework, no build step, no server.

---

## 1. File map
```
index.html              Engine + base content + UI (single file, read top to bottom)
lang/ms.js zh.js ta.js  Language editions (data only)
lang/*-packs.js         Pack card + character translations (registerLangPacks)
packs/*.js              Industry packs (data only); _template.js is not loaded
art/<id>.svg|png        Character portraits, found by file name
art-styles/<style>/     Alternative portrait sets (copy into art/ to use)
fonts/                  Bundled web fonts (Bricolage Grotesque, Noto Sans Tamil)
icons/, manifest.webmanifest   App icon and install metadata
sw.js                   Offline cache (service worker)
tools/art-list.js       Rebuilds art/README.md
tests/smoke.py          Automatic play-test
docs/                   GDD, modder notes, this guide
```

## 2. How `index.html` is organised
In order, top to bottom:

| Section (search for the comment) | What it does |
|---|---|
| `<head>` | Fonts, manifest, CSS, then the **registries** (`LANGS`, `PACKS`, `registerLang`, `registerPack`), then `<script src>` for every lang and pack file |
| `<body>` markup | Game screen, intro overlay, trainer overlay, end overlay, pause menu |
| `// ---------- data ----------` | `METERS`, `P` (base characters), `CARDS` (78 base cards), `BIAS`, `WIN`, `SHOCKS`, `ENDINGS` |
| `// ---------- expansion packs ----------` | Merges pack characters into `P`, tags pack cards, `ALL_CARDS()`, `ACTIVE()`, `findCard()` |
| `// ---------- state ----------` | `store` (localStorage wrapper), seeded RNG, `newGame()`, `eff()` (effects × ramp), `pickCard()` |
| `// ---------- character art ----------` | `portraitHTML()`, `artMiss()`: file-name art with emoji fallback |
| `// ---------- rendering ----------` | Meters, preview dots, card HTML, `nextCard()` |
| `// ---------- input ----------` | Drag/swipe, buttons, keys, **`choose()`**: the turn logic |
| `// ---------- end / debrief ----------` | `showEnd()`: scores, HR style, lessons, result code, WhatsApp link |
| `// ---------- industry picker & cast ----------` | Start-screen tiles and cast list |
| `// ---------- sound ----------` | WebAudio blips, mute, pause menu wiring |
| `// ---------- workshop results ----------` | Result codes, Trainer view, CSV |
| `// ---------- languages ----------` | `UI_EN`, `U()`, `applyLang()` |
| `// ---------- offline support ----------` | Registers `sw.js` (http/https only) |
| `// ---------- boot ----------` | Initial render |

## 3. Boot sequence
1. Registries defined in `<head>`.
2. Each `lang/*.js` calls `registerLang(code, name, data)`; each `packs/*.js` calls `registerPack(pack)`.
3. Main script runs: pack people merged into `P`, pack cards tagged with `card.pack`.
4. `applyLang(saved language)` snapshots English text once, then overlays the chosen language.
5. Intro overlay shows; **Open the office** → `newGame()`.

## 4. Game state
```js
S = { cash, morale, comp, rep, week }    // meters 0–100, week from 0
queue      // follow-ups: [{id, at: week}]
log        // every decision: {week, card, side, opt, d (effects), risky, people, profit, bias}
usedOnce   // Set of card ids already shown (for once:1)
lastIds    // last 12 card ids (no repeats)
PACK, LANG, code   // chosen industry, language, workshop code
```

### Turn logic: `choose(side)`
1. Apply `eff(option)` (effects × `1 + min(1, week/156) × 0.6`), clamp 0–100.
2. Log the decision; queue `next` follow-up if any.
3. `week++`; +1 cash; every 13 weeks quarterly result `round((morale−45)/4)`.
4. Warnings at 20/80; every 26 weeks (week % 26 == 13) a random shock.
5. After 330 ms: ending check (any meter 0 or 100 → that ending; week ≥ 156 → `win`), else `nextCard()`.

### Card choice: `pickCard()`
Anniversary (week 52, 104) → due follow-up → crisis card if `cond` true (50%) → pack card (50% when a pack is active) → random base card. Excludes `req` cards, used `once` cards, the last 12 cards, and ids ending in `intro`.

### Randomness
`rng` is `Math.random`, or a seeded generator when a workshop code is set (same code → same draws). Follow-ups still depend on each player's choices.

## 5. Saved data (browser localStorage, prefix `bb_`)
| Key | Contents |
|---|---|
| `bb_lang` | Language code |
| `bb_pack` | Chosen industry id |
| `bb_best` | Longest run in weeks |
| `bb_endings` | Endings found (array) |
| `bb_muted` | Sound off |
| `bb_pname` | Player's name for result codes |
| `bb_results` | Trainer view: pasted results `{code: result}` |

Nothing is sent over the network. Clearing site data resets everything.

## 6. Result code format (v1)
```
BB1-<base64url( UTF-8 JSON )>
```
JSON fields:
| Field | Meaning |
|---|---|
| `c` | Workshop code |
| `p` | Industry id (`base` or pack id) |
| `e` | Ending id (`cash0`, `win`, …) |
| `w` | Weeks survived |
| `pp` | People-first % |
| `lw` | Followed-the-law % |
| `b` | Bias tags taken |
| `r` | Card ids where the risky option was taken |
| `ch` | `{cardId: 'L' or 'R'}` for every card played |
| `n` | Player name (optional) |
| `t` | Timestamp |

The Trainer view finds codes with the pattern `BB1-[A-Za-z0-9_-]+`, so surrounding WhatsApp text is ignored. Change the prefix to `BB2-` if the format changes.

## 7. Languages: `applyLang(code)`
On first call, English text of every card, character, ending, bias label and shock is snapshotted. Each switch restores English and then overlays `LANGS[code]` wherever a translation exists: base cards from `cards`, pack cards from `packs[packId]`, interface from `ui` (via `U(key)`, falling back to `UI_EN`). `ui.time` can be a function for languages with different word order (Chinese).

## 8. Offline (`sw.js`)
- On install, caches the `FILES` list. On fetch: cached copy first, else download and cache (same-origin only). This is how art files become available offline.
- **Releasing an update:** change `VERSION`. Old caches are deleted on activation.
- Only active over http/https; opening `index.html` directly skips it (no need, the files are local).

## 9. Testing
```
pip install playwright && python -m playwright install chromium
python tests/smoke.py
```
Checks content integrity, plays every industry and language, workshop-code repeatability, and result-code round trip. Exit code 1 on any problem.

Manual checks before a release: phone size (≈390 × 800), one full Trainer view flow (finish → copy code → paste → CSV), offline reload when served over http.

## 10. Release checklist
1. `python tests/smoke.py` passes.
2. `node tools/art-list.js` if characters or art changed.
3. New files added to `FILES` in `sw.js`; `VERSION` bumped.
4. Commit and push to `main`; GitHub Pages serves the folder as-is.

## 11. Known limits and next steps
- All cards are in memory (~160): fine up to a few thousand.
- Trainer view is per device; there's no shared backend by design.
- Pack cards are English-only in other languages until translated (`packs` key in lang files).
- No accessibility audit yet (screen reader labels on meters, colour contrast of warnings).

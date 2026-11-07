# Boss & Boss: Modder Notes

How to add industry packs, characters, art and translations. No programming experience needed, just careful copy-and-edit. Everything is a plain text file you can open in Notepad, TextEdit or VS Code.

---

## 1. What you can change, and where

| You want to… | Edit or add | Code changes? |
|---|---|---|
| Add a new industry | `packs/<id>.js` + 1 line in `index.html` + 1 line in `sw.js` | No |
| Change a character's picture | `art/<character id>.svg` or `.png` | No |
| Switch the whole art style | Copy a folder from `art-styles/` into `art/` | No |
| Translate | `lang/<code>.js` | No |
| Edit a base-game card | `index.html`, inside `const CARDS=[...]` | Only that text |

## 2. Make an industry pack (step by step)

1. Copy `packs/_template.js` to `packs/myindustry.js`.
2. Fill it in (format below).
3. In `index.html`, find the `<!-- EXPANSION PACKS -->` comment and add:
   ```html
   <script src="packs/myindustry.js"></script>
   ```
4. In `sw.js`, add `'packs/myindustry.js',` to the `FILES` list and change `VERSION` (e.g. `bb-v9` → `bb-v10`) so installed copies update.
5. Open `index.html`. Your pack appears under **Choose your industry**. Play it.

### Pack file format
```js
registerPack({
 id:'myindustry',              // short, lowercase, unique
 icon:'🏷️',                    // one emoji for the tile
 name:'Your Industry, Town',
 tagline:'One funny line about this world',
 i18n:{ ms:{name:'',tagline:''}, zh:{name:'',tagline:''}, ta:{name:'',tagline:''} },
 people:{
   my_boss:{ n:'Name', r:'Role', e:'🙂', c:'#e6e6e6', bio:'One memorable line.' },
 },
 introCard:{ id:'my_intro', p:'my_boss', once:1, t:'Welcome line.',
   L:{ l:'Left choice', e:[0,0,0,0] }, R:{ l:'Right choice', e:[0,0,0,0] } },
 cards:[ /* 8 cards recommended, see §3 */ ]
});
```

| Field | Rules |
|---|---|
| `id` | Lowercase letters only. Also used as the prefix idea for card and character ids |
| Character id | Pack prefix + name, e.g. `mk_ravi`. **Must be unique across the whole game** |
| `e` (emoji) | Shown when there's no art file for this character |
| `c` (colour) | Light pastel hex for the emoji circle |
| `bio` | ≤ 12 words. Personality, not job description |
| Intro card id | Must end with `intro` (e.g. `my_intro`) so it isn't counted in the debrief |

## 3. Writing cards

```js
{ id:'my_overtime', p:'my_boss', once:1,
  t:'The situation, in the character\'s own voice.',
  L:{ l:'Risky shortcut', e:[10,-10,-15,0], law:'What the law actually says.' },
  R:{ l:'The fair option', e:[-10,10,10,0] } }
```

| Field | Meaning |
|---|---|
| `id` | Unique; start with your pack prefix |
| `p` | Character id who says it |
| `t` | The situation. ≤ 25 words. In the speaker's voice |
| `L` / `R` | Left / right option. `l` = label (≤ 6 words) |
| `e` | Effects `[cash, morale, compliance, reputation]` |
| `law` | Put on the **risky** option only. Shown in the debrief if the player picks it, and counts against "Followed the law" |
| `once:1` | Show at most once per run (use for big story moments) |
| `bias:'age'` | Flags a hiring-bias choice. One of `age`, `origin`, `parent`, `language`, `disability`, `gender` |
| `next:['card_id', 4]` | On an option: queue a follow-up card 4 weeks later |
| `req:1` | On the follow-up card: only appears via `next`, never randomly |
| `cond:s=>s.cash<25` | Only eligible when the condition holds (`s.cash`, `s.morale`, `s.comp`, `s.rep`, `s.week`) |

### Balance rules of thumb
- Effects between **−25 and +25**. Use ±5 for small, ±10 normal, ±15–20 big, ±25 only for scandals.
- **Every option must cost something.** If one side is all positive, it's not a decision.
- Usually the two options pull in **opposite directions** on at least two meters.
- Keep a pack's average cash effect near zero; the base game already drains cash slightly.
- Story arcs: 2–3 cards max, 3–6 weeks apart.

### Writing and tone checklist
- [ ] Sounds like a real person at a Malaysian workplace said it
- [ ] Humour comes from the situation or the personality, **not** from race, religion, gender, accent or disability
- [ ] Manglish is light and natural ("can or not", "lah", "boss"), not overdone
- [ ] Both options are things a reasonable boss might actually choose
- [ ] Law tip is accurate, simplified, and names the Act where possible. Check against the current Act or a practitioner. Write "as of <year>" in your notes
- [ ] No real company or real person's name

## 4. Characters and art

Art is found **by file name only**:
```
art/<character id>.svg   (checked first)
art/<character id>.png
```
- No file → the character's emoji is shown. Nothing breaks.
- Portrait shape about **200 × 232** (width × height), face in the upper half. Square works.
- PNG: keep under ~150 KB each (use 400 × 464 px for sharp phone screens).
- `art/README.md` lists every character id. Regenerate it when you add characters (see `docs/DEVELOPER.md`).
- Whole style swap: copy all files from e.g. `art-styles/retro/` into `art/`.
- After replacing an existing picture on a live site, change `VERSION` in `sw.js` so installed phones refresh.

### Art brief for illustrators
> One portrait per character id in `art/README.md`. 200 × 232 ratio, head-and-shoulders, character facing forward or ¾, plain or style-consistent background. Show their role through clothing or a prop (Kak Ros's broom, Ravi's chef hat). Diverse and respectful depiction of Malaysian dress: tudung, songkok, baju kurung, kebaya, pottu, turban, uniforms. Deliver as PNG (400 × 464) or SVG, named exactly by id.

## 5. Translations

Each language is one file in `lang/`: `ms.js`, `zh.js`, `ta.js`. Structure:
```js
registerLang('ms','Bahasa Melayu',{
 meters:['Tunai','Semangat','Pematuhan','Reputasi'],
 people:{ aina:['Aina','Eksekutif admin','Bio…'] },         // [name, role, bio]
 cards:{ ot:['Text','Left label','Right label','Law tip'] },  // base-game cards
 packs:{ mamak:{ mk_recipe:['Text','Left','Right','Law'] } },  // pack cards (optional)
 endings:{ cash0:['Title','Description'] },
 bias:{ age:'…' }, shocks:['…'], notes:{ 'English note':'Translation' },
 ui:{ /* every interface label; copy the keys from UI_EN in index.html */ }
});
```
- Anything missing falls back to English automatically, so you can translate bit by bit.
- Pack **names and taglines** go in the pack file's `i18n`. Pack **cards** (including the intro card) and pack **characters** go in `lang/<code>-packs.js`, which calls `registerLangPacks('ms',{packs:{…},people:{…}})` with the same `[text, left, right, law]` and `[name, role, bio]` shapes. When you add a pack, add its translations there.
- New language: create `lang/xx.js`, add `<script src="lang/xx.js">` in `index.html`, add `'xx'` to `LANG_ORDER` in `index.html`, and add the file to `sw.js`.
- Keep `<b>…</b>` tags in intro texts. Keep emoji.

## 6. Test before you share
1. Open `index.html`, pick your pack, play 3 runs. Every pack card should appear within a couple of runs.
2. Switch each language and look at your cards (English fallback is fine).
3. Lose on purpose: check the debrief shows your law tips and bias flags.
4. Optional automatic check: see `tests/` in `docs/DEVELOPER.md`.

## 7. Sharing a pack
Send the single `packs/<id>.js` file plus any `art/<id>.*` files. The receiver follows §2 steps 3–4.

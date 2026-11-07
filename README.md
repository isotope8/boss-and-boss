# Boss & Boss

A swipe game about running a Malaysian company when you're also the HR department.
Keep Cash, Morale, Compliance and Reputation in balance for 3 years.

Plain HTML and JavaScript. No server, no build step, no accounts, no tracking.

## Play it
| Device | How |
|---|---|
| Any computer, no internet | Double-click `index.html` |
| Web | Host this folder on any static host (e.g. GitHub Pages) and open the link |
| iPhone / iPad | Open the link in Safari → Share → **Add to Home Screen** |
| Android | Open the link in Chrome → **Install app** |
| Windows / Mac | Open the link in Chrome or Edge → **Install** icon in the address bar (Mac Safari: File → **Add to Dock**) |

Once installed from the link, it works offline.

## Workshop use
1. Give everyone the same workshop code and industry on the start screen.
2. At the end, each player taps **Copy result code** or **Send by WhatsApp**.
3. On your device, open **Trainer view**, paste the codes (whole WhatsApp messages are fine), and see the room's results. **Download CSV** for your records.

Result codes are the result as JSON in base64. Paste one into any base64 decoder to see exactly what it contains: name (optional), workshop code, industry, ending, weeks, scores, and the left/right choice on each card. Nothing is sent anywhere unless the player sends it.

## Files
| Path | What it is |
|---|---|
| `index.html` | The whole game engine and base 78 cards |
| `lang/*.js` | Bahasa Melayu, Chinese, Tamil text |
| `packs/*.js` | The 10 industry expansion packs |
| `sw.js` | Offline cache (list of files + 15 lines of code) |
| `manifest.webmanifest`, `icons/` | App name and icons for installing |
| `fonts/` | Fonts, bundled so nothing loads from the internet |
| `art/` | Character pictures, one file per character, named by id (see `art/README.md`) |
| `art-styles/` | Other art styles you can copy into `art/` |
| `docs/` | Design document, modder notes, developer guide |
| `tools/`, `tests/` | Art list builder, automatic play-test |

## Add an expansion pack
1. Copy `packs/_template.js` to `packs/your-pack.js` and fill it in.
2. Add `<script src="packs/your-pack.js"></script>` next to the other packs in `index.html`.
3. Add `'packs/your-pack.js',` to the list in `sw.js` and change `VERSION` so installed copies update.

## Documentation
- `docs/GDD.md`: game design document
- `docs/MODDING.md`: make packs, art and translations
- `docs/DEVELOPER.md`: how the code works, testing, releases
- `docs/art-styles.html`: art style exploration (open in a browser)

## Change the art
Drop `art/<id>.svg` or `art/<id>.png` into the `art/` folder. The file name is the only link: no code changes. `art/README.md` lists every character id. A character with no file shows its emoji.

## Notes
Employment rules are simplified for gameplay and are not legal advice. Chinese and Tamil text needs a native-speaker review.

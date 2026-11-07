"""
Smoke test for Boss & Boss. Plays the game automatically and reports problems.

Setup once:   pip install playwright && python -m playwright install chromium
Run:          python tests/smoke.py            (from the game folder)

Checks:
  1. Every pack and language file loads; every card's speaker exists; card ids are unique.
  2. A short random game in every industry, and in every language, runs without errors
     and never shows "undefined" on a card.
  3. The same workshop code gives the same sequence of cards.
  4. A result code survives encode -> decode.
"""
import pathlib, random, sys
from playwright.sync_api import sync_playwright

URL = pathlib.Path(__file__).resolve().parent.parent.joinpath('index.html').as_uri()
problems = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 800})
    page.on('pageerror', lambda e: problems.append('JavaScript error: ' + str(e)))
    page.goto(URL)
    page.wait_for_timeout(400)

    # 1. Content integrity
    info = page.evaluate("""() => ({
        packs: PACKS.map(p => p.id),
        langs: Object.keys(LANGS),
        badSpeaker: ALL_CARDS().filter(c => !P[c.p]).map(c => c.id),
        dupIds: ALL_CARDS().map(c => c.id).filter((v, i, a) => a.indexOf(v) !== i),
    })""")
    print('Packs:', ', '.join(info['packs']))
    print('Languages: en,', ', '.join(info['langs']))
    if info['badSpeaker']: problems.append('Cards with unknown speaker: ' + ', '.join(info['badSpeaker']))
    if info['dupIds']: problems.append('Duplicate card ids: ' + ', '.join(info['dupIds']))

    # 2. Play every industry (English) and every language (base game)
    runs = [('en', pk) for pk in ['base'] + info['packs']] + [(l, 'base') for l in info['langs']]
    for lang, pack in runs:
        page.evaluate(f"() => {{ applyLang('{lang}'); PACK='{pack}'; $('intro').classList.remove('on'); $('end').classList.remove('on'); $('code').value=''; newGame() }}")
        bad = page.evaluate("""async () => { const bad = [];
            for (let i = 0; i < 30; i++) {
              if ($('end').classList.contains('on')) break;
              const t = document.querySelector('.card:not(.back)').innerText;
              if (/undefined|null/.test(t)) bad.push(cur.id);
              choose(Math.random() < .5 ? 'L' : 'R');
              await new Promise(r => setTimeout(r, 345));
            } return bad }""")
        print(f'  played {lang}/{pack}: ok' if not bad else f'  played {lang}/{pack}: PROBLEM {bad}')
        if bad: problems.append(f'"undefined" shown in {lang}/{pack}: {bad}')

    # 3. Workshop code gives a repeatable sequence
    def sequence():
        page.evaluate("() => { applyLang('en'); PACK='base'; $('end').classList.remove('on'); $('code').value='TEST1'; newGame() }")
        return page.evaluate("""async () => { const s = [];
            for (let i = 0; i < 6; i++) { s.push(cur.id); if ($('end').classList.contains('on')) break; choose('R'); await new Promise(r => setTimeout(r, 345)) }
            return s }""")
    a, b = sequence(), sequence()
    print('Workshop code repeatable:', a == b)
    if a != b: problems.append('Same workshop code gave different sequences')

    # 4. Result code round trip
    ok = page.evaluate("""() => { const r = {c:'X', p:'bank', e:'win', w:156, pp:50, lw:90, b:['age'], r:[], ch:{ot:'R'}, n:'Siti Nurhaliza 测试 தமிழ்'};
                            return JSON.stringify(decodeResult(encodeResult(r))) === JSON.stringify(r) }""")
    print('Result code round trip:', ok)
    if not ok: problems.append('Result code encode/decode mismatch')
    browser.close()

print()
if problems:
    print('PROBLEMS FOUND:'); [print(' -', x) for x in problems]; sys.exit(1)
print('All checks passed.')

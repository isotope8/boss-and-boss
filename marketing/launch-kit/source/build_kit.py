import html, json, os
from kitcopy import COPY
FILES = sorted(os.listdir('ready'))
esc = html.escape

PLAN = [
 ("Before Day 1", "Everywhere", "Put the game online and get the link. Fill in <b>Your game link</b> and <b>Your contact</b> at the top of this page. Add the link-in-bio line to TikTok, Instagram and Facebook.", "—"),
 ("Before Day 1", "Profiles", "Set the profile picture (14), LinkedIn banner (15), Facebook cover (16) and email signature (17). Print the A3 poster (09) for your office or event and the A4 workshop poster (10) for client visits.", "13–17, 09, 10"),
 ("Day 1", "WhatsApp Status, TikTok, Reels, Shorts", "Post the video. Reply to every comment in the first hour.", "01 + video captions"),
 ("Day 1", "WhatsApp (friends, family groups)", "Send the friends message with the video. Ask: “Which ending did you get?”", "01 + WhatsApp message"),
 ("Day 2", "Instagram, Facebook", "Post the 10-slide carousel.", "03 + carousel caption"),
 ("Day 3", "LinkedIn", "Post the long LinkedIn text with the video or the PDF carousel.", "01 or 04 + LinkedIn post"),
 ("Day 4", "Facebook (SME groups you belong to)", "Post the SME-owner text with the square image. Follow each group's rules.", "05 + Facebook post"),
 ("Day 5", "WhatsApp (10–20 HR contacts, one by one)", "Send the HR-contact message personally. Change [Name]. Don't bulk-send.", "07 + HR message"),
 ("Day 6", "Email (5–10 L&D or HR managers)", "Send the email with the one-pager PDF attached.", "11 + email"),
 ("Day 7", "All", "Re-share the best player comments or ending screenshots (ask permission first).", "—"),
 ("Day 8", "LinkedIn", "Post the short “What would you do?” card question. Answer every comment.", "05 + short LinkedIn post"),
 ("Day 10", "TikTok, Reels", "Re-post the video with a new first line, e.g. “POV: you're the boss of a mamak chain”.", "01"),
 ("Day 12", "WhatsApp", "Follow up with HR contacts who replied. Offer a free pilot session to 2–3 companies.", "HR message"),
 ("Day 14", "LinkedIn, Facebook", "Share what you learned: e.g. “Most players went bankrupt in under 10 weeks.” Invite workshop bookings.", "07"),
]

def caption_blocks():
    out = []
    for sec, items in COPY:
        out.append(f'<h3>{esc(sec)}</h3>')
        for i, (title, lang, text) in enumerate(items):
            out.append(f'<div class="cap" data-lang="{lang}"><div class="ch"><b>{esc(title)}</b><span class="lg">{lang}</span><button class="cp">Copy</button></div><pre data-raw="{esc(text)}"></pre></div>')
    return '\n'.join(out)

def file_cards():
    out = []
    for f in FILES:
        path = 'ready/' + f
        name = f.rsplit('.', 1)[0]
        if f.endswith('.mp4'):
            prev = f'<video src="{esc(path)}" controls muted playsinline preload="metadata"></video>'
        elif f.endswith('.pdf'):
            prev = '<div class="pdf">PDF<br>' + ('10 pages' if 'Carousel' in f else 'for print') + '</div>'
        else:
            prev = f'<img src="{esc(path)}" loading="lazy" alt="">'
        out.append(f'<a class="file" href="{esc(path)}" target="_blank">{prev}<span>{esc(name)}</span></a>')
    return '\n'.join(out)

page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boss &amp; Boss launch kit</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&display=swap">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Bricolage Grotesque',system-ui,sans-serif;background:#f6efe0;color:#1d1a16;line-height:1.5}}
header{{background:#0f3d3e;color:#fbf4e6;padding:32px 20px 26px}}
.w{{max-width:980px;margin:0 auto;padding:0 20px}}
header .w{{padding:0}}
h1{{font-size:38px;font-weight:800;line-height:1.05}} h1 em{{font-style:normal;color:#e8a33d}}
header p{{opacity:.85;margin-top:6px}}
h2{{font-size:26px;font-weight:800;margin:38px 0 10px}}
h3{{font-size:18px;font-weight:800;margin:26px 0 8px;color:#0f3d3e}}
.fill{{background:#fff;border:2px solid #e2d6bd;border-radius:14px;padding:16px;margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.fill label{{font-size:13px;font-weight:700;display:block;margin-bottom:4px}}
.fill input{{width:100%;font:inherit;padding:10px 12px;border-radius:10px;border:1.5px solid #cdbf9f}}
@media(max-width:640px){{.fill{{grid-template-columns:1fr}}}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px}}
.box{{background:#fff;border-radius:14px;padding:14px 16px;border:2px solid #e2d6bd}}
.box b{{display:block;margin-bottom:2px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;font-size:15px}}
td,th{{text-align:left;padding:10px 12px;border-bottom:1px solid #eadfc8;vertical-align:top}}
th{{background:#0f3d3e;color:#fbf4e6;font-size:14px}}
.files{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
.file{{background:#fff;border:2px solid #e2d6bd;border-radius:12px;overflow:hidden;text-decoration:none;color:inherit;font-size:12.5px;display:flex;flex-direction:column}}
.file img,.file video{{width:100%;aspect-ratio:4/5;object-fit:cover;background:#0f3d3e;display:block}}
.file span{{padding:8px 9px;line-height:1.3}}
.pdf{{aspect-ratio:4/5;background:#0f3d3e;color:#e8a33d;font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;text-align:center}}
.filter{{display:flex;gap:8px;margin:6px 0 4px}}
.filter button,.cp{{font:inherit;font-weight:700;border:2px solid #0f3d3e;background:#fff;color:#0f3d3e;border-radius:20px;padding:5px 14px;cursor:pointer}}
.filter button.on,.cp{{background:#0f3d3e;color:#fbf4e6}}
.cp.ok{{background:#2e8b57;border-color:#2e8b57}}
.cap{{background:#fff;border:2px solid #e2d6bd;border-radius:14px;margin-bottom:10px;overflow:hidden}}
.ch{{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid #eadfc8}}
.ch b{{flex:1;font-size:15px}}
.lg{{font-size:12px;font-weight:800;background:#f2c46b;border-radius:8px;padding:2px 8px}}
pre{{white-space:pre-wrap;font-family:inherit;font-size:15px;padding:12px 14px}}
pre mark{{background:#ffe08a;padding:0 3px;border-radius:4px}}
ul{{padding-left:22px}} li{{margin:4px 0}}
footer{{text-align:center;font-size:13px;opacity:.6;padding:40px 20px}}
</style></head><body>
<header><div class="w"><h1>Boss <em>&amp;</em> Boss: launch kit</h1>
<p>Strategy, ready-to-upload files, and every caption ready to copy. Fill in the two boxes below once; every caption updates.</p></div></header>
<div class="w">
<div class="fill">
 <div><label for="link">Your game link</label><input id="link" placeholder="e.g. https://isotope8.github.io/boss-and-boss/"></div>
 <div><label for="contact">Your contact (WhatsApp number or email)</label><input id="contact" placeholder="e.g. +60 12-345 6789"></div>
</div>

<h2>1. Strategy in one minute</h2>
<div class="cards">
 <div class="box"><b>🎯 Goal</b>Players spread the game for free. The real win is <b>HR and L&amp;D managers</b> booking workshops.</div>
 <div class="box"><b>👥 Players</b>Malaysian working adults, 22–45. They share funny, relatable things on WhatsApp and TikTok.</div>
 <div class="box"><b>💼 Buyers</b>HR managers, L&amp;D, SME owners. Reach them personally on WhatsApp, LinkedIn and email.</div>
 <div class="box"><b>📣 Where</b>1. WhatsApp (status, groups, one-to-one) · 2. LinkedIn (buyers) · 3. TikTok / Reels (reach) · 4. Facebook (SME owners 35+)</div>
 <div class="box"><b>🪝 The hook</b>“Which ending did you get?” Invite people to compare endings and tag “the Kak Ros / Uncle Lim in your office”.</div>
 <div class="box"><b>⏰ When</b>Post 12–1pm or 8–10pm Malaysia time. Reply to every comment in the first hour.</div>
</div>
<h3>Golden rules</h3>
<ul>
 <li>Send buyer messages <b>one by one</b>, with their name. No bulk blasts.</li>
 <li>Offer <b>2–3 free pilot sessions</b> first, then use their feedback as testimonials (with permission).</li>
 <li>Say “simplified, not legal advice”. Don't claim HRD Corp claimability until you've confirmed it.</li>
 <li>Use a link you can count clicks on (e.g. a short link), because the game itself tracks nothing.</li>
 <li>Track: link clicks, comments, DMs, and the number of workshop enquiries. That last one is what matters.</li>
</ul>

<h2>2. 14-day posting plan</h2>
<table><tr><th>When</th><th>Where</th><th>What to do</th><th>File + text</th></tr>
{''.join(f'<tr><td><b>{d}</b></td><td>{w}</td><td>{t}</td><td>{f}</td></tr>' for d,w,t,f in PLAN)}
</table>

<h2>3. Files ready to upload</h2>
<div class="cards" style="margin-bottom:12px">
 <div class="box"><b>🖨️ Printing</b>Print the PDFs at <b>100% / actual size</b> on matte paper: 09 at A3, 10 and 11 at A4. The blank “Book a session” and “Contact” lines are for writing or a sticker with your number.</div>
 <div class="box"><b>🔳 QR code</b>Posters and file 18 point to <b>isotope8.github.io/boss-and-boss</b> (the planned GitHub Pages link). If your link ends up different, ask for the QR and posters to be regenerated.</div>
 <div class="box"><b>🎨 Brand</b>File 12 has the colours, fonts and voice rules. Use the transparent logos (13) on your own slides and documents.</div>
</div>
<p style="margin-bottom:10px">In the <b>ready</b> folder. The number matches the plan; the name says where it goes. Tap a file to open it full size.</p>
<div class="files">{file_cards()}</div>

<h2>4. Captions and messages</h2>
<div class="filter"><button data-f="all" class="on">All</button><button data-f="EN">English</button><button data-f="BM">BM</button></div>
<p style="font-size:14px;opacity:.75">Yellow words are filled in from the boxes at the top, or need your edit (like [Name]).</p>
{caption_blocks()}
</div>
<footer>Boss &amp; Boss launch kit · edit the text in copy.py and rebuild, or just edit after pasting.</footer>
<script>
const get=k=>{{try{{return localStorage.getItem('kit_'+k)||''}}catch(e){{return ''}}}};
const set=(k,v)=>{{try{{localStorage.setItem('kit_'+k,v)}}catch(e){{}}}};
const L=document.getElementById('link'),C=document.getElementById('contact');
L.value=get('link')||'https://isotope8.github.io/boss-and-boss/';C.value=get('contact');
const fill=t=>t.replace(/\\[LINK\\]/g,L.value.trim()||'[LINK]').replace(/\\[CONTACT\\]/g,C.value.trim()||'[CONTACT]');
const escH=s=>s.replace(/[&<>]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[c]));
function render(){{document.querySelectorAll('pre').forEach(p=>{{const t=fill(p.dataset.raw);
  p.innerHTML=escH(t).replace(/\\[(LINK|CONTACT|Name|Nama|Your name|Nama anda)\\]/g,'<mark>[$1]</mark>').replace(/\\[(.+?)\\]/g,m=>m.startsWith('[')&&!m.includes('<')?'<mark>'+m+'</mark>':m)
   .replace(new RegExp(escH(L.value.trim()||'§§').replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&'),'g'),m=>'<mark>'+m+'</mark>')}})}}
L.oninput=()=>{{set('link',L.value);render()}};C.oninput=()=>{{set('contact',C.value);render()}};render();
document.querySelectorAll('.cp').forEach(b=>b.onclick=()=>{{const t=fill(b.closest('.cap').querySelector('pre').dataset.raw);
  const done=()=>{{b.textContent='Copied ✓';b.classList.add('ok');setTimeout(()=>{{b.textContent='Copy';b.classList.remove('ok')}},1500)}};
  const fallback=()=>{{const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{{document.execCommand('copy');done()}}catch(e){{}}ta.remove()}};
  try{{navigator.clipboard.writeText(t).then(done,fallback)}}catch(e){{fallback()}}}});
document.querySelectorAll('.filter button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.filter button').forEach(x=>x.classList.toggle('on',x===b));
  document.querySelectorAll('.cap').forEach(c=>c.style.display=b.dataset.f==='all'||c.dataset.lang===b.dataset.f?'':'none')}});
</script></body></html>'''
open('index.html', 'w').write(page)

# Plain-text copy of every caption, for anyone who prefers a document
md = ['# Boss & Boss captions\n', 'Replace [LINK] with your game link and [CONTACT] with your WhatsApp or email.\n']
for sec, items in COPY:
    md.append(f'\n## {sec}\n')
    for title, lang, text in items:
        md.append(f'\n### {title} ({lang})\n\n```\n{text}\n```\n')
open('CAPTIONS.md', 'w').write(''.join(md))
print('built', len(FILES), 'files listed')

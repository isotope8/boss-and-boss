"""
Draws cartoon portraits for the cast from a short description of each character.
Run from the game folder:  python3 tools/draw-cast.py          (only draws characters without art)
                           python3 tools/draw-cast.py --all    (redraws every character listed below)
Output: art/<id>.svg (200 x 232), newspaper-cartoon style matching art/ros.svg.
Hand-drawn files (ros, uncle, aina, sys) are never overwritten.
"""
import os, sys

HAND_DRAWN = {'ros', 'uncle', 'aina', 'sys'}
SKIN = {'light': '#f3cfa8', 'fair': '#eec29c', 'tan': '#e0aa80', 'medium': '#d39b70', 'brown': '#b97d55', 'deep': '#8f5a3a'}
INK = '#2a211b'

HEAD = '''<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter>
<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" seed="7"/><feColorMatrix values="0 0 0 0 0.45 0 0 0 0 0.36 0 0 0 0 0.25 0 0 0 0.10 0"/></filter>
<style>.fill{stroke:#2a211b;stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round}.line{fill:none;stroke:#2a211b;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}.thin{fill:none;stroke:#2a211b;stroke-width:1.8;stroke-linecap:round}.blush{fill:#e98a7a;opacity:.45;stroke:none}.dark{fill:#2a211b}</style></defs>'''

def F(d, color, cls='fill'):
    return f'<path class="{cls}" fill="{color}" d="{d}"/>'

def L(d, cls='line'):
    return f'<path class="{cls}" d="{d}"/>'

# ---------------- body / outfits ----------------
SHOULDERS = 'M24 232 Q30 164 100 156 Q170 164 176 232Z'

def outfit(o, c, c2):
    s = ''
    if o == 'shirt_tie':
        s += F(SHOULDERS, '#f5f1e8') + F('M94 160 L106 160 L111 206 L100 220 L89 206Z', c) + L('M78 158 L94 174 M122 158 L106 174')
    elif o == 'blazer':
        s += F(SHOULDERS, c) + F('M80 158 L100 196 L120 158 Q100 166 80 158Z', '#f5f1e8')
        if c2: s += F('M96 166 L104 166 L107 196 L100 204 L93 196Z', c2)
        s += L('M80 158 L92 204 M120 158 L108 204')
    elif o == 'polo':
        s += F(SHOULDERS, c) + F('M80 158 L100 180 L120 158 Q100 166 80 158Z', c2 or c) + L('M100 180 L100 200')
    elif o == 'tshirt':
        s += F(SHOULDERS, c) + L('M82 160 Q100 172 118 160')
    elif o == 'scrubs':
        s += F(SHOULDERS, c) + F('M82 160 L100 188 L118 160Z', '#f0d5b5' if not c2 else c2) + L('M48 200 Q60 190 66 216', 'thin')
    elif o == 'chef':
        s += F(SHOULDERS, '#fbfaf5') + L('M100 160 L100 232') + ''.join(f'<circle class="dark" cx="{x}" cy="{y}" r="2.6"/>' for x in (90, 110) for y in (184, 204, 222)) + F('M82 158 Q100 170 118 158 L116 168 Q100 176 84 168Z', c)
    elif o == 'hiviz':
        s += F(SHOULDERS, c2 or '#4a6fa5') + F('M52 180 L74 160 L86 232 L60 232Z M148 180 L126 160 L114 232 L140 232Z', '#f28c28') + L('M58 206 L80 202 M142 206 L120 202', 'thin')
        s += '<path d="M58 206 L80 202 M142 206 L120 202" stroke="#e8e8e8" stroke-width="5" fill="none"/>'
    elif o == 'coverall':
        s += F(SHOULDERS, c) + F('M80 158 L100 176 L120 158 Q100 166 80 158Z', c2 or c) + '<path d="M40 200 L160 200" stroke="#e8e8e8" stroke-width="6" fill="none"/>' + L('M100 176 L100 232')
    elif o == 'baju':  # baju kurung / baju Melayu (simple)
        s += F(SHOULDERS, c) + L('M88 160 Q100 168 112 160')
        if c2: s += F('M30 210 Q100 196 170 210 L172 232 L28 232Z', c2)  # samping
    elif o == 'baju_melayu':
        s += F(SHOULDERS, c) + F('M86 158 L100 168 L114 158 Q100 162 86 158Z', c) + L('M100 168 L100 210') + ''.join(f'<circle class="dark" cx="100" cy="{y}" r="2.2"/>' for y in (178, 190, 202))
        if c2: s += F('M30 212 Q100 198 170 212 L172 232 L28 232Z', c2)
    elif o == 'apron':
        s += F(SHOULDERS, c) + F('M70 170 L130 170 L136 232 L64 232Z', c2 or '#f5f1e8') + L('M78 170 Q86 160 88 158 M122 170 Q114 160 112 158', 'thin')
    elif o == 'jacket':
        s += F(SHOULDERS, c) + F('M84 158 L100 172 L116 158 Q100 164 84 158Z', c2 or '#f5f1e8') + L('M100 172 L100 232') + L('M70 196 L84 196 M116 196 L130 196', 'thin')
    elif o == 'kebaya':
        s += F(SHOULDERS, c) + F('M86 158 L100 190 L114 158Z', c2 or '#f5e6c8') + ''.join(f'<circle cx="100" cy="{y}" r="3" fill="#e8b84a" stroke="#2a211b" stroke-width="1.2"/>' for y in (196, 210))
    return s

# ---------------- hair & headwear ----------------
def hair_back(h, c):
    if h == 'long':
        return F('M54 104 Q48 50 100 46 Q152 50 146 104 L152 176 Q100 188 48 176Z', c)
    if h == 'bob':
        return F('M56 104 Q50 50 100 48 Q150 50 144 104 L148 150 Q100 160 52 150Z', c)
    if h == 'ponytail':
        return F('M138 80 Q170 96 160 150 Q150 120 136 104Z', c)
    if h == 'bun':
        return f'<circle class="fill" fill="{c}" cx="100" cy="44" r="16"/>'
    return ''

def hair_front(h, c):
    if h in ('short', 'side_part', 'ponytail', 'bun', 'gray'):
        part = 'M60 98 Q54 42 100 40 Q148 40 142 96 Q132 70 112 64 Q96 74 70 72 Q62 80 60 98Z'
        if h == 'side_part':
            part = 'M60 98 Q54 42 100 40 Q148 40 142 96 Q138 74 126 66 Q106 62 84 72 Q66 74 60 98Z'
        if h in ('ponytail', 'bun'):
            part = 'M62 96 Q56 46 100 44 Q146 46 140 96 Q130 68 100 64 Q74 66 62 96Z'
        return F(part, c)
    if h == 'long' or h == 'bob':
        return F('M62 96 Q58 48 100 46 Q144 48 140 96 Q126 66 104 68 Q90 80 62 96Z', c)
    if h == 'spiky':
        return F('M60 96 L58 60 L70 66 L72 44 L86 58 L94 38 L104 56 L116 40 L120 60 L134 48 L132 68 L144 64 L140 96 Q120 72 100 70 Q78 72 60 96Z', c)
    if h == 'curly':
        return ''.join(f'<circle class="fill" fill="{c}" cx="{x}" cy="{y}" r="13"/>' for x, y in [(66, 80), (76, 60), (94, 50), (112, 50), (128, 60), (136, 80)])
    if h == 'bald':
        return F('M58 104 Q52 78 66 68 Q64 88 70 102Z', c) + F('M142 104 Q148 78 134 68 Q136 88 130 102Z', c) + '<path d="M84 62 Q94 56 106 58" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/>'
    return ''

def headwear(w, c):
    if w == 'songkok':
        return F('M64 78 L66 50 Q100 40 134 50 L136 78 Q100 70 64 78Z', '#1e1e24')
    if w == 'kopiah':
        return F('M66 76 Q66 48 100 44 Q134 48 134 76 Q100 68 66 76Z', '#f7f4ea') + L('M70 64 Q100 58 130 64', 'thin')
    if w == 'hardhat':
        return F('M56 84 Q56 40 100 38 Q144 40 144 84Z', c or '#f2c230') + F('M48 84 L152 84 L152 92 L48 92Z', c or '#f2c230') + L('M100 40 L100 84', 'thin')
    if w == 'chef':
        return F('M66 78 L66 56 Q52 50 58 34 Q70 18 86 28 Q100 12 116 28 Q132 18 142 34 Q148 50 134 56 L134 78Z', '#fbfaf5') + L('M66 66 L134 66', 'thin')
    if w == 'cap':
        return F('M60 80 Q60 44 100 42 Q140 44 140 80Z', c or '#c8382f') + F('M58 80 Q30 80 30 90 Q60 92 100 86Z', c or '#c8382f')
    if w == 'helmet':
        return F('M54 98 Q50 38 100 36 Q150 38 146 98 Q100 88 54 98Z', c or '#2f6d3a') + F('M64 90 Q100 80 136 90 L134 104 Q100 96 66 104Z', '#9fd0e6')
    return ''

def tudung(c):
    return F('M50 124 Q44 54 100 44 Q156 54 150 124 Q154 168 100 180 Q46 168 50 124Z', c)

# ---------------- face ----------------
def face(p):
    sk = SKIN[p['skin']]
    s = ''
    tud = p.get('tudung')
    if tud:
        s += tudung(tud)
        s += f'<ellipse class="fill" fill="{sk}" cx="100" cy="114" rx="34" ry="39"/>' + L('M68 94 Q100 72 132 94')
    else:
        s += f'<ellipse class="fill" fill="{sk}" cx="57" cy="110" rx="8" ry="12"/><ellipse class="fill" fill="{sk}" cx="143" cy="110" rx="8" ry="12"/>'
        s += F('M60 98 Q60 52 100 50 Q140 52 140 98 L140 120 Q136 154 100 158 Q64 154 60 120Z', sk)
    return s

def features(p):
    s = ''
    ey = 108 if p.get('tudung') else 104
    e = p.get('eyes', 'open')
    brow = p.get('brow', 'normal')
    if brow == 'raised':
        s += L(f'M78 {ey-14} Q86 {ey-20} 94 {ey-15} M106 {ey-15} Q114 {ey-20} 122 {ey-14}')
    elif brow == 'stern':
        s += L(f'M78 {ey-14} L94 {ey-10} M106 {ey-10} L122 {ey-14}')
    elif brow == 'worried':
        s += L(f'M78 {ey-10} L94 {ey-15} M106 {ey-15} L122 {ey-10}')
    else:
        s += L(f'M78 {ey-12} Q86 {ey-16} 94 {ey-12} M106 {ey-12} Q114 {ey-16} 122 {ey-12}')
    if e == 'smile':
        s += L(f'M80 {ey+2} Q87 {ey-4} 94 {ey+2} M106 {ey+2} Q113 {ey-4} 120 {ey+2}')
    elif e == 'tired':
        s += f'<circle class="dark" cx="86" cy="{ey+1}" r="3.6"/><circle class="dark" cx="114" cy="{ey+1}" r="3.6"/>' + L(f'M79 {ey-3} L93 {ey-3} M107 {ey-3} L121 {ey-3}') + L(f'M80 {ey+8} Q86 {ey+11} 92 {ey+8} M108 {ey+8} Q114 {ey+11} 120 {ey+8}', 'thin')
    else:
        s += f'<ellipse class="dark" cx="86" cy="{ey}" rx="4.2" ry="5.2"/><ellipse class="dark" cx="114" cy="{ey}" rx="4.2" ry="5.2"/><circle cx="87.5" cy="{ey-2}" r="1.5" fill="#fff"/><circle cx="115.5" cy="{ey-2}" r="1.5" fill="#fff"/>'
    g = p.get('glasses')
    if g == 'round':
        s += f'<circle class="line" cx="86" cy="{ey}" r="12"/><circle class="line" cx="114" cy="{ey}" r="12"/>' + L(f'M98 {ey-1} Q100 {ey-4} 102 {ey-1}')
    elif g == 'rect':
        s += f'<rect class="line" x="73" y="{ey-9}" width="25" height="18" rx="5"/><rect class="line" x="102" y="{ey-9}" width="25" height="18" rx="5"/>' + L(f'M98 {ey-1} L102 {ey-1}')
    elif g == 'shades':
        s += f'<rect class="fill" fill="#1b1b1b" x="72" y="{ey-9}" width="26" height="17" rx="6"/><rect class="fill" fill="#1b1b1b" x="102" y="{ey-9}" width="26" height="17" rx="6"/>' + L(f'M98 {ey-2} L102 {ey-2}')
    ny = ey + 6
    s += L(f'M100 {ny} Q94 {ny+12} 102 {ny+14}')
    if p.get('blush', True):
        s += f'<circle class="blush" cx="76" cy="{ey+18}" r="7"/><circle class="blush" cx="124" cy="{ey+18}" r="7"/>'
    if p.get('pottu'):
        s += f'<circle cx="100" cy="{ey-18}" r="3" fill="#c8382f"/>'
    if p.get('wrinkles'):
        s += L(f'M72 {ey-2} l-6 -3 M72 {ey+3} l-7 0 M128 {ey-2} l6 -3 M128 {ey+3} l7 0', 'thin')
    my = ey + 28
    m = p.get('mouth', 'smile')
    if m == 'grin':
        s += F(f'M84 {my} Q100 {my+14} 116 {my} Q100 {my+5} 84 {my}Z', '#fff') + L(f'M83 {my} Q100 {my+15} 117 {my}')
    elif m == 'open':
        s += F(f'M88 {my} Q100 {my+15} 112 {my}Z', '#8a2a2a')
    elif m == 'flat':
        s += L(f'M88 {my+3} L112 {my+3}')
    elif m == 'smirk':
        s += L(f'M88 {my+4} Q104 {my+8} 114 {my}')
    elif m == 'frown':
        s += L(f'M88 {my+7} Q100 {my} 112 {my+7}')
    else:
        s += L(f'M86 {my+1} Q100 {my+10} 114 {my+1}')
    fh = p.get('facial')
    hc = p.get('hair_color', INK)
    if fh in ('moustache', 'beard'):
        s += F(f'M84 {my-4} Q92 {my-10} 100 {my-6} Q108 {my-10} 116 {my-4} Q108 {my-2} 100 {my-4} Q92 {my-2} 84 {my-4}Z', hc)
    if fh == 'beard':
        s += F(f'M62 122 Q66 158 100 162 Q134 158 138 122 Q132 146 100 150 Q68 146 62 122Z', hc)
    if fh == 'stubble':
        s += ''.join(f'<circle cx="{x}" cy="{y}" r="0.9" fill="#2a211b" opacity=".5"/>' for x, y in [(80, 140), (88, 146), (96, 149), (104, 149), (112, 146), (120, 140), (84, 143), (116, 143), (100, 151)])
    return s

# ---------------- props ----------------
def prop(pr):
    if not pr: return ''
    P = {
     'mug': F('M138 182 h26 v30 a8 8 0 0 1 -8 8 h-10 a8 8 0 0 1 -8 -8Z', '#fbf4e6') + L('M164 188 q10 2 8 12 q-2 8 -8 8') + L('M146 174 q-4 -8 2 -14 M156 174 q-4 -8 2 -14'),
     'teh': F('M140 186 L166 186 L162 222 L144 222Z', '#e9c79a') + F('M140 186 L166 186 L165 196 L141 196Z', '#f5ead6') + L('M150 178 q-4 -8 2 -14'),
     'phone': F('M140 170 h24 v42 h-24Z', '#2a2a2a') + '<rect x="144" y="175" width="16" height="30" fill="#9fd0e6"/>',
     'selfie': F('M146 150 h26 v46 h-26Z', '#2a2a2a') + '<rect x="150" y="155" width="18" height="34" fill="#ffd0e0"/>' + F('M156 196 L156 232 L162 232 L162 196Z', '#888'),
     'clipboard': F('M136 168 h34 v50 h-34Z', '#b98a52') + F('M140 174 h26 v40 h-26Z', '#fff') + L('M144 184 h18 M144 192 h18 M144 200 h12', 'thin') + F('M147 164 h12 v8 h-12Z', '#888'),
     'laptop': F('M118 196 L180 196 L176 172 L122 172Z', '#9aa3ad') + F('M110 196 L188 196 L184 204 L114 204Z', '#6b737c') + '<circle cx="149" cy="184" r="4" fill="#fff"/>',
     'wrench': F('M146 226 L170 172 L176 175 L152 229Z', '#9aa3ad') + F('M166 162 a10 10 0 1 1 14 12 l-6 -4 l-4 -2Z', '#9aa3ad'),
     'stetho': L('M74 160 Q66 196 86 206 Q100 212 110 200 M126 160 Q132 186 118 196') + '<circle class="fill" fill="#9aa3ad" cx="110" cy="202" r="6"/>',
     'notepad': F('M138 172 h30 v40 h-30Z', '#fff') + L('M142 182 h22 M142 190 h22 M142 198 h16', 'thin') + F('M168 168 L174 170 L160 214 L154 212Z', '#e8b84a'),
     'lanyard_press': L('M80 162 L100 196 L120 162') + F('M88 194 h24 v18 h-24Z', '#fff') + '<text x="100" y="207" font-size="8" text-anchor="middle" font-family="sans-serif" font-weight="700" fill="#2a211b">PRESS</text>',
     'lanyard': L('M80 162 L100 196 L120 162') + F('M90 194 h20 v22 h-20Z', '#fff'),
     'box': F('M132 180 h40 v38 h-40Z', '#d9a865') + L('M132 192 h40 M152 180 v12', 'thin'),
     'briefcase': F('M134 188 h40 v30 h-40Z', '#5b3a22') + F('M146 182 h16 v6 h-16Z', '#5b3a22'),
     'gold_chain': '<path d="M80 162 Q100 186 120 162" stroke="#e8b84a" stroke-width="4" fill="none"/>',
     'ladle': F('M150 230 L166 168 L170 169 L156 231Z', '#9aa3ad') + F('M158 168 a12 9 0 1 0 22 2Z', '#9aa3ad'),
     'pearls': ''.join(f'<circle cx="{100+28*__import__("math").cos(a/10)}" cy="{168+12*__import__("math").sin(a/10)}" r="3" fill="#fbfaf5" stroke="#2a211b" stroke-width="1"/>' for a in range(3, 30, 3)),
     'tablet': F('M136 172 h34 v44 h-34Z', '#2a2a2a') + '<rect x="140" y="176" width="26" height="36" fill="#cde3f7"/>',
     'keys': '<circle class="line" cx="156" cy="196" r="8"/>' + L('M162 202 L172 214 M168 208 L172 206'),
     'walkie': F('M144 168 h18 v44 h-18Z', '#2a2a2a') + F('M148 156 h4 v12 h-4Z', '#2a2a2a') + '<rect x="147" y="176" width="12" height="10" fill="#9fd0e6"/>',
     'headset': L('M58 100 Q60 46 100 44 Q140 46 142 100') + F('M52 96 h12 v20 h-12Z', '#2a2a2a') + F('M136 96 h12 v20 h-12Z', '#2a2a2a') + L('M58 116 Q66 136 86 138'),
     'flower': f'<circle cx="138" cy="70" r="6" fill="#e8b84a"/>' + ''.join(f'<circle cx="{138+9*__import__("math").cos(a)}" cy="{70+9*__import__("math").sin(a)}" r="6" fill="#d9426a"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)),
     'helmet_hold': F('M134 196 Q134 170 156 168 Q178 170 178 196Z', '#2f6d3a') + F('M138 194 h36 v6 h-36Z', '#2a2a2a'),
     'scalpel_mask': F('M74 132 Q100 126 126 132 L124 150 Q100 158 76 150Z', '#9fd0e6'),
    }
    return P.get(pr, '')

# ---------------- special characters ----------------
def robot():
    return (F('M40 232 Q46 178 100 170 Q154 178 160 232Z', '#9fb6c8') + F('M60 70 h80 v86 a10 10 0 0 1 -10 10 h-60 a10 10 0 0 1 -10 -10Z', '#cfdde8')
            + L('M100 70 L100 50') + '<circle class="fill" fill="#d8423a" cx="100" cy="46" r="7"/>'
            + F('M70 92 h60 v34 h-60Z', '#1f2a36') + '<circle cx="86" cy="109" r="7" fill="#6ff2c4"/><circle cx="114" cy="109" r="7" fill="#6ff2c4"/>'
            + L('M84 144 h32') + ''.join(f'<rect x="{x}" y="140" width="5" height="8" fill="#2a211b"/>' for x in (88, 98, 108))
            + F('M50 104 h10 v24 h-10Z M140 104 h10 v24 h-10Z', '#9fb6c8') + '<text x="100" y="206" font-size="13" text-anchor="middle" font-family="sans-serif" font-weight="700" fill="#2a211b">3000</text>')

def elephant():
    return (F('M30 232 Q26 150 70 128 Q100 112 130 128 Q174 150 170 232Z', '#9c9c94')
            + F('M44 90 Q30 150 64 160 Q78 130 74 100Z', '#8f8f87') + F('M156 90 Q170 150 136 160 Q122 130 126 100Z', '#8f8f87')
            + F('M66 96 Q66 52 100 50 Q134 52 134 96 Q132 128 116 140 Q112 180 104 206 Q98 214 92 206 Q96 186 92 150 Q70 134 66 96Z', '#a8a8a0')
            + '<ellipse class="dark" cx="86" cy="96" rx="4" ry="5"/><ellipse class="dark" cx="114" cy="96" rx="4" ry="5"/>'
            + L('M80 84 Q86 80 92 84 M108 84 Q114 80 120 84') + F('M88 138 Q80 150 84 160 Q90 150 94 142Z', '#f5efe0') + F('M112 138 Q120 150 116 160 Q110 150 106 142Z', '#f5efe0')
            + F('M150 196 Q158 160 176 150 Q176 176 162 200Z', '#4f8a3a') + F('M20 190 Q30 160 48 156 Q44 180 30 196Z', '#4f8a3a'))

def group():
    def mini(cx, cy, sk, extra=''):
        return (F(f'M{cx-34} 232 Q{cx-30} {cy+48} {cx} {cy+44} Q{cx+30} {cy+48} {cx+34} 232Z', extra or '#7ea6d8')
                + f'<circle class="fill" fill="{sk}" cx="{cx}" cy="{cy}" r="26"/><circle class="dark" cx="{cx-9}" cy="{cy-2}" r="2.8"/><circle class="dark" cx="{cx+9}" cy="{cy-2}" r="2.8"/>'
                + L(f'M{cx-9} {cy+10} Q{cx} {cy+17} {cx+9} {cy+10}'))
    return (mini(56, 120, SKIN['tan'], '#9cc9a2') + F('M28 116 Q26 82 56 78 Q86 82 84 116 Q86 142 56 150 Q26 142 28 116Z', '#3f4f86') + f'<circle class="fill" fill="{SKIN["tan"]}" cx="56" cy="122" r="21"/><circle class="dark" cx="48" cy="120" r="2.8"/><circle class="dark" cx="64" cy="120" r="2.8"/>' + L('M48 131 Q56 137 64 131')
            + mini(144, 116, SKIN['fair'], '#e9a7bf') + F('M118 108 Q120 84 144 84 Q168 84 170 108 Q160 96 144 96 Q128 96 118 108Z', INK)
            + mini(100, 98, SKIN['brown'], '#f2c46b') + F('M74 92 Q76 66 100 66 Q124 66 126 92 Q114 80 100 80 Q86 80 74 92Z', INK))

# ---------------- the cast ----------------
CAST = {
 # base game
 'faizal': dict(skin='tan', hair='short', outfit='coverall', c='#3f6fae', c2='#2f5a92', mouth='grin', prop='wrench', bg='#9cc9a2'),
 'mei': dict(skin='light', hair='bob', outfit='blazer', c='#7a6fb8', glasses='rect', mouth='smile', prop='laptop', bg='#d6d0f0'),
 'raj': dict(skin='brown', hair='side_part', outfit='shirt_tie', c='#2f6fb8', facial='moustache', mouth='grin', prop='phone', bg='#f3dd9b'),
 'jtk': dict(skin='tan', hair='short', outfit='baju_melayu', c='#c9d8e8', headwear='songkok', glasses='rect', brow='stern', mouth='flat', prop='clipboard', bg='#bcd3e6'),
 'siti': dict(skin='medium', tudung='#5aa69a', outfit='baju', c='#cfe8e0', mouth='smile', prop='headset', bg='#cfe8e0'),
 'bank': dict(skin='fair', hair='side_part', hair_color='#3a3a3a', outfit='blazer', c='#3a4a5c', c2='#c8382f', glasses='round', mouth='grin', prop='briefcase', bg='#d9e0e6'),
 'infl': dict(skin='fair', hair='long', hair_color='#5a3a2a', outfit='tshirt', c='#ff8fb8', mouth='open', eyes='smile', prop='selfie', bg='#ffd0e0'),
 'client': dict(skin='tan', tudung='#8e5aa8', outfit='kebaya', c='#e8dcf5', c2='#f6e6ff', mouth='smirk', prop='pearls', bg='#e8dcf5'),
 'press': dict(skin='medium', hair='curly', outfit='tshirt', c='#6b7c8f', glasses='round', mouth='smile', prop='notepad', bg='#e6e6e6'),
 'agent': dict(skin='tan', hair='spiky', outfit='polo', c='#1f1f1f', c2='#2a2a2a', glasses='shades', mouth='smirk', prop='gold_chain', bg='#cccccc'),
 'sales': dict(skin='fair', hair='short', outfit='shirt_tie', c='#e8a33d', mouth='grin', eyes='smile', prop='box', bg='#f5e2c8'),
 'ai': 'robot',
 'nephew': dict(skin='light', hair='spiky', outfit='blazer', c='#d9a03a', c2='#2a2a2a', glasses='shades', mouth='smirk', prop='phone', bg='#f7e3a1'),
 'jess': dict(skin='light', hair='bun', hair_color='#3b2a20', outfit='tshirt', c='#f08a6a', mouth='flat', eyes='open', prop='tablet', bg='#f9d5c0'),
 'staff': 'group',
 # E&E Penang
 'ee_seng': dict(skin='light', hair='short', outfit='polo', c='#2f6fb8', c2='#d9e4f2', mouth='grin', prop='walkie', bg='#cfe0f5'),
 'ee_priya': dict(skin='brown', hair='long', outfit='blazer', c='#2a3a5c', glasses='rect', pottu=True, brow='raised', mouth='flat', prop='clipboard', bg='#f0d9c4'),
 'ee_zul': dict(skin='tan', hair='short', outfit='polo', c='#5aa66a', c2='#3f8a4f', eyes='tired', facial='stubble', mouth='smile', prop='teh', bg='#d5ecd4'),
 'ee_bishnu': dict(skin='medium', hair='short', outfit='coverall', c='#7a8a9a', c2='#5f6f80', mouth='smile', prop='lanyard', bg='#f6e0b5'),
 # Palm oil Sabah
 'po_haji': dict(skin='medium', hair='short', hair_color='#6b6158', headwear='kopiah', outfit='baju_melayu', c='#d9cba8', facial='beard', wrinkles=True, mouth='smile', prop='walkie', bg='#d9e8c4'),
 'po_siva': dict(skin='deep', hair='short', outfit='tshirt', c='#4f7f4f', facial='moustache', headwear='cap', mouth='grin', prop='clipboard', bg='#f2dcc0'),
 'po_lena': dict(skin='tan', hair='ponytail', outfit='jacket', c='#3f7a6a', glasses='round', mouth='smile', prop='tablet', bg='#e2e2f2'),
 'po_jumbo': 'elephant',
 # Oil & gas
 'og_azman': dict(skin='tan', hair='short', headwear='hardhat', c='#f5f5f0', outfit='coverall', c2='#e86a2a', facial='moustache', mouth='flat', brow='stern', prop='walkie', bg='#c9dbe8'),
 'og_danny': dict(skin='medium', hair='short', headwear='hardhat', outfit='coverall', c='#e86a2a', c2='#c8552a', mouth='grin', prop='wrench', bg='#f0d7b8'),
 'og_imran': dict(skin='tan', hair='side_part', outfit='shirt_tie', c='#1f3a6a', glasses='rect', mouth='smile', prop='laptop', bg='#dfe3ea'),
 # Mamak
 'mk_ravi': dict(skin='deep', hair='short', headwear='chef', outfit='chef', c='#c8382f', facial='moustache', mouth='smirk', prop='ladle', bg='#f6d3a8'),
 'mk_chong': dict(skin='light', hair='spiky', outfit='apron', c='#4a6fa5', c2='#f5f1e8', eyes='tired', mouth='smile', prop='teh', bg='#d3e3f3'),
 'mk_amir': dict(skin='tan', hair='short', outfit='jacket', c='#2f8a4f', c2='#e8e8e8', mouth='grin', prop='helmet_hold', bg='#d7f0d0'),
 'mk_nora': dict(skin='fair', tudung='#3f4f86', outfit='blazer', c='#3f4f86', glasses='round', brow='raised', mouth='flat', prop='clipboard', bg='#e8e0f4'),
 # Resort Langkawi
 'rs_jun': dict(skin='light', hair='side_part', outfit='blazer', c='#2a5a6a', c2='#e8a33d', mouth='grin', eyes='smile', prop='lanyard', bg='#d5ecf0'),
 'rs_puansri': dict(skin='fair', tudung='#c8a03a', outfit='kebaya', c='#d9426a', c2='#f7d6e0', glasses='shades', mouth='frown', prop='pearls', bg='#f6d6e6'),
 'rs_marco': dict(skin='light', hair='curly', hair_color='#3b2a20', headwear='chef', outfit='chef', c='#3a7a3a', facial='moustache', mouth='open', prop='ladle', bg='#f3e3c3'),
 'rs_karim': dict(skin='medium', hair='short', outfit='blazer', c='#3a3a5a', c2='#2a8a8a', facial='beard', mouth='smile', prop='tablet', bg='#dfe6d6'),
 # Construction
 'cn_ali': dict(skin='tan', hair='short', headwear='hardhat', c='#f2c230', outfit='hiviz', c2='#6b8aa5', facial='moustache', mouth='grin', prop='walkie', bg='#f3dfa8'),
 'cn_keong': dict(skin='fair', hair='bald', hair_color='#3a3a3a', outfit='polo', c='#c8382f', c2='#a82a22', mouth='smirk', prop='keys', bg='#d6dfe8'),
 'cn_kavitha': dict(skin='brown', hair='bun', headwear='hardhat', c='#f5f5f0', outfit='hiviz', c2='#3f6fae', pottu=True, brow='stern', mouth='flat', prop='clipboard', bg='#f6d2c2'),
 'cn_tansri': dict(skin='light', hair='side_part', hair_color='#d8d4cc', outfit='blazer', c='#2a2a3a', c2='#e8b84a', wrinkles=True, mouth='smirk', prop='briefcase', bg='#e3dcef'),
 # Logistics
 'lg_lim': dict(skin='fair', hair='short', hair_color='#5a5a5a', headwear='cap', c='#2f6fb8', outfit='polo', c2='#2a5a92', facial='stubble', wrinkles=True, mouth='grin', prop='keys', bg='#e2dccb'),
 'lg_hema': dict(skin='brown', hair='long', outfit='blazer', c='#8a3a5a', pottu=True, mouth='smile', prop='tablet', bg='#f1d6e2'),
 'lg_danial': dict(skin='tan', hair='spiky', outfit='hiviz', c2='#3f3f3f', eyes='smile', mouth='grin', prop='selfie', bg='#d3ecd9'),
 # Bank
 'bk_jason': dict(skin='light', hair='side_part', outfit='blazer', c='#22344f', c2='#7a4ab8', mouth='grin', brow='raised', prop='mug', bg='#dfe2ec'),
 'bk_zarina': dict(skin='tan', tudung='#2a4a5a', outfit='blazer', c='#2a4a5a', glasses='rect', brow='raised', mouth='flat', prop='clipboard', bg='#e6dcef'),
 'bk_huimin': dict(skin='light', hair='ponytail', outfit='blazer', c='#4a6a9a', eyes='tired', brow='worried', mouth='open', prop='laptop', bg='#f6dccf'),
 # Hospital
 'hp_mary': dict(skin='medium', hair='bun', hair_color='#5a5a5a', outfit='scrubs', c='#2f6f8a', wrinkles=True, brow='stern', mouth='flat', prop='stetho', bg='#d8ecf2'),
 'hp_wong': dict(skin='light', hair='side_part', outfit='scrubs', c='#3f8a6a', glasses='rect', brow='stern', mouth='frown', prop='stetho', bg='#e2e6f3'),
 'hp_thivya': dict(skin='brown', hair='bun', outfit='scrubs', c='#5a9ac8', pottu=True, mouth='smile', prop='phone', bg='#f3dbe6'),
 'hp_budi': dict(skin='tan', hair='short', hair_color='#d8d4cc', headwear='songkok', outfit='baju_melayu', c='#c8a86a', glasses='round', wrinkles=True, mouth='grin', eyes='smile', prop='', bg='#efe3c6'),
 # Tech
 'tc_darren': dict(skin='light', hair='side_part', outfit='tshirt', c='#3a3a3a', mouth='grin', prop='laptop', bg='#d8e2f6'),
 'tc_nurul': dict(skin='tan', tudung='#2a2a3a', outfit='tshirt', c='#6a4ab8', glasses='rect', mouth='smirk', prop='laptop', bg='#e0f0dc'),
 'tc_arun': dict(skin='deep', hair='curly', outfit='jacket', c='#3a3a5a', eyes='tired', facial='stubble', mouth='smile', prop='headset', bg='#e6dccb'),
 'tc_grace': dict(skin='fair', hair='bob', outfit='blazer', c='#8a2a2a', c2='#2a2a2a', brow='raised', mouth='smirk', prop='mug', bg='#f2dcdc'),
}

def draw(cid, p):
    bgc = '#e6e6e6' if isinstance(p, str) else p.get('bg', '#e6e6e6')
    body = ''
    if p == 'robot': body = robot(); bgc = '#cde3f7'
    elif p == 'elephant': body = elephant(); bgc = '#d8e8c8'
    elif p == 'group': body = group(); bgc = '#d8e6cf'
    else:
        hc = p.get('hair_color', INK)
        body += hair_back(p.get('hair', ''), hc) if not p.get('tudung') else ''
        body += outfit(p['outfit'], p.get('c', '#7ea6d8'), p.get('c2'))
        if p.get('prop') == 'stetho': body += prop('stetho')
        if not p.get('tudung'):
            body += F('M88 140 L112 140 L114 162 L86 162Z', SKIN[p['skin']])
        body += face(p)
        if not p.get('tudung'):
            body += hair_front(p.get('hair', ''), hc)
            body += headwear(p.get('headwear', ''), p.get('c') if p.get('headwear') in ('hardhat', 'cap') and p.get('outfit') != 'coverall' else None)
        body += features(p)
        if p.get('prop') not in ('stetho',): body += prop(p.get('prop'))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 232">{HEAD}'
           f'<rect width="200" height="232" fill="#fbf4e6"/><circle cx="100" cy="112" r="86" fill="{bgc}" opacity=".55"/><rect width="200" height="232" filter="url(#paper)"/>'
           f'<g filter="url(#rough)" opacity=".95">{body}</g></svg>\n')
    return svg

if __name__ == '__main__':
    redraw = '--all' in sys.argv
    n = 0
    for cid, p in CAST.items():
        path = f'art/{cid}.svg'
        if cid in HAND_DRAWN or (os.path.exists(path) and not redraw):
            continue
        open(path, 'w').write(draw(cid, p)); n += 1
    print(f'drew {n} portraits')

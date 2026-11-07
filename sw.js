// Offline support. Keeps a copy of every game file so the game works without internet.
// To ship an update: change VERSION, then reload the page twice.
const VERSION = 'bb-v10';
const FILES = [
  'art/agent.svg',
  'art/ai.svg',
  'art/aina.svg',
  'art/bank.svg',
  'art/bk_huimin.svg',
  'art/bk_jason.svg',
  'art/bk_zarina.svg',
  'art/client.svg',
  'art/cn_ali.svg',
  'art/cn_kavitha.svg',
  'art/cn_keong.svg',
  'art/cn_tansri.svg',
  'art/ee_bishnu.svg',
  'art/ee_priya.svg',
  'art/ee_seng.svg',
  'art/ee_zul.svg',
  'art/faizal.svg',
  'art/hp_budi.svg',
  'art/hp_mary.svg',
  'art/hp_thivya.svg',
  'art/hp_wong.svg',
  'art/infl.svg',
  'art/jess.svg',
  'art/jtk.svg',
  'art/lg_danial.svg',
  'art/lg_hema.svg',
  'art/lg_lim.svg',
  'art/mei.svg',
  'art/mk_amir.svg',
  'art/mk_chong.svg',
  'art/mk_nora.svg',
  'art/mk_ravi.svg',
  'art/nephew.svg',
  'art/og_azman.svg',
  'art/og_danny.svg',
  'art/og_imran.svg',
  'art/po_haji.svg',
  'art/po_jumbo.svg',
  'art/po_lena.svg',
  'art/po_siva.svg',
  'art/press.svg',
  'art/raj.svg',
  'art/ros.svg',
  'art/rs_jun.svg',
  'art/rs_karim.svg',
  'art/rs_marco.svg',
  'art/rs_puansri.svg',
  'art/sales.svg',
  'art/siti.svg',
  'art/staff.svg',
  'art/sys.svg',
  'art/tc_arun.svg',
  'art/tc_darren.svg',
  'art/tc_grace.svg',
  'art/tc_nurul.svg',
  'art/uncle.svg',
  'fonts/bricolage-grotesque-latin-400-normal.woff2',
  'fonts/bricolage-grotesque-latin-600-normal.woff2',
  'fonts/bricolage-grotesque-latin-800-normal.woff2',
  'fonts/fonts.css',
  'fonts/noto-sans-tamil-tamil-400-normal.woff2',
  'fonts/noto-sans-tamil-tamil-600-normal.woff2',
  'fonts/noto-sans-tamil-tamil-800-normal.woff2',
  'icons/apple-touch-icon.png',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'index.html',
  'lang/ms-packs.js',
  'lang/ms.js',
  'lang/ta-packs.js',
  'lang/ta.js',
  'lang/zh-packs.js',
  'lang/zh.js',
  'manifest.webmanifest',
  'packs/bank.js',
  'packs/construction.js',
  'packs/electronics.js',
  'packs/hospital.js',
  'packs/logistics.js',
  'packs/mamak.js',
  'packs/oilgas.js',
  'packs/palmoil.js',
  'packs/resort.js',
  'packs/tech.js',
  './'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // Use the saved copy if there is one; otherwise download it and save a copy (this is how art files get saved).
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request).then(res => {
    if (res.ok && new URL(e.request.url).origin === location.origin) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); }
    return res;
  })));
});

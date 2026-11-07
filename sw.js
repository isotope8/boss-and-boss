// Offline support. Keeps a copy of every game file so the game works without internet.
// To ship an update: change VERSION, then reload the page twice.
const VERSION = 'bb-v8';
const FILES = [
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
  'lang/ms.js',
  'lang/ta.js',
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
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request)));
});

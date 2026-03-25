const CACHE_NAME = 'jarvis-v1';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(res => res || fetch(e.request))
  );
});

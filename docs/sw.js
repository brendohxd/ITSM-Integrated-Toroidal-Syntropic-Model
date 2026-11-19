const CACHE_NAME = 'itsm-pwa-v17-20261119';
const ASSETS = [
  './',
  './index.html',
  './research.html',
  './claims.html',
  './papers.html',
  './architecture.html',
  './vision.html',
  './reproduce.html',
  './styles.css',
  './atlas.css?v=20261119a',
  './topology.js?v=20261119a',
  './assets/atlas/t3-periodic-cell_v1.svg',
  './assets/atlas/t3-face-pairs_v1.svg',
  './assets/atlas/itsm-periodic-mark_v1.svg',
  './assets/atlas/itsm-research-share_v1.png',

  './manifest.json',
  './site.webmanifest',
  './favicon.ico',
  './favicon.svg',
  './favicon-32x32.png',
  './favicon-16x16.png',
  './apple-touch-icon.png',
  './android-chrome-192x192.png',
  './android-chrome-512x512.png',
  './android-chrome-maskable-192x192.png',
  './android-chrome-maskable-512x512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS).catch((err) => {
        console.warn('Pre-caching warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key.startsWith('itsm-pwa-') && key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && event.request.method === 'GET') {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => caches.match(event.request))
  );
});

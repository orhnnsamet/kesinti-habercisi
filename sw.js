const CACHE_NAME = "kesinti-habercisi-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./kesintiler.json"
];

// Kurulumda temel dosyaları telefona önbellekle
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// Eski önbellekleri temizle
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => key !== CACHE_NAME && caches.delete(key)))
    )
  );
  self.clients.claim();
});

// İnternet varsa güncel veriyi getir, yoksa hafızadan aç
self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});

// Offline-välimuisti. Nosta versionumeroa aina kun sivua päivitetään.
const CACHE = "niemet-v21";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png",
  "img/silta.jpg", "img/lounge.jpg", "img/carl.jpg", "img/hauta.jpg", "img/jilji.jpg", "img/kaste.jpg", "aineisto/pubiruoat.jpg"];
self.addEventListener("install", e => {
  // cache: "reload" ohittaa selaimen HTTP-välimuistin (GitHub Pages: max-age=600)
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES.map(f => new Request(f, { cache: "reload" })))));
  self.skipWaiting();
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
// Verkko ensin (aina tuorein ohjelma), välimuisti jos ei yhteyttä.
// cache: "no-cache" = kysy aina palvelimelta onko uudempaa (ETag → 304 jos ei muutoksia).
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  const req = e.request.mode === "navigate" ? new Request(e.request.url, { cache: "no-cache" }) : new Request(e.request, { cache: "no-cache" });
  e.respondWith(fetch(req).then(r => {
    if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return r;
  }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match("index.html"))));
});

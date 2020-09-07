var cacheName = "devdiv-v1";
const staticAssets = [
  "/",
  "/static/logo.png",
  "/static/css/Main.css",
  "/static/css/style.css",
  "/static/css/bootstrap.min.css",
  "/static/manifest.webmanifest",
  "/static/js/main.js",
  "/static/js/navbar.js",
  "/static/js/scroll.js",
  "/static/js/jquery-3.2.1.min.js",
  "/static/js/jquery.min.js",
  "/static/debut_light.webp",
  "/divdev+pictures/default.png",
  "/static/pat.svg",
  "/post/",
];

self.addEventListener("install", async (e) => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  self.clients.claim();
});

self.addEventListener("fetch", async (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (url.origin === location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

async function cacheFirst(req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}

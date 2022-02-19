var cacheName = "devdiv-pwa-v" + new Date().getTime();
const DEBUG = false
var host = self.location.protocol + "//" + self.location.host + "/static";
if (DEBUG === false) {
  host = "https://d2rkspfokjrj1j.cloudfront.net/static";
}
const staticAssets = [
  // CSS
  `${host}/css/Main.css`,
  `${host}/css/post.css`,
  `${host}/css/reset.css`,

  // JAVASCRIPTS
  `${host}/js/main.js`,
  `${host}/js/navbar.js`,
  `${host}/js/scroll.js`,
  // IMAGES
  `${host}/debut_light.webp`,
  `${host}/logo.png`,
  // MANIFEST
  `${host}/manifest.webmanifest`,
];

self.addEventListener("install", async (e) => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  self.clients.claim();
  e.waitUntil(
    caches.keys().then(function(keyList) {
        return Promise.all(keyList.map(function (key) {
            if (key !== cacheName) {
                return caches.delete(key);
            }
        }));
    })
  );
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

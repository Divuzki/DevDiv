const CACHE_VERSION = 1;

const DEBUG = true;
var host = "//" + self.location.host + "/static";
if (DEBUG === false) {
  host = "https://d2rkspfokjrj1j.cloudfront.net/static";
}

const BASE_CACHE_FILES = [
  // CSS
  `${host}/css/Main.css`,
  `${host}/css/style.css`,

  // JAVASCRIPTS
  `${host}/js/main.js`,
  `${host}/js/navbar.js`,
  `${host}/js/scroll.js`,
  // IMAGES
  `${host}/logo.png`,
  // MANIFEST
  `${host}/manifest.webmanifest`,
];

const OFFLINE_CACHE_FILES = ["pwa_file/error-slash-offline.html"];

const NOT_FOUND_CACHE_FILES = ["pwa_file/error-slash-not-found.html"];

const OFFLINE_PAGE = "/offline.html";
const NOT_FOUND_PAGE = "/404.html";

const CACHE_VERSIONS = {
  assets: "assets-v" + CACHE_VERSION,
  content: "content-v" + CACHE_VERSION,
  offline: "offline-v" + CACHE_VERSION,
  notFound: "404-v" + CACHE_VERSION,
};

/**
 * installServiceWorker
 * @returns {Promise}
 */
function installServiceWorker() {
  return Promise.all([
    caches.open(CACHE_VERSIONS.assets).then((cache) => {
      return cache.addAll(BASE_CACHE_FILES);
    }),
    caches.open(CACHE_VERSIONS.offline).then((cache) => {
      return cache.addAll(OFFLINE_CACHE_FILES);
    }),
    caches.open(CACHE_VERSIONS.notFound).then((cache) => {
      return cache.addAll(NOT_FOUND_CACHE_FILES);
    }),
  ]);
}

/**
 * cleanupLegacyCache
 * @returns {Promise}
 */
function cleanupLegacyCache() {
  let currentCaches = Object.keys(CACHE_VERSIONS).map((key) => {
    return CACHE_VERSIONS[key];
  });

  return new Promise((resolve, reject) => {
    caches
      .keys()
      .then((keys) => {
        return (legacyKeys = keys.filter((key) => {
          return !~currentCaches.indexOf(key);
        }));
      })
      .then((legacy) => {
        if (legacy.length) {
          Promise.all(
            legacy.map((legacyKey) => {
              return caches.delete(legacyKey);
            })
          )
            .then(() => {
              resolve();
            })
            .catch((err) => {
              reject(err);
            });
        } else {
          resolve();
        }
      })
      .catch(() => {
        reject();
      });
  });
}

self.addEventListener("install", (event) => {
  event.waitUntil(installServiceWorker());
});

// The activate handler takes care of cleaning up old caches.
self.addEventListener("activate", (event) => {
  event.waitUntil(
    Promise.all([cleanupLegacyCache()]).catch((err) => {
      event.skipWaiting();
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
  const cache = await caches.open(CACHE_VERSIONS.assets);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(CACHE_VERSIONS.assets);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}

const CACHE_VERSION = 1;

const BASE_CACHE_FILES = [
    '/style.css',
    '/script.js',
    '/search.json',
    '/manifest.json',
    '/favicon.png',
];

const OFFLINE_CACHE_FILES = [
    '/style.css',
    '/script.js',
    '/offline.html',
];

const NOT_FOUND_CACHE_FILES = [
    '/style.css',
    '/script.js',
    '/404.html',
];

const OFFLINE_PAGE = '/offline/index.html';
const NOT_FOUND_PAGE = '/404.html';

const CACHE_VERSIONS = {
    assets: 'assets-v' + CACHE_VERSION,
    content: 'content-v' + CACHE_VERSION,
    offline: 'offline-v' + CACHE_VERSION,
    notFound: '404-v' + CACHE_VERSION,
};

function installServiceWorker() {
    return Promise.all(
        [
            caches.open(CACHE_VERSIONS.assets)
                .then(
                    (cache) => {
                        return cache.addAll(BASE_CACHE_FILES);
                    }
                ),
            caches.open(CACHE_VERSIONS.offline)
                .then(
                    (cache) => {
                        return cache.addAll(OFFLINE_CACHE_FILES);
                    }
                ),
            caches.open(CACHE_VERSIONS.notFound)
                .then(
                    (cache) => {
                        return cache.addAll(NOT_FOUND_CACHE_FILES);
                    }
                )
        ]
    );
}
'use strict';

self.addEventListener('push', (event) => {
  var push = JSON.parse(event.data.text());

  if (push.data.hasOwnProperty('pixel') && validURL(push.data.pixel)) {
    var pixelUrl = push.data.pixel;
    var getTrackingPixelPromise = getTrackingPixel(pixelUrl);
    var showPushNotificationPromise = showPushNotification(push);
    var promiseChain = Promise.all([
      getTrackingPixelPromise,
      showPushNotificationPromise
    ]);
    event.waitUntil(promiseChain);
  }
  else {
    event.waitUntil(showPushNotification(push));
  };
});

function showPushNotification(push) {
  var tag = push.data.tag;
  if (tag && tag.startsWith('service_message')) {
    return;
  }

  var title = push.data.title;

  var notificationOptions = {
    body: push.data.body,
    icon: push.data.icon,
    badge: push.data.badge,
    data: {
      click_action: push.data.click_action,
    },
    image: push.data.attachment_url,
    tag: push.data.tag,
  };

  if (push.data.hasOwnProperty('actions')) {
    var actions = Array.isArray(push.data.actions) ? push.actions : JSON.parse(push.data.actions);
    if (actions) {
      notificationOptions.actions = actions.filter((action) => action.title != null);
    }
  }

  var notificationPromise = self.registration.showNotification(title, notificationOptions);

  return notificationPromise;
};

function getTrackingPixel(url) {
  var getTrackingPixelPromise = fetch(url);
  return getTrackingPixelPromise;
};

self.addEventListener('notificationclick', function (event) {
  var target = event.notification.data.click_action || '/';
  event.notification.close();

  return clients.openWindow(target);
});

function validURL(url) {
  var pattern = new RegExp('^(https?:\\/\\/)?' +
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' +
    '((\\d{1,3}\\.){3}\\d{1,3}))' +
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' +
    '(\\?[;&a-z\\d%_.~+=-]*)?' +
    '(\\#[-a-z\\d_]*)?$', 'i');
  return !!pattern.test(url);
};
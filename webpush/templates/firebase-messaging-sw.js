// [START initialize_firebase_in_sw]
// Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js");

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
firebase.initializeApp({
  apiKey: "AIzaSyDRIyN62EVYL5HbtqIDjDRK_1PI_0jcoQY",
  authDomain: "devdiv-web.firebaseapp.com",
  projectId: "devdiv-web",
  storageBucket: "devdiv-web.appspot.com",
  messagingSenderId: "192359966552",
  appId: "1:192359966552:web:f8b99e44f4e4cc8435e72d",
  measurementId: "G-6Z8BXD1Z4H",
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
// [END initialize_firebase_in_sw]

// If you would like to customize notifications that are received in the
// background (Web app is closed or not in browser focus) then you should
// implement this optional method.
// [START background_handler]
messaging.setBackgroundMessageHandler(function (payload) {
  console.log(
    "[firebase-messaging-sw.js] Received background message ",
    payload
  );
  // Customize notification here
  payload = payload.data;
  console.log(payload);
  const notificationTitle = payload.title;
  const notificationOptions = {
    body: payload.body,
    icon: payload.icon_url,
    click_action: payload.click_action,
    sound: payload.sound,
  };

  self.addEventListener(
    "notificationclick",
    function (event) {
      event.notification.close();
      // fcp_options.link field from the FCM backend service goes there, but as the host differ, it not handled by Firebase JS Client sdk, so custom handling
      if (
        event.notification &&
        event.notification.data &&
        event.notification.data.FCM_MSG &&
        event.notification.data.FCM_MSG.notification
      ) {
        const url = event.notification.data.FCM_MSG.notification.click_action;
        event.waitUntil(
          self.clients.matchAll({ type: "window" }).then((windowClients) => {
            // Check if there is already a window/tab open with the target URL
            for (var i = 0; i < windowClients.length; i++) {
              var client = windowClients[i];
              // If so, just focus it.
              if (client.url === url && "focus" in client) {
                return client.focus();
              }
            }
            // If not, then open the target URL in a new window/tab.
            if (self.clients.openWindow) {
              console.log("open window");
              return self.clients.openWindow(url);
            }
          })
        );
      }
    },
    false
  );

  return self.registration.showNotification(
    notificationTitle,
    notificationOptions
  );
});
// [END background_handler]

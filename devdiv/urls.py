from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from users import views
from webpush.views import send, add_devices_view
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)

handler404 = 'errorHandler.views.view_404'

urlpatterns = [
    path('HadminD/', admin.site.urls),
    path("firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="firebase-messaging-sw.js",
            content_type="application/javascript",
        ),
        name="firebase-messaging-sw.js"
    ),
    path('push-api/add/device/', add_devices_view, name="push_add_device"),
    path('', include('users.urls', namespace="users")),
    path('pwa_file/<str:tmp>', views.devdiv_tmp_render, name="render_tmp"),
    path('privacy-policy/en/', views.policy_en, name="policy_en"),
    path('privacy-policy/fr/', views.policy_fr, name="policy_fr"),
    re_path(r'^sw(.*.js)$',
            views.devdiv_serviceworker, name='devdiv_sw'),
    path('0u/blog/api/', include('core.api.urls', namespace="post-api")),
    path("send/", send, name="send-web-notifications"),
    # path('/feeds/posts/summary/', include('core.api.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

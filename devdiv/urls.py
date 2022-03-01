from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from users import views

handler404 = 'errorHandler.views.view_404'

urlpatterns = [
    path('HadminD/', admin.site.urls),
    path('', include('users.urls', namespace="users")),
    path('0u/blog/api/', include('core.api.urls', namespace="post-api")),
    path('pwa_file/<str:tmp>', views.devdiv_tmp_render, name="render_tmp"),
    re_path(r'^serviceworker(.*.js)$', views.devdiv_serviceworker, name='devdiv_sw'),
    re_path(r'^sw(.*.js)$', views.sw, name='sw'),
    path('privacy-policy/en/', views.policy_en, name="policy_en"),
    path('privacy-policy/fr/', views.policy_fr, name="policy_fr"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

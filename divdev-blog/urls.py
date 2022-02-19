from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from users import views

handler404 = 'errorHandler.views.view_404'

urlpatterns = [
    path('HadminD/', admin.site.urls),
    path('', include('users.urls')),
    path('0u/blog/api/', include('core.api.urls', namespace="post-api")),
    re_path(r'^serviceworker(.*.js)$', views.devdiv_serviceworker, name='devdiv_sw'),
]


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

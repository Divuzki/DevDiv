from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static

handler404 = 'errorHandler.views.view_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path(r'', include('pwa.urls')),
    path('auth.blog@api/', include('core.api.urls', namespace="blog-api")),
]


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

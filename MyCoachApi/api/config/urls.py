from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf.urls.static import static

from django.conf import settings
from rest_framework import urls as rest_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api_coach/", include("api_coach.urls", namespace="api_coach")),
    path('api-auth/', include('rest_framework.urls')),
]
# urlpatterns += [path("", include(rest_urls, namespace="rest_framework"))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

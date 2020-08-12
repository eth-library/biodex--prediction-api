from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .api_router import router_urls

from frontend.urls import urlpatterns as fe_urlpatterns


urlpatterns = [
    path("lepi-admin/", admin.site.urls),    
    path("api-pred/", include(router_urls)),
]

urlpatterns += fe_urlpatterns

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

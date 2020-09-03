from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .api_router import router_urls
from frontend.urls import urlpatterns as fe_urlpatterns


urlpatterns = [
    path("lepi-admin/", admin.site.urls),    
    url(r"^pred-api/", include(router_urls)),
]

urlpatterns += fe_urlpatterns

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

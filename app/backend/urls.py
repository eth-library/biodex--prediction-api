from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from .api_router import router
from uploadforpredict_rest.views import predict_image_view
from imageClassification_rest.viewsets import get_example_images
from taxonomy_rest.viewsets import query_species_name

from frontend.urls import urlpatterns as fe_urlpatterns


urlpatterns = [
    path("lepi-admin/", admin.site.urls),    
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/auth/", include("djoser.urls")),
    url(r"^api/predict", predict_image_view),
    url(r'^api/example_images', get_example_images),
    url(r'^api/query_species', query_species_name)
]

urlpatterns += fe_urlpatterns

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

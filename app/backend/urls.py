from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

from .api_router import router
from uploadforpredict_rest.views import predict_image_view

from upload.views import image_upload
from uploadforpredict.views import image_upload_for_predict


urlpatterns = [
    path("upload", image_upload, name="upload"),
    path("predict/", image_upload_for_predict, name="predict"),
    path("admin/", admin.site.urls),
    path("api/",include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/auth/", include("djoser.urls")),

    url(r"^api/predict", predict_image_view),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include


from upload.views import image_upload
from uploadforpredict.views import image_upload_for_predict

urlpatterns = [
    path("upload", image_upload, name="upload"),
    path("predict/", image_upload_for_predict, name="predict"),
    url(r'^api/', include('uploadforpredict_rest.urls')),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

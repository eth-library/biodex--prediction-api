from django.urls import path
from frontend.views import home_view, about_view
from upload.views import image_upload
from uploadforpredict.views import image_upload_for_predict

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path("upload/", image_upload, name="upload"),
    path("predict/", image_upload_for_predict, name="predict"),
]

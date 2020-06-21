from django.urls import path
from frontend.views import home_view, about_view, contact_view, login_view, logout_view, predict_view
from upload.views import image_upload
from uploadforpredict.views import image_upload_for_predict

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path("upload/", image_upload, name="upload"),
    path("predict/", predict_view, name="predict"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]

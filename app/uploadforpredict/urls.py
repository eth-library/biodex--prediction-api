from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from uploadforpredict.views import predict_image_view


urlpatterns = [
    path(r'predict/', predict_image_view)
]
from django.urls import path
from frontend.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path("predict/", predict_view, name="predict"),
    path('legal-notice/', legal_view, name='legal-notice'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]

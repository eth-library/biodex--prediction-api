from django.urls import path
from frontend.views import home_view, about_view, contact_view, login_view, logout_view, predict_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path("predict/", predict_view, name="predict"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]

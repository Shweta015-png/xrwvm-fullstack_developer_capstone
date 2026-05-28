from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registration, name='register'),
    path('logout', views.logout_request, name='logout'),
    path(route='get_cars', view=views.get_cars, name='getcars'),
]
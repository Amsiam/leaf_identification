from django.urls import path

from . import views

urlpatterns = [
    path('', views.MyApp.as_view(), name='home'),
]
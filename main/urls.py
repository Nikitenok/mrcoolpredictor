from django.urls import path
from . import views
from .applications import simpleexample

urlpatterns = [
    path('', views.index, name="main"),
    path('model', views.model, name="model"),
]
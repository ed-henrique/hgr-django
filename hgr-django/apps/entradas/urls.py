from django.urls import path
from . import views

urlpatterns = [
    path('', views.entradas_view, name='entradas'),
]

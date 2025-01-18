from django.urls import path
from . import views

urlpatterns = [
    path('', views.portas_de_entrada_view, name='portas_de_entrada'),
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.medidas_de_precaucao_view, name='medidas_de_precaucao'),
]


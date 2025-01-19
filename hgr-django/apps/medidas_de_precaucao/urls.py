from django.urls import path
from . import views

urlpatterns = [
    path('', views.medidas_de_precaucao_view, name='medidas_de_precaucao'),
    path('<int:id>/editar', views.editar_medida_de_precaucao_view, name='editar_medida_de_precaucao'),
    path('<int:id>/excluir', views.excluir_medida_de_precaucao_view, name='excluir_medida_de_precaucao'),
]

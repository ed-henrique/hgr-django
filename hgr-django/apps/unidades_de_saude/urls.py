from django.urls import path
from . import views

urlpatterns = [
    path('', views.unidades_de_saude_view, name='unidades_de_saude'),
    path('<int:id>/editar', views.editar_unidade_de_saude_view, name='editar_unidade_de_saude'),
    path('<int:id>/excluir', views.excluir_unidade_de_saude_view, name='excluir_unidade_de_saude'),
]



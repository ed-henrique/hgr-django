from django.urls import path
from . import views

urlpatterns = [
    path('', views.tipos_de_saida_view, name='tipos_de_saida'),
    path('<int:id>/editar', views.editar_tipo_de_saida_view, name='editar_tipo_de_saida'),
    path('<int:id>/excluir', views.excluir_tipo_de_saida_view, name='excluir_tipo_de_saida'),
]



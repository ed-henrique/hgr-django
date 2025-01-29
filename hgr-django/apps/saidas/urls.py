from django.urls import path
from . import views

urlpatterns = [
    path('', views.saidas_view, name='saidas'),
    path('<int:id>', views.saida_view, name='saida'),
    path('<int:id>/editar', views.editar_saida_view,
         name='editar_saida'),
    path('<int:id>/excluir', views.excluir_saida_view,
         name='excluir_saida'),
]

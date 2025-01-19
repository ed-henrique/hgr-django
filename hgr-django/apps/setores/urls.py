from django.urls import path
from . import views

urlpatterns = [
    path('', views.setores_view, name='setores'),
    path('<int:id>/editar', views.editar_setor_view, name='editar_setor'),
    path('<int:id>/excluir', views.excluir_setor_view, name='excluir_setor'),
]


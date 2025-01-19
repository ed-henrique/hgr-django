from django.urls import path
from . import views

urlpatterns = [
    path('', views.especialidades_view, name='especialidades'),
    path('<int:id>/editar', views.editar_especialidade_view, name='editar_especialidade'),
    path('<int:id>/excluir', views.excluir_especialidade_view, name='excluir_especialidade'),
]

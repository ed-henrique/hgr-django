from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacientes_view, name='pacientes'),
    path('criar', views.criar_paciente_view, name='criar_paciente'),
    path('<int:id>', views.paciente_view, name='paciente'),
    path('<int:id>/editar', views.editar_paciente_view, name='editar_paciente'),
    path('<int:id>/excluir', views.excluir_paciente_view, name='excluir_paciente'),
]

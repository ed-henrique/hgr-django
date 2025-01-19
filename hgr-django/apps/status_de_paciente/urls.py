from django.urls import path
from . import views

urlpatterns = [
    path('', views.status_de_paciente_view, name='status_de_paciente'),
    path('<int:id>/editar', views.editar_status_de_paciente_view, name='editar_status_de_paciente'),
    path('<int:id>/excluir', views.excluir_status_de_paciente_view, name='excluir_status_de_paciente'),
]


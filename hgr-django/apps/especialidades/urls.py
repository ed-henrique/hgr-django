from django.urls import path
from . import views

urlpatterns = [
    path('', views.especialidades_view, name='especialidades'),
    path('<int:id>', views.editar_especialidade_view, name='editar_especialidade'),
]

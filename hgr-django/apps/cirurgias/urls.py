from django.urls import path
from . import views

urlpatterns = [
    path('', views.cirurgias_view, name='cirurgias'),
    path('<int:id>', views.cirurgia_view, name='cirurgia'),
    path('<int:id>/editar', views.editar_cirurgia_view, name='editar_cirurgia'),
    path('<int:id>/excluir', views.excluir_cirurgia_view, name='excluir_cirurgia'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.nacionalidades_etnias_view, name='nacionalidades_etnias'),
    path('<int:id>/editar', views.editar_nacionalidade_etnia_view, name='editar_nacionalidade_etnia'),
    path('<int:id>/excluir', views.excluir_nacionalidade_etnia_view, name='excluir_nacionalidade_etnia'),
]

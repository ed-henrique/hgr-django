from django.urls import path
from . import views

urlpatterns = [
    path('', views.leitos_view, name='leitos'),
    path('<int:id>', views.leito_view, name='leito'),
    path('<int:id>/editar', views.editar_leito_view, name='editar_leito'),
    path('<int:id>/excluir', views.excluir_leito_view, name='excluir_leito'),
]


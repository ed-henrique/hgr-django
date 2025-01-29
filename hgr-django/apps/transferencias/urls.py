from django.urls import path
from . import views

urlpatterns = [
    path('', views.transferencias_view, name='transferencias'),
    path('<int:id>', views.transferencia_view, name='transferencia'),
    path('<int:id>/editar', views.editar_transferencia_view,
         name='editar_transferencia'),
    path('<int:id>/excluir', views.excluir_transferencia_view,
         name='excluir_transferencia'),
]

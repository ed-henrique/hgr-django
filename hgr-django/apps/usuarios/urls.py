from django.urls import path
from . import views

urlpatterns = [
    path("", views.usuarios_view, name="usuarios"),
    path(
        "<int:id>/elevar-autoridade",
        views.elevar_autoridade_usuario_view,
        name="elevar_autoridade_usuario",
    ),
    path(
        "<int:id>/remover-autoridade",
        views.remover_autoridade_usuario_view,
        name="remover_autoridade_usuario",
    ),
    path(
        "<int:id>/desbloquear",
        views.desbloquear_usuario_view,
        name="desbloquear_usuario",
    ),
    path("<int:id>/excluir", views.excluir_usuario_view, name="excluir_usuario"),
    path("<int:id>/bloquear", views.bloquear_usuario_view, name="bloquear_usuario"),
]

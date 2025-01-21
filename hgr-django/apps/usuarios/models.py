from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.tipos_de_usuario.models import TipoDeUsuario
from apps.status_de_usuario.models import StatusDeUsuario


class Usuario(AbstractUser):
    tipo_de_usuario = models.ForeignKey(
        TipoDeUsuario,
        default=1,
        related_name="tipo_de_usuario",
        on_delete=models.PROTECT,
        verbose_name="Tipo de Usuário",
    )
    status_de_usuario = models.ForeignKey(
        StatusDeUsuario,
        default=3,
        related_name="status_de_usuario",
        on_delete=models.PROTECT,
        verbose_name="Status de Usuário",
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.tipos_de_usuario.models import TipoDeUsuario
from apps.status_de_usuario.models import StatusDeUsuario


class Usuario(AbstractUser):
    tipo_de_usuario = models.ForeignKey(
        TipoDeUsuario,
        default=3,
        related_name="tipo_de_usuario",
        on_delete=models.PROTECT,
        verbose_name="Tipo de Usuário",
    )
    status_de_usuario = models.ForeignKey(
        StatusDeUsuario,
        default=1,
        related_name="status_de_usuario",
        on_delete=models.PROTECT,
        verbose_name="Status de Usuário",
    )

    def get_participacao(self):
        from apps.pacientes.models import Paciente

        total = Paciente.objects.filter(removido_em__isnull=True).count()
        partial = Paciente.objects.filter(
            removido_em__isnull=True, responsavel=self
        ).count()

        if total == 0:
            return 0

        return (partial / total) * 100

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

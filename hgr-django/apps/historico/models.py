from django.db import models
from django.utils.timezone import now
from apps.usuarios.models import Usuario


class Historico(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, verbose_name="Usuário")
    data = models.DateField(verbose_name="Data", default=now)
    hora = models.TimeField(verbose_name="Hora", default=now)
    descricao = models.TextField(max_length=132, verbose_name="Descrição")

    class Meta:
        verbose_name = 'Histórico'
        verbose_name_plural = 'Históricos'

        indexes = [
            models.Index(fields=['usuario']),
            models.Index(fields=['data']),
        ]

from django.db import models

from apps.pacientes.models import Paciente
from apps.leitos.models import Leito


class Transferencia(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, verbose_name="Paciente")
    leito_de_origem = models.ForeignKey(
        Leito, on_delete=models.PROTECT, verbose_name="Leito de Origem", related_name='leito_de_origem')
    leito_de_destino = models.ForeignKey(
        Leito, on_delete=models.PROTECT, verbose_name="Leito de Destino", related_name='leito_de_destino')
    data = models.DateField(verbose_name="Data")
    hora = models.TimeField(verbose_name="Hora")
    removido_em = models.DateTimeField(null=True, verbose_name="Removido em")

    class Meta:
        verbose_name = 'Transferência'
        verbose_name_plural = 'Transferências'

        indexes = [
            models.Index(fields=['removido_em']),
            models.Index(fields=['data', 'removido_em']),
            models.Index(fields=['paciente', 'removido_em']),
        ]

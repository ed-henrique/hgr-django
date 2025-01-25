from django.db import models
from django.utils.timezone import now
from apps.leitos.models import Leito
from apps.pacientes.models import Paciente


class HistoricoDeOcupacaoDeLeito(models.Model):
    leito = models.ForeignKey(
        Leito, on_delete=models.PROTECT, verbose_name="Leito", related_name="historico_de_ocupacao_de_leito")
    paciente = models.ForeignKey(
        Paciente, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Paciente")
    ocorrido_em = models.DateTimeField(verbose_name="Ocorrido em", default=now)

    class Meta:
        verbose_name = 'Histórico de Ocupação de Leito'
        verbose_name_plural = 'Históricos de Ocupação de Leito'

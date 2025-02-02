from django.db import models

from apps.pacientes.models import Paciente
from apps.leitos.models import Leito
from apps.unidades_de_saude.models import UnidadeDeSaude
from apps.tipos_de_saida.models import TipoDeSaida


class Saida(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, verbose_name="Paciente"
    )
    leito_de_origem = models.ForeignKey(
        Leito, on_delete=models.PROTECT, verbose_name="Leito de Origem"
    )
    unidade_de_saude_de_destino = models.ForeignKey(
        UnidadeDeSaude,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Unidade de Saúde de Destino",
    )
    tipo_de_saida = models.ForeignKey(
        TipoDeSaida, on_delete=models.PROTECT, verbose_name="Tipo de Saída"
    )
    data = models.DateTimeField(verbose_name="Data")
    removido_em = models.DateTimeField(
        null=True, blank=True, verbose_name="Removido em"
    )

    class Meta:
        verbose_name = "Saída"
        verbose_name_plural = "Saídas"

        indexes = [
            models.Index(fields=["removido_em"]),
            models.Index(fields=["data", "removido_em"]),
            models.Index(fields=["paciente", "removido_em"]),
        ]

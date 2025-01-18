from django.db import models

from apps.pacientes.models import Paciente
from apps.leitos.models import Leito
from apps.unidades_de_saude.models import UnidadeDeSaude

class Entrada(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente")
    unidade_de_saude_de_origem = models.ForeignKey(UnidadeDeSaude, null=True, on_delete=models.PROTECT, verbose_name="Unidade de Saúde de Origem")
    leito_de_destino = models.ForeignKey(Leito, on_delete=models.PROTECT, verbose_name="Leito de Destino")
    data = models.DateField(verbose_name="Data")
    hora = models.TimeField(verbose_name="Hora")
    removido_em = models.DateTimeField(null=True, verbose_name="Removido em")

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

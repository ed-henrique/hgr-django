from django.db import models

from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.status_de_leito.models import StatusDeLeito
from apps.tipos_de_leito.models import TipoDeLeito
from apps.tipos_de_o2.models import TipoDeO2
from apps.tipos_de_vacuo.models import TipoDeVacuo

class Leito(models.Model):
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name="Setor")
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, verbose_name="Especialidade")
    status_de_leito = models.ForeignKey(StatusDeLeito, on_delete=models.PROTECT, verbose_name="Status de Leito")
    tipo_de_leito = models.ForeignKey(TipoDeLeito, on_delete=models.PROTECT, verbose_name="Tipo de Leito")
    tipo_de_o2 = models.ForeignKey(TipoDeO2, on_delete=models.PROTECT, verbose_name="Tipo de O2")
    tipo_de_vacuo = models.ForeignKey(TipoDeVacuo, on_delete=models.PROTECT, verbose_name="Tipo de Vácuo")
    codigo_sus = models.TextField(null=True, verbose_name="Código SUS")
    tem_o2 = models.BooleanField(default=False, verbose_name="Tem O2")
    tem_vacuo = models.BooleanField(default=False, verbose_name="Tem Vácuo")
    tem_codigo_sus = models.BooleanField(default=False, verbose_name="Tem Código SUS")
    removido_em = models.DateTimeField(null=True, verbose_name="Removido em")

    class Meta:
        verbose_name = 'Leito'
        verbose_name_plural = 'Leitos'

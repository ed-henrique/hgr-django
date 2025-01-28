from django.db import models

from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.status_de_leito.models import StatusDeLeito
from apps.tipos_de_leito.models import TipoDeLeito
from apps.tipos_de_o2.models import TipoDeO2
from apps.tipos_de_vacuo.models import TipoDeVacuo


class Leito(models.Model):
    setor = models.ForeignKey(
        Setor, on_delete=models.PROTECT, verbose_name="Setor")
    especialidade = models.ForeignKey(
        Especialidade, on_delete=models.PROTECT, verbose_name="Especialidade")
    paciente = models.ForeignKey(
        'pacientes.Paciente', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Paciente", related_name="leito_paciente")
    status_de_leito = models.ForeignKey(
        StatusDeLeito, on_delete=models.PROTECT, verbose_name="Status de Leito")
    tipo_de_leito = models.ForeignKey(
        TipoDeLeito, on_delete=models.PROTECT, verbose_name="Tipo de Leito")
    tipo_de_o2 = models.ForeignKey(
        TipoDeO2, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Tipo de O2")
    tipo_de_vacuo = models.ForeignKey(
        TipoDeVacuo, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Tipo de Vácuo")
    codigo_sus = models.TextField(
        null=True, blank=True, verbose_name="Código SUS")
    tem_o2 = models.BooleanField(default=False, verbose_name="Tem O2")
    tem_vacuo = models.BooleanField(default=False, verbose_name="Tem Vácuo")
    tem_codigo_sus = models.BooleanField(
        default=False, verbose_name="Tem Código SUS")
    removido_em = models.DateTimeField(
        null=True, blank=True, verbose_name="Removido em")

    @property
    def historico_de_ocupacao(self):
        return self.historico_de_ocupacao_de_leito.all()

    def __str__(self):
        return f"{self.id} - Setor: {self.setor.nome} - Especialidade: {self.especialidade.nome}{f' - Código SUS: {self.codigo_sus}' if self.tem_codigo_sus else ''}{f' - Vácuo: {self.tipo_de_vacuo.nome}' if self.tem_vacuo else ''}{f' - O2: {self.tipo_de_o2.nome}' if self.tem_o2 else ''}"

    class Meta:
        verbose_name = 'Leito'
        verbose_name_plural = 'Leitos'

        indexes = [
            models.Index(fields=['removido_em']),
        ]

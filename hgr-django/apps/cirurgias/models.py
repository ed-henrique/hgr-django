from django.db import models

from apps.pacientes.models import Paciente
from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.tipos_de_cirurgia.models import TipoDeCirurgia

class Cirurgia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente")
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name="Setor")
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, verbose_name="Especialidade")
    tipo_de_cirurgia = models.ForeignKey(TipoDeCirurgia, on_delete=models.PROTECT, verbose_name="Tipo de Cirurgia")
    concluida_com_sucesso = models.BooleanField(default=False, verbose_name="Concluída com Sucesso")
    data = models.DateField(verbose_name="Data")
    hora = models.TimeField(verbose_name="Hora")
    removido_em = models.DateTimeField(null=True, verbose_name="Removido em")

    class Meta:
        verbose_name = 'Cirurgia'
        verbose_name_plural = 'Cirurgias'

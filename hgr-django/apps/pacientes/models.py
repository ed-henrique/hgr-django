from django.db import models

from apps.generos.models import Genero
from apps.usuarios.models import Usuario
from apps.unidades_de_saude.models import UnidadeDeSaude
from apps.medidas_de_precaucao.models import MedidaDePrecaucao
from apps.portas_de_entrada.models import PortaDeEntrada
from apps.especialidades.models import Especialidade
from apps.status_de_paciente.models import StatusDePaciente
from apps.nacionalidades_etnias.models import NacionalidadeEtnia
from apps.tipos_de_cirurgia.models import TipoDeCirurgia
from apps.tipos_de_o2.models import TipoDeO2
from apps.tipos_de_vacuo.models import TipoDeVacuo


class Paciente(models.Model):
    nome = models.CharField(max_length=128, verbose_name="Nome")
    nome_social = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="Nome Social"
    )
    data_de_nascimento = models.DateField(
        null=True, blank=True, verbose_name="Data de Nascimento")
    data_de_internacao = models.DateField(verbose_name="Data de Internação")
    hora_de_internacao = models.TimeField(verbose_name="Hora de Internação")
    data_de_internacao_no_setor = models.DateField(
        verbose_name="Data de Internação no Setor"
    )
    hora_de_internacao_no_setor = models.TimeField(
        verbose_name="Hora de Internação no Setor"
    )
    sexo = models.CharField(
        max_length=1,
        choices=[("M", "Masculino"), ("F", "Feminino")],
        verbose_name="Sexo",
    )
    diagnostico = models.TextField(max_length=2048, verbose_name="Diagnóstico")
    justificativas_pendencias = models.TextField(
        max_length=2048, verbose_name="Justificativas de Pendências"
    )
    problemas_durante_transferencias = models.TextField(
        max_length=2048, null=True, blank=True, verbose_name="Problemas Durante Transferências"
    )
    genero = models.ForeignKey(
        Genero, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Gênero"
    )
    leito = models.ForeignKey(
        'leitos.Leito', on_delete=models.PROTECT, verbose_name="Leito", related_name="paciente_leito")
    responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        verbose_name="Profissional de Saúde Responsável",
    )
    unidade_de_saude_de_origem = models.ForeignKey(
        UnidadeDeSaude,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name="Unidade de Saúde de Origem",
    )
    medida_de_precaucao = models.ForeignKey(
        MedidaDePrecaucao, on_delete=models.PROTECT, verbose_name="Medida de Precaução"
    )
    porta_de_entrada = models.ForeignKey(
        PortaDeEntrada, on_delete=models.PROTECT, verbose_name="Porta de Entrada"
    )
    especialidade = models.ForeignKey(
        Especialidade, on_delete=models.PROTECT, verbose_name="Especialidade"
    )
    status_de_paciente = models.ForeignKey(
        StatusDePaciente, on_delete=models.PROTECT, verbose_name="Status do Paciente"
    )
    nacionalidade_etnia = models.ForeignKey(
        NacionalidadeEtnia, on_delete=models.PROTECT, verbose_name="Nacionalidade/Etnia"
    )
    gestante = models.BooleanField(default=False, verbose_name="Gestante")
    veio_de_ambulancia = models.BooleanField(
        default=False, verbose_name="Veio de Ambulância"
    )
    precisa_de_cirurgia = models.BooleanField(
        default=False, verbose_name="Precisa de Cirurgia"
    )
    tipo_de_cirurgia = models.ForeignKey(
        TipoDeCirurgia,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name="Tipo de Cirurgia",
    )
    precisa_de_o2 = models.BooleanField(
        default=False, verbose_name="Precisa de O2")
    tipo_de_o2 = models.ForeignKey(
        TipoDeO2, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de O2"
    )
    precisa_de_vacuo = models.BooleanField(
        default=False, verbose_name="Precisa de Vácuo"
    )
    tipo_de_vacuo = models.ForeignKey(
        TipoDeVacuo, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Tipo de Vácuo"
    )
    removido_em = models.DateTimeField(
        null=True, blank=True, verbose_name="Removido em")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

        indexes = [
            models.Index(fields=['removido_em']),
            models.Index(fields=['data_de_internacao', 'removido_em']),
        ]

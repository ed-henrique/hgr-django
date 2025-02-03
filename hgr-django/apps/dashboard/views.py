from django import forms
from django.utils.timezone import now
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.usuarios.models import Usuario
from apps.leitos.models import Leito
from apps.entradas.models import Entrada
from apps.cirurgias.models import Cirurgia
from apps.transferencias.models import Transferencia
from apps.saidas.models import Saida
from apps.status_de_paciente.models import StatusDePaciente
from apps.status_de_leito.models import StatusDeLeito
from apps.tipos_de_leito.models import TipoDeLeito
from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.pacientes.models import Paciente
from datetime import date


def filter_by_setor(queryset, setor, setor_field_name="setor"):
    """
    Conditionally filters a queryset by setor if setor is not None.
    :param queryset: The queryset to filter.
    :param setor: The setor object or None.
    :param setor_field_name: The name of the setor field in the queryset (default is "setor").
    :return: Filtered queryset.
    """
    if setor:
        return queryset.filter(**{f"{setor_field_name}": setor})
    return queryset


def filter_by_especialidade(queryset, especialidade, especialidade_field_name="especialidade"):
    """
    Conditionally filters a queryset by especialidade if especialidade is not None.
    :param queryset: The queryset to filter.
    :param setor: The setor object or None.
    :param setor_field_name: The name of the especialidade field in the queryset (default is "especialidade").
    :return: Filtered queryset.
    """
    if especialidade:
        return queryset.filter(**{f"{especialidade_field_name}": especialidade})
    return queryset


def json_date_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("Type not serializable")


class DashboardFilterForm(forms.Form):
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.filter(removido_em__isnull=True),
        required=False,
        label="Setor",
        widget=forms.Select(attrs={"class": "form-select mr-sm-2"}),
        empty_label="",
    )
    especialidade = forms.ModelChoiceField(
        queryset=Especialidade.objects.filter(removido_em__isnull=True),
        required=False,
        label="Especialidade",
        widget=forms.Select(attrs={"class": "form-select"}),
        empty_label="",
    )
    inicio_periodo = forms.DateField(
        required=False,
        label="Início do Período",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}),
    )
    fim_periodo = forms.DateField(
        required=False,
        label="Fim do Período",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}),
    )


@login_required
def dashboard_view(request):
    inicio_do_periodo = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    fim_do_periodo = now().replace(hour=23, minute=59, second=59, microsecond=999999)
    periodo = [inicio_do_periodo, fim_do_periodo]
    especialidade = None
    setor = None

    form = DashboardFilterForm(request.GET or None)

    context = {
        "form": form,
        "title": "Dashboard",
    }

    if form.is_valid():
        form_setor = form.cleaned_data["setor"]
        form_especialidade = form.cleaned_data["especialidade"]
        form_inicio_do_periodo = form.cleaned_data["inicio_periodo"]
        form_fim_do_periodo = form.cleaned_data["fim_periodo"]

        if form_setor:
            setor = form_setor
            context["setor"] = setor

        if form_especialidade:
            especialidade = form_especialidade
            context["especialidade"] = especialidade

        if inicio_do_periodo and fim_do_periodo:
            inicio_do_periodo = form_inicio_do_periodo
            fim_do_periodo = form_fim_do_periodo
            context["inicio_periodo"] = inicio_do_periodo
            context["fim_periodo"] = fim_do_periodo

    # Data Aggregation
    enfermeiros = Usuario.objects.filter(
        status_de_usuario__nome="Ativo").count()
    leitos = Leito.objects.filter(removido_em__isnull=True)

    pacientes = (
        Paciente.objects.filter(removido_em__isnull=True).exclude(
            saida__isnull=False)
    )

    leitos_ocupados = (
        Leito.objects.filter(removido_em__isnull=True,
                             paciente__isnull=False)
    ).count()

    leitos_livres = (
        Leito.objects.filter(removido_em__isnull=True,
                             paciente__isnull=True)
    ).count()

    status_de_paciente = (
        StatusDePaciente.objects.filter(removido_em__isnull=True).annotate(
            paciente_count=Count(
                "paciente",
                filter=Q(paciente__removido_em__isnull=True) & Q(
                    paciente__saida__isnull=True)
            )
        )
        .order_by("nome")
    )

    status_de_leito = (
        StatusDeLeito.objects.filter(removido_em__isnull=True).annotate(
            leito_count=Count("leito", filter=Q(
                leito__removido_em__isnull=True))
        )
        .order_by("nome")
    )

    tipos_de_leito = (
        TipoDeLeito.objects.filter(removido_em__isnull=True).annotate(
            leito_count=Count("leito", filter=Q(
                leito__removido_em__isnull=True))
        )
        .order_by("nome")
    )

    ultimas_entradas = filter_by_especialidade(
        filter_by_setor(
            Entrada.objects.filter(
                removido_em__isnull=True), setor, "leito_de_destino__setor"
        ), especialidade, "leito_de_destino__especialidade"
    ).order_by("-data")[:5]

    ultimas_transferencias = filter_by_especialidade(
        filter_by_setor(
            Transferencia.objects.filter(
                removido_em__isnull=True), setor, "leito_de_destino__setor"
        ), especialidade, "leito_de_destino__especialidade"
    ).order_by("-data")[:5]

    ultimas_saidas = filter_by_especialidade(
        filter_by_setor(
            Saida.objects.filter(
                removido_em__isnull=True), setor, "leito_de_origem__setor"
        ), especialidade, "leito_de_origem__especialidade"
    ).order_by("-data")[:5]

    entradas_por_dia = list(
        filter_by_especialidade(
            filter_by_setor(
                Entrada.objects.filter(
                    removido_em__isnull=True,
                    data__range=periodo,
                ),
                setor,
                "leito_de_destino__setor",
            ),
            especialidade,
            "leito_de_destino__especialidade",
        )
        .annotate(dia=TruncDate("data"))
        .values("dia", "leito_de_destino__setor__cor", "leito_de_destino__setor__nome")
        .annotate(total=Count("id"))
        .order_by("dia", "leito_de_destino__setor__nome")
    )

    cirurgias_por_dia = list(
        filter_by_especialidade(
            filter_by_setor(
                Cirurgia.objects.filter(
                    removido_em__isnull=True,
                    data__range=periodo,
                ),
                setor,
                "setor",
            ),
            especialidade,
            "especialidade",
        )
        .annotate(dia=TruncDate("data"))
        .values("dia", "setor__cor", "setor__nome")
        .annotate(total=Count("id"))
        .order_by("dia", "setor__nome")
    )

    context.update({
        "enfermeiros": enfermeiros,
        "pacientes": pacientes,
        "leitos": leitos,
        "leitos_ocupados": leitos_ocupados,
        "leitos_livres": leitos_livres,
        "status_de_leito": status_de_leito,
        "tipos_de_leito": tipos_de_leito,
        "status_de_paciente": status_de_paciente,
        "ultimas_entradas": ultimas_entradas,
        "ultimas_transferencias": ultimas_transferencias,
        "ultimas_saidas": ultimas_saidas,
        "entradas_por_dia": entradas_por_dia,
        "cirurgias_por_dia": cirurgias_por_dia,
    })

    return render(request, "dashboard/index.html", context)

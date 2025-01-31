from django import forms
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.usuarios.models import Usuario
from apps.leitos.models import Leito
from apps.status_de_paciente.models import StatusDePaciente
from apps.status_de_leito.models import StatusDeLeito
from apps.tipos_de_leito.models import TipoDeLeito
from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.pacientes.models import Paciente


class DashboardFilterForm(forms.Form):
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.filter(removido_em__isnull=True),
        required=False,
        label="Setor",
        widget=forms.Select(attrs={'class': 'form-select mr-sm-2'}),
        empty_label="",
    )
    especialidade = forms.ModelChoiceField(
        queryset=Especialidade.objects.filter(removido_em__isnull=True),
        required=False,
        label="Especialidade",
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="",
    )
    inicio_periodo = forms.DateField(
        required=False,
        label="Início do Período",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    fim_periodo = forms.DateField(
        required=False,
        label="Fim do Período",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


@login_required
def dashboard_view(request):
    form = DashboardFilterForm(request.GET or None)

    # Data Aggregation
    enfermeiros = Usuario.objects.filter(
        status_de_usuario__nome="Ativo").count()
    leitos = Leito.objects.filter(removido_em__isnull=True)
    pacientes = Paciente.objects.filter(removido_em__isnull=True).exclude(
        saida__isnull=False)

    status_de_paciente = StatusDePaciente.objects.filter(removido_em__isnull=True).annotate(
        paciente_count=Count('paciente', filter=Q(
            paciente__removido_em__isnull=True) & Q(paciente__saida__isnull=True))
    ).order_by('nome')
    status_de_leito = StatusDeLeito.objects.filter(removido_em__isnull=True).annotate(
        leito_count=Count('leito', filter=Q(leito__removido_em__isnull=True))
    ).order_by('nome')
    tipos_de_leito = TipoDeLeito.objects.filter(removido_em__isnull=True).annotate(
        leito_count=Count('leito', filter=Q(leito__removido_em__isnull=True))
    ).order_by('nome')

    if form.is_valid():
        setor = form.cleaned_data["setor"]
        especialidade = form.cleaned_data["especialidade"]
        inicio_periodo = form.cleaned_data["inicio_periodo"]
        fim_periodo = form.cleaned_data["fim_periodo"]

    context = {
        'form': form,
        'setor': setor,
        'especialidade': especialidade,
        'inicio_periodo': inicio_periodo,
        'fim_periodo': fim_periodo,
        'title': 'Dashboard',
        'enfermeiros': enfermeiros,
        'pacientes': pacientes,
        'leitos': leitos,
        'status_de_leito': status_de_leito,
        'tipos_de_leito': tipos_de_leito,
        'status_de_paciente': status_de_paciente,
    }

    return render(request, 'dashboard/index.html', context)

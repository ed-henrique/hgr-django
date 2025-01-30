from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import StatusDePaciente
from apps.historico.models import Historico


class StatusDePacienteForm(forms.ModelForm):
    class Meta:
        model = StatusDePaciente
        fields = ['nome', 'cor']
        error_messages = {
            'nome': {
                'unique': 'O nome informado já está cadastrado. Por favor, escolha outro.',
            },
            'cor': {
                'unique': 'A cor informada já está em uso. Escolha uma cor diferente.',
            },
        }


@login_required
@transaction.atomic
def status_de_paciente_view(request):
    if request.method == 'POST':
        form = StatusDePacienteForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user, descricao=f"Criou o Status de Paciente '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")
    else:
        form = StatusDePacienteForm()

    query = request.GET.get('q', '')
    if query:
        objs = StatusDePaciente.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True).order_by('nome')
    else:
        objs = StatusDePaciente.objects.filter(
            removido_em__isnull=True).order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/status-de-paciente/",
        'title': 'Gestão de ' + StatusDePaciente._meta.verbose_name_plural,
        'titulo': StatusDePaciente._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + StatusDePaciente._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'status_de_paciente/index.html', context)


@login_required
@transaction.atomic
def editar_status_de_paciente_view(request, id):
    obj = get_object_or_404(StatusDePaciente, id=id)

    if request.method == 'POST':
        form = StatusDePacienteForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user, descricao=f"Editou o Status de Paciente '{form.initial['nome']}' de cor '{form.initial['cor']}' para o Status de Paciente '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")

            return redirect("/gestao/status-de-paciente")
    else:
        form = StatusDePacienteForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/status-de-paciente/",
        'title': 'Gestão de ' + StatusDePaciente._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + StatusDePaciente._meta.verbose_name,
    }

    return render(request, 'status_de_paciente/editar.html', context)


@login_required
@transaction.atomic
def excluir_status_de_paciente_view(request, id):
    obj = get_object_or_404(StatusDePaciente, id=id)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user, descricao=f"""Removeu o Status de Paciente <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {obj.cor};">{obj.nome}</span>.""")

        return redirect("/gestao/status-de-paciente")

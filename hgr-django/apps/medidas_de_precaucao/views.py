from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import MedidaDePrecaucao
from apps.historico.models import Historico


class MedidaDePrecaucaoForm(forms.ModelForm):
    class Meta:
        model = MedidaDePrecaucao
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
def medidas_de_precaucao_view(request):
    if request.method == 'POST':
        form = MedidaDePrecaucaoForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user, descricao=f"Criou a Medida de Precaução '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")
    else:
        form = MedidaDePrecaucaoForm()

    query = request.GET.get('q', '')
    if query:
        objs = MedidaDePrecaucao.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True).order_by('nome')
    else:
        objs = MedidaDePrecaucao.objects.filter(
            removido_em__isnull=True).order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/medidas-de-precaucao/",
        'title': 'Gestão de ' + MedidaDePrecaucao._meta.verbose_name_plural,
        'titulo': MedidaDePrecaucao._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + MedidaDePrecaucao._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'medidas_de_precaucao/index.html', context)


@login_required
@transaction.atomic
def editar_medida_de_precaucao_view(request, id):
    obj = get_object_or_404(MedidaDePrecaucao, id=id)

    if request.method == 'POST':
        form = MedidaDePrecaucaoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user, descricao=f"Editou a Medida de Precaução '{form.initial['nome']}' de cor '{form.initial['cor']}' para a Medida de Precaução '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")

            return redirect("/gestao/medidas-de-precaucao")
    else:
        form = MedidaDePrecaucaoForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/medidas-de-precaucao/",
        'title': 'Gestão de ' + MedidaDePrecaucao._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + MedidaDePrecaucao._meta.verbose_name,
    }

    return render(request, 'medidas_de_precaucao/editar.html', context)


@login_required
@transaction.atomic
def excluir_medida_de_precaucao_view(request, id):
    obj = get_object_or_404(MedidaDePrecaucao, id=id)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user, descricao=f"Removeu a Medida de Precaução '{obj.nome}' de cor '{obj.cor}'.")

        return redirect("/gestao/medidas-de-precaucao")

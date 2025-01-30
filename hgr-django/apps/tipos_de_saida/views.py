from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import TipoDeSaida
from apps.historico.models import Historico


class TipoDeSaidaForm(forms.ModelForm):
    class Meta:
        model = TipoDeSaida
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
def tipos_de_saida_view(request):
    if request.method == 'POST':
        form = TipoDeSaidaForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user, descricao=f"Criou o Tipo de Saída '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")
    else:
        form = TipoDeSaidaForm()

    query = request.GET.get('q', '')
    if query:
        objs = TipoDeSaida.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True).order_by('nome')
    else:
        objs = TipoDeSaida.objects.filter(
            removido_em__isnull=True).order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/tipos-de-saida/",
        'title': 'Gestão de ' + TipoDeSaida._meta.verbose_name_plural,
        'titulo': TipoDeSaida._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + TipoDeSaida._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'tipos_de_saida/index.html', context)


@login_required
@transaction.atomic
def editar_tipo_de_saida_view(request, id):
    obj = get_object_or_404(TipoDeSaida, id=id)

    if request.method == 'POST':
        form = TipoDeSaidaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user, descricao=f"Editou o Tipo de Saída '{form.initial['nome']}' de cor '{form.initial['cor']}' para o Tipo de Saída '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")

            return redirect("/gestao/tipos-de-saida")
    else:
        form = TipoDeSaidaForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/tipos-de-saida/",
        'title': 'Gestão de ' + TipoDeSaida._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + TipoDeSaida._meta.verbose_name,
    }

    return render(request, 'tipos_de_saida/editar.html', context)


@login_required
@transaction.atomic
def excluir_tipo_de_saida_view(request, id):
    obj = get_object_or_404(TipoDeSaida, id=id)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user, descricao=f"""Removeu o Tipo de Saída <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {obj.cor};">{obj.nome}</span>.""")

        return redirect("/gestao/tipos-de-saida")

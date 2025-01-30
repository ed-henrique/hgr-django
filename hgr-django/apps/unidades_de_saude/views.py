from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import UnidadeDeSaude
from apps.historico.models import Historico


class UnidadeDeSaudeForm(forms.ModelForm):
    class Meta:
        model = UnidadeDeSaude
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
def unidades_de_saude_view(request):
    if request.method == 'POST':
        form = UnidadeDeSaudeForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user, descricao=f"Criou a Unidade De Saúde '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")
    else:
        form = UnidadeDeSaudeForm()

    query = request.GET.get('q', '')
    if query:
        objs = UnidadeDeSaude.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True).order_by('nome')
    else:
        objs = UnidadeDeSaude.objects.filter(
            removido_em__isnull=True).order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/unidades-de-saude/",
        'title': 'Gestão de ' + UnidadeDeSaude._meta.verbose_name_plural,
        'titulo': UnidadeDeSaude._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + UnidadeDeSaude._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'unidades_de_saude/index.html', context)


@login_required
@transaction.atomic
def editar_unidade_de_saude_view(request, id):
    obj = get_object_or_404(UnidadeDeSaude, id=id)

    if request.method == 'POST':
        form = UnidadeDeSaudeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user, descricao=f"Editou a Unidade De Saúde '{form.initial['nome']}' de cor '{form.initial['cor']}' para a Unidade De Saúde '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")

            return redirect("/gestao/unidades_de_saude")
    else:
        form = UnidadeDeSaudeForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/unidades-de-saude/",
        'title': 'Gestão de ' + UnidadeDeSaude._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + UnidadeDeSaude._meta.verbose_name,
    }

    return render(request, 'unidades_de_saude/editar.html', context)


@login_required
@transaction.atomic
def excluir_unidade_de_saude_view(request, id):
    obj = get_object_or_404(UnidadeDeSaude, id=id)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user, descricao=f"Removeu a Unidade De Saúde '{obj.nome}' de cor '{obj.cor}'.")

        return redirect("/gestao/unidades_de_saude")

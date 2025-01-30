from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import NacionalidadeEtnia
from apps.historico.models import Historico


class NacionalidadeEtniaForm(forms.ModelForm):
    class Meta:
        model = NacionalidadeEtnia
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
def nacionalidades_etnias_view(request):
    if request.method == 'POST':
        form = NacionalidadeEtniaForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user, descricao=f"Criou a Nacionalidade/Etnia '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")
    else:
        form = NacionalidadeEtniaForm()

    query = request.GET.get('q', '')
    if query:
        objs = NacionalidadeEtnia.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True).order_by('nome')
    else:
        objs = NacionalidadeEtnia.objects.filter(
            removido_em__isnull=True).order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/nacionalidades-etnias/",
        'title': 'Gestão de ' + NacionalidadeEtnia._meta.verbose_name_plural,
        'titulo': NacionalidadeEtnia._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + NacionalidadeEtnia._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'nacionalidades_etnias/index.html', context)


@login_required
@transaction.atomic
def editar_nacionalidade_etnia_view(request, id):
    obj = get_object_or_404(NacionalidadeEtnia, id=id)

    if request.method == 'POST':
        form = NacionalidadeEtniaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user, descricao=f"Editou a Nacionalidade/Etnia '{form.initial['nome']}' de cor '{form.initial['cor']}' para a Nacionalidade/Etnia '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")

            return redirect("/gestao/nacionalidades-etnias")
    else:
        form = NacionalidadeEtniaForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/nacionalidades-etnias/",
        'title': 'Gestão de ' + NacionalidadeEtnia._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + NacionalidadeEtnia._meta.verbose_name,
    }

    return render(request, 'nacionalidades_etnias/editar.html', context)


@login_required
@transaction.atomic
def excluir_nacionalidade_etnia_view(request, id):
    obj = get_object_or_404(NacionalidadeEtnia, id=id)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user, descricao=f"Removeu a Nacionalidade/Etnia '{obj.nome}' de cor '{obj.cor}'.")

        return redirect("/gestao/nacionalidades-etnias")

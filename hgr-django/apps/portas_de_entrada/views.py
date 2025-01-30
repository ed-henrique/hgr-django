from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import PortaDeEntrada
from apps.historico.models import Historico


class PortaDeEntradaForm(forms.ModelForm):
    class Meta:
        model = PortaDeEntrada
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
def portas_de_entrada_view(request):
    if request.method == 'POST':
        form = PortaDeEntradaForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user, descricao=f"Criou a Porta de Entrada '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")
    else:
        form = PortaDeEntradaForm()

    query = request.GET.get('q', '')
    if query:
        objs = PortaDeEntrada.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True).order_by('nome')
    else:
        objs = PortaDeEntrada.objects.filter(
            removido_em__isnull=True).order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/portas-de-entrada/",
        'title': 'Gestão de ' + PortaDeEntrada._meta.verbose_name_plural,
        'titulo': PortaDeEntrada._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + PortaDeEntrada._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'portas_de_entrada/index.html', context)


@login_required
@transaction.atomic
def editar_porta_de_entrada_view(request, id):
    obj = get_object_or_404(PortaDeEntrada, id=id)

    if request.method == 'POST':
        form = PortaDeEntradaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user, descricao=f"Editou a Porta de Entrada '{form.initial['nome']}' de cor '{form.initial['cor']}' para a Porta de Entrada '{form.cleaned_data['nome']}' de cor '{form.cleaned_data['cor']}'.")

            return redirect("/gestao/portas-de-entrada")
    else:
        form = PortaDeEntradaForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/portas-de-entrada/",
        'title': 'Gestão de ' + PortaDeEntrada._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + PortaDeEntrada._meta.verbose_name,
    }

    return render(request, 'portas_de_entrada/editar.html', context)


@login_required
@transaction.atomic
def excluir_porta_de_entrada_view(request, id):
    obj = get_object_or_404(PortaDeEntrada, id=id)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user, descricao=f"Removeu a Porta de Entrada '{obj.nome}' de cor '{obj.cor}'.")

        return redirect("/gestao/portas-de-entrada")

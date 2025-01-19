from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import StatusDeLeito

class StatusDeLeitoForm(forms.ModelForm):
    class Meta:
        model = StatusDeLeito
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
def status_de_leito_view(request):
    if request.method == 'POST':
        form = StatusDeLeitoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StatusDeLeitoForm()

    query = request.GET.get('q', '')
    if query:
        objs = StatusDeLeito.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = StatusDeLeito.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/status-de-leito/",
        'title': 'Gestão de ' + StatusDeLeito._meta.verbose_name_plural,
        'titulo': StatusDeLeito._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + StatusDeLeito._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'status_de_leito/index.html', context)

@login_required
def editar_status_de_leito_view(request, id):
    obj = get_object_or_404(StatusDeLeito, id=id)

    if request.method == 'POST':
        form = StatusDeLeitoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/status-de-leito")
    else:
        form = StatusDeLeitoForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/status-de-leito/",
        'title': 'Gestão de ' + StatusDeLeito._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + StatusDeLeito._meta.verbose_name,
    }

    return render(request, 'status_de_leito/editar.html', context)

@login_required
def excluir_status_de_leito_view(request, id):
    obj = get_object_or_404(StatusDeLeito, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/status-de-leito")

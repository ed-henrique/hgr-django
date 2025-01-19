from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import TipoDeLeito

class TipoDeLeitoForm(forms.ModelForm):
    class Meta:
        model = TipoDeLeito
        fields = ['nome', 'cor']

def tipos_de_leito_view(request):
    if request.method == 'POST':
        form = TipoDeLeitoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TipoDeLeitoForm()

    query = request.GET.get('q', '')
    if query:
        objs = TipoDeLeito.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = TipoDeLeito.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/tipos-de-leito/",
        'title': 'Gestão de ' + TipoDeLeito._meta.verbose_name_plural,
        'titulo': TipoDeLeito._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + TipoDeLeito._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'tipos_de_leito/index.html', context)

def editar_tipo_de_leito_view(request, id):
    obj = get_object_or_404(TipoDeLeito, id=id)

    if request.method == 'POST':
        form = TipoDeLeitoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/tipos-de-leito")
    else:
        form = TipoDeLeitoForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/tipos-de-leito/",
        'title': 'Gestão de ' + TipoDeLeito._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + TipoDeLeito._meta.verbose_name,
    }

    return render(request, 'tipos_de_leito/editar.html', context)

def excluir_tipo_de_leito_view(request, id):
    obj = get_object_or_404(TipoDeLeito, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/tipos-de-leito")

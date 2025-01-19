from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import MedidaDePrecaucao

class MedidaDePrecaucaoForm(forms.ModelForm):
    class Meta:
        model = MedidaDePrecaucao
        fields = ['nome', 'cor']

def medidas_de_precaucao_view(request):
    if request.method == 'POST':
        form = MedidaDePrecaucaoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MedidaDePrecaucaoForm()

    query = request.GET.get('q', '')
    if query:
        objs = MedidaDePrecaucao.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = MedidaDePrecaucao.objects.all().order_by('nome')

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

def editar_medida_de_precaucao_view(request, id):
    obj = get_object_or_404(MedidaDePrecaucao, id=id)

    if request.method == 'POST':
        form = MedidaDePrecaucaoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
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

def excluir_medida_de_precaucao_view(request, id):
    obj = get_object_or_404(MedidaDePrecaucao, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/medidas-de-precaucao")

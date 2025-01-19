from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import TipoDeO2

class TipoDeO2Form(forms.ModelForm):
    class Meta:
        model = TipoDeO2
        fields = ['nome', 'cor']
        error_messages = {
            'nome': {
                'unique': 'O nome informado já está cadastrado. Por favor, escolha outro.',
            },
            'cor': {
                'unique': 'A cor informada já está em uso. Escolha uma cor diferente.',
            },
        }

def tipos_de_o2_view(request):
    if request.method == 'POST':
        form = TipoDeO2Form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TipoDeO2Form()

    query = request.GET.get('q', '')
    if query:
        objs = TipoDeO2.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = TipoDeO2.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/tipos-de-o2/",
        'title': 'Gestão de ' + TipoDeO2._meta.verbose_name_plural,
        'titulo': TipoDeO2._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + TipoDeO2._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'tipos_de_o2/index.html', context)

def editar_tipo_de_o2_view(request, id):
    obj = get_object_or_404(TipoDeO2, id=id)

    if request.method == 'POST':
        form = TipoDeO2Form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/tipos-de-o2")
    else:
        form = TipoDeO2Form(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/tipos-de-o2/",
        'title': 'Gestão de ' + TipoDeO2._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + TipoDeO2._meta.verbose_name,
    }

    return render(request, 'tipos_de_o2/editar.html', context)

def excluir_tipo_de_o2_view(request, id):
    obj = get_object_or_404(TipoDeO2, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/tipos-de-o2")

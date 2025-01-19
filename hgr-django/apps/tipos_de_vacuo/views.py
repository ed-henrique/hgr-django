from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import TipoDeVacuo

class TipoDeVacuoForm(forms.ModelForm):
    class Meta:
        model = TipoDeVacuo
        fields = ['nome', 'cor']

def tipos_de_vacuo_view(request):
    if request.method == 'POST':
        form = TipoDeVacuoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TipoDeVacuoForm()

    query = request.GET.get('q', '')
    if query:
        objs = TipoDeVacuo.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = TipoDeVacuo.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/tipos-de-vacuo/",
        'title': 'Gestão de ' + TipoDeVacuo._meta.verbose_name_plural,
        'titulo': TipoDeVacuo._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + TipoDeVacuo._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'tipos_de_vacuo/index.html', context)

def editar_tipo_de_vacuo_view(request, id):
    obj = get_object_or_404(TipoDeVacuo, id=id)

    if request.method == 'POST':
        form = TipoDeVacuoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/tipos-de-vacuo")
    else:
        form = TipoDeVacuoForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/tipos-de-vacuo/",
        'title': 'Gestão de ' + TipoDeVacuo._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + TipoDeVacuo._meta.verbose_name,
    }

    return render(request, 'tipos_de_vacuo/editar.html', context)

def excluir_tipo_de_vacuo_view(request, id):
    obj = get_object_or_404(TipoDeVacuo, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/tipos-de-vacuo")

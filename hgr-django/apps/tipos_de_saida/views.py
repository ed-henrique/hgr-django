from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import TipoDeSaida

class TipoDeSaidaForm(forms.ModelForm):
    class Meta:
        model = TipoDeSaida
        fields = ['nome', 'cor']

def tipos_de_saida_view(request):
    if request.method == 'POST':
        form = TipoDeSaidaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TipoDeSaidaForm()

    query = request.GET.get('q', '')
    if query:
        objs = TipoDeSaida.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = TipoDeSaida.objects.all().order_by('nome')

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

def editar_tipo_de_saida_view(request, id):
    obj = get_object_or_404(TipoDeSaida, id=id)

    if request.method == 'POST':
        form = TipoDeSaidaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
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

def excluir_tipo_de_saida_view(request, id):
    obj = get_object_or_404(TipoDeSaida, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/tipos-de-saida")

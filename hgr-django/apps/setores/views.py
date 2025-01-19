from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import Setor

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'cor']
        error_messages = {
            'nome': {
                'unique': 'O nome informado já está cadastrado. Por favor, escolha outro.',
            },
            'cor': {
                'unique': 'A cor informada já está em uso. Escolha uma cor diferente.',
            },
        }

def setores_view(request):
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SetorForm()

    query = request.GET.get('q', '')
    if query:
        objs = Setor.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = Setor.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/setores/",
        'title': 'Gestão de ' + Setor._meta.verbose_name_plural,
        'titulo': Setor._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Setor._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'setores/index.html', context)

def editar_setor_view(request, id):
    obj = get_object_or_404(Setor, id=id)

    if request.method == 'POST':
        form = SetorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/setores")
    else:
        form = SetorForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/setores/",
        'title': 'Gestão de ' + Setor._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + Setor._meta.verbose_name,
    }

    return render(request, 'setores/editar.html', context)

def excluir_setor_view(request, id):
    obj = get_object_or_404(Setor, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/setores")

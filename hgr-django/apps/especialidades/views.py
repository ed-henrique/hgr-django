from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import Especialidade

class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = ['nome', 'cor']

def especialidades_view(request):
    if request.method == 'POST':
        form = EspecialidadeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EspecialidadeForm()

    query = request.GET.get('q', '')
    if query:
        objs = Especialidade.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = Especialidade.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/especialidades/",
        'title': 'Gestão de ' + Especialidade._meta.verbose_name_plural,
        'titulo': Especialidade._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Especialidade._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'especialidades/index.html', context)

def editar_especialidade_view(request, id):
    obj = get_object_or_404(Especialidade, id=id)

    if request.method == 'POST':
        form = EspecialidadeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/especialidades")
    else:
        form = EspecialidadeForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/especialidades/",
        'title': 'Gestão de ' + Especialidade._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + Especialidade._meta.verbose_name,
    }

    return render(request, 'especialidades/editar.html', context)

def excluir_especialidade_view(request, id):
    obj = get_object_or_404(Especialidade, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/especialidades")

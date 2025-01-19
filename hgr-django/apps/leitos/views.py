from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import Leito

class LeitoForm(forms.ModelForm):
    class Meta:
        model = Leito
        fields = [
            'setor',
            'especialidade',
            'status_de_leito',
            'tipo_de_leito',
            'tipo_de_o2',
            'tipo_de_vacuo',
            'codigo_sus',
            'tem_o2',
            'tem_vacuo',
            'tem_codigo_sus',
        ]

@login_required
def leitos_view(request):
    if request.method == 'POST':
        form = LeitoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LeitoForm()

    query = request.GET.get('q', '')
    if query:

        objs = Leito.objects.filter(
            Q(id__icontains=query),
            Q(setor__icontains=query),
            Q(tipo__icontains=query),
            Q(status__icontains=query),
            Q(codigo_sus__icontains=query),
        ).order_by('id')
    else:
        objs = Leito.objects.all().order_by('id')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/leitos/",
        'title': 'Gestão de ' + Leito._meta.verbose_name_plural,
        'titulo': Leito._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Leito._meta.verbose_name,
        'leitos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'leitos/index.html', context)

@login_required
def leito_view(request, id):
    obj = get_object_or_404(Leito, id=id)

    context = {
        'form': form,
        'leito': leito,
        'caminho': "/gestao/leitos/",
        'title': 'Gestão de ' + Leito._meta.verbose_name_plural,
        'titulo': Leito._meta.verbose_name_plural,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'leitos/index.html', context)

@login_required
def editar_leito_view(request, id):
    obj = get_object_or_404(Leito, id=id)

    if request.method == 'POST':
        form = LeitoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/leitos")
    else:
        form = LeitoForm(instance=obj)

    context = {
        'form': form,
        'leito': obj,
        'caminho': "/gestao/leitos/",
        'title': 'Gestão de ' + Leito._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + Leito._meta.verbose_name,
    }

    return render(request, 'leitos/editar.html', context)

@login_required
def excluir_leito_view(request, id):
    obj = get_object_or_404(Leito, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/leitos")

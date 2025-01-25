from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Leito
from .forms import LeitoForm
from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.tipos_de_leito.models import TipoDeLeito
from apps.status_de_leito.models import StatusDeLeito
from apps.tipos_de_o2.models import TipoDeO2
from apps.tipos_de_vacuo.models import TipoDeVacuo


@login_required
def leitos_view(request):
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

    setores = Setor.objects.all().order_by('nome')
    especialidades = Especialidade.objects.all().order_by('nome')
    tipos_de_leito = TipoDeLeito.objects.all().order_by('nome')
    status_de_leito = StatusDeLeito.objects.all().order_by('nome')
    tipos_de_o2 = TipoDeO2.objects.all().order_by('nome')
    tipos_de_vacuo = TipoDeVacuo.objects.all().order_by('nome')

    print(page_objs)

    context = {
        'setores': setores,
        'especialidades': especialidades,
        'tipos_de_leito': tipos_de_leito,
        'status_de_leito': status_de_leito,
        'tipos_de_o2': tipos_de_o2,
        'tipos_de_vacuo': tipos_de_vacuo,
        'caminho': "/gestao/leitos/",
        'title': 'Gestão de ' + Leito._meta.verbose_name_plural,
        'titulo': Leito._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Leito._meta.verbose_name,
        'leitos': page_objs,
    }

    if request.method == 'POST':
        form = LeitoForm(request.POST)
        if form.is_valid():
            Leito.objects.create(
                setor=form.cleaned_data["setor"],
                especialidade=form.cleaned_data["especialidade"],
                status_de_leito=form.cleaned_data["status_de_leito"],
                tipo_de_leito=form.cleaned_data["tipo_de_leito"],
                tipo_de_o2=form.cleaned_data["tipo_de_o2"],
                tipo_de_vacuo=form.cleaned_data["tipo_de_vacuo"],
                codigo_sus=form.cleaned_data["codigo_sus"],
                tem_o2=form.cleaned_data["tem_o2"],
                tem_vacuo=form.cleaned_data["tem_vacuo"],
                tem_codigo_sus=form.cleaned_data["tem_codigo_sus"],
            )

            return redirect("/gestao/leitos/")

        context['form'] = form
        return render(request, 'leitos/index.html', context)
    else:
        form = LeitoForm()

    context['form'] = form
    return render(request, 'leitos/index.html', context)


@login_required
def leito_view(request, id):
    obj = get_object_or_404(Leito, id=id)

    context = {
        'leito': obj,
        'caminho': "/gestao/leitos/",
        'title': 'Gestão de ' + Leito._meta.verbose_name_plural,
        'titulo': Leito._meta.verbose_name_plural,
    }

    return render(request, 'leitos/index.html', context)


@login_required
def editar_leito_view(request, id):
    obj = get_object_or_404(Leito, id=id)

    if request.method == 'POST':
        form = LeitoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/leitos/")
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
        return redirect("/gestao/leitos/")

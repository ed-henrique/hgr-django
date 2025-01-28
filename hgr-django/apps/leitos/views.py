from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from .models import Leito
from .forms import LeitoForm
from apps.setores.models import Setor
from apps.especialidades.models import Especialidade
from apps.tipos_de_leito.models import TipoDeLeito
from apps.status_de_leito.models import StatusDeLeito
from apps.tipos_de_o2.models import TipoDeO2
from apps.tipos_de_vacuo.models import TipoDeVacuo
from apps.historico_de_ocupacao_de_leito.models import HistoricoDeOcupacaoDeLeito


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
            removido_em__isnull=True,
        ).order_by('id')
    else:
        objs = Leito.objects.filter(removido_em__isnull=True).order_by('id')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    setores = Setor.objects.all().order_by('nome')
    especialidades = Especialidade.objects.all().order_by('nome')
    tipos_de_leito = TipoDeLeito.objects.all().order_by('nome')
    status_de_leito = StatusDeLeito.objects.all().order_by('nome')
    tipos_de_o2 = TipoDeO2.objects.all().order_by('nome')
    tipos_de_vacuo = TipoDeVacuo.objects.all().order_by('nome')

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
            with transaction.atomic():
                leito = Leito.objects.create(
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

                HistoricoDeOcupacaoDeLeito.objects.create(leito=leito)

                return redirect("/gestao/leitos/")

        context['form'] = form
        return render(request, 'leitos/index.html', context)
    else:
        form = LeitoForm()

    context['form'] = form
    return render(request, 'leitos/index.html', context)


@login_required
def leito_view(request, id):
    obj = get_object_or_404(Leito, id=id, removido_em__isnull=True)

    paginator = Paginator(
        obj.historico_de_ocupacao.order_by('-ocorrido_em'), 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'leito': obj,
        'historico_de_ocupacao': page_objs,
        'caminho': "/gestao/leitos/",
        'title': 'Gestão de ' + Leito._meta.verbose_name_plural,
        'titulo': Leito._meta.verbose_name_plural,
    }

    return render(request, 'leitos/leito.html', context)


@login_required
def editar_leito_view(request, id):
    obj = get_object_or_404(Leito, id=id, removido_em__isnull=True)

    if request.method == 'POST':
        form = LeitoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/leitos/")
    else:
        form = LeitoForm(instance=obj)

    setores = Setor.objects.all().order_by('nome')
    especialidades = Especialidade.objects.all().order_by('nome')
    tipos_de_leito = TipoDeLeito.objects.all().order_by('nome')
    status_de_leito = StatusDeLeito.objects.all().order_by('nome')
    tipos_de_o2 = TipoDeO2.objects.all().order_by('nome')
    tipos_de_vacuo = TipoDeVacuo.objects.all().order_by('nome')

    context = {
        'form': form,
        'leito': obj,
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
    }

    return render(request, 'leitos/editar.html', context)


@login_required
def excluir_leito_view(request, id):
    obj = get_object_or_404(Leito, id=id, removido_em__isnull=True)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()
        return redirect("/gestao/leitos/")

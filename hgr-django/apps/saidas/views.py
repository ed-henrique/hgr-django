from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from .models import Saida
from .forms import SaidaForm
from apps.leitos.models import Leito
from apps.pacientes.models import Paciente
from apps.unidades_de_saude.models import UnidadeDeSaude
from apps.tipos_de_saida.models import TipoDeSaida


@login_required
def saidas_view(request):
    query = request.GET.get('q', '')
    if query:

        objs = Saida.objects.filter(
            Q(paciente__nome__icontains=query) |
            Q(leito_de_origem__setor__nome__icontains=query) |
            Q(unidade_de_saude_de_destino__nome__icontains=query),
            removido_em__isnull=True,
        ).order_by('id')
    else:
        objs = Saida.objects.filter(
            removido_em__isnull=True).order_by('-data', '-hora')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    pacientes = Paciente.objects.filter(removido_em__isnull=True).exclude(
        saida__isnull=False).order_by('nome')
    unidades_de_saude = UnidadeDeSaude.objects.filter(
        removido_em__isnull=True).order_by('nome')
    tipos_de_saida = TipoDeSaida.objects.filter(
        removido_em__isnull=True).order_by('nome')

    context = {
        'pacientes': pacientes,
        'unidades_de_saude': unidades_de_saude,
        'tipos_de_saida': tipos_de_saida,
        'caminho': "/gestao/saidas/",
        'title': 'Gestão de ' + Saida._meta.verbose_name_plural,
        'titulo': Saida._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Saida._meta.verbose_name,
        'saidas': page_objs,
    }

    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            Saida.objects.create(
                data=form.cleaned_data["data"],
                hora=form.cleaned_data["hora"],
                paciente=form.cleaned_data["paciente"],
                tipo_de_saida=form.cleaned_data["tipo_de_saida"],
                leito_de_origem=form.cleaned_data["leito_de_origem"],
                unidade_de_saude_de_destino=form.cleaned_data["unidade_de_saude_de_destino"],
            )

            return redirect("/gestao/saidas/")

        context['form'] = form
        return render(request, 'saidas/index.html', context)
    else:
        form = SaidaForm()

    context['form'] = form
    return render(request, 'saidas/index.html', context)


@login_required
def saida_view(request, id):
    obj = get_object_or_404(Saida, id=id, removido_em__isnull=True)

    context = {
        'saida': obj,
        'caminho': "/gestao/saidas/",
        'title': 'Gestão de ' + Saida._meta.verbose_name_plural,
        'titulo': Saida._meta.verbose_name_plural,
    }

    return render(request, 'saidas/saida.html', context)


@login_required
def editar_saida_view(request, id):
    obj = get_object_or_404(Saida, id=id, removido_em__isnull=True)

    if request.method == 'POST':
        form = SaidaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(f"/gestao/saidas/{id}")
    else:
        form = SaidaForm(instance=obj)

    pacientes = Paciente.objects.filter(removido_em__isnull=True).exclude(
        saida__isnull=False).order_by('nome')
    unidades_de_saude = UnidadeDeSaude.objects.filter(
        removido_em__isnull=True).order_by('nome')
    tipos_de_saida = TipoDeSaida.objects.filter(
        removido_em__isnull=True).order_by('nome')

    context = {
        'form': form,
        'saida': obj,
        'pacientes': pacientes,
        'unidades_de_saude': unidades_de_saude,
        'tipos_de_saida': tipos_de_saida,
        'caminho': "/gestao/saidas/",
        'title': 'Gestão de ' + Saida._meta.verbose_name_plural,
        'titulo': Saida._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Saida._meta.verbose_name,
    }

    return render(request, 'saidas/editar.html', context)


@login_required
def excluir_saida_view(request, id):
    obj = get_object_or_404(Saida, id=id, removido_em__isnull=True)

    if request.method == 'POST':
        obj.removido_em = now()
        obj.save()
        return redirect("/gestao/saidas/")

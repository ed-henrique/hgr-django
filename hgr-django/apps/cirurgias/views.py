from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from .models import Cirurgia
from .forms import CirurgiaForm
from apps.setores.models import Setor
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidade
from apps.tipos_de_cirurgia.models import TipoDeCirurgia


@login_required
def cirurgias_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Cirurgia.objects.filter(
            Q(paciente__nome__icontains=query)
            | Q(setor__nome__icontains=query)
            | Q(especialidade__nome__icontains=query)
            | Q(tipo_de_cirurgia__nome__icontains=query),
            removido_em__isnull=True,
        ).order_by("id")
    else:
        objs = Cirurgia.objects.filter(removido_em__isnull=True).order_by("-data")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    pacientes = (
        Paciente.objects.filter(removido_em__isnull=True)
        .exclude(saida__isnull=False)
        .order_by("nome")
    )
    setores = Setor.objects.filter(removido_em__isnull=True).order_by("nome")
    especialidades = Especialidade.objects.filter(removido_em__isnull=True).order_by(
        "nome"
    )
    tipos_de_cirurgia = TipoDeCirurgia.objects.filter(
        removido_em__isnull=True
    ).order_by("nome")

    context = {
        "pacientes": pacientes,
        "setores": setores,
        "especialidades": especialidades,
        "tipos_de_cirurgia": tipos_de_cirurgia,
        "caminho": "/gestao/cirurgias/",
        "title": "Gestão de " + Cirurgia._meta.verbose_name_plural,
        "titulo": Cirurgia._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Cirurgia._meta.verbose_name,
        "cirurgias": page_objs,
    }

    if request.method == "POST":
        form = CirurgiaForm(request.POST)
        if form.is_valid():
            Cirurgia.objects.create(
                data=form.cleaned_data["data"],
                paciente=form.cleaned_data["paciente"],
                setor=form.cleaned_data["setor"],
                especialidade=form.cleaned_data["especialidade"],
                tipo_de_cirurgia=form.cleaned_data["tipo_de_cirurgia"],
                concluida_com_sucesso=form.cleaned_data["concluida_com_sucesso"],
            )

            return redirect("/gestao/cirurgias/")

        context["form"] = form
        return render(request, "cirurgias/index.html", context)
    else:
        form = CirurgiaForm()

    context["form"] = form
    return render(request, "cirurgias/index.html", context)


@login_required
def cirurgia_view(request, id):
    obj = get_object_or_404(Cirurgia, id=id, removido_em__isnull=True)

    context = {
        "cirurgia": obj,
        "caminho": "/gestao/cirurgias/",
        "title": "Gestão de " + Cirurgia._meta.verbose_name_plural,
        "titulo": Cirurgia._meta.verbose_name_plural,
    }

    return render(request, "cirurgias/cirurgia.html", context)


@login_required
def editar_cirurgia_view(request, id):
    obj = get_object_or_404(Cirurgia, id=id, removido_em__isnull=True)

    if request.method == "POST":
        form = CirurgiaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(f"/gestao/cirurgias/{id}")
    else:
        form = CirurgiaForm(instance=obj)

    pacientes = (
        Paciente.objects.filter(removido_em__isnull=True)
        .exclude(saida__isnull=False)
        .order_by("nome")
    )
    setores = Setor.objects.filter(removido_em__isnull=True).order_by("nome")
    especialidades = Especialidade.objects.filter(removido_em__isnull=True).order_by(
        "nome"
    )
    tipos_de_cirurgia = TipoDeCirurgia.objects.filter(
        removido_em__isnull=True
    ).order_by("nome")

    context = {
        "form": form,
        "cirurgia": obj,
        "pacientes": pacientes,
        "setores": setores,
        "especialidades": especialidades,
        "tipos_de_cirurgia": tipos_de_cirurgia,
        "caminho": "/gestao/cirurgias/",
        "title": "Gestão de " + Cirurgia._meta.verbose_name_plural,
        "titulo": Cirurgia._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Cirurgia._meta.verbose_name,
    }

    return render(request, "cirurgias/editar.html", context)


@login_required
def excluir_cirurgia_view(request, id):
    obj = get_object_or_404(Cirurgia, id=id, removido_em__isnull=True)

    if request.method == "POST":
        obj.removido_em = now()
        obj.save()
        return redirect("/gestao/cirurgias/")

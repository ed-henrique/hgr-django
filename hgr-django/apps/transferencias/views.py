from django.core.paginator import Paginator
from utils.decorators import is_admin_or_higher_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from .models import Transferencia
from .forms import TransferenciaForm
from apps.leitos.models import Leito
from apps.pacientes.models import Paciente


@login_required
def transferencias_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Transferencia.objects.filter(
            Q(paciente__nome__icontains=query)
            | Q(leito_de_origem__setor__nome__icontains=query)
            | Q(leito_de_destino__setor__nome__icontains=query),
            removido_em__isnull=True,
        ).order_by("id")
    else:
        objs = Transferencia.objects.filter(
            removido_em__isnull=True).order_by("-data")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    pacientes = (
        Paciente.objects.filter(removido_em__isnull=True)
        .exclude(saida__isnull=False)
        .order_by("nome")
    )
    leitos = Leito.objects.filter(
        removido_em__isnull=True, paciente__isnull=True
    ).order_by("id")

    context = {
        "pacientes": pacientes,
        "leitos": leitos,
        "caminho": "/gestao/transferencias/",
        "title": "Gestão de " + Transferencia._meta.verbose_name_plural,
        "titulo": Transferencia._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Transferencia._meta.verbose_name,
        "transferencias": page_objs,
    }

    if request.method == "POST":
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            Transferencia.objects.create(
                data=form.cleaned_data["data"],
                paciente=form.cleaned_data["paciente"],
                leito_de_origem=form.cleaned_data["leito_de_origem"],
                leito_de_destino=form.cleaned_data["leito_de_destino"],
            )

            return redirect("/gestao/transferencias/")

        context["form"] = form
        return render(request, "transferencias/index.html", context)
    else:
        form = TransferenciaForm()

    context["form"] = form
    return render(request, "transferencias/index.html", context)


@login_required
def transferencia_view(request, id):
    obj = get_object_or_404(Transferencia, id=id, removido_em__isnull=True)

    context = {
        "transferencia": obj,
        "caminho": "/gestao/transferencias/",
        "title": "Gestão de " + Transferencia._meta.verbose_name_plural,
        "titulo": Transferencia._meta.verbose_name_plural,
    }

    return render(request, "transferencias/transferencia.html", context)


@login_required
@is_admin_or_higher_required
def editar_transferencia_view(request, id):
    obj = get_object_or_404(Transferencia, id=id, removido_em__isnull=True)

    if request.method == "POST":
        form = TransferenciaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(f"/gestao/transferencias/{id}")
    else:
        form = TransferenciaForm(instance=obj)

    pacientes = (
        Paciente.objects.filter(removido_em__isnull=True)
        .exclude(saida__isnull=False)
        .order_by("nome")
    )
    leitos = (
        Leito.objects.filter(removido_em__isnull=True, paciente__isnull=True)
        .exclude(id=obj.leito_de_origem.id)
        .order_by("id")
    )

    context = {
        "form": form,
        "transferencia": obj,
        "pacientes": pacientes,
        "leitos": leitos,
        "caminho": "/gestao/transferencias/",
        "title": "Gestão de " + Transferencia._meta.verbose_name_plural,
        "titulo": Transferencia._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Transferencia._meta.verbose_name,
    }

    return render(request, "transferencias/editar.html", context)


@login_required
@is_admin_or_higher_required
def excluir_transferencia_view(request, id):
    obj = get_object_or_404(Transferencia, id=id, removido_em__isnull=True)

    if request.method == "POST":
        obj.removido_em = now()
        obj.save()
        return redirect("/gestao/transferencias/")

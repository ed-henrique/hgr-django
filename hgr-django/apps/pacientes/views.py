from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from utils.decorators import is_admin_or_higher_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db import transaction
from django.db.models import Q
from .models import Paciente
from apps.leitos.models import Leito
from apps.entradas.models import Entrada
from apps.transferencias.models import Transferencia
from apps.saidas.models import Saida
from apps.historico_de_ocupacao_de_leito.models import HistoricoDeOcupacaoDeLeito
from .forms import PacienteEditForm, PacienteCreateForm


@login_required
def pacientes_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Paciente.objects.filter(
            Q(nome__icontains=query)
            | Q(leito__setor__nome__icontains=query)
            | Q(responsavel__first_name__icontains=query)
            | Q(status_de_paciente__nome__icontains=query),
            removido_em__isnull=True,
        ).order_by("id")
    else:
        objs = Paciente.objects.filter(removido_em__isnull=True).order_by("id")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "caminho": "/gestao/pacientes/",
        "title": "Gestão de " + Paciente._meta.verbose_name_plural,
        "titulo": Paciente._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Paciente._meta.verbose_name,
        "pacientes": page_objs,
    }

    return render(request, "pacientes/index.html", context)


@login_required
def paciente_view(request, id):
    obj = get_object_or_404(Paciente, id=id, removido_em__isnull=True)

    context = {
        "paciente": obj,
        "caminho": "/gestao/pacientes/",
        "title": "Gestão de " + Paciente._meta.verbose_name_plural,
        "titulo": Paciente._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Paciente._meta.verbose_name,
    }

    return render(request, "pacientes/paciente.html", context)


@login_required
@transaction.atomic
def criar_paciente_view(request):
    if request.method == "POST":
        form = PacienteCreateForm(request.POST, user=request.user)
        if form.is_valid():
            paciente = form.save()

            leito = form.cleaned_data.get("leito")
            leito.paciente = paciente
            leito.save()

            HistoricoDeOcupacaoDeLeito.objects.create(
                paciente=paciente, leito=leito
            )

            Entrada.objects.create(
                paciente=paciente,
                unidade_de_saude_de_origem=paciente.unidade_de_saude_de_origem,
                leito_de_destino=leito,
                data=paciente.data_de_internacao,
            )

            return redirect("/gestao/pacientes/")
    else:
        form = PacienteCreateForm(user=request.user)

    context = {
        "form": form,
        "caminho": "/gestao/pacientes/",
        "title": "Gestão de " + Paciente._meta.verbose_name_plural,
        "titulo": Paciente._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Paciente._meta.verbose_name,
    }

    return render(request, "pacientes/criar.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def editar_paciente_view(request, id):
    obj = get_object_or_404(Paciente, id=id, removido_em__isnull=True)

    if request.method == "POST":
        form = PacienteEditForm(request.POST, instance=obj, paciente=obj)
        if form.is_valid():
            antigo_leito = obj.leito
            leito = form.cleaned_data.get("leito")
            unidade_de_saude_de_origem = form.cleaned_data.get(
                "unidade_de_saude_de_origem")
            data_de_internacao = form.cleaned_data.get(
                "data_de_internacao")
            data_de_internacao_no_setor = form.cleaned_data.get(
                "data_de_internacao_no_setor")

            antigo_leito = Leito.objects.select_for_update().get(pk=antigo_leito.pk)
            leito = Leito.objects.select_for_update().get(pk=leito.pk)

            paciente = form.save()

            if antigo_leito != leito:
                antigo_leito.paciente = None
                antigo_leito.save()

                HistoricoDeOcupacaoDeLeito.objects.create(
                    leito=antigo_leito)

                leito.paciente = paciente
                leito.save()

                HistoricoDeOcupacaoDeLeito.objects.create(
                    leito=leito, paciente=paciente
                )

                Entrada.objects.select_for_update().filter(paciente=obj).update(
                    leito_de_destino=leito,
                    unidade_de_saude_de_origem=unidade_de_saude_de_origem,
                    data_de_internacao=data_de_internacao,
                    data_de_internacao_no_setor=data_de_internacao_no_setor
                )

            return redirect(f"/gestao/pacientes/{id}")
    else:
        form = PacienteEditForm(instance=obj, paciente=obj)

    context = {
        "form": form,
        "paciente": obj,
        "caminho": "/gestao/pacientes/",
        "title": "Gestão de " + Paciente._meta.verbose_name_plural,
        "titulo": Paciente._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Editar " + Paciente._meta.verbose_name,
    }

    return render(request, "pacientes/editar.html", context)


@ login_required
@ transaction.atomic
@is_admin_or_higher_required
def excluir_paciente_view(request, id):
    obj = get_object_or_404(Paciente, id=id, removido_em__isnull=True)

    if request.method == "POST":
        obj.removido_em = now()
        obj.save()

        leito = obj.leito
        leito.paciente = None
        leito.save()

        Entrada.objects.select_for_update().filter(
            paciente=obj).update(removido_em=now())
        Transferencia.objects.select_for_update().filter(
            paciente=obj).update(removido_em=now())
        Saida.objects.select_for_update().filter(
            paciente=obj).update(removido_em=now())
        HistoricoDeOcupacaoDeLeito.objects.select_for_update().filter(paciente=obj).delete()

        return redirect("/gestao/pacientes/")

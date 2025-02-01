from django.core.paginator import Paginator
from utils.decorators import is_admin_or_higher_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import Especialidade
from apps.historico.models import Historico


class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = ["nome", "cor"]
        error_messages = {
            "nome": {
                "unique": "O nome informado já está cadastrado. Por favor, escolha outro.",
            },
            "cor": {
                "unique": "A cor informada já está em uso. Escolha uma cor diferente.",
            },
        }


@login_required
@transaction.atomic
def especialidades_view(request):
    if request.method == "POST":
        form = EspecialidadeForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user,
                descricao=f"""Criou a Especialidade <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.cleaned_data["cor"]};">{form.cleaned_data["nome"]}</span>.""",
            )
    else:
        form = EspecialidadeForm()

    query = request.GET.get("q", "")
    if query:
        objs = Especialidade.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True
        ).order_by("nome")
    else:
        objs = Especialidade.objects.filter(
            removido_em__isnull=True).order_by("nome")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "form": form,
        "caminho": "/gestao/especialidades/",
        "title": "Gestão de " + Especialidade._meta.verbose_name_plural,
        "titulo": Especialidade._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + Especialidade._meta.verbose_name,
        "basicos": page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, "especialidades/index.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def editar_especialidade_view(request, id):
    obj = get_object_or_404(Especialidade, id=id)

    if request.method == "POST":
        form = EspecialidadeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user,
                descricao=f"""Modificou a Especialidade de <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.initial["cor"]};">{form.initial["nome"]}</span> para <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.cleaned_data["cor"]};">{form.cleaned_data["nome"]}</span>.""",
            )

            return redirect("/gestao/especialidades")
    else:
        form = EspecialidadeForm(instance=obj)

    context = {
        "cor": obj.cor,
        "nome": obj.nome,
        "caminho": "/gestao/especialidades/",
        "title": "Gestão de " + Especialidade._meta.verbose_name_plural,
        "mensagem_de_edicao": "Editar " + Especialidade._meta.verbose_name,
    }

    return render(request, "especialidades/editar.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def excluir_especialidade_view(request, id):
    obj = get_object_or_404(Especialidade, id=id)

    if request.method == "POST":
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Removeu a Especialidade <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {obj.cor};">{obj.nome}</span>.""",
        )

        return redirect("/gestao/especialidades")

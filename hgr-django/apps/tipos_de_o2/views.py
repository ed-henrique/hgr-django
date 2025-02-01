from django.core.paginator import Paginator
from utils.decorators import is_admin_or_higher_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import TipoDeO2
from apps.historico.models import Historico


class TipoDeO2Form(forms.ModelForm):
    class Meta:
        model = TipoDeO2
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
def tipos_de_o2_view(request):
    if request.method == "POST":
        form = TipoDeO2Form(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user,
                descricao=f"""Criou o Tipo de O2 <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.cleaned_data["cor"]};">{form.cleaned_data["nome"]}</span>.""",
            )
    else:
        form = TipoDeO2Form()

    query = request.GET.get("q", "")
    if query:
        objs = TipoDeO2.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True
        ).order_by("nome")
    else:
        objs = TipoDeO2.objects.filter(
            removido_em__isnull=True).order_by("nome")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "form": form,
        "caminho": "/gestao/tipos-de-o2/",
        "title": "Gestão de " + TipoDeO2._meta.verbose_name_plural,
        "titulo": TipoDeO2._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + TipoDeO2._meta.verbose_name,
        "basicos": page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, "tipos_de_o2/index.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def editar_tipo_de_o2_view(request, id):
    obj = get_object_or_404(TipoDeO2, id=id)

    if request.method == "POST":
        form = TipoDeO2Form(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user,
                descricao=f"""Modificou o Tipo de O2 de <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.initial["cor"]};">{form.initial["nome"]}</span> para <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.cleaned_data["cor"]};">{form.cleaned_data["nome"]}</span>.""",
            )

            return redirect("/gestao/tipos-de-o2")
    else:
        form = TipoDeO2Form(instance=obj)

    context = {
        "cor": obj.cor,
        "nome": obj.nome,
        "caminho": "/gestao/tipos-de-o2/",
        "title": "Gestão de " + TipoDeO2._meta.verbose_name_plural,
        "mensagem_de_edicao": "Editar " + TipoDeO2._meta.verbose_name,
    }

    return render(request, "tipos_de_o2/editar.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def excluir_tipo_de_o2_view(request, id):
    obj = get_object_or_404(TipoDeO2, id=id)

    if request.method == "POST":
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Removeu o Tipo de O2 <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {obj.cor};">{obj.nome}</span>.""",
        )

        return redirect("/gestao/tipos-de-o2")

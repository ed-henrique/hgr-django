from django.core.paginator import Paginator
from utils.decorators import is_admin_or_higher_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction
from django import forms
from .models import TipoDeCirurgia
from apps.historico.models import Historico


class TipoDeCirurgiaForm(forms.ModelForm):
    class Meta:
        model = TipoDeCirurgia
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
def tipos_de_cirurgia_view(request):
    if request.method == "POST":
        form = TipoDeCirurgiaForm(request.POST)
        if form.is_valid():
            form.save()
            Historico.objects.create(
                usuario=request.user,
                descricao=f"""Criou o Tipo de Cirurgia <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.cleaned_data["cor"]};">{form.cleaned_data["nome"]}</span>.""",
            )
    else:
        form = TipoDeCirurgiaForm()

    query = request.GET.get("q", "")
    if query:
        objs = TipoDeCirurgia.objects.filter(
            Q(nome__icontains=query), removido_em__isnull=True
        ).order_by("nome")
    else:
        objs = TipoDeCirurgia.objects.filter(
            removido_em__isnull=True).order_by("nome")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "form": form,
        "caminho": "/gestao/tipos-de-cirurgia/",
        "title": "Gestão de " + TipoDeCirurgia._meta.verbose_name_plural,
        "titulo": TipoDeCirurgia._meta.verbose_name_plural,
        "mensagem_de_cadastro": "Cadastrar " + TipoDeCirurgia._meta.verbose_name,
        "basicos": page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, "tipos_de_cirurgia/index.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def editar_tipo_de_cirurgia_view(request, id):
    obj = get_object_or_404(TipoDeCirurgia, id=id)

    if request.method == "POST":
        form = TipoDeCirurgiaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            Historico.objects.create(
                usuario=request.user,
                descricao=f"""Modificou o Tipo de Cirurgia de <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.initial["cor"]};">{form.initial["nome"]}</span> para <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {form.cleaned_data["cor"]};">{form.cleaned_data["nome"]}</span>.""",
            )

            return redirect("/gestao/tipos-de-cirurgia")
    else:
        form = TipoDeCirurgiaForm(instance=obj)

    context = {
        "cor": obj.cor,
        "nome": obj.nome,
        "caminho": "/gestao/tipos-de-cirurgia/",
        "title": "Gestão de " + TipoDeCirurgia._meta.verbose_name_plural,
        "mensagem_de_edicao": "Editar " + TipoDeCirurgia._meta.verbose_name,
    }

    return render(request, "tipos_de_cirurgia/editar.html", context)


@login_required
@transaction.atomic
@is_admin_or_higher_required
def excluir_tipo_de_cirurgia_view(request, id):
    obj = get_object_or_404(TipoDeCirurgia, id=id)

    if request.method == "POST":
        obj.removido_em = now()
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Removeu o Tipo de Cirurgia <span class="badge d-inline-flex align-items-center fw-bolder text-center" style="background-color: {obj.cor};">{obj.nome}</span>.""",
        )

        return redirect("/gestao/tipos-de-cirurgia")

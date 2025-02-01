from django.core.paginator import Paginator
from utils.decorators import is_superadmin_required, is_admin_or_higher_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.db.models import Q
from .models import Usuario
from apps.historico.models import Historico
from apps.tipos_de_usuario.models import TipoDeUsuario
from apps.status_de_usuario.models import StatusDeUsuario


@login_required
@transaction.atomic
def usuarios_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Usuario.objects.filter(
            Q(first_name__icontains=query) | Q(email__icontains=query),
        ).order_by("status_de_usuario", "tipo_de_usuario", "first_name")
    else:
        objs = Usuario.objects.all().order_by(
            "status_de_usuario", "tipo_de_usuario", "first_name"
        )

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "caminho": "/gestao/leitos/",
        "title": "Gestão de " + Usuario._meta.verbose_name_plural,
        "usuarios": page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part
        p.participacao_formatada = f"{part:.2f}"

    return render(request, "usuarios/index.html", context)


@login_required
@transaction.atomic
@is_superadmin_required
def elevar_autoridade_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        tipo_de_usuario = TipoDeUsuario.objects.get(nome="Administrador")
        obj.tipo_de_usuario = tipo_de_usuario
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Concedeu privilégios de administrador ao usuário ID: {obj.id} - {obj.first_name}.""",
        )

        return redirect("/gestao/usuarios/")


@login_required
@transaction.atomic
@is_superadmin_required
def remover_autoridade_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        tipo_de_usuario = TipoDeUsuario.objects.get(
            nome="Profissional de Saúde")
        obj.tipo_de_usuario = tipo_de_usuario
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Removeu os privilégios de administrador do usuário ID: {obj.id} - {obj.first_name}.""",
        )

        return redirect("/gestao/usuarios/")


@login_required
@transaction.atomic
@is_admin_or_higher_required
def desbloquear_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        status_de_usuario = StatusDeUsuario.objects.get(nome="Ativo")
        obj.status_de_usuario = status_de_usuario
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Desbloqueou o usuário ID: {obj.id} - {obj.first_name}.""",
        )

        return redirect("/gestao/usuarios/")


@login_required
@transaction.atomic
@is_admin_or_higher_required
def bloquear_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        status_de_usuario = StatusDeUsuario.objects.get(nome="Bloqueado")
        obj.status_de_usuario = status_de_usuario
        obj.save()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Bloqueou o usuário ID: {obj.id} - {obj.first_name}.""",
        )

        return redirect("/gestao/usuarios/")


@login_required
@transaction.atomic
@is_admin_or_higher_required
def excluir_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        obj.delete()

        Historico.objects.create(
            usuario=request.user,
            descricao=f"""Rejeitou o cadastro do usuário {obj.first_name} ({obj.email}).""",
        )

        return redirect("/gestao/usuarios/")

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Usuario
from apps.tipos_de_usuario.models import TipoDeUsuario
from apps.status_de_usuario.models import StatusDeUsuario


@login_required
def usuarios_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Usuario.objects.filter(
            Q(first_name__icontains=query),
            Q(email__icontains=query),
        ).order_by("tipo_de_usuario", "first_name")
    else:
        objs = Usuario.objects.all().order_by("tipo_de_usuario", "first_name")

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
def elevar_autoridade_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        tipo_de_usuario = TipoDeUsuario.objects.filter(nome="Administrador")
        obj.status_de_usuario = tipo_de_usuario
        return redirect("/gestao/usuarios/")


@login_required
def remover_autoridade_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        tipo_de_usuario = TipoDeUsuario.objects.filter(nome="Profissional de Saúde")
        obj.status_de_usuario = tipo_de_usuario
        return redirect("/gestao/usuarios/")


@login_required
def desbloquear_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        status_de_usuario = StatusDeUsuario.objects.filter(nome="Ativo")
        obj.status_de_usuario = status_de_usuario
        return redirect("/gestao/usuarios/")


@login_required
def bloquear_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        status_de_usuario = StatusDeUsuario.objects.filter(nome="Bloqueado")
        obj.status_de_usuario = status_de_usuario
        return redirect("/gestao/usuarios/")


@login_required
def excluir_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        obj.delete()
        return redirect("/gestao/usuarios/")

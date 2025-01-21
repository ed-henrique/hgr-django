from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Usuario


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

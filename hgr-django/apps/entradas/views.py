from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Entrada


@login_required
def entradas_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Entrada.objects.filter(
            Q(id__icontains=query)
            | Q(paciente__nome__icontains=query)
            | Q(leito_de_destino__setor__nome__icontains=query),
            removido_em__isnull=True,
        ).order_by("id")
    else:
        objs = Entrada.objects.filter(removido_em__isnull=True).order_by("-data")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "caminho": "/gestao/entradas/",
        "title": "Gestão de " + Entrada._meta.verbose_name_plural,
        "titulo": Entrada._meta.verbose_name_plural,
        "entradas": page_objs,
    }

    return render(request, "entradas/index.html", context)

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from .models import Historico


@login_required
def historico_view(request):
    query = request.GET.get("q", "")
    if query:
        objs = Historico.objects.filter(
            Q(data__icontains=query) | Q(usuario__first_name__icontains=query),
        ).order_by("id")
    else:
        objs = Historico.objects.all().order_by("-data")

    paginator = Paginator(objs, 10)
    page_number = request.GET.get("page")
    page_objs = paginator.get_page(page_number)

    context = {
        "caminho": "/gestao/historico/",
        "title": "Gestão de " + Historico._meta.verbose_name_plural,
        "titulo": Historico._meta.verbose_name_plural,
        "historico": page_objs,
    }

    return render(request, "historico/index.html", context)

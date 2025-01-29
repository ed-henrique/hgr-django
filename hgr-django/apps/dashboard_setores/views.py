from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.leitos.models import Leito
from apps.status_de_leito.models import StatusDeLeito
from apps.setores.models import Setor


@login_required
def dashboard_setores_view(request):
    objs = Setor.objects.filter(removido_em__isnull=True).order_by('-nome').prefetch_related(
        Prefetch('leito_set', queryset=Leito.objects.filter(
            removido_em__isnull=True))
    )
    status_de_leito = StatusDeLeito.objects.filter(
        removido_em__isnull=True).order_by('-nome')

    context = {
        'caminho': "/dashboard/setores/",
        'title': 'Dashboard de ' + Setor._meta.verbose_name_plural,
        'setores': objs,
        'status_de_leito': status_de_leito,
    }

    return render(request, 'dashboard_setores/index.html', context)

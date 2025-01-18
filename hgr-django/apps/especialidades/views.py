from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Especialidade

def especialidades_view(request):
    total_especialidades = Especialidade.objects.count()
    especialidades_list = Especialidade.objects.all().order_by('nome')

    paginator = Paginator(especialidades_list, 10)
    page_number = request.GET.get('_page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Gestão de Especialidades',
        'basicos': page_obj,
    }

    for p in page_obj:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'especialidades/index.html', context)

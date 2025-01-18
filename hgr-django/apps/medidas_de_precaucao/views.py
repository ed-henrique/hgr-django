from django.core.paginator import Paginator
from django.shortcuts import render
from .models import MedidaDePrecaucao

def medidas_de_precaucao_view(request):
    objs = MedidaDePrecaucao.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('_page')
    page_objs = paginator.get_page(page_number)

    context = {
        'title': 'Gestão de ' + MedidaDePrecaucao._meta.verbose_name_plural,
        'titulo': MedidaDePrecaucao._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + MedidaDePrecaucao._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'medidas_de_precaucao/index.html', context)

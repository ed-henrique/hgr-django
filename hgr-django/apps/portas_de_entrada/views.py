from django.core.paginator import Paginator
from django.shortcuts import render
from .models import PortaDeEntrada

def portas_de_entrada_view(request):
    objs = PortaDeEntrada.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('_page')
    page_objs = paginator.get_page(page_number)

    context = {
        'title': 'Gestão de ' + PortaDeEntrada._meta.verbose_name_plural,
        'titulo': PortaDeEntrada._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + PortaDeEntrada._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'portas_de_entrada/index.html', context)

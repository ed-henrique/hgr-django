from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Paciente
from .forms import PacienteCreateForm


@login_required
def pacientes_view(request):
    query = request.GET.get('q', '')
    if query:

        objs = Paciente.objects.filter(
            Q(nome__icontains=query),
            Q(leito__setor__icontains=query),
            Q(responsavel__nome__icontains=query),
            Q(status_de_paciente__nome__icontains=query),
            removido_em__isnull=True,
        ).order_by('id')
    else:
        objs = Paciente.objects.filter(removido_em__isnull=True).order_by('id')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'caminho': "/gestao/pacientes/",
        'title': 'Gestão de ' + Paciente._meta.verbose_name_plural,
        'titulo': Paciente._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Paciente._meta.verbose_name,
        'pacientes': page_objs,
    }

    return render(request, 'pacientes/index.html', context)


@login_required
def paciente_view(request, id):
    pass


@login_required
def criar_paciente_view(request):
    if request.method == 'POST':
        form = PacienteCreateForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/gestao/pacientes/")
    else:
        form = PacienteCreateForm(user=request.user)

    context = {
        'form': form,
        'caminho': "/gestao/pacientes/",
        'title': 'Gestão de ' + Paciente._meta.verbose_name_plural,
        'titulo': Paciente._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + Paciente._meta.verbose_name,
    }

    print(form.errors)

    return render(request, 'pacientes/criar.html', context)


@login_required
def editar_paciente_view(request):
    pass


@login_required
def excluir_paciente_view(request):
    pass

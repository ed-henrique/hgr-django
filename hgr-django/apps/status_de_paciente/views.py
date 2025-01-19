from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import StatusDePaciente

class StatusDePacienteForm(forms.ModelForm):
    class Meta:
        model = StatusDePaciente
        fields = ['nome', 'cor']

def status_de_paciente_view(request):
    if request.method == 'POST':
        form = StatusDePacienteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StatusDePacienteForm()

    query = request.GET.get('q', '')
    if query:
        objs = StatusDePaciente.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = StatusDePaciente.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/status-de-paciente/",
        'title': 'Gestão de ' + StatusDePaciente._meta.verbose_name_plural,
        'titulo': StatusDePaciente._meta.verbose_name_plural,
        'mensagem_de_cadastro': 'Cadastrar ' + StatusDePaciente._meta.verbose_name,
        'basicos': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'status_de_paciente/index.html', context)

def editar_status_de_paciente_view(request, id):
    obj = get_object_or_404(StatusDePaciente, id=id)

    if request.method == 'POST':
        form = StatusDePacienteForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/gestao/status-de-paciente")
    else:
        form = StatusDePacienteForm(instance=obj)

    context = {
        'cor': obj.cor,
        'nome': obj.nome,
        'caminho': "/gestao/status-de-paciente/",
        'title': 'Gestão de ' + StatusDePaciente._meta.verbose_name_plural,
        'mensagem_de_edicao': 'Editar ' + StatusDePaciente._meta.verbose_name,
    }

    return render(request, 'status_de_paciente/editar.html', context)

def excluir_status_de_paciente_view(request, id):
    obj = get_object_or_404(StatusDePaciente, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/status-de-paciente")

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nome',
            'email',
            'tipo_de_usuario',
            'status_de_usuario',
        ]

def usuarios_view(request):
    query = request.GET.get('q', '')
    if query:

        objs = Usuario.objects.filter(Q(nome__icontains=query)).order_by('nome')
    else:
        objs = Usuario.objects.all().order_by('nome')

    paginator = Paginator(objs, 10)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {
        'form': form,
        'caminho': "/gestao/usuarios/",
        'title': 'Gestão de ' + Usuario._meta.verbose_name_plural,
        'titulo': Usuario._meta.verbose_name_plural,
        'usuarios': page_objs,
    }

    for p in page_objs:
        part = p.get_participacao()
        p.participacao = part 
        p.participacao_formatada = f"{part:.2f}"

    return render(request, 'usuarios/index.html', context)

def excluir_usuario_view(request, id):
    obj = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/gestao/usuarios")

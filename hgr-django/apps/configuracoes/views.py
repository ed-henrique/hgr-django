from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import NewNameForm, NewUsernameForm, NewEmailForm, NewPasswordForm


@login_required
def configuracoes_view(request):
    context = {
        "name_form": NewNameForm(),
        "username_form": NewUsernameForm(),
        "email_form": NewEmailForm(),
        "password_form": NewPasswordForm(request.user),
        "caminho": "/configuracoes/",
        "title": "Configurações",
    }

    return render(request, "configuracoes/index.html", context)


@login_required
def mudar_nome_view(request):
    if request.method == "POST":
        form = NewNameForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["name"]
            request.user.save()
            return redirect("configuracoes")
    else:
        form = NewNameForm()

    context = {
        "name_form": form,
        "username_form": NewUsernameForm(),
        "email_form": NewEmailForm(),
        "password_form": NewPasswordForm(request.user),
        "caminho": "/configuracoes/",
        "title": "Configurações",
    }

    return render(request, "configuracoes/index.html", context)


@login_required
def mudar_nome_de_usuario_view(request):
    if request.method == "POST":
        form = NewUsernameForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data["username"]
            request.user.save()
            return redirect("configuracoes")
    else:
        form = NewUsernameForm()

    context = {
        "name_form": NewNameForm(),
        "username_form": form,
        "email_form": NewEmailForm(),
        "password_form": NewPasswordForm(request.user),
        "caminho": "/configuracoes/",
        "title": "Configurações",
    }

    return render(request, "configuracoes/index.html", context)


@login_required
def mudar_email_view(request):
    if request.method == "POST":
        form = NewEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            return redirect("configuracoes")
    else:
        form = NewEmailForm()

    context = {
        "name_form": NewNameForm(),
        "username_form": NewUsernameForm(),
        "email_form": form,
        "password_form": NewPasswordForm(request.user),
        "caminho": "/configuracoes/",
        "title": "Configurações",
    }

    return render(request, "configuracoes/index.html", context)


@login_required
def mudar_senha_view(request):
    if request.method == "POST":
        form = NewPasswordForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["password"]
            request.user.set_password(new_password)
            request.user.save()

            update_session_auth_hash(request, request.user)

            messages.success(request, "Sua senha foi alterada com sucesso.")
            return redirect("configuracoes")
    else:
        form = NewPasswordForm(request.user)

    context = {
        "name_form": NewNameForm(),
        "username_form": NewUsernameForm(),
        "email_form": NewEmailForm(),
        "password_form": form,
        "caminho": "/configuracoes/",
        "title": "Configurações",
    }

    return render(request, "configuracoes/index.html", context)

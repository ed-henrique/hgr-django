from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.hashers import make_password
from django.contrib.auth import views as auth_views
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django import forms
from apps.usuarios.models import Usuario
from .forms import CustomSignupForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Insira o seu nome de usuário",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": mark_safe(
                    "&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7"
                    ";&#xb7;&#xb7;&#xb7;"
                ),
            }
        )
    )


class CustomLoginView(auth_views.LoginView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Entrar"
        return context


def cadastro_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            Usuario.objects.create(
                first_name=form.cleaned_data["name"],
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=make_password(form.cleaned_data["password"]),
            )

            return redirect("entrar")
    else:
        form = CustomSignupForm()
    return render(
        request, "autenticacao/cadastro.html", {"form": form, "title": "Cadastro"}
    )

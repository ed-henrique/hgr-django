from django import forms
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario


class CustomSignupForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Nome",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Seu nome"}
        ),
    )
    username = forms.CharField(
        max_length=100,
        label="Nome de Usuário",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Seu nome de usuário"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Seu email"}
        ),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Sua senha"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirme sua senha"}
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("As senhas não coincidem.")
        return cleaned_data

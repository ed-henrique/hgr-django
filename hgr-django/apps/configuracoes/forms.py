from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario


class NewNameForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Novo Nome",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Seu novo nome"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class NewUsernameForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Novo Nome de Usuário",
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Seu novo nome de usuário"}
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class NewEmailForm(forms.Form):
    email = forms.EmailField(
        label="Novo Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Seu novo email"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class NewPasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Sua senha atual"}
        ),
    )
    password = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Sua nova senha"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirme a Nova Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "Confirme sua nova senha"}
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Store the user instance

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not check_password(old_password, self.user.password):
            raise ValidationError("A senha atual está incorreta.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("As senhas não coincidem.")
        return cleaned_data

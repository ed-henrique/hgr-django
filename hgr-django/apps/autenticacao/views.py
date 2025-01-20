from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.safestring import mark_safe
from django import forms


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


def cadastro_view(request):
    pass

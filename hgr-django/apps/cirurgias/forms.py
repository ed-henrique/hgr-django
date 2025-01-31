from django import forms
from .models import Cirurgia
from apps.saidas.models import Saida
from apps.entradas.models import Entrada
from django.utils.timezone import now


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M",
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class CirurgiaForm(forms.ModelForm):
    class Meta:
        model = Cirurgia
        fields = [
            "data",
            "paciente",
            "setor",
            "especialidade",
            "tipo_de_cirurgia",
            "concluida_com_sucesso",
        ]

    data = DateTimeLocalField(
        label="Data",
        widget=DateTimeLocalInput(
            attrs={"class": "form-control"},
        ),
    )
    concluida_com_sucesso = forms.BooleanField(
        label="Concluída com Sucesso",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )

    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get("data")
        paciente = cleaned_data.get("paciente")

        if Saida.objects.filter(paciente=paciente).exists():
            self.add_error(
                "paciente",
                "O paciente selecionado não pode estar registrado como já tendo saído do HGR.",
            )

        current_datetime = now()
        entrada = Entrada.objects.filter(paciente=paciente).order_by("-data").first()

        if data and data < entrada.data:
            self.add_error(
                "data",
                "A data da cirurgia não pode ser antes da data de entrada do paciente.",
            )

        # Validate data_de_internacao (date of admission)
        if data and data > current_datetime:
            self.add_error("data", "A data da cirurgia não pode estar no futuro.")

        return cleaned_data

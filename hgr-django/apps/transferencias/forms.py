from django import forms
from .models import Transferencia
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


class TransferenciaForm(forms.ModelForm):
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
                "A data da transferência não pode ser antes da data de entrada do paciente.",
            )

        ultima_transferencia = (
            Transferencia.objects.filter(paciente=paciente, removido_em__isnull=True)
            .order_by("-data")
            .first()
        )

        if data and data < ultima_transferencia.data:
            self.add_error(
                "data",
                "A data da transferência não pode ser antes da data da última transferência do paciente.",
            )

        # Validate data_de_internacao (date of admission)
        if data and data > current_datetime:
            self.add_error("data", "A data da transferência não pode estar no futuro.")

        cleaned_data["leito_de_origem"] = paciente.leito

        return cleaned_data

    data = DateTimeLocalField(
        label="Data",
        widget=DateTimeLocalInput(
            attrs={"class": "form-control"},
        ),
    )

    class Meta:
        model = Transferencia
        fields = [
            "data",
            "paciente",
            "leito_de_destino",
        ]

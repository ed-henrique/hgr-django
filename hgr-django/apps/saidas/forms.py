from django import forms
from .models import Saida
from apps.entradas.models import Entrada
from apps.transferencias.models import Transferencia
from apps.pacientes.models import Paciente
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


class SaidaForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get("data")
        paciente = cleaned_data.get("paciente")

        current_datetime = now()

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
                "A data da saída não pode ser antes da data de entrada do paciente.",
            )

        ultima_transferencia = (
            Transferencia.objects.filter(paciente=paciente, removido_em__isnull=True)
            .order_by("-data")
            .first()
        )

        if data and data < ultima_transferencia.data:
            self.add_error(
                "data",
                "A data da saída não pode ser antes da data da última transferência do paciente.",
            )

        # Validate data_de_internacao (date of admission)
        if data and data > current_datetime:
            self.add_error("data", "A data da saída não pode estar no futuro.")

        cleaned_data["leito_de_origem"] = paciente.leito

        return cleaned_data

    data = DateTimeLocalField(
        label="Data",
        widget=DateTimeLocalInput(
            attrs={"class": "form-control"},
        ),
    )
    paciente = forms.ModelChoiceField(
        label="Paciente",
        queryset=Paciente.objects.filter(removido_em__isnull=True)
        .exclude(saida__isnull=False)
        .order_by("nome"),
        widget=forms.Select(
            attrs={"class": "form-select mr-sm-2"},
        ),
        empty_label=None,
    )

    class Meta:
        model = Saida
        fields = [
            "data",
            "paciente",
            "tipo_de_saida",
            "unidade_de_saude_de_destino",
        ]

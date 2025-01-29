from django import forms
from .models import Transferencia
from django.utils.timezone import now


class TransferenciaForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get("data")
        hora = cleaned_data.get("hora")
        paciente = cleaned_data.get("paciente")

        current_date = now().date()
        current_time = now().time()

        # Validate data_de_internacao (date of admission)
        if data and data > current_date:
            self.add_error(
                "data", "A data da transferência não pode estar no futuro."
            )

        # Validate hora_de_internacao (time of admission)
        if data and hora:
            if data == current_date and hora > current_time:
                self.add_error(
                    "hora",
                    "A hora da transferência não pode estar no futuro.",
                )

        cleaned_data["leito_de_origem"] = paciente.leito

        return cleaned_data

    data = forms.DateField(
        label="Data",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"},
            format="%Y-%m-%d",
        ),
    )
    hora = forms.TimeField(
        label="Hora",
        widget=forms.TimeInput(
            attrs={"class": "form-control", "type": "time"},
            format="%H:%M",
        ),
    )

    class Meta:
        model = Transferencia
        fields = [
            'data',
            'hora',
            'paciente',
            'leito_de_destino',
        ]

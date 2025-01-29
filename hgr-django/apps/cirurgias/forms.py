from django import forms
from .models import Cirurgia
from django.utils.timezone import now


class CirurgiaForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get("data")
        hora = cleaned_data.get("hora")

        current_date = now().date()
        current_time = now().time()

        # Validate data_de_internacao (date of admission)
        if data and data > current_date:
            self.add_error(
                "data", "A data da cirurgia não pode estar no futuro."
            )

        # Validate hora_de_internacao (time of admission)
        if data and hora:
            if data == current_date and hora > current_time:
                self.add_error(
                    "hora",
                    "A hora da cirurgia não pode estar no futuro.",
                )

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
    concluida_com_sucesso = forms.BooleanField(
        label="Concluída com Sucesso",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )

    class Meta:
        model = Cirurgia
        fields = [
            'data',
            'hora',
            'paciente',
            'setor',
            'especialidade',
            'tipo_de_cirurgia',
            'concluida_com_sucesso',
        ]

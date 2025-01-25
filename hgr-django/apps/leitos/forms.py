from django import forms
from .models import Leito


class LeitoForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        tem_o2 = cleaned_data.get("tem_o2")
        tipo_de_o2 = cleaned_data.get("tipo_de_o2")
        tem_vacuo = cleaned_data.get("tem_vacuo")
        tipo_de_vacuo = cleaned_data.get("tipo_de_vacuo")
        tem_codigo_sus = cleaned_data.get("tem_codigo_sus")
        codigo_sus = cleaned_data.get("codigo_sus")

        # Validation for tem_o2 and tipo_de_o2
        if tem_o2 and not tipo_de_o2:
            self.add_error(
                "tipo_de_o2", "O tipo de O2 é obrigatório se o leito tiver O2.")
        elif not tem_o2 and tipo_de_o2:
            self.cleaned_data["tipo_de_o2"] = None

        # Validation for tem_vacuo and tipo_de_vacuo
        if tem_vacuo and not tipo_de_vacuo:
            self.add_error(
                "tipo_de_vacuo", "O tipo de vácuo é obrigatório se o leito tiver vácuo.")
        elif not tem_vacuo and tipo_de_vacuo:
            self.cleaned_data["tipo_de_vacuo"] = None

        # Validation for tem_codigo_sus and codigo_sus
        if tem_codigo_sus and not codigo_sus:
            self.add_error(
                "codigo_sus", "O código SUS é obrigatório se o leito tiver código SUS.")
        elif not tem_codigo_sus and codigo_sus:
            self.cleaned_data["codigo_sus"] = None

        if codigo_sus:
            # Get the original value of codigo_sus from the database
            original_codigo_sus = Leito.objects.get(
                pk=self.instance.pk).codigo_sus if self.instance.pk else None

            # Check if codigo_sus has changed and if the new value already exists
            if codigo_sus != original_codigo_sus and Leito.objects.filter(codigo_sus=codigo_sus).exists():
                self.add_error(
                    "codigo_sus", "Este código SUS já está sendo usado.")

        return cleaned_data

    class Meta:
        model = Leito
        fields = [
            'setor',
            'especialidade',
            'status_de_leito',
            'tipo_de_leito',
            'tipo_de_o2',
            'tipo_de_vacuo',
            'codigo_sus',
            'tem_o2',
            'tem_vacuo',
            'tem_codigo_sus',
        ]

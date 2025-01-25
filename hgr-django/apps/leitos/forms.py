from django import forms
from django.core.exceptions import ValidationError
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
            self.add_error(
                "tem_o2", "Não é possível adicionar um tipo de O2 sem o leito ter O2.")

        # Validation for tem_vacuo and tipo_de_vacuo
        if tem_vacuo and not tipo_de_vacuo:
            self.add_error(
                "tipo_de_vacuo", "O tipo de vácuo é obrigatório se o leito tiver vácuo.")
        elif not tem_vacuo and tipo_de_vacuo:
            self.add_error(
                "tem_vacuo", "Não é possível adicionar um tipo de vácuo sem o leito ter vácuo.")

        # Validation for tem_codigo_sus and codigo_sus
        if tem_codigo_sus and not codigo_sus:
            self.add_error(
                "codigo_sus", "O código SUS é obrigatório se o leito tiver código SUS.")
        elif not tem_codigo_sus and codigo_sus:
            self.add_error(
                "tem_codigo_sus", "Não é possível adicionar um código SUS sem marcar a opção 'Tem Código SUS'.")

        # Check if codigo_sus is unique
        if codigo_sus and Leito.objects.filter(codigo_sus=codigo_sus).exists():
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

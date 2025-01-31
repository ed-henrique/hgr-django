from django import forms
from django.db.models import Q
from .models import Paciente
from apps.leitos.models import Leito
from apps.saidas.models import Saida
from apps.unidades_de_saude.models import UnidadeDeSaude
from apps.medidas_de_precaucao.models import MedidaDePrecaucao
from apps.portas_de_entrada.models import PortaDeEntrada
from apps.especialidades.models import Especialidade
from apps.status_de_paciente.models import StatusDePaciente
from apps.tipos_de_o2.models import TipoDeO2
from apps.tipos_de_vacuo.models import TipoDeVacuo
from apps.tipos_de_cirurgia.models import TipoDeCirurgia
from apps.nacionalidades_etnias.models import NacionalidadeEtnia
from apps.generos.models import Genero
from apps.usuarios.models import Usuario
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


class PacienteCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            self.fields["responsavel"].initial = self.user
            self.fields["responsavel"].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        leito = cleaned_data.get("leito")
        precisa_de_o2 = cleaned_data.get("precisa_de_o2")
        tipo_de_o2 = cleaned_data.get("tipo_de_o2")
        precisa_de_vacuo = cleaned_data.get("precisa_de_vacuo")
        tipo_de_vacuo = cleaned_data.get("tipo_de_vacuo")
        precisa_de_cirurgia = cleaned_data.get("precisa_de_cirurgia")
        tipo_de_cirurgia = cleaned_data.get("tipo_de_cirurgia")
        data_de_nascimento = cleaned_data.get("data_de_nascimento")
        data_de_internacao = cleaned_data.get("data_de_internacao")

        current_datetime = now()
        current_date = current_datetime.date()

        if data_de_nascimento and data_de_nascimento > current_date:
            self.add_error(
                "data_de_nascimento", "A data de nascimento não pode estar no futuro."
            )

        # Validate data_de_internacao (date of admission)
        if data_de_internacao and data_de_internacao > current_datetime:
            self.add_error(
                "data_de_internacao", "A data de internação não pode estar no futuro."
            )

        # Validation for precisa_de_o2 and tipo_de_o2
        if precisa_de_o2 and not tipo_de_o2:
            self.add_error(
                "tipo_de_o2", "O tipo de O2 é obrigatório se o paciente precisar de O2."
            )
        elif not precisa_de_o2 and tipo_de_o2:
            self.cleaned_data["tipo_de_o2"] = None

        # Validation for precisa_de_vacuo and tipo_de_vacuo
        if precisa_de_vacuo and not tipo_de_vacuo:
            self.add_error(
                "tipo_de_vacuo",
                "O tipo de vácuo é obrigatório se o paciente precisar de vácuo.",
            )
        elif not precisa_de_vacuo and tipo_de_vacuo:
            self.cleaned_data["tipo_de_vacuo"] = None

        # Validation for precisa_de_cirurgia and tipo_de_cirurgia
        if precisa_de_cirurgia and not tipo_de_cirurgia:
            self.add_error(
                "tipo_de_cirurgia",
                "O tipo de cirurgia é obrigatório se o paciente precisar de cirurgia.",
            )
        elif not precisa_de_cirurgia and tipo_de_cirurgia:
            self.cleaned_data["tipo_de_cirurgia"] = None

        ocupantes = Paciente.objects.filter(leito=leito, removido_em__isnull=True)

        # If editing an existing Paciente, exclude it from the query
        if self.instance and self.instance.pk:
            ocupantes = ocupantes.exclude(pk=self.instance.pk)

        # Check if any Paciente is occupying the leito
        for paciente in ocupantes:
            if not Saida.objects.filter(paciente=paciente).exists():
                self.add_error(
                    "leito", "Este leito já está sendo ocupado por outro paciente."
                )
                break

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user:
            instance.responsavel = self.user

        if not instance.data_de_internacao_no_setor:
            instance.data_de_internacao_no_setor = instance.data_de_internacao

        if commit:
            instance.save()

        return instance

    nome = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
    )
    nome_social = forms.CharField(
        label="Nome Social",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
        required=False,  # Optional field
    )
    data_de_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"},
        ),
        required=False,
    )
    data_de_internacao = DateTimeLocalField(
        label="Data de Internação",
        widget=DateTimeLocalInput(
            attrs={"class": "form-control"},
        ),
    )
    sexo = forms.ChoiceField(
        label="Sexo",
        choices=[("M", "Masculino"), ("F", "Feminino")],
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
    )
    diagnostico = forms.CharField(
        label="Diagnóstico",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3},
        ),
    )
    justificativas_pendencias = forms.CharField(
        label="Justificativas/Pendências",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3},
        ),
        required=False,  # Optional field
    )
    problemas_durante_transferencias = forms.CharField(
        label="Problemas Durante Transferências",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3},
        ),
        required=False,  # Optional field
    )
    genero = forms.ModelChoiceField(
        label="Gênero",
        queryset=Genero.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    leito = forms.ModelChoiceField(
        label="Leito",
        queryset=Leito.objects.filter(paciente__isnull=True, removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    unidade_de_saude_de_origem = forms.ModelChoiceField(
        label="Unidade de Saúde de Origem",
        queryset=UnidadeDeSaude.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        required=False,  # Optional field
        empty_label="Nenhuma",
    )
    medida_de_precaucao = forms.ModelChoiceField(
        label="Medida de Precaução",
        queryset=MedidaDePrecaucao.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    porta_de_entrada = forms.ModelChoiceField(
        label="Porta de Entrada",
        queryset=PortaDeEntrada.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    especialidade = forms.ModelChoiceField(
        label="Especialidade",
        queryset=Especialidade.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    status_de_paciente = forms.ModelChoiceField(
        label="Status do Paciente",
        queryset=StatusDePaciente.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    nacionalidade_etnia = forms.ModelChoiceField(
        label="Nacionalidade/Etnia",
        queryset=NacionalidadeEtnia.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    gestante = forms.BooleanField(
        label="Gestante",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )
    veio_de_ambulancia = forms.BooleanField(
        label="Veio de Ambulância",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )
    precisa_de_cirurgia = forms.BooleanField(
        label="Precisa de Cirurgia",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )
    tipo_de_cirurgia = forms.ModelChoiceField(
        label="Tipo de Cirurgia",
        queryset=TipoDeCirurgia.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select", "disabled": ""},
        ),
        required=False,  # Optional field
        empty_label=None,
    )
    precisa_de_o2 = forms.BooleanField(
        label="Precisa de O2",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )
    tipo_de_o2 = forms.ModelChoiceField(
        label="Tipo de O2",
        queryset=TipoDeO2.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select", "disabled": ""},
        ),
        required=False,  # Optional field
        empty_label=None,
    )
    precisa_de_vacuo = forms.BooleanField(
        label="Precisa de Vácuo",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"},
        ),
        required=False,  # Optional field
    )
    tipo_de_vacuo = forms.ModelChoiceField(
        label="Tipo de Vácuo",
        queryset=TipoDeVacuo.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select", "disabled": ""},
        ),
        required=False,  # Optional field
        empty_label=None,
    )

    class Meta:
        model = Paciente
        fields = [
            "nome",
            "nome_social",
            "data_de_nascimento",
            "data_de_internacao",
            "sexo",
            "diagnostico",
            "justificativas_pendencias",
            "problemas_durante_transferencias",
            "genero",
            "leito",
            "responsavel",
            "unidade_de_saude_de_origem",
            "medida_de_precaucao",
            "porta_de_entrada",
            "especialidade",
            "status_de_paciente",
            "nacionalidade_etnia",
            "gestante",
            "veio_de_ambulancia",
            "precisa_de_cirurgia",
            "tipo_de_cirurgia",
            "precisa_de_o2",
            "tipo_de_o2",
            "precisa_de_vacuo",
            "tipo_de_vacuo",
        ]


class PacienteEditForm(forms.ModelForm):
    def __init__(self, *args, paciente=None, **kwargs):
        super().__init__(*args, **kwargs)

        if paciente:
            self.fields["leito"].queryset = Leito.objects.filter(
                Q(paciente__isnull=True) | Q(paciente=paciente),
                removido_em__isnull=True,
            )

    def clean(self):
        cleaned_data = super().clean()

        leito = cleaned_data.get("leito")
        precisa_de_o2 = cleaned_data.get("precisa_de_o2")
        tipo_de_o2 = cleaned_data.get("tipo_de_o2")
        precisa_de_vacuo = cleaned_data.get("precisa_de_vacuo")
        tipo_de_vacuo = cleaned_data.get("tipo_de_vacuo")
        precisa_de_cirurgia = cleaned_data.get("precisa_de_cirurgia")
        tipo_de_cirurgia = cleaned_data.get("tipo_de_cirurgia")
        data_de_nascimento = cleaned_data.get("data_de_nascimento")
        data_de_internacao = cleaned_data.get("data_de_internacao")

        current_datetime = now()
        current_date = current_datetime.date()

        if data_de_nascimento and data_de_nascimento > current_date:
            self.add_error(
                "data_de_nascimento", "A data de nascimento não pode estar no futuro."
            )

        # Validate data_de_internacao (date of admission)
        if data_de_internacao and data_de_internacao > current_datetime:
            self.add_error(
                "data_de_internacao", "A data de internação não pode estar no futuro."
            )

        # Validation for precisa_de_o2 and tipo_de_o2
        if precisa_de_o2 and not tipo_de_o2:
            self.add_error(
                "tipo_de_o2", "O tipo de O2 é obrigatório se o paciente precisar de O2."
            )
        elif not precisa_de_o2 and tipo_de_o2:
            self.cleaned_data["tipo_de_o2"] = None

        # Validation for precisa_de_vacuo and tipo_de_vacuo
        if precisa_de_vacuo and not tipo_de_vacuo:
            self.add_error(
                "tipo_de_vacuo",
                "O tipo de vácuo é obrigatório se o paciente precisar de vácuo.",
            )
        elif not precisa_de_vacuo and tipo_de_vacuo:
            self.cleaned_data["tipo_de_vacuo"] = None

        # Validation for precisa_de_cirurgia and tipo_de_cirurgia
        if precisa_de_cirurgia and not tipo_de_cirurgia:
            self.add_error(
                "tipo_de_cirurgia",
                "O tipo de cirurgia é obrigatório se o paciente precisar de cirurgia.",
            )
        elif not precisa_de_cirurgia and tipo_de_cirurgia:
            self.cleaned_data["tipo_de_cirurgia"] = None

        ocupantes = Paciente.objects.filter(leito=leito, removido_em__isnull=True)

        # If editing an existing Paciente, exclude it from the query
        if self.instance and self.instance.pk:
            ocupantes = ocupantes.exclude(pk=self.instance.pk)

        # Check if any Paciente is occupying the leito
        for paciente in ocupantes:
            if not Saida.objects.filter(paciente=paciente).exists():
                self.add_error(
                    "leito", "Este leito já está sendo ocupado por outro paciente."
                )
                break

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.data_de_internacao_no_setor = instance.data_de_internacao

        if commit:
            instance.save()

        return instance

    nome = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
    )
    nome_social = forms.CharField(
        label="Nome Social",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
        required=False,  # Optional field
    )
    data_de_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"},
            format="%Y-%m-%d",
        ),
        required=False,
    )
    data_de_internacao = DateTimeLocalField(
        label="Data de Internação",
        widget=DateTimeLocalInput(
            attrs={"class": "form-control"},
        ),
    )
    sexo = forms.ChoiceField(
        label="Sexo",
        choices=[("M", "Masculino"), ("F", "Feminino")],
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
    )
    diagnostico = forms.CharField(
        label="Diagnóstico",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3},
        ),
    )
    responsavel = forms.ModelChoiceField(
        label="Leito",
        queryset=Usuario.objects.filter(status_de_usuario__nome="Ativo"),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    justificativas_pendencias = forms.CharField(
        label="Justificativas/Pendências",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3},
        ),
        required=False,  # Optional field
    )
    problemas_durante_transferencias = forms.CharField(
        label="Problemas Durante Transferências",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3},
        ),
        required=False,  # Optional field
    )
    genero = forms.ModelChoiceField(
        label="Gênero",
        queryset=Genero.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    leito = forms.ModelChoiceField(
        label="Leito",
        queryset=Leito.objects.none(),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    unidade_de_saude_de_origem = forms.ModelChoiceField(
        label="Unidade de Saúde de Origem",
        queryset=UnidadeDeSaude.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        required=False,  # Optional field
        empty_label="Nenhuma",
    )
    medida_de_precaucao = forms.ModelChoiceField(
        label="Medida de Precaução",
        queryset=MedidaDePrecaucao.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    porta_de_entrada = forms.ModelChoiceField(
        label="Porta de Entrada",
        queryset=PortaDeEntrada.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    especialidade = forms.ModelChoiceField(
        label="Especialidade",
        queryset=Especialidade.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    status_de_paciente = forms.ModelChoiceField(
        label="Status do Paciente",
        queryset=StatusDePaciente.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    nacionalidade_etnia = forms.ModelChoiceField(
        label="Nacionalidade/Etnia",
        queryset=NacionalidadeEtnia.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
        empty_label=None,
    )
    gestante = forms.BooleanField(
        label="Gestante",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            },
        ),
        required=False,  # Optional field
    )
    veio_de_ambulancia = forms.BooleanField(
        label="Veio de Ambulância",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            },
        ),
        required=False,  # Optional field
    )
    precisa_de_cirurgia = forms.BooleanField(
        label="Precisa de Cirurgia",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "onchange": "toggleInput('id_precisa_de_cirurgia', 'id_tipo_de_cirurgia')",
            },
        ),
        required=False,  # Optional field
    )
    tipo_de_cirurgia = forms.ModelChoiceField(
        label="Tipo de Cirurgia",
        queryset=TipoDeCirurgia.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select", "disabled": ""},
        ),
        required=False,  # Optional field
        empty_label=None,
    )
    precisa_de_o2 = forms.BooleanField(
        label="Precisa de O2",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "onchange": "toggleInput('id_precisa_de_o2', 'id_tipo_de_o2')",
            },
        ),
        required=False,  # Optional field
    )
    tipo_de_o2 = forms.ModelChoiceField(
        label="Tipo de O2",
        queryset=TipoDeO2.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select", "disabled": ""},
        ),
        required=False,  # Optional field
        empty_label=None,
    )
    precisa_de_vacuo = forms.BooleanField(
        label="Precisa de Vácuo",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "onchange": "toggleInput('id_precisa_de_vacuo', 'id_tipo_de_vacuo')",
            },
        ),
        required=False,  # Optional field
    )
    tipo_de_vacuo = forms.ModelChoiceField(
        label="Tipo de Vácuo",
        queryset=TipoDeVacuo.objects.filter(removido_em__isnull=True),
        widget=forms.Select(
            attrs={"class": "form-select", "disabled": ""},
        ),
        required=False,  # Optional field
        empty_label=None,
    )

    class Meta:
        model = Paciente
        fields = [
            "nome",
            "nome_social",
            "data_de_nascimento",
            "data_de_internacao",
            "sexo",
            "diagnostico",
            "justificativas_pendencias",
            "problemas_durante_transferencias",
            "genero",
            "leito",
            "responsavel",
            "unidade_de_saude_de_origem",
            "medida_de_precaucao",
            "porta_de_entrada",
            "especialidade",
            "status_de_paciente",
            "nacionalidade_etnia",
            "gestante",
            "veio_de_ambulancia",
            "precisa_de_cirurgia",
            "tipo_de_cirurgia",
            "precisa_de_o2",
            "tipo_de_o2",
            "precisa_de_vacuo",
            "tipo_de_vacuo",
        ]

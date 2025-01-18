from django.db import models

class Especialidade(models.Model):
    cor = models.CharField(max_length=7, unique=True, verbose_name='Cor')
    nome = models.CharField(max_length=128, unique=True, verbose_name='Nome')
    removido_em = models.DateTimeField(null=True, blank=True, verbose_name='Removido em')

    def get_participacao(self):
        from apps.pacientes.models import Paciente

        total_patient_count = Paciente.objects.filter(removido_em__isnull=True).count()
        total_patient_especialidade_count = Paciente.objects.filter(removido_em__isnull=True, especialidade=self).count()

        if total_patient_count == 0:
            return 0
        
        return (total_patient_especialidade_count / total_patient_count) * 100


    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'

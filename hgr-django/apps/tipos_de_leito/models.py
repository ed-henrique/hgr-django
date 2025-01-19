from django.db import models

class TipoDeLeito(models.Model):
    cor = models.CharField(max_length=7, unique=True, verbose_name='Cor')
    nome = models.CharField(max_length=128, unique=True, verbose_name='Nome')
    removido_em = models.DateTimeField(null=True, blank=True, verbose_name='Removido em')

    def get_participacao(self):
        from apps.pacientes.models import Paciente

        total = Paciente.objects.filter(removido_em__isnull=True).count()
        partial = Paciente.objects.filter(removido_em__isnull=True, tipo_de_leito=self).count()

        if total == 0:
            return 0
        
        return (partial / total) * 100

    class Meta:
        verbose_name = 'Tipo de Leito'
        verbose_name_plural = 'Tipos de Leito'

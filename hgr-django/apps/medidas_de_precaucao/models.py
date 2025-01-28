from django.db import models


class MedidaDePrecaucao(models.Model):
    cor = models.CharField(max_length=7, unique=True, verbose_name='Cor')
    nome = models.CharField(max_length=128, unique=True, verbose_name='Nome')
    removido_em = models.DateTimeField(
        null=True, blank=True, verbose_name='Removido em')

    def get_participacao(self):
        from apps.pacientes.models import Paciente

        total = Paciente.objects.filter(removido_em__isnull=True).count()
        partial = Paciente.objects.filter(
            removido_em__isnull=True, medida_de_precaucao=self).count()

        if total == 0:
            return 0

        return (partial / total) * 100

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Medida de Precaução'
        verbose_name_plural = 'Medidas de Precaução'

        indexes = [
            models.Index(fields=['removido_em']),
        ]

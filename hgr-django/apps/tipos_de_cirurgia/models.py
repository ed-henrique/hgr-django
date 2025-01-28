from django.db import models


class TipoDeCirurgia(models.Model):
    cor = models.CharField(max_length=7, unique=True, verbose_name='Cor')
    nome = models.CharField(max_length=128, unique=True, verbose_name='Nome')
    removido_em = models.DateTimeField(
        null=True, blank=True, verbose_name='Removido em')

    def get_participacao(self):
        from apps.cirurgias.models import Cirurgia

        total = Cirurgia.objects.filter(removido_em__isnull=True).count()
        partial = Cirurgia.objects.filter(
            removido_em__isnull=True, tipo_de_cirurgia=self).count()

        if total == 0:
            return 0

        return (partial / total) * 100

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Cirurgia'
        verbose_name_plural = 'Tipos de Cirurgia'

        indexes = [
            models.Index(fields=['removido_em']),
        ]

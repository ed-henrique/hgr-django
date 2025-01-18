from django.db import models

class TipoDeCirurgia(models.Model):
    cor = models.CharField(max_length=7, unique=True, verbose_name='Cor')
    nome = models.CharField(max_length=128, unique=True, verbose_name='Nome')
    removido_em = models.DateTimeField(null=True, verbose_name='Removido em')

    class Meta:
        verbose_name = 'Tipo de Cirurgia'
        verbose_name_plural = 'Tipos de Cirurgia'

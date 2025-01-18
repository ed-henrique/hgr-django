from django.db import models

class StatusDeUsuario(models.Model):
    nome = models.CharField(max_length=32, unique=True, verbose_name='Nome')

    class Meta:
        verbose_name = 'Status de Usuário'
        verbose_name_plural = 'Status de Usuário'

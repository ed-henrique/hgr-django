from django.db import models

class TipoDeUsuario(models.Model):
    nome = models.CharField(max_length=32, unique=True, verbose_name='Nome')

    class Meta:
        verbose_name = 'Tipo de Usuário'
        verbose_name_plural = 'Tipos de Usuário'

from django.db import models


class StatusDeUsuario(models.Model):
    nome = models.CharField(max_length=32, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Status de Usuário'
        verbose_name_plural = 'Status de Usuário'

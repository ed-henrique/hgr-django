from django.db import models

class Genero(models.Model):
    nome = models.CharField(unique=True, max_length=32, verbose_name='Nome')

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

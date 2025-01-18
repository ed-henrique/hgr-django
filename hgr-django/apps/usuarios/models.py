from django.contrib.auth.models import User
from django.db import models

from apps.tipos_de_usuario.models import TipoDeUsuario
from apps.status_de_usuario.models import StatusDeUsuario

class Usuario(models.Model):
    usuario = models.OneToOneField(User, related_name='usuario', on_delete=models.PROTECT, verbose_name='Usuário')
    tipo_de_usuario = models.ForeignKey(TipoDeUsuario, related_name='tipo_de_usuario', on_delete=models.PROTECT, verbose_name='Tipo de Usuário')
    status_de_usuario = models.ForeignKey(StatusDeUsuario, related_name='status_de_usuario', on_delete=models.PROTECT, verbose_name='Status de Usuário')


    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

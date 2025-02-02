# Generated by Django 5.1.5 on 2025-01-21 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status_de_usuario', '0001_initial'),
        ('tipos_de_usuario', '0001_initial'),
        ('usuarios', '0002_alter_usuario_managers_remove_usuario_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='status_de_usuario',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='status_de_usuario', to='status_de_usuario.statusdeusuario', verbose_name='Status de Usuário'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_de_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tipo_de_usuario', to='tipos_de_usuario.tipodeusuario', verbose_name='Tipo de Usuário'),
        ),
    ]

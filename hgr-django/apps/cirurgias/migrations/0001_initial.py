# Generated by Django 5.1.5 on 2025-01-17 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('especialidades', '0001_initial'),
        ('pacientes', '0001_initial'),
        ('setores', '0001_initial'),
        ('tipos_de_cirurgia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cirurgia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concluida_com_sucesso', models.BooleanField(default=False, verbose_name='Concluída com Sucesso')),
                ('data', models.DateField(verbose_name='Data')),
                ('hora', models.TimeField(verbose_name='Hora')),
                ('removido_em', models.DateTimeField(null=True, verbose_name='Removido em')),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='especialidades.especialidade', verbose_name='Especialidade')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pacientes.paciente', verbose_name='Paciente')),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='setores.setor', verbose_name='Setor')),
                ('tipo_de_cirurgia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tipos_de_cirurgia.tipodecirurgia', verbose_name='Tipo de Cirurgia')),
            ],
            options={
                'verbose_name': 'Cirurgia',
                'verbose_name_plural': 'Cirurgias',
            },
        ),
    ]

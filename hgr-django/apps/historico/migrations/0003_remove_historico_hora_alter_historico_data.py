# Generated by Django 5.1.5 on 2025-01-31 15:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0002_alter_historico_data_alter_historico_hora'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historico',
            name='hora',
        ),
        migrations.AlterField(
            model_name='historico',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
    ]

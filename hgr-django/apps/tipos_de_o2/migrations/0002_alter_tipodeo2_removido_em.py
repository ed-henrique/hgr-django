# Generated by Django 5.1.5 on 2025-01-18 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipos_de_o2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipodeo2',
            name='removido_em',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Removido em'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especialidades', '0002_alter_especialidade_removido_em'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='especialidade',
            index=models.Index(fields=['removido_em'], name='especialida_removid_441019_idx'),
        ),
    ]

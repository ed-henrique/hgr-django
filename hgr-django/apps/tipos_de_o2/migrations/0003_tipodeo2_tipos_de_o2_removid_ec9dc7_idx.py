# Generated by Django 5.1.5 on 2025-01-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipos_de_o2', '0002_alter_tipodeo2_removido_em'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='tipodeo2',
            index=models.Index(fields=['removido_em'], name='tipos_de_o2_removid_ec9dc7_idx'),
        ),
    ]

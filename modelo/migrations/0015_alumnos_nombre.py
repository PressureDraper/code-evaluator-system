# Generated by Django 4.0.4 on 2022-05-08 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0014_alumnos_idmaestro'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnos',
            name='nombre',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0021_alter_evaluaciones_calificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejercicios',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
    ]

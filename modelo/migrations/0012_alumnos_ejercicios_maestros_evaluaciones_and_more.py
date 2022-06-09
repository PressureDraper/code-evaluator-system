# Generated by Django 4.0.4 on 2022-04-15 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0011_testfiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='alumnos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('passwd', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ejercicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=254)),
                ('descripcion', models.CharField(max_length=254)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('sInicializacion', models.FileField(blank=True, upload_to='upload/maestro')),
                ('sEntradas', models.FileField(blank=True, upload_to='upload/maestro')),
                ('sSalida', models.FileField(blank=True, upload_to='upload/maestro')),
                ('sParametros', models.FileField(blank=True, upload_to='upload/maestro')),
                ('sEdoFinal', models.FileField(blank=True, upload_to='upload/maestro')),
            ],
        ),
        migrations.CreateModel(
            name='maestros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('passwd', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='evaluaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script', models.FileField(blank=True, upload_to='upload/alumno')),
                ('resultado', models.CharField(blank=True, max_length=254)),
                ('calificacion', models.IntegerField(blank=True)),
                ('intentos', models.IntegerField(blank=True)),
                ('idAlumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelo.alumnos')),
                ('idEjercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelo.ejercicios')),
            ],
        ),
        migrations.AddField(
            model_name='ejercicios',
            name='idMaestro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelo.maestros'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-13 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]

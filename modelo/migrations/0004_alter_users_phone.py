# Generated by Django 4.0.2 on 2022-02-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0003_alter_users_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]
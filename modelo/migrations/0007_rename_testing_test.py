# Generated by Django 4.0.2 on 2022-03-30 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0006_rename_uname_testing_username'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='testing',
            new_name='test',
        ),
    ]

# Generated by Django 2.2.13 on 2020-07-03 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_delete_process'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queue',
            options={'ordering': ['version_start_date']},
        ),
    ]
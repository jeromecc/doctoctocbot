# Generated by Django 2.2.4 on 2019-10-06 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_auto_20190925_0421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='domain',
        ),
    ]
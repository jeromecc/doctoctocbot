# Generated by Django 2.2.4 on 2019-12-10 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_provider_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='project',
        ),
    ]

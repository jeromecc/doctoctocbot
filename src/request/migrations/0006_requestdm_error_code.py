# Generated by Django 2.2.17 on 2021-02-02 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0005_requestdm'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestdm',
            name='error_code',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
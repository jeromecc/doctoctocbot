# Generated by Django 2.2.4 on 2019-09-23 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20190630_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='launch',
            field=models.DateField(blank=True, default=None, help_text='Launch date of the account', null=True),
        ),
    ]

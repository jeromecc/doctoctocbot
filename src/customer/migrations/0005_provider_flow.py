# Generated by Django 2.2.4 on 2019-12-04 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20191204_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='flow',
            field=models.CharField(choices=[('proforma', 'Proforma'), ('invoice', 'Invoice')], default='invoice', max_length=8),
        ),
    ]

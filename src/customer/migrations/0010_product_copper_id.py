# Generated by Django 2.2.4 on 2019-12-12 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='copper_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]

# Generated by Django 2.2.4 on 2019-12-14 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20191213_0215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='copper_id',
            new_name='silver_id',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='copper_id',
            new_name='silver_id',
        ),
        migrations.RenameField(
            model_name='provider',
            old_name='copper_id',
            new_name='silver_id',
        ),
    ]

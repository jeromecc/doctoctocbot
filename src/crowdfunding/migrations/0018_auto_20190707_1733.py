# Generated by Django 2.2.1 on 2019-07-07 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0017_auto_20190226_0334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectinvestment',
            old_name='id',
            new_name='uuid',
        ),
    ]

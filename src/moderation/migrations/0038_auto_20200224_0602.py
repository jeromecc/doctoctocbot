# Generated by Django 2.2.10 on 2020-02-24 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0037_auto_20191101_0133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercategoryrelationship',
            options={'get_latest_by': 'created'},
        ),
    ]
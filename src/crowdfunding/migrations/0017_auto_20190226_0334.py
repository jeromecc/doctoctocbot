# Generated by Django 2.0.13 on 2019-02-26 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0016_auto_20190225_0631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tier',
            options={'ordering': ['-max']},
        ),
    ]

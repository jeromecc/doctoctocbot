# Generated by Django 2.2.1 on 2019-07-07 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0001_squashed_0018_auto_20190707_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='slug',
            field=models.SlugField(),
        ),
    ]

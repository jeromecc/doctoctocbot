# Generated by Django 2.2.10 on 2020-03-22 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0019_community_allow_unknown'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='language',
            field=models.CharField(blank=True, help_text='ISO language code', max_length=3),
        ),
    ]

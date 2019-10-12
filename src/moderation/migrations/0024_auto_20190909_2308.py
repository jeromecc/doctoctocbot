# Generated by Django 2.2.4 on 2019-09-09 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
        ('moderation', '0023_moderator_community'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moderator',
            name='community',
        ),
        migrations.AddField(
            model_name='moderator',
            name='community',
            field=models.ManyToManyField(to='community.Community'),
        ),
    ]

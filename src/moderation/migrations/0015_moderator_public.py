# Generated by Django 2.0.13 on 2019-05-16 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0014_moderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderator',
            name='public',
            field=models.BooleanField(default=True, help_text='Does this moderator want to appear on the public list?'),
        ),
    ]
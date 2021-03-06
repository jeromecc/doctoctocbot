# Generated by Django 2.2.17 on 2021-02-09 01:53

from django.db import migrations, models
import messenger.models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0008_auto_20210208_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='backoff',
            field=models.PositiveIntegerField(default=messenger.models.get_backoff, help_text='period between 2 API message_create events in seconds'),
        ),
    ]

# Generated by Django 2.0.8 on 2018-11-19 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0007_auto_20181115_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetdj',
            name='quotedstatus',
            field=models.NullBooleanField(default=None, help_text='Is quoted_status'),
        ),
        migrations.AddField(
            model_name='tweetdj',
            name='retweetedstatus',
            field=models.NullBooleanField(default=None, help_text='Is retweeted_status'),
        ),
    ]

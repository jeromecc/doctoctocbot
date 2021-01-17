# Generated by Django 2.2.13 on 2021-01-13 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0037_auto_20201207_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='twitter_follow_member',
            field=models.BooleanField(default=False, help_text="Bot's Twitter account will follow the members of this community."),
        ),
    ]
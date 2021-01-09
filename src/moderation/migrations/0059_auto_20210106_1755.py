# Generated by Django 2.2.13 on 2021-01-06 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0058_category_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialuser',
            name='twitter_block',
            field=models.ManyToManyField(blank=True, help_text='Twitter users blocked by this user', related_name='block_by', to='moderation.SocialUser'),
        ),
        migrations.AddField(
            model_name='socialuser',
            name='twitter_follow_request',
            field=models.ManyToManyField(blank=True, help_text='Twitter users with pending follow request for this user', related_name='follow_request_by', to='moderation.SocialUser'),
        ),
    ]

# Generated by Django 2.0.13 on 2019-05-01 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0011_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='socialgraph',
            field=models.BooleanField(default=False, help_text='Include in moderation social graph?'),
        ),
    ]

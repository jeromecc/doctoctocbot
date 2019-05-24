# Generated by Django 2.0.13 on 2019-05-21 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0016_donotretweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donotretweet',
            name='socialuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donotretweet', to='moderation.SocialUser', verbose_name='socialuser'),
        ),
    ]

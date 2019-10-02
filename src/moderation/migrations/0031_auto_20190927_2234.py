# Generated by Django 2.2.4 on 2019-09-27 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0030_change_moderator_primary_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderator',
            name='socialuser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='moderation.SocialUser'),
        ),
    ]

# Generated by Django 2.2.4 on 2019-09-28 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0033_moderator_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderator',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='community.Community'),
        ),
    ]

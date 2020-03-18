# Generated by Django 2.2.10 on 2020-03-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0011_auto_20200318_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='community', through='community.CommunityCategoryRelationship', to='moderation.Category'),
        ),
        migrations.AlterField(
            model_name='community',
            name='cooperation',
            field=models.ManyToManyField(blank=True, related_name='cooperating_with', through='community.Cooperation', to='community.Community'),
        ),
        migrations.AlterField(
            model_name='community',
            name='membership',
            field=models.ManyToManyField(blank=True, related_name='member_of', to='moderation.Category'),
        ),
        migrations.AlterField(
            model_name='community',
            name='trust',
            field=models.ManyToManyField(blank=True, related_name='trusted_by', through='community.Trust', to='community.Community'),
        ),
    ]
# Generated by Django 2.0.13 on 2019-04-03 01:20

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_auto_20181029_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_id', models.BigIntegerField(unique=True)),
                ('slug', models.CharField(max_length=25, unique=True)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('uid', models.CharField(blank=True, max_length=25, null=True)),
                ('label', models.CharField(blank=True, max_length=25, null=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
    ]

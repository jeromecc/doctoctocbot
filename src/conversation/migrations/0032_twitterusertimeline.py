# Generated by Django 2.2.17 on 2021-01-30 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0031_auto_20210115_0330'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterUserTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('statusid', models.BigIntegerField(blank=True, help_text='Status id of the most recent status retrieved', null=True)),
            ],
        ),
    ]
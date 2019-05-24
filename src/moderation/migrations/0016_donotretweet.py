# Generated by Django 2.0.13 on 2019-05-21 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0015_auto_20190520_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoNotRetweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.BooleanField(default=True, help_text='Is this row current?')),
                ('duration', models.IntegerField(blank=True, help_text='Duration in days, null means unlimited', null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('socialuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moderation.SocialUser', verbose_name='socialuser')),
            ],
        ),
    ]

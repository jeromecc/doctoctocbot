# Generated by Django 2.2.10 on 2020-03-09 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0024_auto_20200227_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retweet',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('identity', models.UUIDField()),
                ('version_start_date', models.DateTimeField()),
                ('version_end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('version_birth_date', models.DateTimeField()),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retweeted', to='conversation.Tweetdj')),
            ],
            options={
                'abstract': False,
                'unique_together': {('id', 'identity')},
            },
        ),
    ]

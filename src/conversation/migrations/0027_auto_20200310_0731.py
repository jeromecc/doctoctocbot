# Generated by Django 2.2.10 on 2020-03-10 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20191013_2322'),
        ('conversation', '0026_retweet_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retweeted',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('identity', models.UUIDField()),
                ('version_start_date', models.DateTimeField()),
                ('version_end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('version_birth_date', models.DateTimeField()),
                ('status', models.BigIntegerField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Account')),
            ],
            options={
                'abstract': False,
                'unique_together': {('id', 'identity')},
            },
        ),
        migrations.DeleteModel(
            name='Retweet',
        ),
    ]

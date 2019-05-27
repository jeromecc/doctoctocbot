# Generated by Django 2.0.13 on 2019-05-25 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('moderation', '0017_auto_20190522_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaign_account', to='moderation.SocialUser')),
                ('categories', models.ManyToManyField(to='moderation.Category')),
            ],
            options={
                'verbose_name': 'Campaign',
                'verbose_name_plural': 'Campaigns',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='CampaignMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(help_text='What order to display this person within the department.', verbose_name='Ordre')),
                ('campaign', models.ForeignKey(help_text='Messages are part of this campaign.', on_delete=django.db.models.deletion.CASCADE, to='messenger.Campaign', verbose_name='Campaign')),
            ],
            options={
                'verbose_name': 'Campaign Message',
                'verbose_name_plural': 'Campaign Messages',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.BooleanField(default=False, help_text='Has this message been received.', verbose_name='Received')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('message', models.ForeignKey(help_text='Receipt for this message.', on_delete=django.db.models.deletion.CASCADE, to='messenger.Message', verbose_name='Message')),
                ('user', models.ForeignKey(help_text='Receipt for a message sent to this user', on_delete=django.db.models.deletion.CASCADE, to='moderation.SocialUser', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Facture',
                'verbose_name_plural': 'Receipts',
            },
        ),
        migrations.AddField(
            model_name='campaignmessage',
            name='message',
            field=models.ForeignKey(help_text='Messages are part of this campaign.', on_delete=django.db.models.deletion.CASCADE, to='messenger.Message', verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='messages',
            field=models.ManyToManyField(help_text='Messages from this Campaign', related_name='messages', through='messenger.CampaignMessage', to='messenger.Message', verbose_name='Messages'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='receipts',
            field=models.ManyToManyField(to='messenger.Receipt'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='recipients',
            field=models.ManyToManyField(to='moderation.SocialUser'),
        ),
    ]

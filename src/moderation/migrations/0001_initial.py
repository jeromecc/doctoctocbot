# Generated by Django 2.0.8 on 2018-10-28 04:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion

import versions.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('label_en', models.CharField(max_length=255, unique=True)),
                ('label_fr', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Moderation',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('identity', models.UUIDField()),
                ('version_start_date', models.DateTimeField()),
                ('version_end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('version_birth_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('identity', models.UUIDField()),
                ('version_start_date', models.DateTimeField()),
                ('version_end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('version_birth_date', models.DateTimeField()),
                ('user_id', models.BigIntegerField()),
                ('status_id', models.BigIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SocialUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True)),
            ],
            options={
                'ordering': ('user_id',),
            },
        ),
        migrations.CreateModel(
            name='UserCategoryRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='moderation.Category')),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moderated', to='moderation.SocialUser')),
                ('social_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoryrelationships', to='moderation.SocialUser')),
            ],
        ),
        migrations.AddField(
            model_name='socialuser',
            name='category',
            field=models.ManyToManyField(through='moderation.UserCategoryRelationship', to='moderation.Category'),
        ),
        migrations.AddField(
            model_name='socialuser',
            name='social_media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='moderation.SocialMedia'),
        ),
        migrations.AlterUniqueTogether(
            name='queue',
            unique_together={('id', 'identity')},
        ),
        migrations.AddField(
            model_name='profile',
            name='socialuser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moderation.SocialUser'),
        ),
        migrations.AddField(
            model_name='moderation',
            name='moderator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderations', to='moderation.SocialUser'),
        ),
        migrations.AddField(
            model_name='moderation',
            name='queue',
            field=versions.fields.VersionedForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moderation.Queue'),
        ),
        migrations.AlterUniqueTogether(
            name='usercategoryrelationship',
            unique_together={('social_user', 'category')},
        ),
        migrations.AlterUniqueTogether(
            name='moderation',
            unique_together={('id', 'identity')},
        ),
    ]

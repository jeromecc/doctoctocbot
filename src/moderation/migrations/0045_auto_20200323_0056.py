# Generated by Django 2.2.10 on 2020-03-22 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0044_categorymetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymetadata',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='categorymetadata',
            name='description_fr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='categorymetadata',
            name='label_en',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='categorymetadata',
            name='label_fr',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]

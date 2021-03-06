# Generated by Django 2.2.10 on 2020-03-23 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0046_auto_20200323_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_en',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_fr',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='categorymetadata',
            name='description',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='categorymetadata',
            name='description_en',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
        migrations.AlterField(
            model_name='categorymetadata',
            name='description_fr',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
    ]

# Generated by Django 2.2.17 on 2021-03-11 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0040_auto_20210202_0539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the blog.', max_length=254)),
                ('link', models.CharField(help_text='Link text.', max_length=254)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='community', to='community.Blog'),
        ),
    ]

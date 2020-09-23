# Generated by Django 2.2.13 on 2020-09-03 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('tagging', '0016_category_is_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagkeyword',
            name='taggit_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tagging_tagkeyword', to='taggit.Tag'),
        ),
    ]

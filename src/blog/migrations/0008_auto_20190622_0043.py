# Generated by Django 2.2.1 on 2019-06-21 22:43

import blog.models
from django.conf import settings
from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blogpage_authors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='authors',
            field=modelcluster.fields.ParentalManyToManyField(default=blog.models.get_anonymous_user, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.0.10 on 2019-02-13 17:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crowdfunding', '0008_auto_20190121_0056'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectInvestor',
            new_name='ProjectInvestment',
        ),
    ]

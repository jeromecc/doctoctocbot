# Generated by Django 2.0 on 2018-10-06 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0003_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercategoryrelationship',
            unique_together={('social_user', 'category')},
        ),
    ]

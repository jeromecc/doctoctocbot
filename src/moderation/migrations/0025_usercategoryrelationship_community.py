# Generated by Django 2.2.4 on 2019-09-10 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0024_auto_20190909_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercategoryrelationship',
            name='community',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='community.Community'),
        ),
    #    migrations.AddField(
    #        model_name='usercategoryrelationship',
    #        name='community',
    #        field=models.IntegerField(default=1),
    #    ),
    ]

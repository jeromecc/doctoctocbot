# Generated by Django 2.2.10 on 2020-03-17 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20191013_2322'),
        ('community', '0007_auto_20191022_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='helper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='helper_community', to='bot.Account'),
        ),
    ]
# Generated by Django 2.2.4 on 2019-12-10 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_remove_provider_project'),
        ('crowdfunding', '0002_auto_20190707_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Provider'),
        ),
    ]
